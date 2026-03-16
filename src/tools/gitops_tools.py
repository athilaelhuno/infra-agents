from typing import List, Dict
from src.tools.shell_runner import run_command
from src.utils.logger import logger
from src.utils.safety import confirm_execution, human_readable_summary

def flux_get_kustomizations() -> Dict:
    """
    Lists flux kustomizations and their health + human summary.
    """
    cmd = ["flux", "get", "kustomizations", "--no-header"]
    result = run_command(cmd)
    
    repos = []
    if result.success:
        for line in result.stdout.strip().split("\n"):
            parts = line.split("\t")
            if len(parts) >= 4:
                repos.append({
                    "name": parts[0].strip(),
                    "revision": parts[1].strip(),
                    "suspended": parts[2].strip(),
                    "ready": parts[3].strip(),
                    "message": parts[4].strip() if len(parts) > 4 else ""
                })
    
    h_summary = human_readable_summary(
        "FLUX SYNC STATUS",
        f"Found {len(repos)} kustomizations." if result.success else result.stderr,
        result.success
    )
    
    return {"repos": repos, "human_summary": h_summary, "success": result.success}

def gitlab_create_mr(title: str, description: str, branch: str) -> Dict:
    """
    Uses 'glab' CLI to create a Merge Request with MANDATORY confirmation.
    """
    action = f"Create GitLab Merge Request: {title}"
    if not confirm_execution(action, branch):
        return {"success": False, "human_summary": "MR creation cancelled by user."}

    cmd = ["glab", "mr", "create", "-t", title, "-d", description, "-b", branch, "--yes"]
    result = run_command(cmd)
    
    h_summary = human_readable_summary("GITLAB MR CREATE", result.stdout, result.success)
    
    return {
        "success": result.success,
        "human_summary": h_summary,
        "stdout": result.stdout,
        "stderr": result.stderr
    }
