import json

from langchain_core.messages import SystemMessage, HumanMessage

from summarizer_model import get_summarizer_model


SUMMARIZER_PROMPT = """You are an enterprise data analyst assistant.
Given a user question, the SQL query that was executed, and its result set, provide a clear concise answer.

Rules:
- Answer in 2-3 sentences maximum
- Lead with the direct answer, not with filler phrases
- Reference specific numbers/values from the result
- If result is empty, say no data was found and suggest why
- Never mention SQL, tables, or technical details in your answer
- Use business language, not technical language"""

async def summarize(question,sql,result):
    model = get_summarizer_model()
    response=await model.ainvoke(
        [
            SystemMessage(content=SUMMARIZER_PROMPT),
            HumanMessage(content=f"""Question: {question}

        SQL: {sql}
        
        Result: {json.dumps(result, indent=2)}
        
        Answer:""")
        ]

    )
    return response.content.strip()