from fastapi import APIRouter
from .orchestrator import router as orchestrator_router
from .agent import agent_router

api_router = APIRouter()

api_router.include_router(orchestrator_router, prefix="/orchestrator", tags=["orchestrator"])
api_router.include_router(agent_router, prefix="/agent", tags=["agent"])

@api_router.get("/health")
async def health_checker():
    return {"Status": "OK"}
