
from langchain.tools import tool
from app.services.rag.chain import ask_question


@tool
def search_knowledge_base(question: str) -> str:
    """
    Search the knowledge base for relevant runbooks,
    troubleshooting procedures, and historical incidents.

    Input:
    - question: A complete natural-language question describing
      what information needs to be retrieved.

    Use this tool for historical knowledge and documented
    troubleshooting guidance.
    """
    return ask_question(question)
