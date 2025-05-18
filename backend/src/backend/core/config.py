from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    app_name: str = "Infra-Copilot"
    environment: str = Field(default="dev", env="ENVIRONMENT")
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    groq_api_key: str = Field(default="", env="GROQ_API_KEY")
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
