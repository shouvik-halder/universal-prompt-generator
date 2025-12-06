from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "analysis-service"
    host: str = "0.0.0.0"
    port: int = 8001
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()