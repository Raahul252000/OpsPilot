import time
from app.schemas.incidents import Incidents
from app.services.incident_classifier import classifier_chain
from app.services.incident_investigator import build_retrieval_query, investigate_with_logs
from app.services.rag.chain import ask_question


async def create_new_incident(incident: Incidents):

    print("[A] Starting classification...")
    start = time.perf_counter()

    # Step 1: Classify the incident
    classification = classifier_chain.invoke({
        "title": incident.title,
        "description": incident.description,
        "service": incident.service,
    })

    print(f"[A] Classification completed in {time.perf_counter() - start:.1f}s")

    classification_data = classification.model_dump()

    # Step 2: Build a query for knowledge retrieval
    retrieval_query = build_retrieval_query(title=incident.title,
                          description=incident.description,
                          service=incident.service,
                          classification=classification_data)

    print("[B] Starting RAG...")
    start = time.perf_counter()
    # Step 3: Investigate using RAG
    rag_findings = ask_question(retrieval_query)

    print(f"[B] RAG completed in {time.perf_counter() - start:.1f}s")

    print("[C] Starting tool-based investigation...")
    # Step 4: Tool call with the rag findings
    investigation_result = investigate_with_logs(
        incident_question=retrieval_query,
        rag_findings=rag_findings
    )
    print("[C] Tool-based investigation completed")

    return {
        "title": incident.title,
        "description": incident.description,
        "service": incident.service,
        "status": "open",
        "classification": classification_data,
        "investigation_result": investigation_result,
    }