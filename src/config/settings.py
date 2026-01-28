from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict


class Settings(BaseSettings):
    supabase_db_url: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
