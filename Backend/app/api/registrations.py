from fastapi import APIRouter, HTTPException, Query, Body
from typing import List
from app.schemas.registration import RegistrationResponse
from app.services import registration_service
from pydantic import BaseModel

router = APIRouter(tags=["Registrations"])

class RegisterRequest(BaseModel):
    user_id: int

@router.post("/events/{event_id}/register", response_model=RegistrationResponse, status_code=201)
def register_for_event(event_id: int, request: RegisterRequest):
    return registration_service.register_user_for_event(event_id, request.user_id)

@router.delete("/events/{event_id}/register", status_code=204)
def cancel_registration(event_id: int, user_id: int = Query(...)):
    registration_service.cancel_registration(event_id, user_id)
    return None

@router.get("/events/{event_id}/registrations", response_model=List[RegistrationResponse])
def get_event_registrations(event_id: int):
    return registration_service.get_registrations_by_event(event_id)

@router.get("/registrations/me", response_model=List[RegistrationResponse])
def get_my_registrations(user_id: int = Query(..., description="The ID of the user")):
    # Explicit user_id since no auth
    return registration_service.get_registrations_by_user(user_id)
