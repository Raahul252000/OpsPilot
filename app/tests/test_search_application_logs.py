
from app.tools.search_application_logs import (
    search_application_logs,
)
from app.services.llm import genai_llm


if __name__ == '__main__':
    print("Tool name:", search_application_logs.name)
    print("Tool description:", search_application_logs.description)
    print("Tool arguments:", search_application_logs.args)

    # Give Gemini access to the tool definition.
    llm_with_tools = genai_llm.bind_tools(
        [search_application_logs]
    )

    messages = [
        (
            "human",
            """
            Investigate why the user-api service is returning HTTP 500 errors.
            Search the logs for database connection pool exhaustion.
            """
        )
    ]

    # Stage 1: Ask Gemini to decide whether a tool is needed.
    response = llm_with_tools.invoke(messages)

    print("Tool calls requested:", response.tool_calls)

    # Stage 2: Execute the requested tool.
    for tool_call in response.tool_calls:
        if tool_call["name"] == search_application_logs.name:
            result = search_application_logs.invoke(
                tool_call["args"]
            )

            print("\nTool execution result:")
            print(result)
