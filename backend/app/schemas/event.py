from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    venue_id: Optional[UUID] = None
    capacity: int
    registration_fee: float = Field(default=0, ge=0)
    organizer_id: UUID
    status: str = "scheduled"


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    venue_id: UUID
    capacity: int
    registration_fee: float = Field(default=0, ge=0)


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    venue_id: Optional[UUID] = None
    capacity: Optional[int] = None
    organizer_id: Optional[UUID] = None
    status: Optional[str] = None


class EventResponse(EventBase):
    id: UUID

    model_config = {"from_attributes": True}
