from datetime import datetime, timedelta, timezone
from typing import Any

from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    subject: Any,
    expires_delta: timedelta | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    expire = (
        now + expires_delta
        if expires_delta
        else now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": str(subject),
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def verify_google_id_token(credential: str) -> dict[str, Any]:
    """Verify the Google ID token received from the frontend."""
    if not settings.GOOGLE_CLIENT_ID:
        raise ValueError("Google authentication is not configured")

    try:
        google_user = id_token.verify_oauth2_token(
            credential,
            GoogleRequest(),
            settings.GOOGLE_CLIENT_ID,
        )
    except ValueError as exc:
        raise ValueError("Invalid Google credential") from exc

    email = google_user.get("email")
    email_verified = google_user.get("email_verified")

    if not email or not email_verified:
        raise ValueError("Google account email is not verified")

    return google_user
