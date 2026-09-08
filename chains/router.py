from agents.analyst_agent import run_analyst_agent
from agents.sql_agent import run_sql_agent
from agents.python_agent import run_python_agent
from agents.kpi_agent import run_kpi_agent

from utils.response_formatter import clean_response


def detect_intent(question: str) -> str:
    """
    Detect which agent should handle the user's question.
    """

    question_lower = question.lower()

    sql_keywords = [
        "sql", "select", "join", "query", "database", "table",
        "group by", "window function",
    ]

    python_keywords = [
        "python", "pandas", "numpy", "dataframe", "code",
    ]

    if any(keyword in question_lower for keyword in sql_keywords):
        return "sql"

    if any(keyword in question_lower for keyword in python_keywords):
        return "python"

    kpi_keywords = [
        "kpi", "key performance indicator", "metrics",
        "what should i track", "dashboard metrics",
    ]

    return (
        "kpi"
        if any(keyword in question_lower for keyword in kpi_keywords)
        else "analyst"
    )


def route_question(question: str, chat_history: list | None = None):
    """
    Route the question to the correct AI agent.
    """

    intent = detect_intent(question)

    if intent == "sql":
        response = run_sql_agent(question)
    elif intent == "python":
        response = run_python_agent(question)
    elif intent == "kpi":
        response = run_kpi_agent(question)
    else:
        response = run_analyst_agent(question, chat_history=chat_history)

    cleaned_response = clean_response(response)

    return intent, cleaned_response