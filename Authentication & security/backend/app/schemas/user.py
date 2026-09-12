from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    age: Optional[int] = None
    college: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    college: Optional[str] = None
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: UUID
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class User(UserInDBBase):
    pass
