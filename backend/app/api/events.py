from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.schemas.event import EventCreate, EventUpdate, EventResponse
from app.services import event_service
from app.db.session import get_db

router = APIRouter()


@router.get("", response_model=List[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return event_service.get_all_events(db)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: UUID,
    db: Session = Depends(get_db)
):
    return event_service.get_event_by_id(db, event_id)


@router.post("", response_model=EventResponse, status_code=201)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    return event_service.create_event(db, event)


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: UUID,
    event_update: EventUpdate,
    db: Session = Depends(get_db)
):
    return event_service.update_event(
        db,
        event_id,
        event_update
    )


@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: UUID,
    db: Session = Depends(get_db)
):
    event_service.delete_event(db, event_id)
    return None
