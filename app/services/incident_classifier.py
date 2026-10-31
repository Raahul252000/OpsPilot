from langchain_core.prompts import ChatPromptTemplate
from app.services.llm import genai_llm
from app.schemas.classification import IncidentClassification

"""
    * ChatPromptTemplate defines the messages sent to the model.
    * {title}, {description}, and {service} are placeholders filled with incident data.
    * prompt | llm uses LCEL to connect the prompt to the LLM.
    * classifier_chain is a reusable pipeline; it doesn't call the model until you invoke it.
"""
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an experienced production support engineer.
    
        Analyze the incident provided by the user.
    
        Return:
        1. Category
        2. Severity: low, medium, high, or critical
        3. A short summary
        4. Possible impact
    
        Do not invent facts that are not provided.
        If information is insufficient, mention the uncertainty.
        """
    ),
    (
        "human",
        """
        Incident title: {title}
        Description: {description}
        Service: {service}
        """
    )
])

# setting the llm to return the structured output as per the pydantic model
structured_llm = genai_llm.with_structured_output(IncidentClassification)

classifier_chain = prompt | structured_llm
