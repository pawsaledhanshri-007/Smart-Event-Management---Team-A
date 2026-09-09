from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.schemas.venue import VenueCreate, VenueUpdate, VenueResponse
from app.services import venue_service
from app.db.session import get_db
router = APIRouter()


@router.get("", response_model=List[VenueResponse])
def get_venues(db: Session = Depends(get_db)):
    return venue_service.get_all_venues(db)


@router.get("/{venue_id}", response_model=VenueResponse)
def get_venue(
    venue_id: UUID,
    db: Session = Depends(get_db)
):
    return venue_service.get_venue_by_id(db, venue_id)


@router.post("", response_model=VenueResponse, status_code=201)
def create_venue(
    venue: VenueCreate,
    db: Session = Depends(get_db)
):
    return venue_service.create_venue(db, venue)


@router.put("/{venue_id}", response_model=VenueResponse)
def update_venue(
    venue_id: UUID,
    venue_update: VenueUpdate,
    db: Session = Depends(get_db)
):
    return venue_service.update_venue(db, venue_id, venue_update)


@router.delete("/{venue_id}", status_code=204)
def delete_venue(
    venue_id: UUID,
    db: Session = Depends(get_db)
):
    venue_service.delete_venue(db, venue_id)
    return None
