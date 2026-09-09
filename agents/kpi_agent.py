from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from prompts.kpi_prompt import kpi_prompt
from config import GOOGLE_API_KEY, GEMINI_MODEL


def create_kpi_agent():
    """
    Create the KPI recommendation and analysis chain.
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
        kpi_prompt
        | llm
        | StrOutputParser()
    )


def run_kpi_agent(
    question: str,
    chat_history: list | None = None,
) -> str:
    """
    Run the KPI agent with optional conversation history.
    """

    if chat_history is None:
        chat_history = []

    kpi_agent = create_kpi_agent()

    return kpi_agent.invoke(
        {
            "question": question,
            "chat_history": chat_history,
        }
    )