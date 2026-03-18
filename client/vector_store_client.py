from langchain_chroma import Chroma

from client.embedding_client import get_embedding_client

_chroma = None
def get_vector_store():
    global _chroma

    if _chroma is not None:
        return _chroma

    _chroma = Chroma(
        collection_name="schema",
        embedding_function=get_embedding_client(),
        port=1100,
        host="localhost"
    )
    return _chroma
