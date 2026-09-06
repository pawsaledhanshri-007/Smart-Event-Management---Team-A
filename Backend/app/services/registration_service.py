from typing import List
from app.schemas.registration import RegistrationCreate, RegistrationResponse
from app.repositories.registration_repository import registration_repository
from app.repositories.event_repository import event_repository
from fastapi import HTTPException

def get_registrations_by_event(event_id: int) -> List[RegistrationResponse]:
    event = event_repository.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return registration_repository.get_by_event(event_id)

def get_registrations_by_user(user_id: int) -> List[RegistrationResponse]:
    # Placeholder: Integration point with Authentication team
    # Verify user_id is valid, or this might just return registrations for the authenticated user ID
    return registration_repository.get_by_user(user_id)

def register_user_for_event(event_id: int, user_id: int) -> RegistrationResponse:
    event = event_repository.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    # Placeholder: Integration point with Authentication team
    # Verify user_id exists and is valid
        
    existing_reg = registration_repository.get_by_event_and_user(event_id, user_id)
    if existing_reg:
        raise HTTPException(status_code=409, detail="User already registered for this event")
        
    current_count = registration_repository.count_by_event(event_id)
    if current_count >= event.capacity:
        raise HTTPException(status_code=409, detail="Event capacity exceeded")
        
    reg_create = RegistrationCreate(event_id=event_id, user_id=user_id)
    return registration_repository.create(reg_create)

def cancel_registration(event_id: int, user_id: int) -> bool:
    success = registration_repository.delete(event_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Registration not found")
    return success
