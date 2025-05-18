from fastapi import APIRouter
from src.backend.schemas.llm import LLMRequest

agent_router = APIRouter()

@agent_router.post("/infracomplete")
async def infra_complete(request: LLMRequest):

    return {"msg": f"Got your Prompt: {request.prompt}"}
