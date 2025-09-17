"""Service file for interacting with BigQuery."""

# https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.query.ScalarQueryParameterType
# Use the query params provided by the sdk library.

from pathlib import Path

import polars as pl
from google.cloud import bigquery

from mock_copilotkit_server.config import config


def get_bigquery_client(project_id: str) -> bigquery.Client:
    """Get a BigQuery client.

    Uses credentials from GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    return bigquery.Client(project=project_id)


########################################################
# Polars functions for handling local data.
########################################################


# TODO - use data store environment variable to resolve path.
def resolve_table_path(table_name: str) -> Path:
    """Resolve the path to a table file relative to this package.

    Args:
        table_name: The name of the table (without df_ prefix and .parquet extension)

    Returns:
        Path to the parquet file
    """
    # Get the directory where this module is located
    module_dir = Path(__file__).parent.parent
    # Navigate to the stores directory from the package root
    f = module_dir / "stores" / f"df_{table_name}.parquet"

    if not f.parent.exists():
        f.parent.mkdir(parents=True, exist_ok=True)

    return f


def read_in_table(table_name: str) -> pl.DataFrame:
    path = resolve_table_path(table_name)

    if not path.exists():
        client = get_bigquery_client(config.bigquery_project_id)
        table = client.query_and_wait(
            f"SELECT * FROM `audience-builder-tintash.retail_transactions_enhanced.{table_name}`"
        )
        df = pl.from_pandas(table.to_dataframe())
        df.write_parquet(path)

    return pl.read_parquet(path)


# TODO - refactor to store value of category across request (all actions).
def find_and_filter_to_largest_match_category(df: pl.DataFrame, category: str) -> pl.DataFrame:
    data = filter_to_category_str_matches(df, category)
    filtered_category = filter_category_by_largest(data)
    return filter_to_category_str_matches(data, filtered_category, exact_match=True)


def filter_to_category_str_matches(
    df_category_summary: pl.DataFrame, category: str, exact_match: bool = False
) -> pl.DataFrame:
    return df_category_summary.filter(
        pl.col("category").str.to_lowercase().str.contains(category.lower())
        if not exact_match
        else pl.col("category").str.to_lowercase() == category.lower()
    )


def filter_category_by_largest(df: pl.DataFrame) -> str:
    return (
        df.group_by("category")
        .agg(pl.col("total_records").sum())
        .sort("total_records", descending=False)
        .tail(1)["category"]
        .item()
    )


def find_largest_n_brands_by_category(df: pl.DataFrame, n: int) -> list[str]:
    return (
        df.group_by(["category", "brand"])
        .agg(pl.col("total_records").sum())
        .sort("total_records", descending=False)
        .tail(n)["brand"]
        .to_list()
    )
