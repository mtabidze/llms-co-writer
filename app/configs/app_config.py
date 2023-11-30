# Copyright (c) 2023 Mikheil Tabidze
from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    log_level: str = "INFO"
    secret_keys: list[str] = []
    openai_api_key: str
    openai_model: str = "gpt-4"
    redis_dsn: RedisDsn | None = Field(default=None)
    redis_expiration_seconds: int = Field(default=3600)
    aws_region: str | None = Field(default=None)
    aws_access_key_id: str | None = Field(default=None)
    aws_secret_access_key: str | None = Field(default=None)
    aws_inferences_table_name: str | None = Field(default=None)
