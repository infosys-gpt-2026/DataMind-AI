from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from prompts.sql_prompt import sql_prompt # pyright: ignore[reportAttributeAccessIssue]
from config import GOOGLE_API_KEY, GEMINI_MODEL


def create_sql_agent():

    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY not found in .env file"
        )

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )

    return (
        sql_prompt
        | llm
        | StrOutputParser()
    )


def run_sql_agent(question: str):

    sql_agent = create_sql_agent()

    return sql_agent.invoke({"question": question})