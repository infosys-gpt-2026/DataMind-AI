import os

from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

from langchain_core.prompts import ChatPromptTemplate # pyright: ignore[reportMissingImports]
from langchain_core.output_parsers import StrOutputParser # pyright: ignore[reportMissingImports]

from langchain_google_genai import ChatGoogleGenerativeAI # pyright: ignore[reportMissingImports]


# Load environment variables
load_dotenv()


# -----------------------------
# 1. Initialize the LLM
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


# -----------------------------
# 2. Create Prompt Template
# -----------------------------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are DataMind AI, a professional AI Data Analyst Assistant.

Your responsibilities are:

1. Explain data clearly and accurately.
2. Identify important business insights.
3. Suggest useful KPIs and metrics.
4. Provide practical recommendations.
5. Use simple language when possible.

Always structure your answer professionally.
"""
    ),
    (
        "human",
        "{question}"
    )
])


# -----------------------------
# 3. Create Output Parser
# -----------------------------
output_parser = StrOutputParser()


# -----------------------------
# 4. Create LCEL Chain
# -----------------------------
chain = prompt | llm | output_parser


# -----------------------------
# 5. Ask User Question
# -----------------------------
question = """
A company has experienced a 20% decrease in sales.
What analysis should a Data Analyst perform?
"""


# -----------------------------
# 6. Invoke the Chain
# -----------------------------
response = chain.invoke({
    "question": question
})


# -----------------------------
# 7. Print Response
# -----------------------------
print("\n🤖 DataMind AI Response:\n")

print(response)