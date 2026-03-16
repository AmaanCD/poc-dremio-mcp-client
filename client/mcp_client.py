import os
from langchain_mcp_adapters.client import MultiServerMCPClient


__mcp_client : MultiServerMCPClient | None = None

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

def get_mcp_client() -> MultiServerMCPClient:
    global __mcp_client

    if __mcp_client is not None:
        return __mcp_client

    __mcp_client= MultiServerMCPClient(config())
    return __mcp_client





