from typing import List
from app.schemas.event import EventCreate, EventUpdate, EventResponse
from app.repositories.event_repository import event_repository
from app.repositories.venue_repository import venue_repository
from fastapi import HTTPException

def get_all_events() -> List[EventResponse]:
    return event_repository.get_all()

def get_event_by_id(event_id: int) -> EventResponse:
    event = event_repository.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

def create_event(event: EventCreate) -> EventResponse:
    venue = venue_repository.get_by_id(event.venue_id)
    if not venue:
        raise HTTPException(status_code=400, detail="Invalid venue_id")
    
    # Placeholder: Integration point with Authentication team
    # Verify organizer_id belongs to a valid user/has permissions here
    
    return event_repository.create(event)

def update_event(event_id: int, event_update: EventUpdate) -> EventResponse:
    if event_update.venue_id is not None:
        venue = venue_repository.get_by_id(event_update.venue_id)
        if not venue:
            raise HTTPException(status_code=400, detail="Invalid venue_id")
            
    if event_update.organizer_id is not None:
        # Placeholder: Integration point with Authentication team
        # Verify new organizer_id is valid
        pass

    event = event_repository.update(event_id, event_update)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

def delete_event(event_id: int) -> bool:
    success = event_repository.delete(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return success
