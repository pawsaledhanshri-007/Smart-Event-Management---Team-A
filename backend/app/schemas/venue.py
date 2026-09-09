from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class VenueBase(BaseModel):
    name: str
    location: Optional[str] = None
    capacity: int


class VenueCreate(VenueBase):
    pass


class VenueUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None


class VenueResponse(VenueBase):
    id: UUID

    model_config = {"from_attributes": True}
