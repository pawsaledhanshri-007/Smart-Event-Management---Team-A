import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    CheckConstraint,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    __table_args__ = (
        CheckConstraint(
            "end_time > start_time",
            name="ck_events_time_order"
        ),

        CheckConstraint(
            "capacity > 0",
            name="ck_events_capacity_positive"
        ),

        CheckConstraint(
            "status IN ('scheduled', 'ongoing', 'completed', 'cancelled')",
            name="ck_events_status_valid"
        ),

        Index(
            "ix_events_venue_time_range",
            "venue_id",
            "start_time",
            "end_time"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    venue_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("venues.id", ondelete="RESTRICT"),
    nullable=False,
    index=True
    )

    organizer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="scheduled"
    )

    venue = relationship(
        "Venue",
        back_populates="events"
    )

    organizer = relationship(
        "User",
        back_populates="events_organized"
    )

    registrations = relationship(
        "Registration",
        back_populates="event"
    )