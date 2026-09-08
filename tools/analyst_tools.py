import os
import pandas as pd

from langchain_core.tools import tool


# ============================================================
# DATASET STATE
# ============================================================

_state = {
    "df": None,
    "path": None,
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_dataframe():
    """
    Return the currently loaded DataFrame.
    """

    return _state.get("df")


def find_column_name(column_name: str):
    """
    Find a column name case-insensitively.
    """

    df = get_dataframe()

    if df is None:
        return None

    # Exact match
    if column_name in df.columns:
        return column_name

    return next(
        (
            column
            for column in df.columns # pyright: ignore[reportGeneralTypeIssues]
            if column.lower() == column_name.lower()
        ),
        None,
    )


# ============================================================
# LOAD DATASET
# ============================================================

@tool
def load_dataset(file_path: str) -> str:
    """
    Load a CSV, XLSX, or XLS dataset into memory.

    Supported formats:
    - CSV
    - XLSX
    - XLS
    """

    try:

        if not os.path.exists(file_path):

            return (
                f"File not found: '{file_path}'.\n"
                "Please provide a valid file path."
            )

        file_extension = os.path.splitext(
            file_path
        )[1].lower()

        # Load CSV
        if file_extension == ".csv":

            df = pd.read_csv(file_path)

        # Load Excel
        elif file_extension in [".xlsx", ".xls"]:

            df = pd.read_excel(file_path)

        else:

            return (
                f"Unsupported file format: '{file_extension}'.\n"
                "Supported formats: CSV, XLSX, XLS."
            )

        # Store dataset
        _state["df"] = df # pyright: ignore[reportArgumentType]
        _state["path"] = file_path # pyright: ignore[reportArgumentType]

        return (
            "Dataset loaded successfully.\n\n"
            f"File: {file_path}\n"
            f"Rows: {df.shape[0]}\n"
            f"Columns: {df.shape[1]}\n\n"
            f"Column Names:\n"
            f"{list(df.columns)}"
        )

    except Exception as error:

        return (
            f"Failed to load dataset.\n"
            f"Error: {str(error)}"
        )


# ============================================================
# DATASET STATUS
# ============================================================

@tool
def get_dataset_status() -> str:
    """
    Check whether a dataset is currently loaded.
    """

    df = get_dataframe()

    if df is None:

        return (
            "No dataset loaded. "
            "Call load_dataset first."
        )

    return (
        "Dataset is currently loaded.\n\n"
        f"File: {_state['path']}\n"
        f"Rows: {df.shape[0]}\n"
        f"Columns: {df.shape[1]}"
    )


# ============================================================
# DATA SUMMARY
# ============================================================

@tool
def get_data_summary() -> str:
    """
    Return a comprehensive summary of the currently loaded dataset.

    Includes:
    - Shape
    - Columns
    - Data types
    - Missing values
    - Duplicate rows
    - Numeric statistics
    """

    df = get_dataframe()

    if df is None:

        return (
            "No dataset loaded. "
            "Call load_dataset first."
        )

    missing_values = df.isnull().sum()

    duplicate_rows = df.duplicated().sum()

    numeric_df = df.select_dtypes(
        include="number"
    )

    summary = f"""
DATASET OVERVIEW
----------------
File: {_state["path"]}

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

    if not numeric_df.empty:

        summary += (
            "\n"
            + numeric_df.describe().to_string()
        )

    else:

        summary += (
            "\nNo numeric columns found."
        )

    return summary


# ============================================================
# DATASET PREVIEW
# ============================================================

@tool
def get_dataset_preview(n: int = 10) -> str:
    """
    Return the first n rows of the dataset.

    Default: 10 rows
    Maximum: 50 rows
    """

    df = get_dataframe()

    if df is None:

        return (
            "No dataset loaded. "
            "Call load_dataset first."
        )

    # Prevent extremely large output
    n = max(1, min(n, 50))

    return (
        f"Dataset Preview "
        f"(First {n} Rows)\n\n"
        + df.head(n).to_string(index=False)
    )


# ============================================================
# COLUMN VALUES
# ============================================================

@tool
def get_column_values(
    column_name: str,
    n: int = 20
) -> str:
    """
    Return information about a column including:

    - Data type
    - Missing values
    - Unique values
    - Sample values

    Column matching is case-insensitive.
    """

    df = get_dataframe()

    if df is None:

        return (
            "No dataset loaded. "
            "Call load_dataset first."
        )

    actual_column = find_column_name(
        column_name
    )

    if actual_column is None:

        return (
            f"Column '{column_name}' not found.\n\n"
            f"Available columns:\n"
            f"{list(df.columns)}"
        )

    column = df[actual_column]

    unique_values = (
        column
        .dropna()
        .unique()
    )

    n = max(1, min(n, 100))

    sample_values = list(
        unique_values[:n]
    )

    return (
        f"Column: {actual_column}\n"
        f"Data Type: {column.dtype}\n"
        f"Missing Values: "
        f"{column.isnull().sum()}\n"
        f"Unique Values: "
        f"{column.nunique()}\n\n"
        f"Values:\n"
        f"{sample_values}"
    )


# ============================================================
# PANDAS QUERY
# ============================================================

@tool
def run_pandas_query(query: str) -> str:
    """
    Filter the dataset using pandas DataFrame.query() syntax.

    Examples:

    region == 'West'

    sales > 1000

    region == 'West' and sales > 1000

    Returns up to 50 matching rows.
    """

    df = get_dataframe()

    if df is None:

        return (
            "No dataset loaded. "
            "Call load_dataset first."
        )

    try:

        result = df.query(query)

        if result.empty:

            return (
                "No rows matched the query."
            )

        return (
            f"Query successful.\n"
            f"Matching Rows: {len(result)}\n\n"
            f"{result.head(50).to_string(index=False)}"
        )

    except Exception as error:

        return (
            "Query failed.\n"
            f"Query: {query}\n"
            f"Error: {str(error)}\n\n"
            f"Available columns: "
            f"{list(df.columns)}"
        )


# ============================================================
# CALCULATE AGGREGATE
# ============================================================

@tool
def calculate_aggregate(
    column: str,
    operation: str,
    group_by: str = ""
) -> str:
    """
    Calculate an aggregate for a numeric column.

    Supported operations:

    - sum
    - mean
    - median
    - min
    - max
    - count
    - std

    Optionally group the result by another column.

    Examples:

    calculate total sales:
    column="sales", operation="sum"

    calculate sales by region:
    column="sales",
    operation="sum",
    group_by="region"
    """

    df = get_dataframe()

    if df is None:

        return (
            "No dataset loaded. "
            "Call load_dataset first."
        )

    actual_column = find_column_name(
        column
    )

    if actual_column is None:

        return (
            f"Column '{column}' not found.\n"
            f"Available columns: "
            f"{list(df.columns)}"
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

    operation = operation.lower().strip()

    if operation not in valid_operations:

        return (
            f"Invalid operation: '{operation}'.\n\n"
            f"Supported operations:\n"
            f"{valid_operations}"
        )

    try:

        # GROUP BY
        if group_by:

            actual_group_by = find_column_name(
                group_by
            )

            if actual_group_by is None:

                return (
                    f"Group-by column "
                    f"'{group_by}' not found.\n\n"
                    f"Available columns:\n"
                    f"{list(df.columns)}"
                )

            result = (
                df
                .groupby(actual_group_by)[
                    actual_column
                ]
                .agg(operation)
                .sort_values(
                    ascending=False
                )
            )

            return (
                f"{operation.upper()} of "
                f"'{actual_column}' "
                f"by '{actual_group_by}'\n\n"
                f"{result.to_string()}"
            )

        # NORMAL AGGREGATE
        result = (
            df[actual_column]
            .agg(operation)
        )

        return (
            f"{operation.upper()} of "
            f"'{actual_column}': {result}"
        )

    except Exception as error:

        return (
            "Aggregation failed.\n"
            f"Error: {str(error)}"
        )


# ============================================================
# TOP / BOTTOM VALUES
# ============================================================

@tool
def get_top_values(
    column: str,
    n: int = 5,
    ascending: bool = False
) -> str:
    """
    Return the top or bottom rows based on a column.

    Examples:

    Top 5 sales:
    column="sales", n=5, ascending=False

    Lowest 5 sales:
    column="sales", n=5, ascending=True
    """

    df = get_dataframe()

    if df is None:

        return (
            "No dataset loaded. "
            "Call load_dataset first."
        )

    actual_column = find_column_name(
        column
    )

    if actual_column is None:

        return (
            f"Column '{column}' not found.\n"
            f"Available columns: "
            f"{list(df.columns)}"
        )

    try:

        n = max(1, min(n, 50))

        result = (
            df
            .sort_values(
                by=actual_column,
                ascending=ascending
            )
            .head(n)
        )

        label = (
            "Lowest"
            if ascending
            else "Top"
        )

        return (
            f"{label} {n} rows by "
            f"'{actual_column}'\n\n"
            f"{result.to_string(index=False)}"
        )

    except Exception as error:

        return (
            "Sorting failed.\n"
            f"Error: {str(error)}"
        )


# ============================================================
# DATASET TOOLS
# ============================================================

ANALYST_TOOLS = [

    # Dataset management
    load_dataset,
    get_dataset_status,

    # Dataset understanding
    get_data_summary,
    get_dataset_preview,
    get_column_values,

    # Analysis
    run_pandas_query,
    calculate_aggregate,
    get_top_values,
]