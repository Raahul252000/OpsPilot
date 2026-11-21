
from app.services.incident_classifier import classifier_chain


if __name__ == '__main__':

    result = classifier_chain.invoke({
        "title": "User API returning HTTP 500 errors",
        "description": (
            "The user-api service is experiencing intermittent "
            "HTTP 500 errors. Database connection acquisition "
            "is timing out, and database queries are slow."
        ),
        "service": "user-api",
    })

    print("\nClassification result:")
    print(result)

    print("\nAs dictionary:")
    print(result.model_dump())
