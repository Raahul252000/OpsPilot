
from langchain_core.messages import HumanMessage

from app.services.llm import ollama_llm
from app.tools.search_application_logs import search_application_logs

if __name__ == '__main__':

    llm_with_tools = ollama_llm.bind_tools(
        [search_application_logs]
    )

    messages = [
        HumanMessage(
            content="""
            Investigate database connection pool exhaustion
            in the user-api service.
    
            Search the application logs.
    
            Use multiple relevant technical keywords, such as:
            - connection timeout
            - pool exhausted
            - database connection
            - connection acquisition
    
            Do not search using only the incident summary phrase.
            """
        )
    ]

    response = llm_with_tools.invoke(messages)

    print("\nQwen tool calls:")
    print(response.tool_calls)

    if response.tool_calls:
        for tool_call in response.tool_calls:

            print("\nRequested arguments:")
            print(tool_call["args"])

            result = search_application_logs.invoke(
                tool_call["args"]
            )

            print("\nMatching logs:")
            print("Total:", len(result))

            for log in result:
                print(log["message"])
    else:
        print("\nQwen did not request a tool call.")
        print("Response:", response.content)
