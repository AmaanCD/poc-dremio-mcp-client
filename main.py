from fastapi import FastAPI
from langchain_core.messages import HumanMessage

from dremio_mcp import DremioMcpClient
from meta_data_builder import fetch_metadata
from query_creator_agent import create_agent_planner
from sql_planner_agent import execute_planning
from vector_search_schema import query_schema
from relevant_schema_finder import get_relevant_schema_finder
from sql_builder_agent import generate_sql
from summerizer import summarize


tools = None
dremio_mcp_client: DremioMcpClient | None = None
async def call_agent(question:str):

    global tools
    agent = create_agent_planner(tools)
    message = {"messages": [HumanMessage(content=question)]}
    result = await agent.ainvoke(
        message
    )
    print(result)
    return result["messages"][-1]


async def query_create(question:str):
    global tools

    agent = execute_planning(tools)
    message = {"messages": [HumanMessage(content=question)]}
    result = await agent.ainvoke(
        message
    )
    print(result)
    return result["messages"][-1]


app = FastAPI()

@app.on_event("startup")
async def start_up_function():
    global tools
    global dremio_mcp_client
    dremio_mcp_client = DremioMcpClient()
    tools = await dremio_mcp_client.connect()
    await fetch_metadata()


@app.get("/query")
async def query(question:str):
    #return await query_create(question)
    global dremio_mcp_client
    result = query_schema(question)
    print(result)
    schema = get_relevant_schema_finder(result)

    data = await generate_sql(question, schema)
    print(data)
    query_data = await dremio_mcp_client.execute_query(data["sql"])
    print(query_data)
    result_data = await summarize(question,data["sql"],query_data)
    return result_data





@app.post("/ask")
async def ask(request:str):
    # api_key = os.environ.get("OPENAI_API_KEY")
    # url = "https://api.groq.com/openai/v1/models"
    #
    # headers = {
    #     "Authorization": f"Bearer {api_key}",
    #     "Content-Type": "application/json"
    # }
    #
    # response = requests.get(url, headers=headers)
    #
    # print(response.json())
    return await call_agent(request)



