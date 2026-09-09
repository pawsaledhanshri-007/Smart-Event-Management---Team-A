from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class RegistrationBase(BaseModel):
    event_id: UUID
    user_id: UUID


class RegistrationCreate(RegistrationBase):
    pass


class RegistrationResponse(RegistrationBase):
    id: UUID
    registered_at: datetime

    model_config = {"from_attributes": True}
