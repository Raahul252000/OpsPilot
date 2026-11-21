import time
from app.schemas.incidents import Incidents
from app.services.incident_classifier import classifier_chain
from app.services.incident_investigator import manual_investigator_agent, build_retrieval_query
from app.services.agent.incident_investigator_agent import investigate_with_real_agent


async def create_new_incident(incident: Incidents):

    print("[A] Starting incident classification...")
    start = time.perf_counter()

    # Step 1: Classify the incident
    classification = classifier_chain.invoke({
        "title": incident.title,
        "description": incident.description,
        "service": incident.service,
    })

    print(f"[A] Incident Classification completed in {time.perf_counter() - start:.1f}s")

    classification_data = classification.model_dump()

    # Step 2: Build a query for knowledge retrieval
    retrieval_query = build_retrieval_query(title=incident.title,
                          description=incident.description,
                          service=incident.service,
                          classification=classification_data)

    print("[B] Starting tool-based investigation")

    # # Calling our manually created agent
    # investigation_result = manual_investigator_agent(
    #     incident_question=retrieval_query
    # )

    # Calling agent created with langchain
    investigation_result = investigate_with_real_agent(incident_question=retrieval_query)
    print("[B] Tool-based investigation completed")
    print(f"Investigation result: {investigation_result}")
    return {
        "title": incident.title,
        "description": incident.description,
        "service": incident.service,
        "status": "open",
        "classification": classification_data,
        "investigation_result": investigation_result,
    }