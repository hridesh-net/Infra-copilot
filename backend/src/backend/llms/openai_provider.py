import openai
from backend.llms.base import BaseLLMProvider
from backend.core.config import settings

class OpenAIProvider(BaseLLMProvider):
    """OpenAI implementation of the LLM provider interface.

    Args:
        BaseLLMProvider (_type_): _description_
    """

    def __init__(self):
        openai.api_key = settings.openai_api_key

    async def generate_resp(self, prompt: str, **kwargs) -> str:
        """
        Generate a completion from a prompt.
        """
        pass
