from functools import lru_cache

from loguru import logger
from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = 0
    database_url: AnyUrl = None


@lru_cache
def get_settings() -> BaseSettings:
    logger.info("Loading config settings from the environment...")
    return Settings()
