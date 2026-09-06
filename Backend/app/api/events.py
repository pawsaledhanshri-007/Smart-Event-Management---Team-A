from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.event import EventCreate, EventUpdate, EventResponse
from app.services import event_service

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("", response_model=List[EventResponse])
def get_events():
    return event_service.get_all_events()

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int):
    return event_service.get_event_by_id(event_id)

@router.post("", response_model=EventResponse, status_code=201)
def create_event(event: EventCreate):
    return event_service.create_event(event)

@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event_update: EventUpdate):
    return event_service.update_event(event_id, event_update)

@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int):
    event_service.delete_event(event_id)
    return None
