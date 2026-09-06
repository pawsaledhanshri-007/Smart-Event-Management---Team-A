from pydantic import BaseModel
from datetime import datetime

class RegistrationBase(BaseModel):
    event_id: int
    user_id: int

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationResponse(RegistrationBase):
    id: int
    registered_at: datetime

    model_config = {"from_attributes": True}
