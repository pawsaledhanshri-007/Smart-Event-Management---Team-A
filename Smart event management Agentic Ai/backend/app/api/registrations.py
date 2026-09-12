from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.schemas.registration import RegistrationResponse
from app.services import registration_service
from app.db.session import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter(tags=["Registrations"])

@router.post(
    "/events/{event_id}/register",
    response_model=RegistrationResponse,
    status_code=201
)
def register_for_event(
    event_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return registration_service.register_user_for_event(
        db,
        current_user.id,
        event_id,
    )

@router.delete(
    "/events/{event_id}/register",
    status_code=204
)
def cancel_registration(
    event_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    registration_service.cancel_registration(
        db,
        current_user.id,
        event_id,
    )
    return None

@router.get(
    "/events/{event_id}/registrations",
    response_model=List[RegistrationResponse]
)
def get_event_registrations(
    event_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return registration_service.get_registrations_by_user(
        db,
        current_user.id
    )
