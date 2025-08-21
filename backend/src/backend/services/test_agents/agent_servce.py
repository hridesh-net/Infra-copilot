from src.backend.agents.pre_processing.pre_processing import PromptGenerator
from src.backend.agents.infra_blueprint.blueprint import BlueprintGen

async def test_prompt_gen(data):
    prompt_gen = PromptGenerator()

    return prompt_gen.run_one_cycle(data)

async def test_blueprint_gen(data):
    blueprint = BlueprintGen()

    return blueprint.run_one_cycle(data)
