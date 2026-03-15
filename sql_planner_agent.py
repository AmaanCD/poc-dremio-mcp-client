from langchain.agents import create_agent

from llm_grok import get_model

agent = None
def execute_planning(tools):
    global agent
    if agent is None :
        model = get_model()
        agent = create_agent(
            tools=tools,
            model=model,
            system_prompt="""
            You are a SQL query planner which will convert natural language to sql query.
    
    Your job is to generate a valid SQL query to answer the user's question.
    
    Guidelines:
    
    Use the available tools to inspect schemas, tables, and metadata if needed.
    
    Do NOT guess table or column names. Always verify using tools.
    
    Generate a syntactically correct SQL use explain if required to validate.
    
    Do not include explanations or extra text.
    
    Return the result strictly in JSON format:
    
    {
    "query": "SQL_QUERY_HERE"
    }
    
    Only return valid JSON. Do not include any text outside the JSON.
    Give me final result only
            """
        )
        return agent
    else:
        return agent