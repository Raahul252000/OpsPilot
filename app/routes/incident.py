from fastapi import APIRouter
from app.schemas.incidents import Incidents, IncidentResponse
from app.services.incident import create_new_incident
router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.post("/", response_model=IncidentResponse)
async def create_incidents(incidents: Incidents):
    res = await create_new_incident(incidents)
    return res