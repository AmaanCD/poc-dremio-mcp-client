import json



from components.dremio_tools import get_tools
from components.query_creator_service import create_query
from helper.schema_context_creator import create_schema_context


async def execute_sql_query(question:str):
    response = await create_query(question)
    print(response["query"])
    sql_query = response["query"]
    tools = await get_tools()
    by_name = {item.name : item for item in tools}
    result = await by_name["RunSqlQuery"].ainvoke({
        "query": sql_query
    })
    current_object =next(item for item in result if item["type"] == "text")
    print(current_object)
    result_object = current_object["text"]
    final_result = json.loads(result_object)
    print(final_result)

    return {
        "sql_query" :sql_query,
        "context" : create_schema_context(response["docs"]),
        "question" : question,
        "query_result" : final_result["result"]
    }

