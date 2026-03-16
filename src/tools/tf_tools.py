import re
from typing import List, Optional, Dict
from src.tools.shell_runner import run_command
from src.tools.proxy_runner import run_ssh_command
from src.utils.logger import logger
from src.utils.safety import confirm_execution, human_readable_summary

def get_base_cmd(use_terragrunt: bool = True) -> str:
    return "terragrunt" if use_terragrunt else "terraform"

def tf_plan(working_dir: str, use_terragrunt: bool = True, proxy_config: Optional[Dict] = None) -> Dict:
    """
    Runs terraform/terragrunt plan and returns a summarized JSON + human-readable text.
    """
    cmd_str = f"{get_base_cmd(use_terragrunt)} plan -no-color"
    
    if proxy_config:
        result = run_ssh_command(
            host=proxy_config['host'],
            user=proxy_config['user'],
            key_path=proxy_config['key_path'],
            command=f"cd {working_dir} && {cmd_str}"
        )
    else:
        result = run_command(cmd_str.split(), cwd=working_dir)
    
    summary = {
        "add": 0,
        "change": 0,
        "destroy": 0,
        "status": "success" if result.success else "error",
        "human_summary": ""
    }
    
    if result.success:
        match = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", result.stdout)
        if match:
            summary["add"] = int(match.group(1))
            summary["change"] = int(match.group(2))
            summary["destroy"] = int(match.group(3))
        
        info = f"Plan: {summary['add']} to add, {summary['change']} to change, {summary['destroy']} to destroy."
        summary["human_summary"] = human_readable_summary("TERRAFORM PLAN", info, True)
    else:
        summary["human_summary"] = human_readable_summary("TERRAFORM PLAN", result.stderr, False)
            
    return summary

def tf_apply(working_dir: str, use_terragrunt: bool = True) -> Dict:
    """
    Runs terraform/terragrunt apply with MANDATORY user confirmation.
    """
    action = f"Apply Terraform changes in {working_dir}"
    if not confirm_execution(action, working_dir):
        return {"success": False, "human_summary": "Action cancelled by user."}

    cmd = [get_base_cmd(use_terragrunt), "apply", "-auto-approve", "-no-color"]
    result = run_command(cmd, cwd=working_dir)
    
    h_summary = human_readable_summary("TERRAFORM APPLY", result.stdout[-500:], result.success)
    
    return {
        "success": result.success,
        "human_summary": h_summary,
        "stdout": result.stdout[-500:],
        "stderr": result.stderr
    }
