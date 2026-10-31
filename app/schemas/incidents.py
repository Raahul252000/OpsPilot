from pydantic import BaseModel, Field
from typing import Literal

class Incidents(BaseModel):
    title: str
    description: str
    service: str


class IncidentClassification(BaseModel):
    category: Literal[
        "database",
        "api",
        "infrastructure",
        "deployment",
        "network",
        "security",
        "unknown"
    ]

    severity: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ]

    summary: str = Field(
        description="A short summary of the incident"
    )

    possible_impact: str = Field(
        description="Potential impact based on the provided details"
    )

# Response model
class IncidentResponse(BaseModel):
    title: str
    description: str
    service: str
    status: str
    classification: IncidentClassification
    investigation_result: str