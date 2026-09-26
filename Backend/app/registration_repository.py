from typing import List

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.registration import Registration


class RegistrationRepository:

    def get_all(self, db: Session) -> List[Registration]:
        return db.query(Registration).all()

    def get_by_event_id(
        self,
        db: Session,
        event_id: UUID
    ) -> List[Registration]:
        return (
            db.query(Registration)
            .filter(Registration.event_id == event_id)
            .all()
        )


registration_repository = RegistrationRepository()