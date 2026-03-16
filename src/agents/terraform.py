from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from src.tools import tf_tools
from src.utils.logger import logger

class TerraformContext(BaseModel):
    working_dir: str = Field(..., description="Local path to the terraform/terragrunt module")
    use_terragrunt: bool = True
    environment: str = "dev"

class TerraformAgent:
    """
    Dedicated agent for Terraform/Terragrunt operations.
    """
    def __init__(self, context: TerraformContext):
        self.context = context

    def plan(self) -> Dict:
        logger.info(f"TerraformAgent: planning in {self.context.working_dir}")
        return tf_tools.tf_plan(self.context.working_dir, self.context.use_terragrunt)

    def apply(self) -> Dict:
        logger.info(f"TerraformAgent: applying in {self.context.working_dir}")
        return tf_tools.tf_apply(self.context.working_dir, self.context.use_terragrunt)
