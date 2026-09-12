import uuid
from enum import Enum

from sqlalchemy import String, Integer, CheckConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

class UserRole(str, Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    PARTICIPANT = "participant"

class User(Base, TimestampMixin):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "role IN ('admin', 'organizer', 'participant')",
            name="ck_users_role_valid"
        ),
        CheckConstraint(
            "age IS NULL OR (age > 0 AND age < 120)",
            name="ck_users_age_valid"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    college: Mapped[str | None] = mapped_column(String(150), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=UserRole.PARTICIPANT.value
    )

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    events_organized = relationship("Event", back_populates="organizer")
    registrations = relationship("Registration", back_populates="user")
