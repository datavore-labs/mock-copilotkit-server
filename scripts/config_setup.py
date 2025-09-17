"""Configuration for BigQuery aggregation table setup."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Dict, List


class AggregationType(StrEnum):
    """Types of aggregation tables to create."""

    CATEGORY = "ad_category_combined"
    PARENT_COMPANY = "ad_parent_company"
    BRAND = "ad_brand_name"


@dataclass
class TableConfig:
    """Configuration for a specific aggregation table."""

    # Table name suffix (e.g., ad_category_combined, ad_parent_company)
    name_suffix: str

    # Primary grouping field
    group_by_field: str

    # Additional grouping fields
    additional_group_fields: List[str] = field(default_factory=list)

    # Clustering fields
    clustering_fields: List[str] = field(default_factory=list)

    # Filter condition
    filter_condition: str = ""

    @property
    def table_name(self) -> str:
        """Get the full table name."""
        return f"ibotta_enhanced_agg_{self.name_suffix}_20250724"


@dataclass
class BigQueryConfig:
    """Configuration for BigQuery aggregation tables."""

    # Project and dataset configuration
    project_id: str = "audience-builder-tintash"
    dataset_id: str = "retail_transactions_enhanced"
    source_table: str = "ibotta_enhanced_20250724"

    # Base name for aggregation tables
    base_agg_name: str = "ibotta_enhanced_agg"

    # Date suffix
    date_suffix: str = "20250724"

    # Table configurations
    table_configs: Dict[AggregationType, TableConfig] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize default table configurations if not provided."""
        if not self.table_configs:
            self.table_configs = {
                AggregationType.CATEGORY: TableConfig(
                    name_suffix="ad_category_combined",
                    group_by_field="AD_CATEGORY_COMBINED",
                    additional_group_fields=["MIN_PURCHASE_DATE"],
                    clustering_fields=[
                        "AD_CATEGORY_COMBINED",
                        "AD_BRAND_NAME",
                    ],
                    filter_condition="AD_CATEGORY_COMBINED IS NOT NULL",
                ),
                AggregationType.PARENT_COMPANY: TableConfig(
                    name_suffix="ad_parent_company",
                    group_by_field="AD_PARENT_COMPANY",
                    additional_group_fields=["MIN_PURCHASE_DATE"],
                    clustering_fields=[
                        "AD_PARENT_COMPANY",
                        "AD_CATEGORY_COMBINED",
                    ],
                    filter_condition="AD_PARENT_COMPANY IS NOT NULL",
                ),
                AggregationType.BRAND: TableConfig(
                    name_suffix="ad_brand_name",
                    group_by_field="AD_BRAND_NAME",
                    additional_group_fields=["MIN_PURCHASE_DATE"],
                    clustering_fields=[
                        "AD_BRAND_NAME",
                        "AD_CATEGORY_COMBINED",
                    ],
                    filter_condition="AD_BRAND_NAME IS NOT NULL",
                ),
            }

    def get_table_names(self) -> List[str]:
        """Get all table names."""
        return [config.table_name for config in self.table_configs.values()]

    def get_table_config(self, agg_type: AggregationType) -> TableConfig:
        """Get configuration for a specific aggregation type."""
        return self.table_configs[agg_type]


# Default configuration
DEFAULT_CONFIG = BigQueryConfig()
