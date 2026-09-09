import os

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from langchain_core.output_parsers import (
    StrOutputParser,
)

from prompts.kpi_prompt import kpi_prompt


load_dotenv()


def create_kpi_chain():

    api_key = os.getenv("GOOGLE_API_KEY")

    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.6-flash",
    )

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.3,
    )

    return (
        kpi_prompt
        | llm
        | StrOutputParser()
    )