from langchain.agents import create_agent

from app.services.llm import ollama_llm

from app.tools.search_knowledge_base import search_knowledge_base
from app.tools.search_application_logs import search_application_logs
from app.tools.get_service_metrics import get_service_metrics
from langchain.messages import AIMessage
from langgraph.errors import GraphRecursionError

AVAILABLE_TOOLS = [
    search_knowledge_base,
    search_application_logs,
    get_service_metrics,
]

SYSTEM_PROMPT = """
You are OpsPilot, an AI engineering incident investigation assistant.

Investigate the incident using the available tools.

Available tools:

1. search_knowledge_base:
   Search historical incident reports and troubleshooting runbooks.

2. search_application_logs:
   Search application logs.
   Always provide both service and keywords.

3. get_service_metrics:
   Retrieve operational metrics for a service.

Instructions:

- Read the incident details carefully.
- Use the tools that are relevant to the incident.
- You may call multiple tools when necessary.
- Do not invent tool results or operational data.
- Treat tool results as evidence.
- Clearly distinguish confirmed observations from hypotheses.
- Metrics are simulated, not live production data.
- Never claim that an incident is resolved.

After gathering evidence, produce a concise investigation report.
"""

incident_agent = create_agent(
    model=ollama_llm,
    tools=AVAILABLE_TOOLS,
    system_prompt=SYSTEM_PROMPT,
)

def get_response_text(response) -> str:
    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = [
            block["text"]
            for block in content
            if isinstance(block, dict) and block.get("text")
        ]
        return "\n".join(text_parts)

    return ""


def investigate_with_real_agent(incident_question: str) -> str:
    inputs = {
        "messages": [
            {
                "role": "user",
                "content": incident_question,
            }
        ]
    }

    try:
        result = incident_agent.invoke(
            inputs,
            config={"recursion_limit": 12},
        )

    except GraphRecursionError as exc:
        raise RuntimeError(
            "Incident investigation exceeded the agent recursion limit."
        ) from exc

    # Find the last AI response containing actual text.
    for message in reversed(result["messages"]):
        if (
            isinstance(message, AIMessage)
            and isinstance(message.content, str)
            and message.content.strip()
        ):
            return message.content.strip()

    raise RuntimeError(
        "Agent completed without producing a final text response."
    )