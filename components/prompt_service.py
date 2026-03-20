


def build_prompt(question:str,documents:list):
    schema_context = "\n\n---\n\n".join(
        doc.page_content for doc, score in documents
    )
    prompt = f"""AVAILABLE SCHEMAS:
    {schema_context}

    USER QUESTION:
    {question}

    
    """
    return prompt

def build_system_prompt():
    return f"""
You are an expert SQL assistant.
STRICT OUTPUT RULES — you must follow these without exception:
1. Return final created  SQL query. No explanations. No markdown. No preamble.
2. Do NOT Make up data,table and column which do not exist
3. Use Alias where it is required for aggregation functions
"""

