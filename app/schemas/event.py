from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    time: time
    venue_id: int
    capacity: int

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    venue_id: Optional[int] = None
    capacity: Optional[int] = None
    status: Optional[str] = None

class EventInDBBase(EventBase):
    id: int
    status: str
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Event(EventInDBBase):
    pass
