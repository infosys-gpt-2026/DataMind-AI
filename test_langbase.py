import os
from dotenv import load_dotenv
from langbase import Langbase, get_runner

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("LANGBASE_API_KEY")

if not api_key:
    raise ValueError("LANGBASE_API_KEY not found in .env")

print("🚀 Starting DataMind AI with Langbase...")

# Initialize Langbase
langbase = Langbase(api_key=api_key)

# Run your Pipe
response = langbase.pipes.run(
    name="datamind-ai-analyst",
    messages=[
        {
            "role": "user",
            "content": "What are the most important KPIs for a sales dashboard?"
        }
    ]
)

print("\n🤖 DataMind AI Response:\n")

runner = get_runner(response)

for content in runner.text_generator():
    print(content, end="", flush=True)