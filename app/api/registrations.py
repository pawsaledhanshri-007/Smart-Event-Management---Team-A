from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_admin, get_current_user
from app.models.event import Event
from app.models.registration import Registration
from app.schemas.registration import Registration as RegistrationSchema
from app.models.user import User

router = APIRouter()

@router.post("/events/{event_id}/register", response_model=RegistrationSchema, status_code=status.HTTP_201_CREATED)
def register_for_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Register current user for an event.
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    if event.status != "SCHEDULED":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event is not scheduled")
        
    # Check if already registered
    existing_reg = db.query(Registration).filter(
        Registration.user_id == current_user.id,
        Registration.event_id == event_id,
        Registration.status == "REGISTERED"
    ).first()
    if existing_reg:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already registered for this event")
        
    # Check capacity
    current_registrations_count = db.query(Registration).filter(
        Registration.event_id == event_id,
        Registration.status == "REGISTERED"
    ).count()
    if current_registrations_count >= event.capacity:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Event capacity exceeded")
        
    registration = Registration(
        user_id=current_user.id,
        event_id=event_id,
        status="REGISTERED"
    )
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

@router.delete("/events/{event_id}/register", status_code=status.HTTP_204_NO_CONTENT)
def cancel_registration(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cancel registration for an event.
    """
    registration = db.query(Registration).filter(
        Registration.user_id == current_user.id,
        Registration.event_id == event_id,
        Registration.status == "REGISTERED"
    ).first()
    
    if not registration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
        
    registration.status = "CANCELLED"
    db.commit()
    return None

@router.get("/events/{event_id}/registrations", response_model=List[RegistrationSchema])
def get_event_registrations(
    event_id: int,
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """
    Get all registrations for a specific event. Only for admins.
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        
    registrations = db.query(Registration).filter(Registration.event_id == event_id).offset(skip).limit(limit).all()
    return registrations

@router.get("/registrations/me", response_model=List[RegistrationSchema])
def get_my_registrations(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get current user's registrations.
    """
    registrations = db.query(Registration).filter(Registration.user_id == current_user.id).offset(skip).limit(limit).all()
    return registrations
