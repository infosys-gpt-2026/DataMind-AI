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
from config import GOOGLE_API_KEY, GEMINI_MODEL


# ============================================================
# VALIDATE API KEY
# ============================================================

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env file"
    )


# ============================================================
# LLM
# ============================================================

llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GOOGLE_API_KEY,
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

AGENT_SYSTEM_PROMPT = """
You are DataMind AI, a professional AI Data Analyst Assistant.

You analyze real datasets using the tools provided to you.

IMPORTANT TOOL RULES:

1. NEVER invent dataset values, statistics, categories,
   calculations, or results.

2. For dataset overview, columns, data types, missing values,
   duplicates, or numeric summaries:
   → use get_data_summary

3. For viewing rows from the dataset:
   → use get_dataset_preview

4. For regions, products, categories, unique values,
   or values inside a specific column:
   → use get_column_values

5. For totals, averages, median, minimum, maximum,
   count, standard deviation, or grouped calculations:
   → use calculate_aggregate

6. For filtering records:
   → use run_pandas_query

7. For loading CSV or Excel datasets:
   → use load_dataset

CRITICAL RULE:

Do NOT tell the user to load a dataset unless a dataset-related
tool explicitly returns:

"No dataset loaded. Call load_dataset first."

The dataset remains available during the current application session.

Always use actual tool results when answering dataset questions.

Provide clean, concise, professional answers.

Do not expose internal tool output unnecessarily.

When a tool returns a result, summarize it clearly for the user.
"""


# ============================================================
# PROMPT
# ============================================================

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            AGENT_SYSTEM_PROMPT,
        ),

        MessagesPlaceholder(
            variable_name="chat_history",
        ),

        (
            "human",
            "{question}",
        ),

        MessagesPlaceholder(
            variable_name="agent_scratchpad",
        ),
    ]
)


# ============================================================
# CREATE AGENT
# ============================================================

analyst_agent = create_tool_calling_agent(
    llm,
    ANALYST_TOOLS,
    agent_prompt,
)


# ============================================================
# AGENT EXECUTOR
# ============================================================

analyst_agent_executor = AgentExecutor(
    agent=analyst_agent,
    tools=ANALYST_TOOLS,
    verbose=True,
    handle_parsing_errors=True,
)


# ============================================================
# RESPONSE CLEANER
# ============================================================

def extract_text(response):
    """Extract clean text from Gemini responses."""

    if isinstance(response, str):
        return response

    if isinstance(response, list):
        text_parts = []

        for item in response:
            if isinstance(item, dict):

                # Gemini text block
                if item.get("type") == "text":
                    text_parts.append(
                        item.get("text", "")
                    )

                # Fallback
                elif "text" in item:
                    text_parts.append(
                        str(item["text"])
                    )

            elif isinstance(item, str):
                text_parts.append(item)

        return "".join(text_parts).strip()

    return str(response)

# ============================================================
# RUN ANALYST AGENT
# ============================================================
def run_analyst_agent(
    question: str,
    chat_history: list | None = None
) -> str:

    if chat_history is None:
        chat_history = []

    result = analyst_agent_executor.invoke({
        "question": question,
        "chat_history": chat_history,
    })

    return extract_text(result["output"])