from pydantic import BaseModel
from typing import Optional

class VenueBase(BaseModel):
    name: str
    location: str
    capacity: int

class VenueCreate(VenueBase):
    pass

class VenueUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None

class VenueResponse(VenueBase):
    id: int

    model_config = {"from_attributes": True}
