from langchain_core.messages import HumanMessage

from agents.sql_agent import create_dremio_agent

async def execute(question:str):
    agent = await create_dremio_agent()
    message = {
        "messages" : [
            HumanMessage(content=question)
        ]

    }
    result = await agent.ainvoke(message)
    return result