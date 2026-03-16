from pydantic import BaseModel, Field
from typing import List, Dict
from src.tools import gitops_tools
from src.utils.logger import logger

class GitOpsContext(BaseModel):
    repo_url: str
    target_branch: str = "main"

class GitOpsAgent:
    def __init__(self, context: GitOpsContext):
        self.context = context

    def get_sync_status(self) -> Dict:
        logger.info("GitOpsAgent: Checking Flux sync status")
        return gitops_tools.flux_get_kustomizations()

    def propose_change(self, title: str, description: str, branch: str) -> Dict:
        logger.info(f"GitOpsAgent: Proposing MR '{title}' on branch {branch}")
        return gitops_tools.gitlab_create_mr(title, description, branch)
