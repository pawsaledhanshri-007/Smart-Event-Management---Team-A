import bcrypt
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import User, Venue, Event, Registration

def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def seed_database():
    db = SessionLocal()
    try:
        admin = db.scalar(
            select(User).where(User.email == "admin@eventmanager.com")
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
            select(User).where(User.email == "organizer1@eventmanager.com")
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
            select(User).where(User.email == "organizer2@eventmanager.com")
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

        participants = [
            ("Aman Kumar", "participant1@eventmanager.com", "9876543213", 21, "Chandigarh University"),
            ("Neha Verma", "participant2@eventmanager.com", "9876543214", 22, "Chitkara University"),
            ("Simran Kaur", "participant3@eventmanager.com", "9876543215", 20, "Chandigarh University"),
            ("Arjun Mehta", "participant4@eventmanager.com", "9876543216", 23, "Lovely Professional University"),
        ]
        participant_objs = []
        for name, email, phone, age, college in participants:
            user = db.scalar(select(User).where(User.email == email))
            if not user:
                user = User(
                    name=name,
                    email=email,
                    password_hash=hash_password("Participant@123"),
                    role="participant",
                    phone=phone,
                    age=age,
                    college=college,
                )
                db.add(user)
            participant_objs.append(user)

        db.flush()

        venue_defs = [
            ("University Auditorium", "Chandigarh University", 500),
            ("Innovation Hall", "Mohali", 200),
            ("Seminar Hall A", "Chandigarh University", 120),
            ("Open Air Amphitheatre", "Chandigarh University", 1000),
        ]
        venues = []
        for name, location, capacity in venue_defs:
            venue = db.scalar(select(Venue).where(Venue.name == name))
            if not venue:
                venue = Venue(name=name, location=location, capacity=capacity)
                db.add(venue)
            venues.append(venue)

        db.flush()
        now = datetime.now(timezone.utc)

        events_data = [
            ("AI & Machine Learning Summit", "A technical summit covering modern AI and machine learning.", venues[0], organizer1, 7, 2, 6, 450),
            ("Startup & Innovation Meetup", "Networking event for students, founders and innovators.", venues[1], organizer2, 9, 3, 6, 180),
            ("Python Workshop", "Hands-on Python programming workshop for students.", venues[2], organizer1, 11, 2, 5, 100),
            ("Cybersecurity Awareness Seminar", "Seminar covering cybersecurity awareness and best practices.", venues[2], organizer2, 13, 2, 4, 100),
            ("Annual Cultural Fest", "University cultural festival featuring music, dance and performances.", venues[3], organizer1, 15, 3, 9, 900),
        ]

        created_events = []
        for title, description, venue, organizer, days, start_h, end_h, capacity in events_data:
            event = db.scalar(select(Event).where(Event.title == title))
            if not event:
                event = Event(
                    title=title,
                    description=description,
                    venue_id=venue.id,
                    organizer_id=organizer.id,
                    start_time=now + timedelta(days=days, hours=start_h),
                    end_time=now + timedelta(days=days, hours=end_h),
                    capacity=capacity,
                    status="scheduled",
                )
                db.add(event)
                db.flush()
            created_events.append(event)

        registrations = [
            (participant_objs[0], created_events[0]),
            (participant_objs[1], created_events[0]),
            (participant_objs[2], created_events[0]),
            (participant_objs[0], created_events[1]),
            (participant_objs[3], created_events[1]),
            (participant_objs[1], created_events[2]),
            (participant_objs[2], created_events[2]),
            (participant_objs[3], created_events[4]),
        ]

        for user, event in registrations:
            existing = db.scalar(
                select(Registration).where(
                    Registration.user_id == user.id,
                    Registration.event_id == event.id,
                )
            )
            if not existing:
                db.add(
                    Registration(
                        user_id=user.id,
                        event_id=event.id,
                        status="confirmed",
                    )
                )

        db.commit()
        print("Database seeded successfully!")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
