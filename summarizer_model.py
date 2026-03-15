from functools import lru_cache

from langchain_openai import ChatOpenAI
from settings import settings

@lru_cache(maxsize=1)
def get_summarizer_model():
    return ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
        temperature=0.3,     # slight creativity for natural language output
        model="llama-3.3-70b-versatile",
        api_key=settings.api_key
    )