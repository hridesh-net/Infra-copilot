from fastapi import APIRouter
from .orchestrator import router as orchestrator_router

api_router = APIRouter()

api_router.include_router(orchestrator_router, prefix="/orchestrator", tags=["orchestrator"])
