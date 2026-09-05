from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_admin, get_current_user
from app.models.venue import Venue
from app.schemas.venue import Venue as VenueSchema, VenueCreate, VenueUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[VenueSchema])
def read_venues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve venues.
    """
    venues = db.query(Venue).offset(skip).limit(limit).all()
    return venues

@router.get("/{id}", response_model=VenueSchema)
def read_venue(id: int, db: Session = Depends(get_db)):
    """
    Get venue by ID.
    """
    venue = db.query(Venue).filter(Venue.id == id).first()
    if not venue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")
    return venue

@router.post("/", response_model=VenueSchema, status_code=status.HTTP_201_CREATED)
def create_venue(
    *,
    db: Session = Depends(get_db),
    venue_in: VenueCreate,
    current_user: User = Depends(get_current_admin),
):
    """
    Create new venue. Only for admins.
    """
    venue = Venue(
        name=venue_in.name,
        capacity=venue_in.capacity,
        location=venue_in.location
    )
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue

@router.put("/{id}", response_model=VenueSchema)
def update_venue(
    *,
    db: Session = Depends(get_db),
    id: int,
    venue_in: VenueUpdate,
    current_user: User = Depends(get_current_admin),
):
    """
    Update a venue. Only for admins.
    """
    venue = db.query(Venue).filter(Venue.id == id).first()
    if not venue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")
    
    update_data = venue_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(venue, field, value)
    
    db.commit()
    db.refresh(venue)
    return venue
