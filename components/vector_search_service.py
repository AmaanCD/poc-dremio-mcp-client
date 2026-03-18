from client.vector_store_client import get_vector_store

def search(question:str):
    vs = get_vector_store()
    return vs.similarity_search_with_score(question,k=2)