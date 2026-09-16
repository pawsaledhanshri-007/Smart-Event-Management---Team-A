import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.models.auth_session import AuthSession
from app.models.user import User


def issue_token_pair(db: Session, user: User) -> dict[str, object]:
    """Create a revocable server-side session plus access/refresh JWTs."""
    now = datetime.now(timezone.utc)
    refresh_expires = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_jti = secrets.token_urlsafe(32)

    session = AuthSession(
        user_id=user.id,
        refresh_jti_hash=security.hash_token_id(refresh_jti),
        expires_at=refresh_expires,
    )
    db.add(session)
    db.flush()

    access_token = security.create_access_token(
        subject=user.id,
        session_id=session.id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = security.create_refresh_token(
        subject=user.id,
        session_id=session.id,
        jti=refresh_jti,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


def rotate_refresh_token(db: Session, refresh_token: str) -> tuple[User, dict[str, object]]:
    payload = security.decode_token(refresh_token, expected_type="refresh")

    try:
        user_id = uuid.UUID(str(payload["sub"]))
        session_id = uuid.UUID(str(payload["sid"]))
        refresh_jti = str(payload["jti"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Invalid refresh token") from exc

    session = db.query(AuthSession).filter(AuthSession.id == session_id).first()
    if not session or session.user_id != user_id:
        raise ValueError("Invalid refresh token")

    now = datetime.now(timezone.utc)
    if session.revoked_at is not None or session.expires_at <= now:
        raise ValueError("Refresh session is expired or revoked")

    if not secrets.compare_digest(
        session.refresh_jti_hash,
        security.hash_token_id(refresh_jti),
    ):
        # Reuse of an old/rotated refresh token invalidates the whole session.
        session.revoked_at = now
        db.commit()
        raise ValueError("Refresh token has already been rotated")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        session.revoked_at = now
        db.commit()
        raise ValueError("User account is unavailable")

    new_jti = secrets.token_urlsafe(32)
    session.refresh_jti_hash = security.hash_token_id(new_jti)
    session.updated_at = now

    access_token = security.create_access_token(
        subject=user.id,
        session_id=session.id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    new_refresh_token = security.create_refresh_token(
        subject=user.id,
        session_id=session.id,
        jti=new_jti,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.commit()

    return user, {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


def revoke_refresh_session(db: Session, refresh_token: str) -> None:
    try:
        payload = security.decode_token(refresh_token, expected_type="refresh")
        session_id = uuid.UUID(str(payload["sid"]))
    except (KeyError, TypeError, ValueError):
        # Logout is idempotent; an invalid/expired token is treated as already logged out.
        return

    session = db.query(AuthSession).filter(AuthSession.id == session_id).first()
    if session and session.revoked_at is None:
        session.revoked_at = datetime.now(timezone.utc)
        db.commit()


def revoke_all_user_sessions(db: Session, user_id: uuid.UUID) -> int:
    now = datetime.now(timezone.utc)
    sessions = (
        db.query(AuthSession)
        .filter(AuthSession.user_id == user_id, AuthSession.revoked_at.is_(None))
        .all()
    )
    for session in sessions:
        session.revoked_at = now
    if sessions:
        db.commit()
    return len(sessions)
