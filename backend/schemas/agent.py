from pydantic import BaseModel
from typing import Optional
from enum import Enum


class AgentRole(str, Enum):
    PROMPT_REFINER = "prompt_refiner"
    PLANNER = "planner"
    VALIDATOR = "validator"
    TERRAFORM_GENERATOR = "terraform_generator"
    USER_FOLLOWER = "user_follower"
    EXECUTOR = "executor"
    COST_ESTIMATOR = "cost_estimator"

class AgentInput(BaseModel):
    """
    Input received by each agent — includes the shared context.
    """
    context: dict
    role: AgentRole

class AgentOutput(BaseModel):
    """
    Output returned by each agent — updated context and trace.
    """
    updated_context: dict
    debug_trace: Optional[str] = None
