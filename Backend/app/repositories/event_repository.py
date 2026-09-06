from typing import List, Optional
from app.schemas.event import EventCreate, EventUpdate, EventResponse

class EventRepository:
    def __init__(self):
        self._events = {}
        self._id_counter = 1

    def get_all(self) -> List[EventResponse]:
        return list(self._events.values())

    def get_by_id(self, event_id: int) -> Optional[EventResponse]:
        return self._events.get(event_id)

    def create(self, event: EventCreate) -> EventResponse:
        event_id = self._id_counter
        self._id_counter += 1
        new_event = EventResponse(id=event_id, **event.model_dump())
        self._events[event_id] = new_event
        return new_event

    def update(self, event_id: int, event_update: EventUpdate) -> Optional[EventResponse]:
        if event_id not in self._events:
            return None
        existing_event = self._events[event_id]
        update_data = event_update.model_dump(exclude_unset=True)
        updated_event = existing_event.model_copy(update=update_data)
        self._events[event_id] = updated_event
        return updated_event

    def delete(self, event_id: int) -> bool:
        if event_id in self._events:
            del self._events[event_id]
            return True
        return False

event_repository = EventRepository()
