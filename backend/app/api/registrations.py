from fastapi import APIRouter, Query, Depends
from typing import List
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.schemas.registration import RegistrationResponse
from app.services import registration_service
from app.db.session import get_db


router = APIRouter(tags=["Registrations"])


class RegisterRequest(BaseModel):
    user_id: UUID


@router.post(
    "/events/{event_id}/register",
    response_model=RegistrationResponse,
    status_code=201
)
def register_for_event(
    event_id: UUID,
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    return registration_service.register_user_for_event(
        db,
        event_id,
        request.user_id
    )


@router.delete(
    "/events/{event_id}/register",
    status_code=204
)
def cancel_registration(
    event_id: UUID,
    user_id: UUID = Query(...),
    db: Session = Depends(get_db)
):
    registration_service.cancel_registration(
        db,
        event_id,
        user_id
    )
    return None


@router.get(
    "/events/{event_id}/registrations",
    response_model=List[RegistrationResponse]
)
def get_event_registrations(
    event_id: UUID,
    db: Session = Depends(get_db)
):
    return registration_service.get_registrations_by_event(
        db,
        event_id
    )


@router.get(
    "/registrations/me",
    response_model=List[RegistrationResponse]
)
def get_my_registrations(
    user_id: UUID = Query(..., description="The ID of the user"),
    db: Session = Depends(get_db)
):
    return registration_service.get_registrations_by_user(
        db,
        user_id
    )
