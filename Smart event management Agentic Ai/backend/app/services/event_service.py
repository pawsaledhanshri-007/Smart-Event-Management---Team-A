from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Event, Venue

def create_event(
    db: Session,
    title: str,
    description: str | None,
    venue_id: UUID,
    organizer_id: UUID,
    start_time,
    end_time,
    capacity: int,
) -> Event:
    venue = db.scalar(select(Venue).where(Venue.id == venue_id))
    if not venue:
        raise ValueError("Venue does not exist.")

    if end_time <= start_time:
        raise ValueError("Event end time must be after start time.")

    if capacity <= 0:
        raise ValueError("Event capacity must be greater than 0.")

    if capacity > venue.capacity:
        raise ValueError("Event capacity cannot exceed venue capacity.")

    event = Event(
        title=title,
        description=description,
        venue_id=venue_id,
        organizer_id=organizer_id,
        start_time=start_time,
        end_time=end_time,
        capacity=capacity,
        status="scheduled",
    )

    db.add(event)

    try:
        db.commit()
        db.refresh(event)
    except Exception:
        db.rollback()
        raise

    return event
