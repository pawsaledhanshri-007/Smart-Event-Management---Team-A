from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_admin, get_current_user
from app.models.event import Event
from app.models.venue import Venue
from app.schemas.event import Event as EventSchema, EventCreate, EventUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[EventSchema])
def read_events(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve events. Open to any authenticated user.
    """
    events = db.query(Event).offset(skip).limit(limit).all()
    return events

@router.get("/{id}", response_model=EventSchema)
def read_event(
    id: int, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get event by ID.
    """
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

@router.post("/", response_model=EventSchema, status_code=status.HTTP_201_CREATED)
def create_event(
    *,
    db: Session = Depends(get_db),
    event_in: EventCreate,
    current_user: User = Depends(get_current_admin),
):
    """
    Create new event. Only for admins.
    """
    venue = db.query(Venue).filter(Venue.id == event_in.venue_id).first()
    if not venue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")
    
    event = Event(
        **event_in.model_dump(),
        created_by=current_user.id
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.put("/{id}", response_model=EventSchema)
def update_event(
    *,
    db: Session = Depends(get_db),
    id: int,
    event_in: EventUpdate,
    current_user: User = Depends(get_current_admin),
):
    """
    Update an event. Only for admins.
    """
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    if event_in.venue_id is not None:
        venue = db.query(Venue).filter(Venue.id == event_in.venue_id).first()
        if not venue:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")

    update_data = event_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    return event

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_admin),
):
    """
    Delete/Cancel an event. Only for admins.
    """
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    db.delete(event)
    db.commit()
    return None
