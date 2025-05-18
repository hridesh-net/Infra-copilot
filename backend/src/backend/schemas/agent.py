from pydantic import BaseModel, Field
from typing import Any

class AgentInput(BaseModel):
    """
    Represents a natural language prompt input to the agent.
    """
    prompt: str = Field(..., example="Create a 3-tier architecture with autoscaling and RDS")

class ResourceConfig(BaseModel):
    """
    Represents configuration for a single resource in the infrastructure blueprint.
    """
    type: str = Field(..., example="ec2")
    config: dict[str, Any] = Field(..., example={"instance_type": "t3.micro", "count": 2})

class Blueprint(BaseModel):
    """
    Represents the agent-generated infrastructure blueprint to be converted into Terraform.
    """
    resources: list[ResourceConfig]
