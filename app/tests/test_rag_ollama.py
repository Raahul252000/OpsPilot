from app.services.rag.chain import ask_question


if __name__ == '__main__':

    result = ask_question(
        "What are the common causes of database connection pool exhaustion?"
    )

    print("\nRAG Investigation:")
    print(result)