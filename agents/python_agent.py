import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from prompts.python_prompt import python_prompt


load_dotenv()


def create_python_agent():

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in .env file"
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2,
    )

    return python_prompt | llm | StrOutputParser()


def run_python_agent(question: str):

    agent = create_python_agent()

    return agent.invoke({"question": question})