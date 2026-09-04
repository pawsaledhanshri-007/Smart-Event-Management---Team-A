import bcrypt
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import (
    User,
    Venue,
    Event,
    Registration,
)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def seed_database():
    db = SessionLocal()

    try:
        # -------------------------------------------------
        # 1. USERS
        # -------------------------------------------------

        admin = db.scalar(
            select(User).where(
                User.email == "admin@eventmanager.com"
            )
        )

        if not admin:
            admin = User(
                name="System Admin",
                email="admin@eventmanager.com",
                password_hash=hash_password("Admin@123"),
                role="admin",
                phone="9876543210",
                age=35,
                college="Event Management System",
            )
            db.add(admin)

        organizer1 = db.scalar(
            select(User).where(
                User.email == "organizer1@eventmanager.com"
            )
        )

        if not organizer1:
            organizer1 = User(
                name="Rahul Sharma",
                email="organizer1@eventmanager.com",
                password_hash=hash_password("Organizer@123"),
                role="organizer",
                phone="9876543211",
                age=28,
                college="Chandigarh University",
            )
            db.add(organizer1)

        organizer2 = db.scalar(
            select(User).where(
                User.email == "organizer2@eventmanager.com"
            )
        )

        if not organizer2:
            organizer2 = User(
                name="Priya Singh",
                email="organizer2@eventmanager.com",
                password_hash=hash_password("Organizer@123"),
                role="organizer",
                phone="9876543212",
                age=27,
                college="Punjab University",
            )
            db.add(organizer2)

        participant1 = db.scalar(
            select(User).where(
                User.email == "participant1@eventmanager.com"
            )
        )

        if not participant1:
            participant1 = User(
                name="Aman Kumar",
                email="participant1@eventmanager.com",
                password_hash=hash_password("Participant@123"),
                role="participant",
                phone="9876543213",
                age=21,
                college="Chandigarh University",
            )
            db.add(participant1)

        participant2 = db.scalar(
            select(User).where(
                User.email == "participant2@eventmanager.com"
            )
        )

        if not participant2:
            participant2 = User(
                name="Neha Verma",
                email="participant2@eventmanager.com",
                password_hash=hash_password("Participant@123"),
                role="participant",
                phone="9876543214",
                age=22,
                college="Chitkara University",
            )
            db.add(participant2)

        participant3 = db.scalar(
            select(User).where(
                User.email == "participant3@eventmanager.com"
            )
        )

        if not participant3:
            participant3 = User(
                name="Simran Kaur",
                email="participant3@eventmanager.com",
                password_hash=hash_password("Participant@123"),
                role="participant",
                phone="9876543215",
                age=20,
                college="Chandigarh University",
            )
            db.add(participant3)

        participant4 = db.scalar(
            select(User).where(
                User.email == "participant4@eventmanager.com"
            )
        )

        if not participant4:
            participant4 = User(
                name="Arjun Mehta",
                email="participant4@eventmanager.com",
                password_hash=hash_password("Participant@123"),
                role="participant",
                phone="9876543216",
                age=23,
                college="Lovely Professional University",
            )
            db.add(participant4)

        db.flush()

        # -------------------------------------------------
        # 2. VENUES
        # -------------------------------------------------

        venue1 = db.scalar(
            select(Venue).where(
                Venue.name == "University Auditorium"
            )
        )

        if not venue1:
            venue1 = Venue(
                name="University Auditorium",
                location="Chandigarh University",
                capacity=500,
            )
            db.add(venue1)

        venue2 = db.scalar(
            select(Venue).where(
                Venue.name == "Innovation Hall"
            )
        )

        if not venue2:
            venue2 = Venue(
                name="Innovation Hall",
                location="Mohali",
                capacity=200,
            )
            db.add(venue2)

        venue3 = db.scalar(
            select(Venue).where(
                Venue.name == "Seminar Hall A"
            )
        )

        if not venue3:
            venue3 = Venue(
                name="Seminar Hall A",
                location="Chandigarh University",
                capacity=120,
            )
            db.add(venue3)

        venue4 = db.scalar(
            select(Venue).where(
                Venue.name == "Open Air Amphitheatre"
            )
        )

        if not venue4:
            venue4 = Venue(
                name="Open Air Amphitheatre",
                location="Chandigarh University",
                capacity=1000,
            )
            db.add(venue4)

        db.flush()

        # -------------------------------------------------
        # 3. EVENTS
        # -------------------------------------------------

        now = datetime.now(timezone.utc)

        events_data = [
            {
                "title": "AI & Machine Learning Summit",
                "description": "A technical summit covering modern AI and machine learning.",
                "venue": venue1,
                "organizer": organizer1,
                "start_time": now + timedelta(days=7, hours=2),
                "end_time": now + timedelta(days=7, hours=6),
                "capacity": 450,
            },
            {
                "title": "Startup & Innovation Meetup",
                "description": "Networking event for students, founders and innovators.",
                "venue": venue2,
                "organizer": organizer2,
                "start_time": now + timedelta(days=9, hours=3),
                "end_time": now + timedelta(days=9, hours=6),
                "capacity": 180,
            },
            {
                "title": "Python Workshop",
                "description": "Hands-on Python programming workshop for students.",
                "venue": venue3,
                "organizer": organizer1,
                "start_time": now + timedelta(days=11, hours=2),
                "end_time": now + timedelta(days=11, hours=5),
                "capacity": 100,
            },
            {
                "title": "Cybersecurity Awareness Seminar",
                "description": "Seminar covering cybersecurity awareness and best practices.",
                "venue": venue3,
                "organizer": organizer2,
                "start_time": now + timedelta(days=13, hours=2),
                "end_time": now + timedelta(days=13, hours=4),
                "capacity": 100,
            },
            {
                "title": "Annual Cultural Fest",
                "description": "University cultural festival featuring music, dance and performances.",
                "venue": venue4,
                "organizer": organizer1,
                "start_time": now + timedelta(days=15, hours=3),
                "end_time": now + timedelta(days=15, hours=9),
                "capacity": 900,
            },
        ]

        created_events = []

        for event_data in events_data:
            event = db.scalar(
                select(Event).where(
                    Event.title == event_data["title"]
                )
            )

            if not event:
                event = Event(
                    title=event_data["title"],
                    description=event_data["description"],
                    venue_id=event_data["venue"].id,
                    organizer_id=event_data["organizer"].id,
                    start_time=event_data["start_time"],
                    end_time=event_data["end_time"],
                    capacity=event_data["capacity"],
                    status="scheduled",
                )
                db.add(event)
                db.flush()

            created_events.append(event)

        # -------------------------------------------------
        # 4. REGISTRATIONS
        # -------------------------------------------------

        registrations = [
            (participant1, created_events[0]),
            (participant2, created_events[0]),
            (participant3, created_events[0]),

            (participant1, created_events[1]),
            (participant4, created_events[1]),

            (participant2, created_events[2]),
            (participant3, created_events[2]),

            (participant4, created_events[4]),
        ]

        for user, event in registrations:

            existing_registration = db.scalar(
                select(Registration).where(
                    Registration.user_id == user.id,
                    Registration.event_id == event.id,
                )
            )

            if not existing_registration:
                registration = Registration(
                    user_id=user.id,
                    event_id=event.id,
                    status="confirmed",
                )
                db.add(registration)

        # -------------------------------------------------
        # COMMIT
        # -------------------------------------------------

        db.commit()

        print("======================================")
        print("Database seeded successfully!")
        print("======================================")
        print("Users        :", db.query(User).count())
        print("Venues       :", db.query(Venue).count())
        print("Events       :", db.query(Event).count())
        print("Registrations:", db.query(Registration).count())
        print("======================================")

    except Exception as e:
        db.rollback()
        print("ERROR:", e)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()