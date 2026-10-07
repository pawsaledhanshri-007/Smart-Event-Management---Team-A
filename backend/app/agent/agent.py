import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def build_model_with_fallbacks(tools):
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    model = ChatOpenAI(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        api_key=groq_api_key,
        base_url="https://api.groq.com/openai/v1",
        temperature=0,
        max_tokens=250,
    )

    return model.bind_tools(tools)
