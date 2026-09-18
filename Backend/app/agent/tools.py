from datetime import datetime
from uuid import UUID

from app.models import Event, Registration
from app.schemas.event import EventCreate, EventUpdate
from app.services.event_service import (
    create_event as create_event_service,
    update_event as update_event_service,
)
from app.services.registration_service import (
    register_user_for_event as service_register_user_for_event,
    cancel_registration as service_cancel_registration,
)
from app.registration_repository import registration_repository
from datetime import datetime, timezone
from uuid import UUID

from langchain_core.tools import tool
from sqlalchemy import or_

from app.db.session import SessionLocal
from app.models.event import Event
from app.models.venue import Venue
from app.repositories.event_repository import event_repository
from app.repositories.venue_repository import venue_repository


@tool
def get_all_events():
    """
    Get all events from the event management system.
    Use this when the user asks to see, list, or browse available events.
    """

    db = SessionLocal()

    try:
        events = event_repository.get_all(db)

        return [
            {
                "id": str(event.id),
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat(),
                "venue_id": str(event.venue_id),
                "capacity": event.capacity,
                "status": event.status,
            }
            for event in events
        ]

    finally:
        db.close()


@tool
def get_event_by_id(event_id: str):
    """
    Get detailed information about a specific event using its UUID.
    Use this when the user asks for details about a particular event.
    """

    db = SessionLocal()

    try:
        event_uuid = UUID(event_id)

        event = event_repository.get_by_id(db, event_uuid)

        if not event:
            return {
                "error": "Event not found"
            }

        return {
            "id": str(event.id),
            "title": event.title,
            "description": event.description,
            "start_time": event.start_time.isoformat(),
            "end_time": event.end_time.isoformat(),
            "venue_id": str(event.venue_id),
            "organizer_id": str(event.organizer_id),
            "capacity": event.capacity,
            "status": event.status,
        }

    except ValueError:
        return {
            "error": "Invalid event ID format. Expected a UUID."
        }

    finally:
        db.close()


@tool
def get_all_venues():
    """
    Get all venues from the event management system.
    Use this when the user asks to list available venues or halls.
    """

    db = SessionLocal()

    try:
        venues = venue_repository.get_all(db)

        return [
            {
                "id": str(venue.id),
                "name": venue.name,
                "location": venue.location,
                "capacity": venue.capacity,
            }
            for venue in venues
        ]

    finally:
        db.close()


@tool
def get_venue_by_id(venue_id: str):
    """
    Get detailed information about a specific venue using its UUID.
    Use this when the user asks about a particular venue or hall.
    """

    db = SessionLocal()

    try:
        venue_uuid = UUID(venue_id)

        venue = venue_repository.get_by_id(db, venue_uuid)

        if not venue:
            return {
                "error": "Venue not found"
            }

        return {
            "id": str(venue.id),
            "name": venue.name,
            "location": venue.location,
            "capacity": venue.capacity,
        }

    except ValueError:
        return {
            "error": "Invalid venue ID format. Expected a UUID."
        }

    finally:
        db.close()
@tool
def find_venues_by_capacity(required_capacity: int):
    """
    Find venues that can accommodate the requested number of people.
    Use this when the user asks for venues suitable for a specific audience size.
    """

    db = SessionLocal()

    try:
        venues = venue_repository.get_all(db)

        suitable_venues = [
            {
                "id": str(venue.id),
                "name": venue.name,
                "location": venue.location,
                "capacity": venue.capacity,
            }
            for venue in venues
            if venue.capacity >= required_capacity
        ]

        if not suitable_venues:
            return {
                "message": f"No venue can accommodate {required_capacity} people."
            }

        return {
            "required_capacity": required_capacity,
            "suitable_venues": suitable_venues,
        }

    finally:
        db.close()
