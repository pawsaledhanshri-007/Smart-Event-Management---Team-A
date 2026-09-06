from typing import List, Optional
from app.schemas.venue import VenueCreate, VenueUpdate, VenueResponse

class VenueRepository:
    def __init__(self):
        self._venues = {}
        self._id_counter = 1

    def get_all(self) -> List[VenueResponse]:
        return list(self._venues.values())

    def get_by_id(self, venue_id: int) -> Optional[VenueResponse]:
        return self._venues.get(venue_id)

    def create(self, venue: VenueCreate) -> VenueResponse:
        venue_id = self._id_counter
        self._id_counter += 1
        new_venue = VenueResponse(id=venue_id, **venue.model_dump())
        self._venues[venue_id] = new_venue
        return new_venue

    def update(self, venue_id: int, venue_update: VenueUpdate) -> Optional[VenueResponse]:
        if venue_id not in self._venues:
            return None
        existing_venue = self._venues[venue_id]
        update_data = venue_update.model_dump(exclude_unset=True)
        updated_venue = existing_venue.model_copy(update=update_data)
        self._venues[venue_id] = updated_venue
        return updated_venue

    def delete(self, venue_id: int) -> bool:
        if venue_id in self._venues:
            del self._venues[venue_id]
            return True
        return False

venue_repository = VenueRepository()
