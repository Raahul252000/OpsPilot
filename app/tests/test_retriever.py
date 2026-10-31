from app.services.rag.retriever import get_documents


def main():
    query = "How do I investigate database connection pool exhaustion?"

    results = get_documents(query=query, k=3)

    print(f"Retrieved {len(results)} documents")

    for index, document in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")

        print("Source:", document.metadata.get("source"))

        print("Content:")
        print(document.page_content)


if __name__ == "__main__":
    main()