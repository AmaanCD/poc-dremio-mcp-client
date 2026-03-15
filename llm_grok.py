from functools import lru_cache

from langchain_openai import ChatOpenAI
from settings import settings




@lru_cache(maxsize=1)
def get_model() -> ChatOpenAI:
    return ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
        temperature=0.0,
        model="qwen/qwen3-32b",
        api_key=settings.api_key,
        model_kwargs={
            "extra_body": {"reasoning_format": "hidden"}
        }

    )
