from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    groq_api_key: str = Field(default="", env="GROQ_API_KEY")
    environment: str = Field(default="dev", env="ENVIRONMENT")
    log_level: str = "INFO"
    app_name: str = "Infra-Copilot"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        populate_by_name=True,  # <--- this line is the key
        extra="allow",
    )

settings = Settings()
