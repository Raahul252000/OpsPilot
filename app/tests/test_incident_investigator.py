
from app.services.incident_investigator import build_retrieval_query

classification = {
    "category": "database",
    "severity": "high",
    "summary": "Database connection timeouts are affecting the API.",
    "possible_impact": "API requests may fail or experience increased latency.",
}



if __name__ == '__main__':

    query = build_retrieval_query(
        title="Database connection timeout",
        description="The API is failing because database connections are timing out.",
        service="user-api",
        classification=classification,
    )

    print(query)
