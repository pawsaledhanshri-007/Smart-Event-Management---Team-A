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

    Participant registration tools inject the verified user ID instead
    of allowing the model to select an arbitrary user ID.
    """

    if role == "admin":
        allowed_tools = ADMIN_TOOLS.copy()

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
            """Cancel the logged-in participant's registration for an event."""
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
        # Conservative default until organizer permissions are defined.
        allowed_tools = DISCOVERY_TOOLS.copy()

    else:
        raise ValueError(f"Unsupported user role: {role}")

    model_with_fallbacks = build_model_with_fallbacks(allowed_tools)

    return create_react_agent(
        model=model_with_fallbacks,
        tools=allowed_tools,
        prompt=(
            "You are the Smart Event Management AI assistant. "
            "Help the user complete event-management tasks using your available tools. "
            "Understand the user's request and call the appropriate tool when needed. "
            "After receiving tool results, explain the actual results in clear, "
            "natural language. Never describe what a tool returns instead of "
            "answering the user's question. Never output meaningless repeated "
            "characters or exclamation marks. "
            "For successful actions, confirm what was changed and identify the "
            "affected event or registration. For failed actions, explain the error "
            "honestly. Never claim an action succeeded unless the tool confirms it. "
            "Respect the tools available to your authenticated role. "
            "Do not invent event details, IDs, dates, or operation results."
        ),
    )
