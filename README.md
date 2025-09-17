Mock copilot server using the copilotkit framework.

- Ignoring type checks + pyright errors for time being, can add those later on.

To Do:

1. Setup machine credentials for Bigquery connection.
2. Get schema input/output for brand graph, add empty code within service flow.


Data stores:

The aggregated data tables are stored locally in parquet files.
These are static, but if they don't exist, will be regenerated.
