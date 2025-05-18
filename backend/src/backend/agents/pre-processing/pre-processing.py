from backend.schemas.context import GlobalContext


class PromptGenerator:

    def __init__(self, ctx: GlobalContext, user_prompt: str):
        ctx.original_prompt = user_prompt

    async def _get_local_context(self):
        pass

    async def call(self):
        pass
