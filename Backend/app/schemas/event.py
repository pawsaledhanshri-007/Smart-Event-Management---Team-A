from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    date_time: datetime
    venue_id: int
    capacity: int
    organizer_id: int

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date_time: Optional[datetime] = None
    venue_id: Optional[int] = None
    capacity: Optional[int] = None
    organizer_id: Optional[int] = None

class EventResponse(EventBase):
    id: int

    model_config = {"from_attributes": True}
