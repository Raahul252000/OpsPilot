from app.services.rag.embeddings import embedding_model


def main():
    text = (
        "Database connection pool exhaustion can cause "
        "API timeouts and elevated latency."
    )

    vector = embedding_model.embed_query(text)

    print("Embedding generated successfully")
    print("Vector dimensions:", len(vector))
    print("First 5 values:", vector[:5])


if __name__ == "__main__":
    main()