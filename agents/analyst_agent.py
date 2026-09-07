import os

from dotenv import load_dotenv

from langchain_classic.agents import (
    create_tool_calling_agent,
    AgentExecutor,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from langchain_google_genai import ChatGoogleGenerativeAI

from tools.analyst_tools import ANALYST_TOOLS


load_dotenv()


# ==============================
# API KEY
# ==============================

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env file"
    )


# ==============================
# LLM
# ==============================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0,
)


# ==============================
# SYSTEM PROMPT
# ==============================

AGENT_SYSTEM_PROMPT = """
You are DataMind AI, a professional AI Data Analyst Assistant.

You have access to tools that can load and analyze real datasets.

IMPORTANT TOOL RULES:

1. NEVER answer questions about a dataset without first using
the appropriate tool.

2. For dataset summary, columns, missing values, data types:
→ use get_data_summary

3. For available regions, products, categories, or unique values:
→ use get_column_values

4. For totals, averages, maximum, minimum, median,
statistics, or grouped calculations:
→ use calculate_aggregate

5. For filtering or displaying matching records:
→ use run_pandas_query

6. For loading a dataset:
→ use load_dataset

CRITICAL RULE:

Do NOT tell the user to load a dataset unless you first call
a dataset-related tool and it explicitly says:

"No dataset loaded. Call load_dataset first."

The dataset remains available during the current application session.

Never invent data, statistics, categories, or results.

Always answer based on actual tool results.

Always provide a clear and professional final answer.
"""


# ==============================
# AGENT PROMPT
# ==============================

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            AGENT_SYSTEM_PROMPT,
        ),

        MessagesPlaceholder(
            variable_name="chat_history"
        ),

        (
            "human",
            "{question}",
        ),

        MessagesPlaceholder(
            variable_name="agent_scratchpad"
        ),
    ]
)


# ==============================
# CREATE AGENT
# ==============================

analyst_agent = create_tool_calling_agent(
    llm,
    ANALYST_TOOLS,
    agent_prompt,
)


# ==============================
# AGENT EXECUTOR
# ==============================

analyst_agent_executor = AgentExecutor(
    agent=analyst_agent,
    tools=ANALYST_TOOLS,
    verbose=True,
    handle_parsing_errors=True,
)


# ==============================
# RUN AGENT FUNCTION
# ==============================

def run_analyst_agent(question: str):

    response = analyst_agent_executor.invoke(
        {
            "question": question,
            "chat_history": [],
        }
    )

    return response["output"]