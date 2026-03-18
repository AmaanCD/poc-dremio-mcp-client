
from langchain_google_genai import ChatGoogleGenerativeAI
import os
__google_llm = None

def get_google_llm():
    global __google_llm

    if __google_llm is not None:
        return __google_llm

    __google_llm = ChatGoogleGenerativeAI(
        model = "gemini-3-flash-preview",
        api_key = os.environ.get("GOOGLE_API_KEY"),
        temperature=0
    )
    return __google_llm
