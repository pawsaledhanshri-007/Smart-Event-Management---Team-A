from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import User, Event, Registration


def register_user_for_event(
    db: Session,
    user_id: UUID,
    event_id: UUID,
) -> Registration:

    # 1. Check user exists
    user = db.scalar(
        select(User).where(
            User.id == user_id,
            User.is_active.is_(True)
        )
    )

    if not user:
        raise ValueError("User does not exist or is inactive.")

    # 2. Check event exists
    event = db.scalar(
        select(Event).where(Event.id == event_id)
    )

    if not event:
        raise ValueError("Event does not exist.")

    # 3. Check event status
    if event.status != "scheduled":
        raise ValueError(
            f"Registration is not allowed for an event with status '{event.status}'."
        )

    # 4. Check whether user is already registered
    existing_registration = db.scalar(
        select(Registration).where(
            Registration.user_id == user_id,
            Registration.event_id == event_id,
        )
    )

    if existing_registration:
        if existing_registration.status == "confirmed":
            raise ValueError(
                "User is already registered for this event."
            )

        # Re-activate a previously cancelled registration
        if existing_registration.status == "cancelled":
            existing_registration.status = "confirmed"
            existing_registration.cancelled_at = None

            db.commit()
            db.refresh(existing_registration)

            return existing_registration

        raise ValueError(
            "User already has a registration for this event."
        )

    # 5. Check event capacity
    confirmed_count = db.scalar(
    select(func.count(Registration.id)).where(
        Registration.event_id == event_id,
        Registration.status == "confirmed",
        )
    )

    # The query above only checks whether one record exists,
    # so count confirmed registrations separately.

    if confirmed_count >= event.capacity:
        raise ValueError(
            "Event capacity is full."
        )

    # 6. Create registration
    registration = Registration(
        user_id=user_id,
        event_id=event_id,
        status="confirmed",
    )

    db.add(registration)

    # 7. Save to database
    try:
        db.commit()
        db.refresh(registration)

    except Exception:
        db.rollback()
        raise

    return registration

def cancel_registration(
    db: Session,
    user_id: UUID,
    event_id: UUID,
) -> Registration:

    # 1. Find the registration
    registration = db.scalar(
        select(Registration).where(
            Registration.user_id == user_id,
            Registration.event_id == event_id,
        )
    )

    if not registration:
        raise ValueError(
            "User is not registered for this event."
        )

    # 2. Check registration status
    if registration.status == "cancelled":
        raise ValueError(
            "Registration is already cancelled."
        )

    if registration.status != "confirmed":
        raise ValueError(
            f"Registration cannot be cancelled because its status is '{registration.status}'."
        )

    # 3. Cancel the registration
    registration.status = "cancelled"
    registration.cancelled_at = func.now()

    # 4. Save changes
    try:
        db.commit()
        db.refresh(registration)

    except Exception:
        db.rollback()
        raise

    return registration