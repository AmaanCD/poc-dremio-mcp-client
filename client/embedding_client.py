from langchain_huggingface import HuggingFaceEmbeddings

_embedding_client = None
def get_embedding_client():
    global _embedding_client

    if _embedding_client is not None:
        return _embedding_client

    _embedding_client = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    return _embedding_client

