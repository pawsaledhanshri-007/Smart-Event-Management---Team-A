import logging
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.auth_security import (
    ChangePasswordRequest,
    EmailVerificationRequest,
    ForgotPasswordRequest,
    MessageResponse,
    RefreshTokenRequest,
    ResendVerificationRequest,
    ResetPasswordRequest,
    TwoFactorCodeRequest,
    TwoFactorLoginRequest,
    TwoFactorSetupResponse,
)
from app.schemas.token import GoogleLoginRequest, LoginResponse, Token
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate
from app.services import auth_session_service, email_service

logger = logging.getLogger(__name__)
router = APIRouter()


def _debug_token(token: str | None) -> str | None:
    return token if settings.AUTH_DEBUG_TOKENS else None


def _send_verification(user: User) -> str:
    token = security.create_purpose_token(
        subject=user.id,
        purpose="email_verification",
        expires_delta=timedelta(
            minutes=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES
        ),
        extra_claims={"email": user.email},
    )
    try:
        email_service.send_verification_email(user.email, token)
    except Exception:
        logger.exception("Unable to send email verification message")
    return token


def _login_or_two_factor(db: Session, user: User) -> dict[str, object]:
    if settings.REQUIRE_EMAIL_VERIFICATION and not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before signing in",
        )

    if user.is_2fa_enabled:
        if not user.totp_secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Two-factor authentication is misconfigured for this account",
            )
        challenge_token = security.create_purpose_token(
            subject=user.id,
            purpose="2fa_login",
            expires_delta=timedelta(
                minutes=settings.TWO_FACTOR_CHALLENGE_EXPIRE_MINUTES
            ),
        )
        return {
            "token_type": "bearer",
            "two_factor_required": True,
            "challenge_token": challenge_token,
        }

    tokens = auth_session_service.issue_token_pair(db, user)
    return {**tokens, "two_factor_required": False}


@router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    normalized_email = str(user_in.email).strip().lower()

    existing_user = db.query(User).filter(User.email == normalized_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists.",
        )

    user = User(
        email=normalized_email,
        name=user_in.name.strip(),
        phone=user_in.phone,
        age=user_in.age,
        college=user_in.college,
        password_hash=security.get_password_hash(user_in.password),
        role=UserRole.PARTICIPANT.value,
        is_active=True,
        is_email_verified=False,
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists.",
        )

    db.refresh(user)
    _send_verification(user)
    return user


@router.post("/login", response_model=LoginResponse)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    normalized_email = form_data.username.strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()

    if not user or not security.verify_password(
        form_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return _login_or_two_factor(db, user)


@router.post("/google", response_model=LoginResponse)
def google_login(
    google_in: GoogleLoginRequest,
    db: Session = Depends(get_db),
):
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google authentication is not configured",
        )

    try:
        google_user = security.verify_google_id_token(google_in.credential)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    normalized_email = str(google_user["email"]).strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()

    if not user:
        google_name = str(google_user.get("name") or "").strip()
        fallback_name = normalized_email.split("@", 1)[0]
        random_password = secrets.token_urlsafe(32)

        user = User(
            email=normalized_email,
            name=google_name or fallback_name,
            password_hash=security.get_password_hash(random_password),
            role=UserRole.PARTICIPANT.value,
            is_active=True,
            is_email_verified=True,
            email_verified_at=datetime.now(timezone.utc),
        )
        db.add(user)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            user = db.query(User).filter(User.email == normalized_email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Unable to create Google user account",
                )
        else:
            db.refresh(user)
    elif not user.is_email_verified:
        # A verified Google identity proves ownership of this email address.
        user.is_email_verified = True
        user.email_verified_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return _login_or_two_factor(db, user)


@router.get("/me", response_model=UserSchema)
def read_users_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


