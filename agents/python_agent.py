from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from prompts.python_prompt import python_prompt
from config import GOOGLE_API_KEY, GEMINI_MODEL


def create_python_agent():
    """
    Create the Python code generation chain.
    """

    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY not found in .env file"
        )

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
    )

    return (
        python_prompt
        | llm
        | StrOutputParser()
    )


def run_python_agent(
    question: str,
    chat_history: list | None = None,
) -> str:
    """
    Run the Python agent with optional conversation history.
    """

    if chat_history is None:
        chat_history = []

    python_agent = create_python_agent()

    return python_agent.invoke(
        {
            "question": question,
            "chat_history": chat_history,
        }
    )