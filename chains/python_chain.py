import os

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from langchain_core.output_parsers import (
    StrOutputParser,
)

from prompts.python_prompt import python_prompt


load_dotenv()


def create_python_chain():

    api_key = os.getenv("GOOGLE_API_KEY")

    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.0-flash",
    )

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.2,
    )

    return (
        python_prompt
        | llm
        | StrOutputParser()
    )