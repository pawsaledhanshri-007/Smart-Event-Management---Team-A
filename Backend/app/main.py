from fastapi import FastAPI
from app.api.events import router as events_router
from app.api.venues import router as venues_router
from app.api.registrations import router as registrations_router

app = FastAPI(
    title="Agentic AI Smart Event Management System - Backend API",
    description="Backend API layer for Events, Venues, and Registrations",
    version="1.0.0"
)

app.include_router(events_router, prefix="/api")
app.include_router(venues_router, prefix="/api")
app.include_router(registrations_router, prefix="/api")
