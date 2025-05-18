from pydantic import BaseModel
from typing import Optional

class TerraformArtifact(BaseModel):
    """
    Represents all Terraform-related artifacts for a session.
    """
    generated_code: str  # HCL or JSON
    plan_output: Optional[str]
    apply_output: Optional[str]
    success: bool = False
