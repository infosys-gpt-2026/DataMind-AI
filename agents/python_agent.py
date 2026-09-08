from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from prompts.python_prompt import python_prompt
from config import GOOGLE_API_KEY, GEMINI_MODEL # pyright: ignore[reportAttributeAccessIssue]


def create_python_agent():

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
        python_prompt
        | llm
        | StrOutputParser()
    )


def run_python_agent(question: str):

    python_agent = create_python_agent()

    return python_agent.invoke({"question": question})