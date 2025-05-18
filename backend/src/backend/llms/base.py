from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    """
    Abstract interface for any LLM provider.
    """

    @abstractmethod
    async def generate_resp(self, prompt: str, **kwargs) -> str:
        """
        Generate a completion from a prompt.
        """
        pass
