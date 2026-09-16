from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginResponse(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    two_factor_required: bool = False
    challenge_token: Optional[str] = None


class TokenPayload(BaseModel):
    sub: Optional[UUID] = None
    sid: Optional[UUID] = None
    type: Optional[str] = None
    jti: Optional[str] = None
    purpose: Optional[str] = None


class GoogleLoginRequest(BaseModel):
    credential: str
