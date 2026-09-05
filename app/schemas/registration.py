from pydantic import BaseModel
from datetime import datetime

class RegistrationBase(BaseModel):
    event_id: int

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationInDBBase(RegistrationBase):
    id: int
    user_id: int
    status: str
    registered_at: datetime

    class Config:
        from_attributes = True

class Registration(RegistrationInDBBase):
    pass
