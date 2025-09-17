import logging
from typing import Any

import polars as pl
from pydantic import BaseModel, computed_field

from mock_copilotkit_server.client.bigquery_client import (
    find_and_filter_to_largest_match_category,
    get_bigquery_client,
    read_in_table,
)
from mock_copilotkit_server.client.mock_data_client import get_mock_spending_data
from mock_copilotkit_server.config import config
from mock_copilotkit_server.service import log_params, log_result

logger = logging.getLogger(__name__)

client = get_bigquery_client(config.bigquery_project_id)


class SpendingData(BaseModel):
    data: list[dict]
    category: str
    selected_brands: list[str]
    chart_type: str = "spending_distribution"
    title: str = "Spending Distribution (Last 30 Days)"

    @computed_field
    @property
    def description(self) -> str:
        return f"Spending patterns for {self.category} consumers in the selected audience."

    def log(self) -> "SpendingData":
        log_result(self)
        return self


def get_live_spending_data(category: str) -> list[dict[str, str | int | float]]:
    # TODO - add in live data here
    df_spending_distribution_all = read_in_table(client, "spending_distribution_20250724")

    df_spending_per_cat = find_and_filter_to_largest_match_category(df_spending_distribution_all, category)

    # Format column names before returning.
    df_to_return = df_spending_per_cat.select(
        [
            pl.col("total_records").alias("count"),
            pl.col("category_percentage").alias("percentage"),
            pl.col("spending_range").alias("range"),
        ]
    )

    if config.debug:
        print("Live spending data:")
        print(f"{category=}")
        print(df_to_return)

    return df_to_return.to_dicts()


def get_spending_data(category: str) -> list[dict[str, str | int | float]]:
    if config.use_live_data:
        return get_live_spending_data(category)
    else:
        return get_mock_spending_data(category)


def handle_get_spending_data(category: str, selected_brands: list[str]) -> dict[str, Any]:
    log_params("getSpendingData", {"category": category, "selected_brands": selected_brands})

    try:
        data = get_spending_data(category)

        result = SpendingData(
            data=data,
            category=category,
            selected_brands=selected_brands,
        )

        return result.log().model_dump()
    except Exception as e:
        logger.error(f"❌ [BACKEND ACTION] Error in getSpendingData: {e!s}", stack_info=True)
        raise
