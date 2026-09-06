from typing import List, Optional
from app.schemas.registration import RegistrationCreate, RegistrationResponse
from datetime import datetime, timezone

class RegistrationRepository:
    def __init__(self):
        self._registrations = {}
        self._id_counter = 1

    def get_by_event(self, event_id: int) -> List[RegistrationResponse]:
        return [reg for reg in self._registrations.values() if reg.event_id == event_id]

    def get_by_user(self, user_id: int) -> List[RegistrationResponse]:
        return [reg for reg in self._registrations.values() if reg.user_id == user_id]

    def get_by_event_and_user(self, event_id: int, user_id: int) -> Optional[RegistrationResponse]:
        for reg in self._registrations.values():
            if reg.event_id == event_id and reg.user_id == user_id:
                return reg
        return None
    
    def count_by_event(self, event_id: int) -> int:
        return sum(1 for reg in self._registrations.values() if reg.event_id == event_id)

    def create(self, registration: RegistrationCreate) -> RegistrationResponse:
        reg_id = self._id_counter
        self._id_counter += 1
        new_reg = RegistrationResponse(
            id=reg_id,
            registered_at=datetime.now(timezone.utc),
            **registration.model_dump()
        )
        self._registrations[reg_id] = new_reg
        return new_reg

    def delete(self, event_id: int, user_id: int) -> bool:
        reg = self.get_by_event_and_user(event_id, user_id)
        if reg:
            del self._registrations[reg.id]
            return True
        return False

registration_repository = RegistrationRepository()
