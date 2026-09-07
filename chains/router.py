from agents.analyst_agent import run_analyst_agent

from chains.sql_chain import create_sql_chain
from chains.python_chain import create_python_chain
from chains.kpi_chain import create_kpi_chain


# =====================================
# DETECT INTENT
# =====================================

def detect_intent(question: str) -> str:

    question = question.lower()


    # ---------------------------------
    # ANALYST / DATASET INTENT
    # ---------------------------------

    analyst_keywords = [
        "dataset",
        "data",
        "load",
        "region",
        "product",
        "category",
        "sales data",
        "available",
        "summary of",
        "missing values",
        "average sales",
        "total sales",
        "highest sales",
        "lowest sales",
        "filter",
        "records",
        "rows",
    ]


    if any(keyword in question for keyword in analyst_keywords):
        return "analyst"


    # ---------------------------------
    # SQL INTENT
    # ---------------------------------

    sql_keywords = [
        "sql",
        "select",
        "join",
        "query",
        "database",
        "mysql",
        "postgresql",
        "table",
        "cte",
        "window function",
    ]

    if any(keyword in question for keyword in sql_keywords):
        return "sql"


    # ---------------------------------
    # PYTHON INTENT
    # ---------------------------------

    python_keywords = [
        "python",
        "pandas",
        "numpy",
        "dataframe",
        "matplotlib",
        "seaborn",
        "python code",
        "script",
    ]

    if any(keyword in question for keyword in python_keywords):
        return "python"


    # ---------------------------------
    # KPI INTENT
    # ---------------------------------

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

    if any(keyword in question for keyword in kpi_keywords):
        return "kpi"


    # Default
    return "analyst"


# =====================================
# GET CHAIN
# =====================================

def get_chain(intent: str):

    if intent == "sql":
        return create_sql_chain()

    elif intent == "python":
        return create_python_chain()

    elif intent == "kpi":
        return create_kpi_chain()

    return None