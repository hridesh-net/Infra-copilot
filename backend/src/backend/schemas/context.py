from typing import Optional, Any
from pydantic import BaseModel, Field
from backend.schemas.blueprint import Blueprint
from backend.schemas.terraform import TerraformArtifact
from enum import Enum

class ExecutionState(str, Enum):
    INIT = "init"
    PLANNED = "planned"
    CONFIRMED = "confirmed"
    GENERATED = "generated"
    APPLIED = "applied"
    FAILED = "failed"

class GlobalContext(BaseModel):
    """
    Shared working context passed between agents.
    Tracks evolving state of the infrastructure design process.
    """
    original_prompt: str
    current_prompt: Optional[str] = None
    llm_outputs: list[str] = []

    blueprint: Optional[Blueprint] = None
    terraform_artifact: Optional[TerraformArtifact] = None

    confirmed: bool = False
    state: ExecutionState = ExecutionState.INIT
    state_node: Optional[str] = None

    metadata: dict[str, Any] = Field(default_factory=dict)
