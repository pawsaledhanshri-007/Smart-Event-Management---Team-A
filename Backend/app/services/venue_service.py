from typing import List, Optional
from app.schemas.venue import VenueCreate, VenueUpdate, VenueResponse
from app.repositories.venue_repository import venue_repository
from fastapi import HTTPException

def get_all_venues() -> List[VenueResponse]:
    return venue_repository.get_all()

def get_venue_by_id(venue_id: int) -> VenueResponse:
    venue = venue_repository.get_by_id(venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue

def create_venue(venue: VenueCreate) -> VenueResponse:
    return venue_repository.create(venue)

def update_venue(venue_id: int, venue_update: VenueUpdate) -> VenueResponse:
    venue = venue_repository.update(venue_id, venue_update)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue
