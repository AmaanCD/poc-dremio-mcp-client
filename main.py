from fastapi import FastAPI

from components.dremio_executor import execute as grok_execute
from components.gemini_dremio_executor import execute as gemini_execute
from components.ingest_schema import ingest
from components.vector_search_service import search
app = FastAPI()

@app.get("/")
async def ask(question:str):
    return await grok_execute(question)


@app.get("/google")
async def ask_gemini(question:str):
    return await gemini_execute(question)


@app.on_event("startup")
async def test():

    await ingest()

@app.get("/vector")
def search_vector(question:str):
    return  search(question)






