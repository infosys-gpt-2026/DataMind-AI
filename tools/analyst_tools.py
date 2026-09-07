import os
import pandas as pd
from langchain_core.tools import tool


# Holds the currently loaded dataframe during the application session
_state = {
    "df": None,
    "path": None,
}


@tool
def load_dataset(file_path: str) -> str:
    """
    Load a CSV or Excel dataset into memory.

    Supported formats:
    - .csv
    - .xlsx
    - .xls
    """

    try:
        if not os.path.exists(file_path):
            return f"File not found: '{file_path}'"

        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == ".csv":
            df = pd.read_csv(file_path)

        elif file_extension in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)

        else:
            return (
                f"Unsupported file format '{file_extension}'. "
                "Supported formats are CSV, XLSX, and XLS."
            )

        _state["df"] = df # pyright: ignore[reportArgumentType]
        _state["path"] = file_path # pyright: ignore[reportArgumentType]

        return (
            f"Dataset loaded successfully.\n\n"
            f"File: {file_path}\n"
            f"Rows: {df.shape[0]}\n"
            f"Columns: {df.shape[1]}\n\n"
            f"Column Names:\n{list(df.columns)}"
        )

    except Exception as e:
        return f"Failed to load dataset: {str(e)}"


@tool
def get_data_summary() -> str:
    """
    Return a comprehensive summary of the currently loaded dataset,
    including shape, columns, data types, missing values, and duplicates.
    """

    df = _state["df"]

    if df is None:
        return "No dataset loaded. Call load_dataset first."

    missing_values = df.isnull().sum()
    duplicate_rows = df.duplicated().sum()

    summary = f"""
DATASET OVERVIEW
----------------
Shape: {df.shape[0]} rows × {df.shape[1]} columns

COLUMNS
-------
{list(df.columns)}

DATA TYPES
----------
{df.dtypes.to_string()}

MISSING VALUES
--------------
{missing_values.to_string()}

DUPLICATE ROWS
--------------
{duplicate_rows}

NUMERIC SUMMARY
---------------
"""

    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:
        summary += "\n" + numeric_df.describe().to_string()
    else:
        summary += "\nNo numeric columns found."

    return summary


@tool
def get_column_values(column_name: str, n: int = 10) -> str:
    """
    Inspect a column and return its data type, missing values,
    number of unique values, and sample unique values.
    """

    df = _state["df"]

    if df is None:
        return "No dataset loaded. Call load_dataset first."

    if column_name not in df.columns:
        return (
            f"Column '{column_name}' not found.\n"
            f"Available columns: {list(df.columns)}"
        )

    column = df[column_name]

    unique_values = column.dropna().unique()

    return (
        f"Column: {column_name}\n"
        f"Data Type: {column.dtype}\n"
        f"Missing Values: {column.isnull().sum()}\n"
        f"Unique Values: {column.nunique()}\n"
        f"Sample Values: {list(unique_values[:n])}"
    )


@tool
def run_pandas_query(query: str) -> str:
    """
    Filter the dataset using pandas DataFrame.query() syntax.

    Example:
    region == 'West' and sales > 1000

    Returns the number of matching rows and up to 20 rows.
    """

    df = _state["df"]

    if df is None:
        return "No dataset loaded. Call load_dataset first."

    try:
        result = df.query(query)

        if result.empty:
            return "No rows matched the query."

        return (
            f"{len(result)} rows matched.\n\n"
            f"{result.head(20).to_string(index=False)}"
        )

    except Exception as e:
        return f"Query failed: {str(e)}"


@tool
def calculate_aggregate(
    column: str,
    operation: str,
    group_by: str = ""
) -> str:
    """
    Calculate an aggregate on a dataset column.

    Supported operations:
    sum, mean, median, min, max, count, std

    Optionally group results by another column.
    """

    df = _state["df"]

    if df is None:
        return "No dataset loaded. Call load_dataset first."

    if column not in df.columns:
        return (
            f"Column '{column}' not found.\n"
            f"Available columns: {list(df.columns)}"
        )

    valid_operations = [
        "sum",
        "mean",
        "median",
        "min",
        "max",
        "count",
        "std",
    ]

    operation = operation.lower()

    if operation not in valid_operations:
        return (
            f"Invalid operation '{operation}'.\n"
            f"Supported operations: {valid_operations}"
        )

    try:

        if group_by:

            if group_by not in df.columns:
                return (
                    f"Group-by column '{group_by}' not found.\n"
                    f"Available columns: {list(df.columns)}"
                )

            result = (
                df.groupby(group_by)[column]
                .agg(operation)
                .sort_values(ascending=False)
            )

            return result.to_string()

        result = df[column].agg(operation)

        return (
            f"{operation.upper()} of '{column}': {result}"
        )

    except Exception as e:
        return f"Aggregation failed: {str(e)}"


@tool
def get_dataset_preview(n: int = 10) -> str:
    """
    Return the first n rows of the currently loaded dataset.
    """

    df = _state["df"]

    if df is None:
        return "No dataset loaded. Call load_dataset first."

    return df.head(n).to_string(index=False)


ANALYST_TOOLS = [
    load_dataset,
    get_data_summary,
    get_dataset_preview,
    get_column_values,
    run_pandas_query,
    calculate_aggregate,
]