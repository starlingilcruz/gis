from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Zesty Api"

    postgres_host: str
    postgres_user: str
    postgres_password: str
    postgres_port: str
    postgres_db: str


@lru_cache()
def get_settings():
    return Settings()