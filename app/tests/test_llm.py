from app.services.incident_classifier import classifier_chain

result = classifier_chain.invoke({
    "title": "Payment API returning 500",
    "description": (
        "Users are unable to complete payments. "
        "The issue started after the latest deployment."
    ),
    "service": "payment-api"
})

print("Result: ", result)
print("Category: ",result.category)
print("Severity: ", result.severity)
print(result.model_dump())