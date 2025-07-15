from typing import Optional
from pydantic import BaseModel

class LLMRequest(BaseModel):
    """
    Request sent to LLM provider.
    """
    prompt: str
    temperature: float = 0.2

class LLMResponse(BaseModel):
    """
    Raw response returned by LLM provider.
    """
    content: str
    tokens_used: Optional[int] = None


class PromptRequest(BaseModel):
    prompt: str
    platform: str
