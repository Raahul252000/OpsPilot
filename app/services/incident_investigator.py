
import json

from langchain_core.messages import HumanMessage, ToolMessage
from app.services.llm import ollama_llm

from app.tools.search_application_logs import search_application_logs
from app.tools.search_knowledge_base import search_knowledge_base
from app.tools.get_service_metrics import get_service_metrics

AVAILABLE_TOOLS = [
    search_knowledge_base,
    search_application_logs,
    get_service_metrics,
]

TOOL_MAP = {
    tool.name: tool
    for tool in AVAILABLE_TOOLS
}


def get_response_text(response) -> str:
    """Extract text from an LLM response."""
    content = response.content

    if isinstance(content, str) and content.strip():
        return content

    if isinstance(content, list):
        text_parts = [
            block["text"]
            for block in content
            if isinstance(block, dict) and block.get("text")
        ]

        if text_parts:
            return "\n".join(text_parts)

    return ""

"""
 - investigate_with_tools() is our manually implemented agent loop. More specifically, it is the orchestration function
  that runs our tool-calling agent. we're currently implementing the agent loop ourselves. 
 - LangChain's create_agent() provides a higher-level way to create and run an agent without manually writing
  much of this orchestration code.
  
So we'll eventually compare:
    - Our current agent: Manually implemented using bind_tools(), ToolMessage and a Python loop.
    - LangChain agent: Implemented using create_agent() with tools and an agent runtime.
Both are agents. One is manually orchestrated; the other uses a framework-managed runtime.

Remember this distinction:
    - LLM = makes decisions.
    - Tools = perform actions.
    - Agent loop = connects decisions, actions and observations.
    - Agent = the system combining these capabilities to achieve a goal.
"""
def investigate_with_tools(incident_question: str) -> str:
    """Investigate an incident using available tools."""

    llm_with_tools = ollama_llm.bind_tools(AVAILABLE_TOOLS)

    messages = [
        HumanMessage(content=f"""
    You are OpsPilot, an AI engineering incident investigation assistant.

    Your task is to investigate the incident using available tools
    and produce an evidence-based investigation report.

    INCIDENT DETAILS:
    {incident_question}

    AVAILABLE TOOLS:

    1. search_knowledge_base:
       Searches runbooks, troubleshooting procedures, and historical
       incident reports.

    2. search_application_logs:
       Searches application logs for a particular service using
       multiple keywords.

    3. get_service_metrics:
       Retrieves service metrics such as CPU, memory, request rate,
       error rate, latency, and database connection pool utilization.

    TOOL ARGUMENT RULES:

    For search_knowledge_base:
    - The only argument is "question".
    - Pass a complete natural-language question.

    For search_application_logs:
    - Pass "service" and "keywords".
    - Keywords must be a list of relevant search terms.

    For get_service_metrics:
    - The only argument is "service".
    - Pass the affected application service name.

    TOOL SELECTION RULES:

    - Use search_knowledge_base for historical knowledge,
      documented procedures, and troubleshooting guidance.
    - Use search_application_logs for actual application log evidence.
    - Use get_service_metrics for service performance and
      resource utilization evidence.
    - You may use one, two, or all three tools depending on the incident.
    - Do not call tools unnecessarily.
    - If a tool returns insufficient information, consider whether
      another search or tool call would help.
    - Correlate evidence from different sources when available.

    FINAL INVESTIGATION EVIDENCE RULES:

    1. Only report facts explicitly present in tool results.
    2. Never invent logs, metrics, configurations, or observations.
    3. Clearly distinguish:
       - Confirmed observations
       - Hypotheses
       - Missing information
    4. Never describe a hypothesis as confirmed.
    5. Do not claim that a query is inefficient unless evidence supports it.
    6. Recommend technologies appropriate to the application's stack.
    7. If a tool did not provide information, explicitly state that
       the information is unavailable.
    8. Clearly identify simulated data as simulated.
       Never present simulated metrics as live production measurements.
    9. Do not recommend changing production configuration without
       first identifying relevant capacity and safety constraints.

    FINAL INVESTIGATION REPORT:

    Structure your response using these sections:

    1. Incident Summary
    2. Confirmed Observations
    3. Correlated Evidence
    4. Possible Root Causes (Hypotheses)
    5. Missing Information
    6. Recommended Diagnostic Steps
    7. Conclusion

    Never claim that the incident is resolved.
    """)
    ]

    max_tool_rounds = 3

    for round_number in range(max_tool_rounds):
        print(f"[Ollama] Requesting response: round {round_number + 1}")

        response = llm_with_tools.invoke(messages)

        messages.append(response)

        print("[Ollama] Tool calls:", response.tool_calls)

        # The model has decided to finish the investigation.
        if not response.tool_calls:
            final_answer = get_response_text(response)

            if final_answer:
                return final_answer

            raise ValueError(
                f"Ollama returned an empty response: {response!r}"
            )

        # Execute every tool requested by the model.
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            print(f"[Ollama] Requested tool: {tool_name}")
            print(f"[Ollama] Tool arguments: {tool_args}")

            selected_tool = TOOL_MAP.get(tool_name)

            if selected_tool is None:
                result = {
                    "error": f"Unsupported tool: {tool_name}"
                }
            else:
                try:
                    result = selected_tool.invoke(tool_args)
                except Exception as exc:
                    print(f"[Tool Error] {tool_name}: {exc}")
                    result = {
                        "error": f"Tool execution failed: {str(exc)}"
                    }

            if isinstance(result, str):
                tool_result = result
            else:
                tool_result = json.dumps(result, default=str)

            print(f"[Ollama] Tool {tool_name} execution completed.")

            messages.append(
                ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call_id,
                )
            )

    # If the tool-call limit is reached, request a final answer
    # without allowing further tool calls.
    print("[Ollama] Tool-call limit reached. Generating final answer.")

    final_response = ollama_llm.invoke(messages)
    final_answer = get_response_text(final_response)

    if final_answer:
        return final_answer

    raise ValueError(
        f"Ollama failed to generate a final investigation: "
        f"{final_response!r}"
    )


def build_retrieval_query(
    title: str,
    description: str,
    service: str,
    classification: dict,
) -> str:
    return (
        f"Incident title: {title}\n"
        f"Affected service: {service}\n"
        f"Category: {classification['category']}\n"
        f"Severity: {classification['severity']}\n"
        f"Summary: {classification['summary']}\n"
        f"Possible impact: {classification['possible_impact']}\n"
        f"Description: {description}"
    )
