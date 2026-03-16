from langchain.agents import create_agent
from client.llm_client import get_client
from components.dremio_tools import get_tools,get_system_prompt_message

__agent = None

async def create_dremio_agent():
    global __agent

    if __agent is not None:
        return __agent

    tools = await get_tools()
    system_prompt = await get_system_prompt_message()
    print(system_prompt)
    print(tools)
    __agent = create_agent(
        model=get_client(),
        tools=tools,
        system_prompt=system_prompt
    )
    return __agent