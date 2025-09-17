#!/usr/bin/env python3
"""Setup script for creating and configuring multiple BigQuery aggregation tables."""

import logging
from pathlib import Path

from config_setup import DEFAULT_CONFIG
from google.cloud import bigquery

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use configuration from config.py
CONFIG = DEFAULT_CONFIG


def get_bigquery_client() -> bigquery.Client:
    """Get a BigQuery client."""
    return bigquery.Client(project=CONFIG.project_id)


def create_aggregation_table(client: bigquery.Client, table_name: str) -> None:
    """Create an aggregation table using SQL from create_aggregation_tables.sql."""
    table_id = f"{CONFIG.project_id}.{CONFIG.dataset_id}.{table_name}"
    logger.info(f"Creating table: {table_id}")

    # Read SQL file
    try:
        # Get the SQL script path
        sql_path = Path(__file__).parent / "create_aggregation_tables_v2.sql"

        if not sql_path.exists():
            logger.error(f"SQL file not found: {sql_path}")
            raise FileNotFoundError(f"SQL file not found: {sql_path}")

        # Read the SQL file
        sql_content = sql_path.read_text()

        # Execute the SQL script
        logger.info(f"Executing SQL script to create table {table_name}")
        query_job = client.query(sql_content)
        query_job.result()  # Wait for completion

        logger.info(f"Created table {table_id}")
    except Exception as e:
        if "Already Exists" in str(e):
            logger.info(f"Table {table_name} already exists, skipping creation")
        else:
            logger.error(f"Error creating table {table_name}: {e}")
            raise


def verify_table_creation(client: bigquery.Client, table_name: str) -> None:
    """Verify that the aggregation table was created successfully."""
    logger.info(f"Verifying table creation for {table_name}...")

    table_id = f"{CONFIG.project_id}.{CONFIG.dataset_id}.{table_name}"

    try:
        table = client.get_table(table_id)
        logger.info(f"Table verified: {table.project}.{table.dataset_id}.{table.table_id}")
        logger.info(f"Table description: {table.description}")
        logger.info(f"Partitioning: {table.time_partitioning}")
        logger.info(f"Clustering: {table.clustering_fields}")

        # Get row count
        query = f"SELECT COUNT(*) as row_count FROM `{table_id}`"
        query_job = client.query(query)
        result = query_job.result()
        row_count = next(iter(result)).row_count
        logger.info(f"Row count: {row_count:,}")

    except Exception as e:
        logger.error(f"Error verifying table {table_name}: {e}")
        raise


def process_aggregation_table(client: bigquery.Client, table_name: str) -> None:
    """Process a single aggregation table (create and verify)."""
    logger.info(f"Processing aggregation table for {table_name}...")

    # Step 1: Create and populate the aggregation table using SQL script
    create_aggregation_table(client, table_name)

    # Step 2: Verify table creation
    verify_table_creation(client, table_name)


def main():
    """Main setup function."""
    logger.info("Starting BigQuery aggregation tables setup...")

    try:
        client = get_bigquery_client()

        # Process each aggregation table type
        for agg_type in ["ad_category_combined", "ad_parent_company", "ad_brand_name"]:
            process_aggregation_table(client, agg_type)

        logger.info("Setup completed successfully!")

    except Exception as e:
        logger.error(f"Setup failed: {e}")
        raise


if __name__ == "__main__":
    main()
