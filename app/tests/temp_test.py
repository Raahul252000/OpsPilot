from app.tools.search_application_logs import search_application_logs


if __name__ == '__main__':

    result = search_application_logs.invoke({
        "service": "user-api",
        "keywords": [
            "connection pool exhaustion",
            "connection timeout",
            "pool exhausted",
            "database connection",
        ],
    })

    print("Matching logs:", len(result))

    for log in result:
        print(log["message"])