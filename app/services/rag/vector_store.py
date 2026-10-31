from pathlib import Path
from langchain_chroma import Chroma
from app.services.rag.embeddings import embedding_model

PROJECT_ROOT = Path(__file__).resolve().parents[3]

VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store" / "chroma"

COLLECTION_NAME = "opspilot_knowledge"


def get_vector_store() -> Chroma:

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=str(VECTOR_STORE_DIR),
    )

    return vector_store