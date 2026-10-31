from app.services.rag.ingestion import (
    load_documents,
    split_documents,
)


def main():
    documents = load_documents()
    chunks = split_documents(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")

    for chunk in chunks[:3]:
        print("\nSource:", chunk.metadata["source"])
        print("Start index:", chunk.metadata["start_index"])
        print("Content preview:", chunk.page_content[:200])


if __name__ == "__main__":
    main()