@tool
def check_venue_availability(
    venue_name: str,
    requested_start: str,
    requested_end: str,
):
    """
    Check whether a venue is available during a requested time range.

    requested_start and requested_end must be ISO 8601 datetime strings,
    for example: 2026-09-25T10:00:00+05:30
    """

    db = SessionLocal()

    try:
        venue = (
            db.query(Venue)
            .filter(Venue.name.ilike(venue_name))
            .first()
        )

        if not venue:
            return {
                "available": False,
                "message": f"Venue '{venue_name}' was not found."
            }

        try:
            start_time = datetime.fromisoformat(requested_start)
            end_time = datetime.fromisoformat(requested_end)
        except ValueError:
            return {
                "available": False,
                "message": (
                    "Invalid date-time format. "
                    "Use ISO format such as "
                    "2026-09-25T10:00:00+05:30."
                )
            }

        if end_time <= start_time:
            return {
                "available": False,
                "message": "The requested end time must be after the start time."
            }

        overlapping_event = (
            db.query(Event)
            .filter(
                Event.venue_id == venue.id,
                Event.status != "cancelled",
                Event.start_time < end_time,
                Event.end_time > start_time,
            )
            .first()
        )

        if overlapping_event:
            return {
                "available": False,
                "venue": venue.name,
                "location": venue.location,
                "message": (
                    f"The venue is occupied by the event "
                    f"'{overlapping_event.title}' during the requested time."
                ),
                "conflicting_event": {
                    "id": str(overlapping_event.id),
                    "title": overlapping_event.title,
                    "start_time": overlapping_event.start_time.isoformat(),
                    "end_time": overlapping_event.end_time.isoformat(),
                    "status": overlapping_event.status,
                },
            }

        return {
            "available": True,
            "venue": venue.name,
            "location": venue.location,
            "capacity": venue.capacity,
            "message": "The venue is available during the requested time.",
        }

    finally:
        db.close()
@tool
def search_events(keyword: str):
    """
    Search events by keyword in their title or description.
    Use this when the user asks to find events related to a topic.
    """

    db = SessionLocal()

    try:
        search_pattern = f"%{keyword}%"

        events = (
            db.query(Event)
            .filter(
                or_(
                    Event.title.ilike(search_pattern),
                    Event.description.ilike(search_pattern),
                )
            )
            .all()
        )

        if not events:
            return {
                "message": f"No events found matching '{keyword}'."
            }

        return [
            {
                "id": str(event.id),
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat(),
                "venue_id": str(event.venue_id),
                "capacity": event.capacity,
                "status": event.status,
            }
            for event in events
        ]

    finally:
        db.close()


@tool
def get_upcoming_events():
    """
    Get upcoming scheduled events.
    Use this when the user asks about future or upcoming events.
    """

    db = SessionLocal()

    try:
        now = datetime.now(timezone.utc)

        events = (
            db.query(Event)
            .filter(
                Event.start_time >= now,
                Event.status == "scheduled",
            )
            .order_by(Event.start_time)
            .all()
        )

        if not events:
            return {
                "message": "There are no upcoming scheduled events."
            }

        return [
            {
                "id": str(event.id),
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat(),
                "venue_id": str(event.venue_id),
                "capacity": event.capacity,
                "status": event.status,
            }
            for event in events
        ]

    finally:
        db.close()
@tool
def get_events_by_status(status: str):
    """
    Get events filtered by status.

    Valid statuses:
    scheduled, ongoing, completed, cancelled
    """

    db = SessionLocal()

    try:
        valid_statuses = {
            "scheduled",
            "ongoing",
            "completed",
            "cancelled",
        }

        status = status.lower().strip()

        if status not in valid_statuses:
            return {
                "error": (
                    "Invalid status. Use one of: "
                    "scheduled, ongoing, completed, cancelled."
                )
            }

        events = (
            db.query(Event)
            .filter(Event.status == status)
            .order_by(Event.start_time)
            .all()
        )

        if not events:
            return {
                "message": f"No events found with status '{status}'."
            }

        return [
            {
                "id": str(event.id),
                "title": event.title,
                "description": event.description,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat(),
                "venue_id": str(event.venue_id),
                "capacity": event.capacity,
                "status": event.status,
            }
            for event in events
        ]

    finally:
        db.close()


