from pydantic import BaseModel, Field
from typing import Optional
from src.tools import itsm_tools
from src.utils.logger import logger

class ITSMContext(BaseModel):
    project_key: str
    space_key: str

class ITSMAgent:
    def __init__(self, context: ITSMContext):
        self.context = context

    def log_action(self, issue_key: str, action_summary: str):
        logger.info(f"ITSMAgent: Logging action to Jira {issue_key}")
        return itsm_tools.jira_update_issue(issue_key, action_summary)

    def create_documentation(self, title: str, content: str):
        logger.info(f"ITSMAgent: Creating Confluence page '{title}'")
        return itsm_tools.confluence_create_page(title, content, self.context.space_key)
