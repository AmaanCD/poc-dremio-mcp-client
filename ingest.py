import json

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def get_vectorstore():

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},  # cosine-ready
    )
    return Chroma(
        collection_name="schema_metadata",
        embedding_function=embeddings,
        port=1100,
        host="localhost"
    )


def ingest(docs: list[dict]) -> None:
    from langchain_core.documents import Document
    vs = get_vectorstore()
    if vs._collection.count() == 0 :
        lc_docs = []
        for d in docs:
            m = dict(d["metadata"])
            m["description"] = d["description"]
            m["columns"] = json.dumps(d["columns"])  # ChromaDB only stores flat strings
            lc_docs.append(Document(page_content=d["content"], metadata=m, id=d["doc_id"]))

        vs.add_documents(lc_docs)
        print(f"✅  Ingested {len(lc_docs)} docs into 'schema_metadata'")
    else :
        print("Value already present in the collection")