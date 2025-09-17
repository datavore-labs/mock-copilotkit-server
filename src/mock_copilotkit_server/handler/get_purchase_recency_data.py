import logging
from typing import Any

import polars as pl
from pydantic import BaseModel, computed_field

from mock_copilotkit_server.client.bigquery_client import (
    find_and_filter_to_largest_match_category,
    get_bigquery_client,
    read_in_table,
)
from mock_copilotkit_server.client.mock_data_client import (
    get_mock_purchase_recency_data,
)
from mock_copilotkit_server.config import config
from mock_copilotkit_server.service import log_params, log_result

logger = logging.getLogger(__name__)

client = get_bigquery_client(config.bigquery_project_id)


class PurchaseRecencyData(BaseModel):
    data: list[dict]
    category: str
    chart_type: str = "purchase_recency"
    title: str = "Purchase Recency Distribution"

    @computed_field
    @property
    def description(self) -> str:
        return (
            f"Analysis of consumers who purchased {self.category} in the "
            "last 30 days and their purchase recency distribution."
        )

    @computed_field
    @property
    def total_consumers(self) -> int:
        return sum([item["count"] for item in self.data])

    def log(self) -> "PurchaseRecencyData":
        log_result(self)
        return self


def get_live_purchase_recency_data(category: str) -> list[dict[str, str | int | float]]:
    df_purchase_recency = read_in_table(client, "purchase_recency_20250724")

    data_filtered = find_and_filter_to_largest_match_category(df_purchase_recency, category)

    df_to_return = data_filtered.select(
        [
            pl.col("total_records").alias("count"),
            pl.col("category_percentage").alias("percentage"),
            pl.col("recency_period").alias("period"),
        ]
    )

    if config.debug:
        print("Live purchase recency data:")
        print(f"{category=}")
        print(df_to_return)

    return df_to_return.to_dicts()


def get_purchase_recency_data(category: str) -> list[dict[str, str | int | float]]:
    if config.use_live_data:
        return get_live_purchase_recency_data(category)
    else:
        return get_mock_purchase_recency_data(category)


# Action handlers
def handle_get_purchase_recency_data(category: str) -> dict[str, Any]:
    log_params("getPurchaseRecencyData", {"category": category})
    try:
        data = get_purchase_recency_data(category)

        result = PurchaseRecencyData(
            data=data,
            category=category,
        )

        return result.log().model_dump()
    except Exception as e:
        logger.error(
            f"❌ [BACKEND ACTION] Error in getPurchaseRecencyData: {e!s}",
            stack_info=True,
        )
        raise
