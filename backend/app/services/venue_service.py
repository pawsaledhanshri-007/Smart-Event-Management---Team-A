from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Event, Venue


def get_venue_available_events(
    db: Session,
    venue_id: UUID,
) -> list[Event]:

    # 1. Check venue exists
    venue = db.scalar(
        select(Venue).where(Venue.id == venue_id)
    )

    if not venue:
        raise ValueError("Venue does not exist.")

    # 2. Get scheduled/ongoing events at this venue
    events = db.scalars(
        select(Event)
        .where(
            Event.venue_id == venue_id,
            Event.status.in_(["scheduled", "ongoing"]),
        )
        .order_by(Event.start_time)
    ).all()

    return list(events)

def check_venue_available(
    db: Session,
    venue_id: UUID,
    start_time,
    end_time,
) -> bool:

    # 1. Check venue exists
    venue = db.scalar(
        select(Venue).where(Venue.id == venue_id)
    )

    if not venue:
        raise ValueError("Venue does not exist.")

    # 2. Validate time
    if end_time <= start_time:
        raise ValueError(
            "Event end time must be after start time."
        )

    # 3. Find overlapping events
    overlapping_event = db.scalar(
        select(Event).where(
            Event.venue_id == venue_id,
            Event.status.in_(["scheduled", "ongoing"]),
            Event.start_time < end_time,
            Event.end_time > start_time,
        )
    )

    # 4. Return availability
    return overlapping_event is None