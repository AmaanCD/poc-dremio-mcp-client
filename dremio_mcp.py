from typing import List

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
import os


def config()-> dict:
    DREMIO_CODE_PATH = r"C:\Users\ASUS\OneDrive\Desktop\ML\Dremio Agent Project\mcp-code-base\dremio-mcp"
    UV_PATH = r"C:\Users\ASUS\AppData\Local\Programs\Python\Python313\Scripts\uv.exe"

    return {
    "dremio": {
        "transport": "stdio",
        "command": UV_PATH,
        "args": [
            "run",
            "--directory",
            DREMIO_CODE_PATH,
            "dremio-mcp-server",
            "run"
        ],
        "env": dict(os.environ),

    }
}


class DremioMcpClient:
    def __init__(self):
        self.tools : List[BaseTool] | None = None
        self.mcp : MultiServerMCPClient | None = None

    async def connect(self)-> List[BaseTool]:
        if self.mcp is not None and self.tools is not None:
            return self.tools

        self.mcp = MultiServerMCPClient(config())
        self.tools = await self.mcp.get_tools()
        return self.tools

    async def get_system_prompt(self):
        if self.mcp is not None and self.tools is not None:
            return await self.mcp.get_prompt("dremio",prompt_name="System Prompt")
        return None

    async def get_sql_tools(self):
        tools = await self.connect()
        tool_name = None
        for tool in tools:
            if tool.name.__contains__("RunSqlQuery"):
                tool_name = tool


        return tool_name

    async def execute_query(self,query:str):
        sql_tool = await self.get_sql_tools()
        result = await sql_tool.ainvoke({
            "query": query
        })
        return result







