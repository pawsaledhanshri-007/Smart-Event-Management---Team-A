from fastapi import APIRouter, Depends
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
import logging

from app.agent.graph import build_agent
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)


class AgentRequest(BaseModel):
    message: str
    # Kept for compatibility with the existing frontend.
    # Never use this field to determine the authenticated user.
    user_id: str | None = None
    session_id: str | None = None


class AgentResponse(BaseModel):
    response: str


@router.post("/chat", response_model=AgentResponse)
def chat_with_agent(
    request: AgentRequest,
    current_user: User = Depends(get_current_user),
):
    # Build the agent using the authenticated user's identity and role.
    user_agent = build_agent(
        user_id=str(current_user.id),
        role=current_user.role,
    )

    # Execute the user's request safely.
    try:
        result = user_agent.invoke(
            {"messages": [HumanMessage(content=f"User request: {request.message}")]}
        )
    except Exception:
        logger.exception(
            "Agent execution failed for authenticated user %s",
            current_user.id,
        )
        return AgentResponse(
            response=(
                "I couldn't complete or confirm this request because "
                "the AI service encountered an error. Please check the "
                "current event or registration status before trying again."
            )
        )

    # DEBUG: Inspect the model's messages and tool calls.
    # Remove this block after diagnosing the issue.

    # Extract the final assistant response.
    final_content = result["messages"][-1].content

    if isinstance(final_content, list):
        response_text = "\n".join(
            item.get("text", "")
            for item in final_content
            if isinstance(item, dict) and item.get("type") == "text"
        )
    else:
        response_text = str(final_content)

    return AgentResponse(response=response_text)
