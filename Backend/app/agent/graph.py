from langgraph.prebuilt import create_react_agent

from app.agent.agent import llm

from app.agent.tools import (
    get_all_events,
    get_event_by_id,
    get_all_venues,
    get_venue_by_id,
    find_venues_by_capacity,
    check_venue_availability,
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


tools = [
    get_all_events,
    get_event_by_id,
    get_all_venues,
    get_venue_by_id,
    find_venues_by_capacity,
    check_venue_availability,
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
]


agent = create_react_agent(
    model=llm,
    tools=tools,
)