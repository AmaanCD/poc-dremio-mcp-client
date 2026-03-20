
def create_schema_context(documents : list)-> str:
    schema_context = "\n\n---\n\n".join(
        doc.page_content for doc, score in documents)

    return schema_context
