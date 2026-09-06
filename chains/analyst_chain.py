import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from prompts.analyst_prompt import analyst_prompt


# Load environment variables
load_dotenv()


# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")


# Check LangSmith configuration
if os.getenv("LANGSMITH_TRACING") == "true":
    print("🔍 LangSmith tracing is enabled")
    print(f"📊 Project: {os.getenv('LANGSMITH_PROJECT')}")


# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)


# Output parser
parser = StrOutputParser()


# LCEL Chain
analyst_chain = analyst_prompt | llm | parser