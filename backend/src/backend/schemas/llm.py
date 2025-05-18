from pydantic import BaseModel, Field

class LLMRequest(BaseModel):
    """
    Represents a request sent to the LLM provider.
    """
    prompt: str = Field(..., example="Generate Terraform code for an EC2 instance")

class LLMResponse(BaseModel):
    """
    Represents a response returned from the LLM provider.
    """
    content: str = Field(..., description="Raw text or JSON returned by the LLM")
