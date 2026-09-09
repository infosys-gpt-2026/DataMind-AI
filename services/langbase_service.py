import os

from dotenv import load_dotenv
from langbase import Langbase


load_dotenv()

LANGBASE_API_KEY = os.getenv("LANGBASE_API_KEY")
LANGBASE_PIPE_NAME = os.getenv(
    "LANGBASE_PIPE_NAME",
    "datamind-ai-analyst"
)


class LangbaseService:
    """Service wrapper for Langbase Pipe execution."""

    def __init__(self):
        if not LANGBASE_API_KEY:
            raise ValueError(
                "LANGBASE_API_KEY not found in environment variables."
            )

        self.client = Langbase(api_key=LANGBASE_API_KEY)

    def run(self, message: str) -> dict:
        """Run a message through the configured Langbase Pipe."""

        return self.client.pipes.run(
            name=LANGBASE_PIPE_NAME,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            stream=False,
        ) # pyright: ignore[reportReturnType]

    def ask(self, message: str) -> str:
        """Return only the generated completion."""

        response = self.run(message)

        return response.get(
            "completion",
            ""
        )