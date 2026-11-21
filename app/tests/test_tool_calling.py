from app.services.llm import ollama_llm
from app.services.agent.incident_investigator_agent import AVAILABLE_TOOLS

llm_with_tools = ollama_llm.bind_tools(AVAILABLE_TOOLS)

if __name__ == '__main__':

    response = llm_with_tools.invoke(
        """
        Investigate database connection timeouts in user-api.
    
        Retrieve service metrics for user-api.
        """
    )

    print("\nCONTENT:")
    print(repr(response.content))

    print("\nSTRUCTURED TOOL CALLS:")
    print(response.tool_calls)

    print("\nINVALID TOOL CALLS:")
    print(response.invalid_tool_calls)

    print("\nADDITIONAL KWARGS:")
    print(response.additional_kwargs)

    print("\nRESPONSE METADATA:")
    print(response.response_metadata)