"""Service file for interacting with BigQuery."""

# https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.query.ScalarQueryParameterType
# Use the query params provided by the sdk library.

import os

import polars as pl
from google.cloud import bigquery


# TODO - add credentials to bigquery client otherwise will fallback to
# environment, which will fail on a non-local machine.
def get_bigquery_client(project_id: str) -> bigquery.Client:
    """Get a BigQuery client."""
    return bigquery.Client(project=project_id)


########################################################
# Polars functions for handling local data.
########################################################


def read_in_table(client: bigquery.Client, table_name: str) -> pl.DataFrame:
    if not os.path.exists(f"stores/df_{table_name}.parquet"):
        table = client.query_and_wait(
            f"SELECT * FROM `audience-builder-tintash.retail_transactions_enhanced.{table_name}`"
        )
        df = pl.from_pandas(table.to_dataframe())
        df.write_parquet(f"stores/df_{table_name}.parquet")

    return pl.read_parquet(f"stores/df_{table_name}.parquet")


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
