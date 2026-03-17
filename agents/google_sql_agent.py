from langchain.agents import create_agent

from client.gemini_llm import get_google_llm
from components.dremio_tools import get_tools,get_system_prompt_message


__agent = None

async def create_gemini_agent():
    global __agent

    if __agent is not None:
        return __agent

    model = get_google_llm()
    tools = await get_tools()
    prompt = await get_system_prompt_message()
    __agent = create_agent(
        model = model,
        tools = tools,
        system_prompt=prompt
    )
    return __agent


