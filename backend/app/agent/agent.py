import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def build_model_with_fallbacks(tools):
    """
    Primary model: Google Gemini
    Optional fallbacks: OpenRouter models

    All models retain access to the existing tools.
    """
    models = []

    # Gemini is the primary model for now.
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is not configured.")

    gemini = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        google_api_key=google_api_key,
        temperature=0,
        max_retries=0,
    )
    models.append(gemini.bind_tools(tools))

    # OpenRouter models remain available as fallbacks.
    # They may fail while the account has insufficient credits.
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    openrouter_url = "https://openrouter.ai/api/v1"

    model_ids = [
        os.getenv(
            "OPENROUTER_MODEL_1",
            "meta-llama/llama-3.3-70b-instruct:free",
        ),
        os.getenv(
            "OPENROUTER_MODEL_2",
            "nvidia/nemotron-3-super-120b-a12b:free",
        ),
        os.getenv(
            "OPENROUTER_MODEL_3",
            "google/gemma-3-12b-it:free",
        ),
    ]

    if openrouter_api_key:
        for model_id in model_ids:
            model = ChatOpenAI(
                model=model_id,
                api_key=openrouter_api_key,
                base_url=openrouter_url,
                temperature=0,
                max_tokens=100,
            )
            models.append(model.bind_tools(tools))

    primary = models[0]
    fallbacks = models[1:]

    if not fallbacks:
        return primary

    return primary.with_fallbacks(
        fallbacks,
        exceptions_to_handle=(Exception,),
    )
