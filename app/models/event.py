from sqlalchemy import Column, Integer, String, DateTime, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String, default="SCHEDULED")  # SCHEDULED, CANCELLED
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    venue = relationship("Venue", back_populates="events")
    creator = relationship("User", back_populates="events_created")
    registrations = relationship("Registration", back_populates="event")
