from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from prompts.kpi_prompt import kpi_prompt
from config import GOOGLE_API_KEY, GEMINI_MODEL


def create_kpi_agent():

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


def run_kpi_agent(question: str) -> str:
    """
    Run the KPI recommendation agent.
    """

    kpi_agent = create_kpi_agent()

    return kpi_agent.invoke(
        {
            "question": question,
        }
    )