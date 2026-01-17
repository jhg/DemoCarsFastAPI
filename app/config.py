import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    data_directory: str = '/data'


@lru_cache
def get_settings() -> Settings:
    data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    if os.path.exists(data_directory):
        os.environ.setdefault("DATA_DIRECTORY", data_directory)
    return Settings()


settings = get_settings()