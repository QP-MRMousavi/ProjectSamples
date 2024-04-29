from typing import Any

from pydantic import AnyHttpUrl, BaseModel, Field, HttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    LOG_LEVEL: str
    LOG_JSON: bool = True
    COLORIZE_LOGS: bool = False
    API_VERSION: str = "v1"

    @validator("COLORIZE_LOGS")
    def set_colorize_logs(cls, val: bool, values: dict[str, Any]) -> bool:
        if values["LOG_JSON"] and val:
            raise ValueError("LOG_JSON and COLORIZE_LOGS are mutually exclusive")
        return val

    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = ["http", "https"]

    MYSQL_SERVER: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    TORTOISE_CONFIG: dict[str, Any] = None  # type: ignore

    @validator("TORTOISE_CONFIG", pre=True)
    def generate_tortoise_config(
        cls, val: dict[str, Any] | None, values: dict[str, Any]
    ) -> dict[str, Any]:
        if isinstance(val, dict):
            return val
        return {
            "connections": {
                "default": f"mysql://{values['MYSQL_USER']}:{values['MYSQL_PASSWORD']}@{values['MYSQL_SERVER']}/{values['MYSQL_DB']}"
            },
            "apps": {
                "app": {
                    "models": ["models", "aerich.models"],
                    "default_connection": "default",
                },
            },
            "timezone": "UTC",
        }

    class Config:
        case_sensitive = True
        env_nested_delimiter = "__"


settings = Settings(_env_file=".env")

# Tortoise
TORTOISE_CONFIG = settings.TORTOISE_CONFIG
