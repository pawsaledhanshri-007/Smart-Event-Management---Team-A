from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    age: Optional[int] = None
    college: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    college: Optional[str] = None


class UserInDBBase(UserBase):
    id: UUID
    role: str
    is_active: bool
    is_email_verified: bool
    is_2fa_enabled: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class User(UserInDBBase):
    pass
