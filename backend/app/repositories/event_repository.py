from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


class EventRepository:

    def get_all(self, db: Session) -> List[Event]:
        return db.query(Event).all()

    def get_by_id(
        self,
        db: Session,
        event_id: UUID
    ) -> Optional[Event]:
        return db.query(Event).filter(Event.id == event_id).first()

    def create(
        self,
        db: Session,
        event: EventCreate
    ) -> Event:

        new_event = Event(
            title=event.title,
            description=event.description,
            start_time=event.start_time,
            end_time=event.end_time,
            venue_id=event.venue_id,
            capacity=event.capacity,
            organizer_id=event.organizer_id,
            status=event.status,
        )

        db.add(new_event)
        db.commit()
        db.refresh(new_event)

        return new_event

    def update(
        self,
        db: Session,
        event_id: UUID,
        event_update: EventUpdate
    ) -> Optional[Event]:

        existing_event = self.get_by_id(db, event_id)

        if not existing_event:
            return None

        update_data = event_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(existing_event, field, value)

        db.commit()
        db.refresh(existing_event)

        return existing_event

    def delete(
        self,
        db: Session,
        event_id: UUID
    ) -> bool:

        existing_event = self.get_by_id(db, event_id)

        if not existing_event:
            return False

        db.delete(existing_event)
        db.commit()

        return True


event_repository = EventRepository()
