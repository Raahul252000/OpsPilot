
from app.services.llm import ollama_llm


if __name__ == '__main__':

    response = ollama_llm.invoke(
        "Explain database connection pool exhaustion in simple terms."
    )

    print("\nQwen Response:")
    print(response.content)
