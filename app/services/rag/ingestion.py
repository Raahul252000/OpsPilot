from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from app.services.rag.embeddings import embedding_model
from app.services.rag.vector_store import get_vector_store

PROJECT_ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"
VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store" / "chroma"


#-----------------------------------------------------------------------------------------------------------------------
def load_documents() -> list[Document]:
    """Load Markdown documents from the knowledge base."""
    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.rglob("*.md"):
        if file_path.name == "README.md":
            continue

        text = file_path.read_text(encoding="utf-8")

        if not text.strip():
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": str(file_path.relative_to(PROJECT_ROOT)),
                    "file_name": file_path.name,
                },
            )
        )

    return documents


#-----------------------------------------------------------------------------------------------------------------------
def split_documents(
    documents: list[Document],
) -> list[Document]:
    """Split documents into smaller overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        add_start_index=True,
    )

    return splitter.split_documents(documents)


#-----------------------------------------------------------------------------------------------------------------------
def store_chunks(chunks: list[Document]) -> Chroma:
    # Open the existing collection, or create it if it doesn't exist.
    vector_store = get_vector_store()

    # Remove the old collection.
    vector_store.delete_collection()

    # Create a fresh, empty collection.
    vector_store = get_vector_store()

    # Generate embeddings and insert the new chunks.
    vector_store.add_documents(chunks)

    return vector_store


#-----------------------------------------------------------------------------------------------------------------------
def ingest_documents() -> Chroma:
    documents = load_documents()
    print(f"Loaded {len(documents)} documents")

    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    vector_store = store_chunks(chunks)
    print("Chunks stored in ChromaDB")

    return vector_store


#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    ingest_documents()