# ---------------------------------------------------------------------
# Forgot password / reset password / change password
# ---------------------------------------------------------------------
@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(
    body: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    normalized_email = str(body.email).strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()

    token: str | None = None
    if user and user.is_active:
        token = security.create_purpose_token(
            subject=user.id,
            purpose="password_reset",
            expires_delta=timedelta(
                minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
            ),
            extra_claims={"ver": user.password_reset_version},
        )
        try:
            email_service.send_password_reset_email(user.email, token)
        except Exception:
            logger.exception("Unable to send password reset email")

    # Generic response prevents account enumeration.
    return MessageResponse(
        message="If an active account exists for that email, password reset instructions have been sent.",
        debug_token=_debug_token(token),
    )


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(
    body: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    try:
        payload = security.decode_purpose_token(body.token, "password_reset")
        user_id = UUID(str(payload["sub"]))
        token_version = int(payload["ver"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token",
        ) from exc

    user = db.query(User).filter(User.id == user_id).first()
    if not user or token_version != user.password_reset_version:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or already-used password reset token",
        )

    user.password_hash = security.get_password_hash(body.new_password)
    user.password_reset_version += 1
    db.commit()
    auth_session_service.revoke_all_user_sessions(db, user.id)

    return MessageResponse(
        message="Password reset successfully. Please sign in again."
    )


@router.post("/change-password", response_model=MessageResponse)
def change_password(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not security.verify_password(
        body.current_password,
        current_user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    if security.verify_password(body.new_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from the current password",
        )

    current_user.password_hash = security.get_password_hash(body.new_password)
    current_user.password_reset_version += 1
    db.commit()
    auth_session_service.revoke_all_user_sessions(db, current_user.id)

    return MessageResponse(
        message="Password changed successfully. All sessions were signed out."
    )


# ---------------------------------------------------------------------
# Normal email verification
# ---------------------------------------------------------------------
@router.post("/resend-verification", response_model=MessageResponse)
def resend_verification(
    body: ResendVerificationRequest,
    db: Session = Depends(get_db),
):
    normalized_email = str(body.email).strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()

    token: str | None = None
    if user and user.is_active and not user.is_email_verified:
        token = _send_verification(user)

    return MessageResponse(
        message="If an unverified account exists for that email, a verification message has been sent.",
        debug_token=_debug_token(token),
    )


@router.post("/verify-email", response_model=MessageResponse)
def verify_email(
    body: EmailVerificationRequest,
    db: Session = Depends(get_db),
):
    try:
        payload = security.decode_purpose_token(body.token, "email_verification")
        user_id = UUID(str(payload["sub"]))
        token_email = str(payload["email"]).strip().lower()
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        ) from exc

    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.email.lower() != token_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token",
        )

    if not user.is_email_verified:
        user.is_email_verified = True
        user.email_verified_at = datetime.now(timezone.utc)
        db.commit()

    return MessageResponse(message="Email verified successfully.")


# ---------------------------------------------------------------------
# Refresh tokens + revocable logout
# ---------------------------------------------------------------------
@router.post("/refresh", response_model=Token)
def refresh_token(
    body: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    try:
        _user, tokens = auth_session_service.rotate_refresh_token(
            db,
            body.refresh_token,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return tokens


@router.post("/logout", response_model=MessageResponse)
def logout(
    body: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    auth_session_service.revoke_refresh_session(db, body.refresh_token)
    return MessageResponse(message="Logged out successfully.")


@router.post("/logout-all", response_model=MessageResponse)
def logout_all(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    count = auth_session_service.revoke_all_user_sessions(db, current_user.id)
    return MessageResponse(message=f"Signed out from {count} active session(s).")


# ---------------------------------------------------------------------
# Optional TOTP 2FA / MFA
# ---------------------------------------------------------------------
@router.post("/2fa/setup", response_model=TwoFactorSetupResponse)
def setup_two_factor(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.is_2fa_enabled:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Two-factor authentication is already enabled",
        )

    secret = security.generate_totp_secret()
    current_user.totp_secret = secret
    db.commit()

    return TwoFactorSetupResponse(
        secret=secret,
        otpauth_uri=security.build_totp_uri(secret, current_user.email),
    )


@router.post("/2fa/enable", response_model=MessageResponse)
def enable_two_factor(
    body: TwoFactorCodeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Run /2fa/setup before enabling two-factor authentication",
        )

    if not security.verify_totp(current_user.totp_secret, body.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid two-factor code",
        )

    current_user.is_2fa_enabled = True
    db.commit()
    return MessageResponse(message="Two-factor authentication enabled.")


@router.post("/2fa/disable", response_model=MessageResponse)
def disable_two_factor(
    body: TwoFactorCodeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_2fa_enabled or not current_user.totp_secret:
        return MessageResponse(message="Two-factor authentication is already disabled.")

    if not security.verify_totp(current_user.totp_secret, body.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid two-factor code",
        )

    current_user.is_2fa_enabled = False
    current_user.totp_secret = None
    db.commit()
    auth_session_service.revoke_all_user_sessions(db, current_user.id)

    return MessageResponse(
        message="Two-factor authentication disabled. All sessions were signed out."
    )


@router.post("/2fa/verify-login", response_model=Token)
def verify_two_factor_login(
    body: TwoFactorLoginRequest,
    db: Session = Depends(get_db),
):
    try:
        payload = security.decode_purpose_token(body.challenge_token, "2fa_login")
        user_id = UUID(str(payload["sub"]))
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired two-factor challenge",
        ) from exc

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active or not user.is_2fa_enabled or not user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Two-factor authentication challenge is no longer valid",
        )

    if settings.REQUIRE_EMAIL_VERIFICATION and not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before signing in",
        )

    if not security.verify_totp(user.totp_secret, body.code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid two-factor code",
        )

    return auth_session_service.issue_token_pair(db, user)
