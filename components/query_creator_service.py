from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from client.grok_llm import get_groq_llm_client
from components.vector_search_service import search
from components.prompt_service import build_prompt,build_system_prompt


class SQLResponse(BaseModel):
    query: str = Field(description="The Dremio SQL query")
    reasoning: str = Field(description="Explanation of the logic")



async def create_query(question:str):
    documents = search(question)
    prompt = build_prompt(question,documents)
    system_prompt = build_system_prompt()
    print(prompt)
    model = get_groq_llm_client()
    model=model.with_structured_output(SQLResponse)
    messages = [SystemMessage(content=system_prompt),HumanMessage(content=prompt)]
    ai_message : SQLResponse = await model.ainvoke(messages)
    return {
        "query": ai_message.query,
        "docs" : documents,
        "question" : question
    }






