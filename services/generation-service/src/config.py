# from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     service_name: str = "generation-service"
#     host: str = "0.0.0.0"
#     port: int = 8002
#     log_level: str = "INFO"
    
#     # Database
#     database_url: str = "postgresql+asyncpg://upg:upg@localhost:5432/upg"
    
#     # Templates
#     templates_dir: str = "/app/templates"

#     class Config:
#         env_file = ".env"


# settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "generation-service"
    host: str = "0.0.0.0"
    port: int = 8002
    log_level: str = "INFO"
    
    # Database
    database_url: str = "postgresql+asyncpg://upg:upg@localhost:5432/upg"
    
    # Templates
    templates_dir: str = "/app/templates"

    class Config:
        env_file = ".env"


settings = Settings()