import pandas as pd # pyright: ignore[reportMissingModuleSource]
from langchain_core.tools import tool

# Holds the currently loaded dataframe between tool calls in a session
_state = {"df": None, "path": None}


@tool
def load_dataset(file_path: str) -> str:
    """Load a CSV file into memory for analysis. Provide a full or relative path to a .csv file."""
    try:
        df = pd.read_csv(file_path)
        _state["df"] = df # pyright: ignore[reportArgumentType]
        _state["path"] = file_path # pyright: ignore[reportArgumentType]
        return (
            f"Loaded '{file_path}' successfully. "
            f"Shape: {df.shape[0]} rows x {df.shape[1]} columns. "
            f"Columns: {list(df.columns)}"
        )
    except Exception as e:
        return f"Failed to load '{file_path}': {e}"


@tool
def get_data_summary() -> str:
    """Return shape, dtypes, missing-value counts, and numeric summary stats for the loaded dataset."""
    df = _state["df"]
    if df is None:
        return "No dataset loaded. Call load_dataset first."
    parts = [
        f"Shape: {df.shape}",
        "\nColumn dtypes:\n" + df.dtypes.to_string(),
        "\nMissing values per column:\n" + df.isnull().sum().to_string(),
        "\nNumeric summary:\n" + df.describe(include="number").to_string(),
    ]
    return "\n".join(parts)


@tool
def get_column_values(column_name: str, n: int = 5) -> str:
    """Return up to n sample unique values from a column — useful for checking categories before filtering."""
    df = _state["df"]
    if df is None:
        return "No dataset loaded. Call load_dataset first."
    if column_name not in df.columns:
        return f"Column '{column_name}' not found. Available columns: {list(df.columns)}"
    values = df[column_name].dropna().unique()[:n]
    return f"Sample values from '{column_name}': {list(values)}"


@tool
def run_pandas_query(query: str) -> str:
    """
    Filter the loaded dataset using pandas DataFrame.query() syntax,
    e.g. "region == 'West' and sales > 1000". Returns row count and up to 20 matching rows.
    """
    df = _state["df"]
    if df is None:
        return "No dataset loaded. Call load_dataset first."
    try:
        result = df.query(query)
        return f"{len(result)} rows matched.\n\n{result.head(20).to_string()}"
    except Exception as e:
        return f"Query failed: {e}"


@tool
def calculate_aggregate(column: str, operation: str, group_by: str = "") -> str:
    """
    Calculate an aggregate on a numeric column. operation must be one of:
    sum, mean, median, min, max, count, std.
    Optionally pass group_by to break the result down by another column's categories.
    """
    df = _state["df"]
    if df is None:
        return "No dataset loaded. Call load_dataset first."
    if column not in df.columns:
        return f"Column '{column}' not found. Available columns: {list(df.columns)}"
    valid_ops = ["sum", "mean", "median", "min", "max", "count", "std"]
    if operation not in valid_ops:
        return f"Invalid operation '{operation}'. Must be one of {valid_ops}"
    try:
        if group_by:
            if group_by not in df.columns:
                return f"Group-by column '{group_by}' not found. Available columns: {list(df.columns)}"
            result = getattr(df.groupby(group_by)[column], operation)()
            return result.to_string()
        return str(getattr(df[column], operation)())
    except Exception as e:
        return f"Aggregation failed: {e}"


ANALYST_TOOLS = [
    load_dataset,
    get_data_summary,
    get_column_values,
    run_pandas_query,
    calculate_aggregate,
]