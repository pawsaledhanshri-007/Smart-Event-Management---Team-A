import base64
import hashlib
import hmac
import secrets
import struct
import time
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import quote
from uuid import UUID

from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def hash_token_id(token_id: str) -> str:
    return hashlib.sha256(token_id.encode("utf-8")).hexdigest()


def create_access_token(
    subject: Any,
    session_id: UUID | str | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    expire = (
        now + expires_delta
        if expires_delta
        else now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": "access",
        "iat": now,
        "exp": expire,
    }
    if session_id is not None:
        payload["sid"] = str(session_id)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(
    subject: Any,
    session_id: UUID | str,
    jti: str,
    expires_delta: timedelta | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    expire = (
        now + expires_delta
        if expires_delta
        else now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    payload = {
        "sub": str(subject),
        "sid": str(session_id),
        "jti": jti,
        "type": "refresh",
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_purpose_token(
    subject: Any,
    purpose: str,
    expires_delta: timedelta,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": "action",
        "purpose": purpose,
        "iat": now,
        "exp": now + expires_delta,
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, expected_type: str | None = None) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise ValueError("Invalid or expired token") from exc

    if expected_type is not None and payload.get("type") != expected_type:
        raise ValueError("Invalid token type")
    return payload


def decode_purpose_token(token: str, expected_purpose: str) -> dict[str, Any]:
    payload = decode_token(token, expected_type="action")
    if payload.get("purpose") != expected_purpose:
        raise ValueError("Invalid token purpose")
    return payload


def generate_totp_secret() -> str:
    # 160-bit random secret encoded as Base32 for authenticator apps.
    return base64.b32encode(secrets.token_bytes(20)).decode("ascii").rstrip("=")


def build_totp_uri(secret: str, email: str) -> str:
    issuer = settings.PROJECT_NAME
    label = quote(f"{issuer}:{email}")
    return (
        f"otpauth://totp/{label}?secret={secret}"
        f"&issuer={quote(issuer)}&algorithm=SHA1&digits=6&period=30"
    )


def _totp_code(secret: str, at_time: int, digits: int = 6, period: int = 30) -> str:
    padding = "=" * ((8 - len(secret) % 8) % 8)
    key = base64.b32decode((secret + padding).upper(), casefold=True)
    counter = int(at_time // period)
    message = struct.pack(">Q", counter)
    digest = hmac.new(key, message, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    binary = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(binary % (10 ** digits)).zfill(digits)


def verify_totp(secret: str, code: str) -> bool:
    clean_code = str(code).replace(" ", "").strip()
    if not (clean_code.isdigit() and len(clean_code) == 6):
        return False
    now = int(time.time())
    for window in (-1, 0, 1):
        candidate = _totp_code(secret, now + (window * 30))
        if hmac.compare_digest(candidate, clean_code):
            return True
    return False


def verify_google_id_token(credential: str) -> dict[str, Any]:
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
