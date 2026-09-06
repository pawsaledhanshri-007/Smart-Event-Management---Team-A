from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.venue import VenueCreate, VenueUpdate, VenueResponse
from app.services import venue_service

router = APIRouter(prefix="/venues", tags=["Venues"])

@router.get("", response_model=List[VenueResponse])
def get_venues():
    return venue_service.get_all_venues()

@router.get("/{venue_id}", response_model=VenueResponse)
def get_venue(venue_id: int):
    return venue_service.get_venue_by_id(venue_id)

@router.post("", response_model=VenueResponse, status_code=201)
def create_venue(venue: VenueCreate):
    return venue_service.create_venue(venue)

@router.put("/{venue_id}", response_model=VenueResponse)
def update_venue(venue_id: int, venue_update: VenueUpdate):
    return venue_service.update_venue(venue_id, venue_update)
