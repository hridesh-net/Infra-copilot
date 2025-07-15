from src.backend.agents.pre_processing.pre_processing import PromptGenerator

async def test_prompt_gen(data):
    prompt_gen = PromptGenerator()

    return prompt_gen.run_one_cycle(data)
