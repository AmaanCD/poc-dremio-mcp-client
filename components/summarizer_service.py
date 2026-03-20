from langchain_core.messages import SystemMessage, HumanMessage

from client.grok_summarizer_llm import get_groq_summarizer_llm


_system_prompt = """
You are a expert summarizer who summarizes the result based on context provided.

Your job is to convert raw SQL query results into a concise, fact based summary.

STRICT RULES:
1. Never say "the query returned" or "the SQL found" — speak in business terms
2. Lead with the KEY INSIGHT — the one number or trend that matters most
3. Add  context — what does this result mean? 
4. Flag anomalies or patterns worth investigating further
5. Keep it under 5 sentences unless the data warrants more
6. Use domain language 
7. Never make up data — only use what is in the query result
"""

def create_human_prompt(request:dict)-> str:
    return f"""
    BUSINESS QUESTION ASKED:
{request["question"]}

SQL QUERY USED TO ANSWER IT:
{request["sql_query"]}

DOMAIN SCHEMA CONTEXT (what these tables represent):
{request["context"]}

QUERY RESULT:
{request["query_result"]}

Now write a business-savvy summary of these findings as if presenting to a senior stakeholder.
Focus on what the numbers MEAN for the business, not just what they are.
"""


async def summarize_response(request:dict):
    prompt = create_human_prompt(request=request)
    model = get_groq_summarizer_llm()
    messages = [
        SystemMessage(content=_system_prompt),
        HumanMessage(content=prompt)
    ]
    return await  model.ainvoke(messages)



