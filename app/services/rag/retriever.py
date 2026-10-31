from langchain_core.documents import Document
from app.services.rag.vector_store import get_vector_store

def get_documents(query: str, k: int = 3) -> list[Document]:
    vector_store = get_vector_store()
    query_response = vector_store.similarity_search(query=query, k=k)
    return query_response