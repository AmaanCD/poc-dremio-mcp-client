from typing import List

from langchain_core.tools import BaseTool
from client.mcp_client import get_mcp_client
__tools : List[BaseTool] | None = None
__system_prompt : str | None = None

__system_prompt_value : str | None = None



async def get_tools() -> List[BaseTool]:
    global __tools


    if __tools is not None:
        return __tools

    mcp =  get_mcp_client()
    __tools = await mcp.get_tools()
    return __tools


async def __get_system_prompt():
    global __system_prompt

    if __system_prompt is not None:
        return __system_prompt

    mcp = get_mcp_client()
    __system_prompt = await mcp.get_prompt(
        prompt_name="System Prompt",
        server_name="dremio"
    )
    return __system_prompt

async def get_system_prompt_message()->str:
    global __system_prompt_value
    if __system_prompt_value is not None:
        return __system_prompt_value


    messages = await __get_system_prompt()
    __system_prompt_value = ", ".join(message.content for message in messages)
    return __system_prompt_value



