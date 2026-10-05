from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

from app.agent.agent import build_model_with_fallbacks

from app.agent.tools import (
    get_all_events,
    get_event_by_id,
    get_all_venues,
    get_venue_by_id,
    find_venues_by_capacity,
    check_venue_availability,
    find_available_venues,
    search_events,
    get_upcoming_events,
    get_events_by_status,
    get_events_at_venue,
    get_all_registrations,
    get_registrations_for_event,
    register_for_event,
    cancel_event_registration,
    create_event,
    update_event,
    cancel_event,
    get_user_registrations,
    create_venue,
    delete_venue,
)

# Read-only discovery tools available to all authenticated roles.
DISCOVERY_TOOLS = [
    get_all_events,
    get_event_by_id,
    get_all_venues,
    get_venue_by_id,
    find_venues_by_capacity,
    check_venue_availability,
    find_available_venues,
    search_events,
    get_upcoming_events,
    get_events_by_status,
    get_events_at_venue,
]


# All original tools remain available to administrators.
ADMIN_TOOLS = [
    *DISCOVERY_TOOLS,
    get_all_registrations,
    get_registrations_for_event,
    register_for_event,
    cancel_event_registration,
    create_event,
    update_event,
    cancel_event,
    get_user_registrations,
    create_venue,
    delete_venue,
]


def build_agent(user_id: str, role: str):
    """
    Construct an agent with tools selected for the authenticated user.

    The authenticated user ID is injected by the backend.
    The model does not get to choose another user's ID.
    """

    if role == "admin":

        @tool("create_event")
        def create_event_as_admin(
            title: str,
            description: str,
            venue_id: str,
            start_time: str,
            end_time: str,
            capacity: int,
            registration_fee: float = 0,
        ):
            """
            Create an event as the authenticated administrator.

            The organizer ID is automatically taken from the authenticated
            admin user. Do not ask the user for an organizer ID.
            """
            return create_event.invoke(
                {
                    "title": title,
                    "description": description,
                    "venue_id": venue_id,
                    "organizer_id": user_id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "capacity": capacity,
                    "registration_fee": registration_fee,
                }
            )

        allowed_tools = [
            *DISCOVERY_TOOLS,
            get_all_registrations,
            get_registrations_for_event,
            register_for_event,
            cancel_event_registration,
            create_event_as_admin,
            update_event,
            cancel_event,
            get_user_registrations,
            create_venue,
            delete_venue,
        ]

    elif role == "participant":

        @tool("get_user_registrations")
        def get_own_registrations():
            """Retrieve registrations belonging to the logged-in participant."""
            return get_user_registrations.invoke({"user_id": user_id})

        @tool("register_for_event")
        def register_self_for_event(event_id: str):
            """Register the logged-in participant for an event."""
            return register_for_event.invoke(
                {
                    "user_id": user_id,
                    "event_id": event_id,
                }
            )

        @tool("cancel_event_registration")
        def cancel_own_event_registration(event_id: str):
            """Cancel the logged-in participant's registration."""
            return cancel_event_registration.invoke(
                {
                    "user_id": user_id,
                    "event_id": event_id,
                }
            )

        allowed_tools = [
            *DISCOVERY_TOOLS,
            get_own_registrations,
            register_self_for_event,
            cancel_own_event_registration,
        ]

    elif role == "organizer":

        allowed_tools = DISCOVERY_TOOLS.copy()

    else:
        raise ValueError(f"Unsupported user role: {role}")

    model_with_fallbacks = build_model_with_fallbacks(allowed_tools)

    return create_react_agent(
        model=model_with_fallbacks,
        tools=allowed_tools,
        prompt=(
            "You are the Smart Event Management AI assistant. "
            "Use the available tools to perform real event-management "
            "operations. Always use actual database results. "
            "Never invent event IDs, venue IDs, user IDs, dates, "
            "venues, registrations, or operation results. "
            "For participant registration operations, operate only "
            "on the authenticated participant. "
            "For admin event creation, the authenticated admin is "
            "automatically the organizer. Never ask for or invent "
            "an organizer ID. "
            "Before creating an event, check venue availability when "
            "the user asks for an available venue or provides a time "
            "range. "
            "When a tool reports success, clearly state what happened. "
            "When a tool reports failure, honestly report the failure. "
            "Do not claim an operation succeeded unless the tool "
            "actually confirms success. "
            "For date and time values, use ISO 8601 format. "
            "For this application in India, use +05:30 when a timezone "
            "is required."
        ),
    )
