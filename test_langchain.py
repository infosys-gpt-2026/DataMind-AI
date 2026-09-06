import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from langchain_google_genai import ChatGoogleGenerativeAI # pyright: ignore[reportMissingImports]

# Load environment variables
load_dotenv()

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

# Ask a question
response = llm.invoke(
    "Explain what a Data Analyst does in simple words."
)

print("\n🤖 AI Response:\n")
print(response.content)