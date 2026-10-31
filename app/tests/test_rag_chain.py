
from app.services.rag.chain import ask_question, rag_chain


question = (
    "Our API requests are timing out. "
    "What should we investigate if database connection "
    "pool exhaustion is a possible cause?"
)

def test_rag_chain():
    print(rag_chain.input_schema.model_json_schema())
    print(rag_chain.output_schema.schema())


if __name__ == '__main__':
    test_rag_chain()

    answer = ask_question(question)

    print("\n--- OpsPilot Answer ---\n")
    print(answer)
