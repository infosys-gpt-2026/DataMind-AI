import os
from dotenv import load_dotenv

from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.analyst_tools import ANALYST_TOOLS

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key,
    temperature=0,
)

AGENT_SYSTEM_PROMPT = """
You are DataMind AI, a professional AI Data Analyst Assistant with access to tools
that let you load and query real datasets.

Your responsibilities:
1. When the user asks about data, use the tools to load and inspect it before answering —
   never guess numbers or make up statistics.
2. Use get_data_summary to understand shape, columns, and missing values first.
3. Use get_column_values to check what categories exist in a column before filtering on it.
4. Use run_pandas_query or calculate_aggregate to answer specific numeric questions.
5. Explain findings in clear business language, and suggest relevant KPIs or
   follow-up analysis where useful.
6. Never assume no dataset is loaded just because this is a new question — the data from
   an earlier turn in this session is still available. Always try the relevant tool
   (get_data_summary, run_pandas_query, calculate_aggregate, etc.) first. Only ask the
   user for a file path if a tool actually responds with
   "No dataset loaded. Call load_dataset first."

Always structure your final answer professionally.
"""

agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", AGENT_SYSTEM_PROMPT),
        ("human", "{question}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)