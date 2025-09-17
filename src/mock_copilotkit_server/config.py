import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    use_live_data: bool = True
    server_reload: bool = False
    server_host: str = "0.0.0.0"
    server_port: int = 8080
    debug: bool = False
    log_level: str = "info"
    bigquery_project_id: str = "audience-builder-tintash"


@lru_cache
def get_config():
    if os.environ.get("ENV") == "dev":
        return Config(
            debug=True,
            use_live_data=True,
            server_reload=True,
            server_host="localhost",
            server_port=8000,
        )

    return Config()


# Default config instance
config = get_config()
