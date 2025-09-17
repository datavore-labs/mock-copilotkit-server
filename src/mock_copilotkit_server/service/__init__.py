import logging
from typing import TypeVar

from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def log_params(service_name: str, params: dict[str, str | list[str]]) -> None:
    logger.info(f"🚀 [BACKEND ACTION] *** {service_name} CALLED *** with {params=}")
    logger.info("🔥 [BACKEND ACTION] *** THIS IS A BACKEND ACTION - LLM SHOULD CALL THIS ***")
    logger.info(f"📊 [BACKEND DATA] Getting {service_name} for {params}")


def log_result(result: T) -> None:
    logger.info(
        f"✅ [BACKEND ACTION] *** SUCCESSFULLY RETURNING DATA *** with " f"{len(result.data)} - {result.chart_type}"
    )
    logger.info(f"🎯 [BACKEND ACTION] Result: {result}")
