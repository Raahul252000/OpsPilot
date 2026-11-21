from app.tools.search_application_logs import search_application_logs


if __name__ == '__main__':

    from langchain.agents import create_agent

    from app.services.llm import ollama_llm
    from app.tools.get_service_metrics import get_service_metrics

    test_agent = create_agent(
        model=ollama_llm,
        tools=[get_service_metrics],
        system_prompt="""
        You are a service monitoring assistant.

        When asked to retrieve metrics for a service,
        you MUST call get_service_metrics.

        After receiving the tool result, summarize the metrics.
        Do not invent any values.
        """,
    )

    result = test_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Retrieve the service metrics for user-api.",
                }
            ]
        },
        config={"recursion_limit": 5},
    )

    print("\n========== AGENT MESSAGES ==========\n")

    for index, message in enumerate(result["messages"]):
        print(f"\nMESSAGE {index}")
        print("TYPE:", message.type)
        print("CONTENT:", repr(message.content))
        print("TOOL CALLS:", getattr(message, "tool_calls", []))
