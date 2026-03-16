from fastapi import FastAPI
from components.dremio_executor import execute
app = FastAPI()

@app.get("/")
async def ask(question:str):
    return await execute(question)



