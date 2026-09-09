from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from prompts.sql_prompt import sql_prompt
from config import GOOGLE_API_KEY, GEMINI_MODEL


def create_sql_agent():
    """
    Create the SQL generation chain.
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
        sql_prompt
        | llm
        | StrOutputParser()
    )


def run_sql_agent(
    question: str,
    chat_history: list | None = None,
) -> str:
    """
    Run the SQL agent with optional conversation history.
    """

    if chat_history is None:
        chat_history = []

    sql_agent = create_sql_agent()

    return sql_agent.invoke(
        {
            "question": question,
            "chat_history": chat_history,
        }
    )