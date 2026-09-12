from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import User, Event, Registration
from app.services.registration_service import register_user_for_event
from app.services.registration_service import (
    register_user_for_event,
    cancel_registration,
)

def get_user(db, email):
    return db.scalar(
        select(User).where(User.email == email)
    )

def get_event(db, title):
    return db.scalar(
        select(Event).where(Event.title == title)
    )

def test_successful_registration():
    db = SessionLocal()
    try:
        user = get_user(db, "participant1@eventmanager.com")
        event = get_event(db, "Python Workshop")
        registration = register_user_for_event(db, user.id, event.id)
        print("\nTEST 1: Successful registration")
        print("PASS")
        print("Registration ID:", registration.id)
    finally:
        db.close()

def test_duplicate_registration():
    db = SessionLocal()
    try:
        user = get_user(db, "participant1@eventmanager.com")
        event = get_event(db, "AI & Machine Learning Summit")
        try:
            register_user_for_event(db, user.id, event.id)
            print("\nTEST 2: Duplicate registration")
            print("FAIL - duplicate was allowed")
        except ValueError as e:
            print("\nTEST 2: Duplicate registration")
            print("PASS")
            print("Message:", e)
    finally:
        db.close()

def test_invalid_user():
    db = SessionLocal()
    try:
        event = get_event(db, "AI & Machine Learning Summit")
        import uuid
        try:
            register_user_for_event(db, uuid.uuid4(), event.id)
            print("\nTEST 3: Invalid user")
            print("FAIL - invalid user was accepted")
        except ValueError as e:
            print("\nTEST 3: Invalid user")
            print("PASS")
            print("Message:", e)
    finally:
        db.close()

def test_invalid_event():
    db = SessionLocal()
    try:
        user = get_user(db, "participant4@eventmanager.com")
        import uuid
        try:
            register_user_for_event(db, user.id, uuid.uuid4())
            print("\nTEST 4: Invalid event")
            print("FAIL - invalid event was accepted")
        except ValueError as e:
            print("\nTEST 4: Invalid event")
            print("PASS")
            print("Message:", e)
    finally:
        db.close()

def test_cancel_registration():
    db = SessionLocal()
    try:
        user = get_user(db, "participant1@eventmanager.com")
        event = get_event(db, "Python Workshop")
        registration = register_user_for_event(db, user.id, event.id)
        cancelled_registration = cancel_registration(db, user.id, event.id)

        print("\nTEST 5: Cancel registration")
        if (
            cancelled_registration.status == "cancelled"
            and cancelled_registration.cancelled_at is not None
        ):
            print("PASS")
            print("Status:", cancelled_registration.status)
            print("Cancelled at:", cancelled_registration.cancelled_at)
        else:
            print("FAIL")

        db.delete(cancelled_registration)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    test_successful_registration()
    test_duplicate_registration()
    test_invalid_user()
    test_invalid_event()
    test_cancel_registration()

    print("\n======================================")
    print("Registration service tests completed")
    print("======================================")
