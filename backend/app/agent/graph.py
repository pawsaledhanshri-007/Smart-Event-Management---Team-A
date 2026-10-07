from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

from app.agent.agent import build_model_with_fallbacks
from app.db.session import SessionLocal
from app.repositories.venue_repository import venue_repository

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
    create_event as create_event_tool,
    update_event,
    cancel_event,
    get_user_registrations,
    create_venue,
    delete_venue,
)

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

ADMIN_TOOLS = [
    *DISCOVERY_TOOLS,
    get_all_registrations,
    get_registrations_for_event,
    register_for_event,
    cancel_event_registration,
    create_event_tool,
    update_event,
    cancel_event,
    get_user_registrations,
    create_venue,
    delete_venue,
]


def build_agent(user_id: str, role: str):
    if role == "admin":

        @tool("admin_create_event")
        def create_event_as_admin(
            title: str,
            venue_name: str,
            start_time: str,
            end_time: str,
            capacity: int,
            venue_location: str = "",
            description: str = "",
            registration_fee: float = 0.0,
        ):
            """Create a new event for the authenticated admin.

            Use this tool whenever an admin asks to create, add, schedule, or organize
            a new event. The admin provides the event title, description, venue name,
            venue location, start time, end time, and capacity.
            """

            db = SessionLocal()

            try:
                venues = venue_repository.get_all(db)

                matching_venue = next(
                    (
                        venue
                        for venue in venues
                        if venue.name.lower() == venue_name.lower()
                        and (
                            not venue_location
                            or not venue.location
                            or venue.location.lower() == venue_location.lower()
                        )
                    ),
                    None,
                )

                if not matching_venue:
                    return {
                        "success": False,
                        "error": (
                            f"Venue '{venue_name}' at "
                            f"'{venue_location}' was not found."
                        ),
                    }

                return create_event_tool.invoke(
                    {
                        "title": title,
                        "description": description or title,
                        "venue_id": str(matching_venue.id),
                        "organizer_id": user_id,
                        "start_time": start_time,
                        "end_time": end_time,
                        "capacity": capacity,
                        "registration_fee": registration_fee,
                    }
                )

            finally:
                db.close()

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
            """Get the authenticated user's registrations."""
            return get_user_registrations.invoke({"user_id": user_id})

        @tool("register_for_event")
        def register_self_for_event(event_id: str):
            """Register the authenticated user for an event."""
            return register_for_event.invoke({"user_id": user_id, "event_id": event_id})

        @tool("cancel_event_registration")
        def cancel_own_event_registration(event_id: str):
            """Cancel the authenticated user's registration for an event."""
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
            f"You are the Smart Event Management assistant. "
            f"The currently authenticated user's ID is {user_id}. "
            f"The user's role is {role}. "
            f"Use this authenticated user ID automatically for operations such as registration, "
            f"cancellation, and other user-specific actions. Never ask the user to provide "
            f"their user ID when it is already available in the authenticated context. "
            "Use the available tools whenever the user's request requires event data "
            "or an event-management operation. "
            "IMPORTANT: After receiving a tool result, you MUST produce a final "
            "human-readable text response. Never finish with an empty response. "
            "Always summarize the relevant tool result for the user. "
            "Keep responses concise, clear, friendly, and easy to scan. "
            "Give the direct answer first. "
            "When presenting events, venues, registrations, or other structured "
            "information, use clear headings, numbered lists, and bullet points. "
            "Use relevant emojis to improve readability, such as "
            "\U0001f4c5 for dates, \u23f0 for time, \U0001f4cd for venue or location, "
            "\U0001f465 for capacity or people, \U0001f4b0 for fees, "
            "\u2705 for successful operations, and \u274c for failures. "
            "Use emojis naturally and sparingly; do not overuse them. "
            "Never output question marks as placeholders for emojis. If you are not "
            "sure which emoji to use, write the heading as plain text without one. "
            "Format important field names in bold Markdown. "
            "Do not use decorative separators such as ***, ---, or similar lines. "
            "Do not repeat the user's question. "
            "Do not produce large blocks of text when a list is clearer. "
            "For simple questions, give a short direct answer. "
            "For successful operations, clearly state what was completed and include "
            "the important details. "
            "For failed operations, clearly state the failure and the reason when available. "
            "Never expose internal tool calls, SQL queries, model details, or implementation details. "
            "Never expose raw UUIDs or internal IDs such as event_id, venue_id, user_id, "
            "organizer_id, or similar identifiers in user-facing responses. "
            "Always use human-readable event names, venue names, locations, dates, times, "
            "and other meaningful details instead. "
            "Registration IDs may be shown when they are useful as user-facing references. "
            "When presenting upcoming events, use the heading '\U0001f4c5 Upcoming Events'. "
            "When presenting venues, use the heading '\U0001f4cd Available Venues'. "
            "When presenting registrations, use the heading '\U0001f4cb Registrations'. "
            "For successful operations, use a concise heading beginning with '\u2705'. "
            "For failed operations, use a concise heading beginning with '\u274c'. "
            "Do not begin structured responses with conversational phrases such as "
            "'Here are...', 'Sure, here are...', or 'I found...'."
        ),
    )
