import requests
from typing import Dict, Optional
from src.utils.logger import logger
from src.utils.config import config
from src.utils.safety import confirm_execution, human_readable_summary

def jira_update_issue(issue_key: str, comment: str) -> Dict:
    """
    Updates a Jira issue with a comment after MANDATORY user approval.
    """
    action = f"Add comment to Jira issue {issue_key}"
    if not confirm_execution(action, issue_key):
        return {"success": False, "human_summary": "Jira update cancelled by user."}

    url = f"{config.get_val('JIRA_URL')}/rest/api/2/issue/{issue_key}/comment"
    auth = (config.get_val('JIRA_USER'), config.get_val('JIRA_TOKEN'))
    
    payload = {"body": comment}
    
    try:
        response = requests.post(url, json=payload, auth=auth)
        response.raise_for_status()
        h_summary = human_readable_summary(f"JIRA UPDATE {issue_key}", "Comment added successfully.", True)
        return {"success": True, "human_summary": h_summary}
    except Exception as e:
        h_summary = human_readable_summary(f"JIRA UPDATE {issue_key}", str(e), False)
        return {"success": False, "human_summary": h_summary}

def confluence_create_page(title: str, content: str, space: str) -> Dict:
    """
    Creates a new Confluence page after MANDATORY user approval.
    """
    action = f"Create Confluence page: {title} in space {space}"
    if not confirm_execution(action, space):
        return {"success": False, "human_summary": "Confluence creation cancelled by user."}

    url = f"{config.get_val('CONFLUENCE_URL')}/rest/api/content"
    auth = (config.get_val('CONFLUENCE_USER'), config.get_val('CONFLUENCE_TOKEN'))
    
    payload = {
        "title": title,
        "type": "page",
        "space": {"key": space},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }
    
    try:
        response = requests.post(url, json=payload, auth=auth)
        response.raise_for_status()
        h_summary = human_readable_summary(f"CONFLUENCE CREATE '{title}'", "Page created successfully.", True)
        return {"success": True, "human_summary": h_summary}
    except Exception as e:
        h_summary = human_readable_summary(f"CONFLUENCE CREATE '{title}'", str(e), False)
        return {"success": False, "human_summary": h_summary}
