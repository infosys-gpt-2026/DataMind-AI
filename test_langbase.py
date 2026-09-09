import os

from dotenv import load_dotenv
from langbase import Langbase


load_dotenv()

LANGBASE_API_KEY = os.getenv("LANGBASE_API_KEY")

if not LANGBASE_API_KEY:
    raise ValueError("LANGBASE_API_KEY not found in .env")


PIPE_NAME = "datamind-ai-analyst"


def run_langbase_test(question: str):
    langbase = Langbase(api_key=LANGBASE_API_KEY) # pyright: ignore[reportArgumentType]

    return langbase.pipes.run(
        name=PIPE_NAME,
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        stream=False,
    )


if __name__ == "__main__":
    print("🚀 DataMind AI — Langbase Test")
    print(f"🔌 Pipe: {PIPE_NAME}")

    response = run_langbase_test(
        "What are the 5 most important KPIs for a sales dashboard?"
    )

    print("\n🤖 DataMind AI Response:\n")
    print(response["completion"]) # pyright: ignore[reportGeneralTypeIssues, reportTypedDictNotRequiredAccess]

    print("\n📊 Metadata:")
    print(f"Model: {response.get('model')}")
    print(f"Provider: {response.get('provider')}")
    print(f"Thread ID: {response.get('threadId')}")

    print("\n✅ Langbase integration successful!")