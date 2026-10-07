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
    registration_fee: float = 0,
) -> Event:

    # 1. Check venue exists
    venue = db.scalar(
        select(Venue).where(Venue.id == venue_id)
    )

    if not venue:
        raise ValueError("Venue does not exist.")

    # 2. Check event time
    if end_time <= start_time:
        raise ValueError(
            "Event end time must be after start time."
        )

    # 3. Check capacity
    if capacity <= 0:
        raise ValueError(
            "Event capacity must be greater than 0."
        )

    # 4. Check capacity does not exceed venue capacity
    if capacity > venue.capacity:
        raise ValueError(
            "Event capacity cannot exceed venue capacity."
        )

    # 5. Create event
    event = Event(
        title=title,
        description=description,
        venue_id=venue_id,
        organizer_id=organizer_id,
        start_time=start_time,
        end_time=end_time,
        capacity=capacity,
	registration_fee=registration_fee,
        status="scheduled",
    )

    db.add(event)

    # 6. Save
    try:
        db.commit()
        db.refresh(event)

    except Exception:
        db.rollback()
        raise

    return event

from datetime import datetime, timezone


def _sync_event_status(event: Event) -> Event:
    now = datetime.now(timezone.utc)

    if event.status == "cancelled":
        return event

    if now >= event.end_time:
        event.status = "completed"
    elif now >= event.start_time:
        event.status = "ongoing"
    else:
        event.status = "scheduled"

    return event

def get_all_events(db: Session) -> list[Event]:
    events = list(db.scalars(select(Event)).all())

    changed = False

    for event in events:
        old_status = event.status
        _sync_event_status(event)

        if old_status != event.status:
            changed = True

    if changed:
        db.commit()

    return events

def get_event_by_id(db: Session, event_id: UUID) -> Event:
    event = db.scalar(
        select(Event).where(Event.id == event_id)
    )

    if not event:
        raise ValueError("Event does not exist.")

    old_status = event.status
    _sync_event_status(event)

    if old_status != event.status:
        db.commit()
        db.refresh(event)

    return event

def update_event(
    db: Session,
    event_id: UUID,
    event_update,
) -> Event:

    event = db.scalar(
        select(Event).where(Event.id == event_id)
    )

    if not event:
        raise ValueError("Event does not exist.")

    update_data = event_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(event, field, value)

    try:
        db.commit()
        db.refresh(event)
    except Exception:
        db.rollback()
        raise

    return event

def delete_event(
    db: Session,
    event_id: UUID,
) -> None:

    event = db.scalar(
        select(Event).where(Event.id == event_id)
    )

    if not event:
        raise ValueError("Event does not exist.")

    db.delete(event)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise