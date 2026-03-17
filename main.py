from fastapi import FastAPI
from components.dremio_executor import execute as grok_execute
from components.gemini_dremio_executor import execute as gemini_execute
from client.gemini_llm import get_google_llm
app = FastAPI()

@app.get("/")
async def ask(question:str):
    return await grok_execute(question)


@app.get("/google")
async def ask_gemini(question:str):
    return await gemini_execute(question)



