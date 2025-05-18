from pydantic import BaseModel
from typing import Optional


class DocChunk(BaseModel):
    """
    A document chunk retrieved from the embedding store.
    """
    content: str
    source: Optional[str] = None
    score: Optional[float] = None  # Optional similarity score
    metadata: Optional[dict] = None

class AgentContext(BaseModel):
    cmd_prompt: str
    ref_context: Optional[list[DocChunk]]
