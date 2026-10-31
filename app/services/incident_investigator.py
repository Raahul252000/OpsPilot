import json
import time
from langchain_core.messages import HumanMessage, ToolMessage
from app.services.llm import genai_llm
from app.tools.search_application_logs import search_application_logs

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


def investigate_with_logs(
    incident_question: str,
    rag_findings: str,
) -> str:

    # Letting llm know that it has tool, if needed it can use it.
    llm_with_tools = genai_llm.bind_tools(
        [search_application_logs]
    )

    messages = [
        HumanMessage(
            content=f"""
            Investigate this incident using the provided evidence.

            Incident details:
            {incident_question}

            Findings from the RAG investigation:
            {rag_findings}

            Search the application logs for the affected service
            and relevant errors. Use the log-search tool before
            producing your final investigation.

            In your final answer:
            - Separate observed evidence from hypotheses.
            - Explain what the logs support.
            - Identify missing information.
            - Recommend the next diagnostic checks.
            - Do not claim the incident is resolved.
            """
        )
    ]
    print("[1] Requesting tool decision from Gemini...")
    start = time.perf_counter()
    # 1. Ask Gemini to choose a tool.
    response = llm_with_tools.invoke(messages)

    print(
        f"[1] Gemini responded in "
        f"{time.perf_counter() - start:.1f}s"
    )
    print("[2] Tool calls:", response.tool_calls)

    messages.append(response)

    # 2. Execute the tool requests from Gemini.
    for tool_call in response.tool_calls:
        if tool_call["name"] != search_application_logs.name:
            continue

        print("[3] Executing log-search tool...")
        result = search_application_logs.invoke(
            tool_call["args"]
        )
        print(f"[3] Tool returned {len(result)} logs")

        # 3. Return the tool result to the conversation.
        messages.append(
            ToolMessage(
                content=json.dumps(result, default=str),
                tool_call_id=tool_call["id"],
            )
        )


    print("[4] Requesting final analysis from Gemini...")
    start = time.perf_counter()
    # 4. Ask Gemini to analyze the returned evidence.
    final_response = llm_with_tools.invoke(messages)

    print(
        f"[4] Final analysis completed in "
        f"{time.perf_counter() - start:.1f}s"
    )

    content = final_response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict) and block.get("text")
        )

    return str(content)