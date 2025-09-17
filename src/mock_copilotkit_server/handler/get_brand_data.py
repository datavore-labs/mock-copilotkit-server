import logging
from typing import Any

import polars as pl
from pydantic import BaseModel, computed_field

from mock_copilotkit_server.client.bigquery_client import (
    find_and_filter_to_largest_match_category,
    find_largest_n_brands_by_category,
    read_in_table,
)
from mock_copilotkit_server.client.mock_data_client import get_mock_brand_data
from mock_copilotkit_server.config import config
from mock_copilotkit_server.service import log_params, log_result

logger = logging.getLogger(__name__)


class BrandData(BaseModel):
    data: list[dict]
    category: str
    selected_recency: str
    chart_type: str = "brand_breakdown"

    @computed_field
    @property
    def title(self) -> str:
        return f"{self.category.title()} Brand Breakdown"

    @computed_field
    @property
    def description(self) -> str:
        return f"Brand distribution for {self.category} consumers in the selected audience."

    def log(self) -> "BrandData":
        log_result(self)
        return self


def get_live_brand_data(category: str) -> list[dict[str, str | int | float]]:
    df_brand_perf = read_in_table("brand_performance_by_category_20250724")
    df_cat_match = find_and_filter_to_largest_match_category(df_brand_perf, category)
    top_10_brands = find_largest_n_brands_by_category(df_cat_match, 10)

    df_to_return = df_cat_match.filter(pl.col("brand").is_in(top_10_brands)).select(
        [
            pl.col("brand").alias("brand"),
            pl.col("total_records").alias("count"),
            pl.col("category_percentage").alias("percentage"),
        ]
    )

    if config.debug:
        print("Live brand data:")
        print(f"{category=}")
        print(df_to_return)

    return df_to_return.to_dicts()


def get_brand_data(category: str) -> list[dict[str, str | int | float]]:
    if config.use_live_data:
        return get_live_brand_data(category)
    else:
        return get_mock_brand_data(category)


def handle_get_brand_data(category: str, selected_recency: str) -> dict[str, Any]:
    log_params("getBrandData", {"category": category, "selected_recency": selected_recency})

    try:
        data = get_brand_data(category)

        result = BrandData(
            data=data,
            category=category,
            selected_recency=selected_recency,
        )

        return result.log().model_dump()

    except Exception as e:
        logger.error(f"❌ [BACKEND ACTION] Error in getBrandData: {e!s}", stack_info=True)
        raise
