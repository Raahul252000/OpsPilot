
from app.tools.search_knowledge_base import search_knowledge_base


if __name__ == '__main__':

    result = search_knowledge_base.invoke({
        "question": "How should we troubleshoot database connection pool exhaustion?"
    })

    print(result)
