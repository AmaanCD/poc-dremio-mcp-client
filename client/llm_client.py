from langchain_openai import ChatOpenAI
from settings import settings
__client : ChatOpenAI | None = None

def get_client():
    global __client

    if __client is not None:
        return __client
    print(settings.api_key)
    __client = ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
        temperature=0.0,
        model="qwen/qwen3-32b",
        api_key=settings.api_key,
        model_kwargs={
            "extra_body": {"reasoning_format": "hidden"}
        }

    )
    return __client
