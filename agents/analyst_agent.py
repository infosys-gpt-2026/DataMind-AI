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

def extract_text(response) -> str:
    """
    Convert Gemini/LangChain response formats
    into a clean text string.
    """

    # Normal string
    if isinstance(response, str):
        return response.strip()

    # Gemini may return a list of content blocks
    if isinstance(response, list):

        text_parts = []

        for item in response:

            if isinstance(item, dict):

                if "text" in item:
                    text_parts.append(
                        str(item["text"])
                    )

                elif "content" in item:
                    text_parts.append(
                        extract_text(item["content"])
                    )

            elif isinstance(item, str):
                text_parts.append(item)

            else:
                text_parts.append(str(item))

        return "\n".join(text_parts).strip()

    # Dictionary response
    if isinstance(response, dict):

        if "text" in response:
            return str(response["text"]).strip()

        if "content" in response:
            return extract_text(response["content"])

        if "output" in response:
            return extract_text(response["output"])

    # AIMessage or similar LangChain object
    if hasattr(response, "content"):
        return extract_text(response.content) # pyright: ignore[reportAttributeAccessIssue]

    # Fallback
    return str(response).strip()


# ============================================================
# RUN ANALYST AGENT
# ============================================================

def run_analyst_agent(question: str, chat_history: list | None = None) -> str:
    """
    Run the Data Analyst agent and return a clean response.

    chat_history lets the agent remember earlier turns in the same session
    (e.g. so a dataset loaded on turn 1 is still known about on turn 2).
    Pass the same list back in on each call and it will be extended by
    the caller (see main.py).
    """

    result = analyst_agent_executor.invoke(
        {
            "question": question,
            "chat_history": chat_history or [],
        }
    )

    response = result.get("output", "")

    return extract_text(response)