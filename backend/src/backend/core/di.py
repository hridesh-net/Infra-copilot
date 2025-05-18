from functools import lru_cache
from backend.core.config import Settings

@lru_cache
def get_settings() -> Settings:
    return Settings()
