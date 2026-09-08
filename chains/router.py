from agents.analyst_agent import run_analyst_agent
from agents.sql_agent import run_sql_agent
from agents.python_agent import run_python_agent
from agents.kpi_agent import run_kpi_agent


def detect_intent(question: str) -> str:

    question = question.lower()

    # SQL
    sql_keywords = [
        "sql",
        "select",
        "join",
        "database",
        "mysql",
        "postgresql",
        "query",
        "cte",
        "window function",
    ]

    # Python
    python_keywords = [
        "python",
        "pandas",
        "numpy",
        "dataframe",
        "matplotlib",
        "seaborn",
        "python code",
    ]

    if any(keyword in question for keyword in sql_keywords):
        return "sql"

    if any(keyword in question for keyword in python_keywords):
        return "python"

    # KPI / Dashboard
    kpi_keywords = [
        "kpi",
        "dashboard",
        "power bi",
        "tableau",
        "metric",
        "visualization",
        "chart",
        "business performance",
    ]

    return (
        "kpi"
        if any(keyword in question for keyword in kpi_keywords)
        else "analyst"
    )


def route_question(question: str):

    intent = detect_intent(question)

    if intent == "sql":

        response = run_sql_agent(question)

    elif intent == "python":

        response = run_python_agent(question)

    elif intent == "kpi":

        response = run_kpi_agent(question)

    else:

        response = run_analyst_agent(question)

    return intent, response