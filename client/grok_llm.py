from langchain_groq import ChatGroq

from settings import settings

_groq_llm_client = None

def get_groq_llm_client():
    global _groq_llm_client

    if  _groq_llm_client is not None:
        return _groq_llm_client

    _groq_llm_client = ChatGroq(
        api_key=settings.api_key,
        model="qwen/qwen3-32b",
        temperature=0,
        max_tokens=None,
        max_retries=2,
        #base_url="https://api.groq.com/openai/v1",
        reasoning_format="hidden",
        reasoning_effort="default"
    )
    return _groq_llm_client

