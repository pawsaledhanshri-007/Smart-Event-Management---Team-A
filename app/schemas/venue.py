from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VenueBase(BaseModel):
    name: str
    capacity: int
    location: str

class VenueCreate(VenueBase):
    pass

class VenueUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None
    location: Optional[str] = None

class VenueInDBBase(VenueBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Venue(VenueInDBBase):
    pass
