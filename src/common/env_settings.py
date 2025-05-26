from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


class DatabaseConfig(BaseModel):
    host: str
    port: int
    name: str
    username: str
    password: str


class AppConfig(BaseModel):
    backend_port: int
    django_secret_key: str
    is_dockerized: bool
    results_count: int


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    app: AppConfig
    database: DatabaseConfig


load_dotenv(dotenv_path=".env", interpolate=True)
env_settings = EnvSettings()