@tool
def get_events_at_venue(venue_name: str):
    """
    Get all events associated with a particular venue name.
    """

    db = SessionLocal()

    try:
        venue = (
            db.query(Venue)
            .filter(Venue.name.ilike(venue_name))
            .first()
        )

        if not venue:
            return {
                "message": f"Venue '{venue_name}' was not found."
            }

        events = (
            db.query(Event)
            .filter(Event.venue_id == venue.id)
            .order_by(Event.start_time)
            .all()
        )

        if not events:
            return {
                "message": f"No events are associated with '{venue.name}'."
            }

        return {
            "venue": {
                "id": str(venue.id),
                "name": venue.name,
                "location": venue.location,
                "capacity": venue.capacity,
            },
            "events": [
                {
                    "id": str(event.id),
                    "title": event.title,
                    "description": event.description,
                    "start_time": event.start_time.isoformat(),
                    "end_time": event.end_time.isoformat(),
                    "capacity": event.capacity,
                    "status": event.status,
                }
                for event in events
            ],
        }

    finally:
        db.close()
@tool
def get_all_registrations():
    """
    Get all registrations in the event management system.
    Use this when the user asks about registrations, attendees, or bookings.
    """

    db = SessionLocal()

    try:
        registrations = registration_repository.get_all(db)

        return [
            {
                "id": str(registration.id),
                "user_id": str(registration.user_id),
                "event_id": str(registration.event_id),
                "status": registration.status,
                "registered_at": registration.registered_at.isoformat(),
                "cancelled_at": (
                    registration.cancelled_at.isoformat()
                    if registration.cancelled_at
                    else None
                ),
            }
            for registration in registrations
        ]

    finally:
        db.close()


@tool
def get_registrations_for_event(event_id: str):
    """
    Get all registrations for a specific event using its UUID.
    Use this when the user asks how many people registered for an event
    or asks for the attendees/bookings of a particular event.
    """

    db = SessionLocal()

    try:
        event_uuid = UUID(event_id)

        registrations = registration_repository.get_by_event_id(
            db,
            event_uuid
        )

        return [
            {
                "id": str(registration.id),
                "user_id": str(registration.user_id),
                "event_id": str(registration.event_id),
                "status": registration.status,
                "registered_at": registration.registered_at.isoformat(),
                "cancelled_at": (
                    registration.cancelled_at.isoformat()
                    if registration.cancelled_at
                    else None
                ),
            }
            for registration in registrations
        ]

    except ValueError:
        return {
            "error": "Invalid event ID format. Expected a UUID."
        }

    finally:
        db.close()
@tool
def register_for_event(user_id: str, event_id: str):
    """
    Register a user for an event.

    Both user_id and event_id must be valid UUID strings.
    Use this when the user explicitly wants to register for an event.
    """

    db = SessionLocal()

    try:
        user_uuid = UUID(user_id)
        event_uuid = UUID(event_id)

        registration = service_register_user_for_event(
            db=db,
            user_id=user_uuid,
            event_id=event_uuid,
        )

        return {
            "success": True,
            "message": "User successfully registered for the event.",
            "registration": {
                "id": str(registration.id),
                "user_id": str(registration.user_id),
                "event_id": str(registration.event_id),
                "status": registration.status,
                "registered_at": registration.registered_at.isoformat(),
            },
        }

    except ValueError as error:
        return {
            "success": False,
            "error": str(error),
        }

    finally:
        db.close()


