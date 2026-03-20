from langchain_groq import ChatGroq
from openai import api_key

from settings import settings

_groq_summarizer_llm = None

def get_groq_summarizer_llm():
    global _groq_summarizer_llm

    if _groq_summarizer_llm is not None:
        return _groq_summarizer_llm

    _groq_summarizer_llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,  # Slight variety for better flow

        api_key=settings.api_key
    )

    return _groq_summarizer_llm