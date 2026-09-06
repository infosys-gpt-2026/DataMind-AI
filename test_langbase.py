import os
import json
from dotenv import load_dotenv
from langbase import Langbase

load_dotenv()

LANGBASE_API_KEY = os.getenv("LANGBASE_API_KEY")

if not LANGBASE_API_KEY:
    raise ValueError("LANGBASE_API_KEY not found in .env")

print("🚀 Starting DataMind AI with Langbase...")
print("🔌 Connecting to datamind-ai-analyst...")

langbase = Langbase(api_key=LANGBASE_API_KEY)

response = langbase.pipes.run(
    name="datamind-ai-analyst",
    messages=[
        {
            "role": "user",
            "content": "What are the most important KPIs for a sales dashboard?"
        }
    ],
    stream=False
)

print("\n🔍 Raw response structure:\n")
print(json.dumps(response, indent=2, default=str))

print("\n🤖 DataMind AI Response:\n")
# Try the most common Langbase response shape
try:
    print(response["choices"][0]["message"]["content"]) # pyright: ignore[reportTypedDictNotRequiredAccess, reportGeneralTypeIssues]
except (KeyError, TypeError):
    print("Could not find response['choices'][0]['message']['content'] — check the raw structure printed above")

print("\n✅ Langbase Pipe test successful!")