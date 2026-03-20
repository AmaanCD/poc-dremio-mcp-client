from components.query_executor import execute_sql_query
from components.summarizer_service import summarize_response


async def give_insight(question:str):
    response = await execute_sql_query(question)
    result = await summarize_response(response)
    return result

