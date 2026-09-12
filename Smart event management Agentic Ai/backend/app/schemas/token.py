from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[UUID] = None
    role: Optional[str] = None


class GoogleLoginRequest(BaseModel):
    # Google Identity Services sends this ID token to the frontend as "credential".
    credential: str
