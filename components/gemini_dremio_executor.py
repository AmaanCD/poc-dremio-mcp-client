from langchain_core.messages import HumanMessage

from agents.google_sql_agent import  create_gemini_agent

async def execute(question:str):
    agent = await create_gemini_agent()
    message = {"messages":[
        HumanMessage(content=question)
    ]}
    return await agent.ainvoke(message)