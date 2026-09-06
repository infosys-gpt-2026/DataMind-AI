import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from langchain_google_genai import ChatGoogleGenerativeAI # pyright: ignore[reportMissingImports]

# Load environment variables
load_dotenv()

# Check API key exists
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY was not found in the .env file")

print("Starting DataMind AI...")
print("Using model: gemini-3.6-flash")

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)

# Ask a question
response = llm.invoke(
    "Explain what a Data Analyst does in simple words."
)

print("\n🤖 AI Response:\n")

# Print response safely
if isinstance(response.content, list):
    for item in response.content:
        if isinstance(item, dict) and item.get("type") == "text":
            print(item.get("text", ""))
else:
    print(response.content)