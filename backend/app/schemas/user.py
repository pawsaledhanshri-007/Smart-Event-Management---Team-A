from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    age: Optional[int] = None
    college: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update
class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    college: Optional[str] = None
    password: Optional[str] = None


# Properties stored in database and returned by API
class UserInDBBase(UserBase):
    id: UUID
    role: str
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# Additional properties to return via API
class User(UserInDBBase):
    pass