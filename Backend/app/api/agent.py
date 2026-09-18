from fastapi import APIRouter
from pydantic import BaseModel

from langchain_core.messages import HumanMessage

from app.agent.graph import agent


router = APIRouter()


class AgentRequest(BaseModel):
    message: str


class AgentResponse(BaseModel):
    response: str


@router.post("/chat", response_model=AgentResponse)
def chat_with_agent(request: AgentRequest):
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(content=request.message)
            ]
        }
    )

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