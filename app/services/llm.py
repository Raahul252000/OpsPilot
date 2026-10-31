from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GEMINI_API_KEY

genai_llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
)

