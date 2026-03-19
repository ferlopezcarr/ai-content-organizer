from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM
    llm_api_url: str = "http://192.168.1.152:1234"
    llm_model: str = "mistral"

    # Database
    database_url: str

    # Server
    backend_host: str = "localhost"
    backend_port: int = 8000

    # Logging
    log_level: str = "INFO"
    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
