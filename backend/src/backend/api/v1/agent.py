from fastapi import APIRouter
from src.backend.schemas.llm import LLMRequest, PromptRequest

from src.backend.services.test_agents.agent_servce import test_prompt_gen


agent_router = APIRouter()

@agent_router.post("/infracomplete")
async def infra_complete(request: LLMRequest):

    return {"msg": f"Got your Prompt: {request.prompt}"}


@agent_router.post("/test/promptgen")
async def prompt_gen(request: PromptRequest):
    print("##### Start #####")
    data: dict[str, str] = request.model_dump()
    print(data)
    print(type(data))

    return await test_prompt_gen(data)
