from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.venues import router as venues_router
from app.api.events import router as events_router
from app.api.registrations import router as registrations_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(venues_router, prefix="/venues", tags=["Venues"])
api_router.include_router(events_router, prefix="/events", tags=["Events"])
api_router.include_router(registrations_router, tags=["Registrations"])
