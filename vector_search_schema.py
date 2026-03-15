import json

from ingest import get_vectorstore


def query_schema(question: str, k: int = 5, score_threshold: float = 0.3) -> list[dict]:
    """
    Natural language → relevant table schemas.

    k=5              covers ~22% of a 22-table catalog; good for exploration
                     use k=3 when passing results to an LLM for SQL generation
    score_threshold  cosine similarity floor; <0.3 is typically irrelevant noise
    """
    vs = get_vectorstore()
    results = vs.similarity_search_with_relevance_scores(question, k=k)

    return [
        {
            "fqn": doc.metadata["fqn"],
            "table_type": doc.metadata["table_type"],
            "score": round(score, 4),
            "description": doc.metadata["description"],
            "columns": json.loads(doc.metadata["columns"]),
            "schema": doc.metadata["schema"],
            "table": doc.metadata["table"],
        }
        for doc, score in results
        #if score >= score_threshold
    ]