@tool
def cancel_event_registration(user_id: str, event_id: str):
    """
    Cancel a user's registration for an event.

    Both user_id and event_id must be valid UUID strings.
    Use this when the user explicitly wants to cancel a registration.
    """

    db = SessionLocal()

    try:
        user_uuid = UUID(user_id)
        event_uuid = UUID(event_id)

        registration = service_cancel_registration(
            db=db,
            user_id=user_uuid,
            event_id=event_uuid,
        )

        return {
            "success": True,
            "message": "Registration successfully cancelled.",
            "registration": {
                "id": str(registration.id),
                "user_id": str(registration.user_id),
                "event_id": str(registration.event_id),
                "status": registration.status,
                "registered_at": registration.registered_at.isoformat(),
                "cancelled_at": (
                    registration.cancelled_at.isoformat()
                    if registration.cancelled_at
                    else None
                ),
            },
        }

    except ValueError as error:
        return {
            "success": False,
            "error": str(error),
        }

    finally:
        db.close()
@tool
def create_event(
    title: str,
    description: str,
    venue_id: str,
    organizer_id: str,
    start_time: str,
    end_time: str,
    capacity: int,
    status: str = "scheduled",
):
    """Create a new event."""

    db = SessionLocal()

    try:
        event_data = EventCreate(
            title=title,
            description=description,
            venue_id=UUID(venue_id),
            organizer_id=UUID(organizer_id),
            start_time=datetime.fromisoformat(start_time),
            end_time=datetime.fromisoformat(end_time),
            capacity=capacity,
            status=status,
        )

        event = create_event_service(db, event_data)

        return {
            "success": True,
            "message": "Event created successfully.",
            "event_id": str(event.id),
            "title": event.title,
            "status": event.status,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

    finally:
        db.close()


@tool
def update_event(
    event_id: str,
    title: str | None = None,
    description: str | None = None,
    venue_id: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    capacity: int | None = None,
    status: str | None = None,
):
    """Update an existing event."""

    db = SessionLocal()

    try:
        update_data = {}

        if title is not None:
            update_data["title"] = title

        if description is not None:
            update_data["description"] = description

        if venue_id is not None:
            update_data["venue_id"] = UUID(venue_id)

        if start_time is not None:
            update_data["start_time"] = datetime.fromisoformat(start_time)

        if end_time is not None:
            update_data["end_time"] = datetime.fromisoformat(end_time)

        if capacity is not None:
            update_data["capacity"] = capacity

        if status is not None:
            update_data["status"] = status

        event_update = EventUpdate(**update_data)

        event = update_event_service(
            db,
            UUID(event_id),
            event_update,
        )

        return {
            "success": True,
            "message": "Event updated successfully.",
            "event_id": str(event.id),
            "title": event.title,
            "status": event.status,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

    finally:
        db.close()


@tool
def cancel_event(event_id: str):
    """Cancel an event by changing its status to cancelled."""

    db = SessionLocal()

    try:
        event = db.get(Event, UUID(event_id))

        if not event:
            return {
                "success": False,
                "error": "Event not found.",
            }

        if event.status == "cancelled":
            return {
                "success": False,
                "error": "Event is already cancelled.",
            }

        event.status = "cancelled"

        db.commit()
        db.refresh(event)

        return {
            "success": True,
            "message": "Event cancelled successfully.",
            "event_id": str(event.id),
            "title": event.title,
            "status": event.status,
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "error": str(e),
        }

    finally:
        db.close()


@tool
def get_user_registrations(user_id: str):
    """Get all event registrations for a specific user."""

    db = SessionLocal()

    try:
        registrations = (
            db.query(Registration)
            .filter(Registration.user_id == UUID(user_id))
            .all()
        )

        result = []

        for registration in registrations:
            result.append({
                "registration_id": str(registration.id),
                "event_id": str(registration.event_id),
                "event_title": registration.event.title,
                "status": registration.status,
                "registered_at": (
                    registration.registered_at.isoformat()
                    if registration.registered_at
                    else None
                ),
                "cancelled_at": (
                    registration.cancelled_at.isoformat()
                    if registration.cancelled_at
                    else None
                ),
            })

        return {
            "success": True,
            "user_id": user_id,
            "registrations": result,
            "count": len(result),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

    finally:
        db.close()