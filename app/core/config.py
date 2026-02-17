from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Vendor Inventory System"
    debug: bool = False
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/inventory_db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
