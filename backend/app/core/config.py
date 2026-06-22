from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Workspace AI"
    app_version: str = "0.1.0"
    environment: str = "development"

    database_url: str

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "phi3:mini"

    telegram_bot_token: str
    telegram_chat_id: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()