from fastapi import FastAPI

from src.backend.api.v1.router import api_router
from src.backend.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)


app.include_router(api_router, prefix="/api/v1")
