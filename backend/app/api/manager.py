from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.api.deps import get_current_admin
from app.models.user import User
from app.models.event import Event
from app.models.registration import Registration


router = APIRouter()


@router.get("/summary")
def get_manager_summary(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    total_events = db.query(Event).count()

    total_registrations = (
        db.query(Registration)
        .filter(Registration.status != "cancelled")
        .count()
    )

    total_revenue = (
        db.query(func.coalesce(func.sum(Event.registration_fee), 0))
        .join(Registration, Registration.event_id == Event.id)
        .filter(Registration.status == "confirmed")
        .scalar()
    )

    pending_payments = 0

    return {
        "total_events": total_events,
        "total_registrations": total_registrations,
        "total_revenue": float(total_revenue or 0),
        "pending_payments": pending_payments,
    }