from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from llm_grok import get_model


async def generate_sql(question: str,schema) -> dict:
    print(f"----------------------{schema}----------------------------------")
    llm = get_model()
    response = await llm.ainvoke([
        SystemMessage(content="""You are an expert SQL generator for Dremio.
Given relevant table schemas and a user question, generate a single valid Dremio SQL query.
Output ONLY the raw SQL query. 
Rules:
- Use fully qualified table names exactly as provided
- Only use columns that exist in the provided schemas  
- Never use SELECT *
- response should start with select or with
- Add LIMIT 100 unless question asks for aggregation
- No thinking, no explanation, no reasoning, no markdown, no comments,no xml tags.
- Return ONLY the SQL, no explanation, no markdown"""),

        HumanMessage(content=f"Schemas:\n{schema}\n\nQuestion: {question}")
    ])
    return {
        "question": question,
        "sql": response.content.strip(),
    }
