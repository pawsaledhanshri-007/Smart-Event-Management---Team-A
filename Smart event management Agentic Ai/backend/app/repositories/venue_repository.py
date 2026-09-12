from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.venue import Venue
from app.schemas.venue import VenueCreate, VenueUpdate

class VenueRepository:
    def get_all(self, db: Session) -> List[Venue]:
        return db.query(Venue).all()

    def get_by_id(self, db: Session, venue_id: UUID) -> Optional[Venue]:
        return db.query(Venue).filter(Venue.id == venue_id).first()

    def create(self, db: Session, venue: VenueCreate) -> Venue:
        new_venue = Venue(
            name=venue.name,
            location=venue.location,
            capacity=venue.capacity,
        )
        db.add(new_venue)
        db.commit()
        db.refresh(new_venue)
        return new_venue

    def update(
        self,
        db: Session,
        venue_id: UUID,
        venue_update: VenueUpdate
    ) -> Optional[Venue]:
        existing_venue = self.get_by_id(db, venue_id)
        if not existing_venue:
            return None

        update_data = venue_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_venue, field, value)

        db.commit()
        db.refresh(existing_venue)
        return existing_venue

    def delete(self, db: Session, venue_id: UUID) -> bool:
        existing_venue = self.get_by_id(db, venue_id)
        if not existing_venue:
            return False

        db.delete(existing_venue)
        db.commit()
        return True

venue_repository = VenueRepository()
