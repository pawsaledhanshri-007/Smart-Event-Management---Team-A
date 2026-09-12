from datetime import timedelta
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.token import GoogleLoginRequest, Token
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate

router = APIRouter()


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

    existing_user = (
        db.query(User)
        .filter(User.email == normalized_email)
        .first()
    )

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
    return user


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    normalized_email = form_data.username.strip().lower()

    user = (
        db.query(User)
        .filter(User.email == normalized_email)
        .first()
    )

    if (
        not user
        or not security.verify_password(
            form_data.password,
            user.password_hash,
        )
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

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = security.create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/google", response_model=Token)
def google_login(
    google_in: GoogleLoginRequest,
    db: Session = Depends(get_db),
):
    """Sign in with Google and return the same JWT used by normal login."""
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google authentication is not configured",
        )

    try:
        google_user = security.verify_google_id_token(
            google_in.credential
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    normalized_email = str(google_user["email"]).strip().lower()

    user = (
        db.query(User)
        .filter(User.email == normalized_email)
        .first()
    )

    if not user:
        google_name = str(google_user.get("name") or "").strip()
        fallback_name = normalized_email.split("@", 1)[0]

        # The current database requires password_hash to be non-null.
        # Google-only users receive a random password that is never shown or used.
        random_password = secrets.token_urlsafe(32)

        user = User(
            email=normalized_email,
            name=google_name or fallback_name,
            password_hash=security.get_password_hash(random_password),
            role=UserRole.PARTICIPANT.value,
            is_active=True,
        )
        db.add(user)

        try:
            db.commit()
        except IntegrityError:
            # Another request may have created the same email at the same time.
            db.rollback()
            user = (
                db.query(User)
                .filter(User.email == normalized_email)
                .first()
            )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Unable to create Google user account",
                )
        else:
            db.refresh(user)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = security.create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserSchema)
def read_users_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
