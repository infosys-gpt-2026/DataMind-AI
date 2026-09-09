from agents.analyst_agent import run_analyst_agent
from agents.sql_agent import run_sql_agent
from agents.python_agent import run_python_agent
from agents.kpi_agent import run_kpi_agent

from services.langbase_service import LangbaseService

from utils.response_formatter import clean_response


def detect_intent(question: str) -> str:
    """
    Detect the appropriate execution path for a user question.

    Routing priority:
    1. SQL
    2. Python / Pandas
    3. KPI / Dashboard
    4. Dataset / Data Analysis
    5. General AI / Conceptual → Langbase
    6. Default → Analyst
    """

    question_lower = question.lower().strip()

    # =========================================================
    # 1. SQL
    # =========================================================

    sql_keywords = [
        "sql",
        "select",
        "join",
        "database",
        "group by",
        "window function",
        "having clause",
        "subquery",
        "cte",
        "common table expression",
    ]

    if any(keyword in question_lower for keyword in sql_keywords):
        return "sql"

    # =========================================================
    # 2. Python / Pandas
    # =========================================================

    python_keywords = [
        "python",
        "pandas",
        "numpy",
        "dataframe",
        "python code",
        "pandas code",
        "write code",
        "code to",
    ]

    if any(keyword in question_lower for keyword in python_keywords):
        return "python"

    # =========================================================
    # 3. KPI / Dashboard
    # =========================================================

    kpi_keywords = [
        "kpi",
        "key performance indicator",
        "what should i track",
        "dashboard metrics",
        "sales dashboard",
        "business metrics",
        "performance metrics",
    ]

    if any(keyword in question_lower for keyword in kpi_keywords):
        return "kpi"

    # =========================================================
    # 4. Dataset / Data Analysis
    #
    # IMPORTANT:
    # Do NOT use generic words such as "what are",
    # "revenue", or "profit" alone here.
    #
    # This prevents conceptual questions such as:
    # "What is the difference between revenue and profit?"
    # from being incorrectly routed to the Analyst Agent.
    # =========================================================

    analyst_keywords = [
        # Dataset references
        "dataset",
        "dataframe",
        "data set",
        "sample_sales.csv",

        # Dataset structure
        "rows",
        "columns",
        "records",
        "transactions",
        "missing values",
        "null values",
        "duplicates",
        "duplicate rows",

        # Analytical operations
        "total sales",
        "total revenue",
        "total profit",
        "total margin",
        "sum of sales",
        "sum of revenue",
        "average sales",
        "average revenue",
        "average units",
        "mean sales",
        "mean revenue",
        "count of",
        "highest sales",
        "lowest sales",
        "maximum sales",
        "minimum sales",
        "top selling",
        "best selling",
        "worst selling",

        # Grouping / breakdown
        "by region",
        "by product",
        "by category",
        "by date",
        "by month",
        "by year",
        "by channel",
        "regional breakdown",
        "product breakdown",
        "sales breakdown",

        # Filtering / analysis
        "filter the data",
        "filter the dataset",
        "analyze the dataset",
        "analyse the dataset",
        "analyze the data",
        "analyse the data",
        "calculate from the dataset",
        "calculate from the data",
        "in the dataset",
        "from the dataset",
        "in this dataset",
        "from this dataset",

        # Dataset loading
        "load the dataset",
        "load the data",
        "load csv",
        "load the csv",
    ]

    if any(keyword in question_lower for keyword in analyst_keywords):
        return "analyst"

    # =========================================================
    # 5. Langbase / General AI / Conceptual Questions
    # =========================================================

    langbase_keywords = [
        "explain",
        "difference between",
        "what is",
        "why is",
        "why are",
        "how does",
        "how do",
        "how can",
        "concept",
        "definition",
        "meaning",
        "best practice",
        "best practices",
        "recommend",
        "recommendation",
        "advice",
        "strategy",
        "strategies",
        "architecture",
        "rag",
        "llm",
        "generative ai",
        "genai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
    ]

    if any(keyword in question_lower for keyword in langbase_keywords):
        return "langbase"

    # =========================================================
    # 6. Default → Analyst Agent
    # =========================================================

    return "analyst"


def route_question(
    question: str,
    chat_history: list | None = None
):
    """
    Route the question to the appropriate AI agent/service.
    """

    if chat_history is None:
        chat_history = []

    intent = detect_intent(question)

    # =========================================================
    # SQL Agent
    # =========================================================

    if intent == "sql":
        response = run_sql_agent(
            question,
            chat_history=chat_history
        )

    # =========================================================
    # Python Agent
    # =========================================================

    elif intent == "python":
        response = run_python_agent(
            question,
            chat_history=chat_history
        )

    # =========================================================
    # KPI Agent
    # =========================================================

    elif intent == "kpi":
        response = run_kpi_agent(
            question,
            chat_history=chat_history
        )

    # =========================================================
    # Langbase
    # =========================================================

    elif intent == "langbase":
        langbase_service = LangbaseService()

        response = langbase_service.ask(question)

    # =========================================================
    # Analyst Agent
    # =========================================================

    else:
        response = run_analyst_agent(
            question,
            chat_history=chat_history
        )

    # =========================================================
    # Clean Response
    # =========================================================

    cleaned_response = clean_response(response)

    return intent, cleaned_response