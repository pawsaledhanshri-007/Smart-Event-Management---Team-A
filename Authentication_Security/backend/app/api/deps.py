from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.models.auth_session import AuthSession
from app.models.user import User, UserRole
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = security.decode_token(token, expected_type="access")
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise credentials_exception
    except (ValueError, TypeError):
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.sub).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # New tokens include a server-side session id. Checking it here makes
    # logout/revocation effective immediately for access tokens as well.
    # sid remains optional only to avoid instantly breaking legacy tokens.
    if token_data.sid is not None:
        auth_session = (
            db.query(AuthSession)
            .filter(AuthSession.id == token_data.sid)
            .first()
        )
        now = datetime.now(timezone.utc)
        if (
            auth_session is None
            or auth_session.user_id != user.id
            or auth_session.revoked_at is not None
            or auth_session.expires_at <= now
        ):
            raise credentials_exception

    return user


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required",
        )
    return current_user


def get_current_event_manager(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role not in {
        UserRole.ADMIN.value,
        UserRole.ORGANIZER.value,
    }:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or organizer permission required",
        )
    return current_user
