


def build_prompt(question:str,documents:list):
    schema_context = "\n\n---\n\n".join(
        doc.page_content for doc, score in documents
    )
    prompt = f"""You are an expert SQL assistant. Use the following table schemas to answer the question.

    AVAILABLE SCHEMAS:
    {schema_context}

    USER QUESTION:
    {question}

    Generate a SQL query to answer the question. Use only the tables and columns described above.
    SQL:"""
    return prompt

