from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, Optional

class ResourceType(str, Enum):
    EC2 = "ec2"
    S3 = "s3"
    RDS = "rds"
    VPC = "vpc"
    LAMBDA = "lambda"
    API_GATEWAY = "api_gateway"

class ResourceConfig(BaseModel):
    """
    Represents one resource type and its configuration details.
    """
    type: ResourceType
    name: str
    config: dict[str, Any]

class Blueprint(BaseModel):
    """
    Represents the full infrastructure plan from the planner agent.
    """
    name: str = Field(..., example="3-tier web app")
    description: Optional[str]
    resources: list[ResourceConfig] = []
