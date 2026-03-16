import typer
from typing import Optional
from src.utils.logger import logger
from src.utils.config import config
from src.agents.terraform import TerraformAgent, TerraformContext
from src.agents.kubernetes import KubernetesAgent, KubernetesContext
from src.agents.gitops import GitOpsAgent, GitOpsContext
from src.agents.itsm import ITSMAgent, ITSMContext

app = typer.Typer(help="Infra Agents Orchestrator")

@app.command()
def main(
    text: str = typer.Argument(..., help="The natural language prompt for the agents"),
    project_root: str = typer.Option(".", "--project-root", "-p", help="Root directory of the target project")
):
    """
    Orchestrate multiple agents to handle infrastructure tasks from a specific project root.
    """
    import os
    abs_project_root = os.path.abspath(project_root)
    logger.info(f"Using project root: {abs_project_root}")
    logger.info(f"Received prompt: {text}")
    
    if "terraform" in text.lower() or "terragrunt" in text.lower():
        print(">> Detected Terraform intent.")
        # Try to find a terraform directory in project_root, default to root itself
        tf_dir = os.path.join(abs_project_root, "infra")
        if not os.path.exists(tf_dir):
            tf_dir = abs_project_root
            
        ctx = TerraformContext(working_dir=tf_dir)
        agent = TerraformAgent(ctx)
        
        if "plan" in text.lower():
            result = agent.plan()
            print(result.get("human_summary", "Plan completed."))
        elif "apply" in text.lower():
            result = agent.apply()
            print(result.get("human_summary", "Apply completed."))
    elif "kube" in text.lower() or "pod" in text.lower():
        print(">> Detected Kubernetes intent.")
        # Check for local kubeconfig in project_root for portability
        kubeconfig_path = os.path.join(abs_project_root, ".kubeconfig")
        cluster_ctx = None
        if os.path.exists(kubeconfig_path):
            cluster_ctx = kubeconfig_path
            
        ctx = KubernetesContext(namespace="default", cluster_ctx=cluster_ctx)
        agent = KubernetesAgent(ctx)
        
        if "health" in text.lower() or "status" in text.lower():
            result = agent.check_health()
            print(result.get("human_summary", "Health check completed."))
        elif "troubleshoot" in text.lower():
            # Simulated extraction of pod name
            result = agent.troubleshoot_pod("example-pod")
            print(result.get("human_summary", "Troubleshoot completed."))
            
    elif "flux" in text.lower() or "git" in text.lower() or "mr" in text.lower():
        print(">> Detected GitOps intent.")
        # For GitOps, the context could be derived from the local git repo in project_root
        git_dir = os.path.join(abs_project_root, ".git")
        repo_url = "https://gitlab.example.com/infra" # Fallback
        
        ctx = GitOpsContext(repo_url=repo_url, target_branch="main")
        agent = GitOpsAgent(ctx)
        
        if "sync" in text.lower() or "status" in text.lower():
            result = agent.get_sync_status()
            print(result.get("human_summary", "Sync status retrieved."))
            
    elif "jira" in text.lower() or "ticket" in text.lower() or "confluence" in text.lower() or "doc" in text.lower():
        print(">> Detected ITSM intent.")
        ctx = ITSMContext(project_key="INFRA", space_key="DOCS")
        agent = ITSMAgent(ctx)
        
        if "update" in text.lower() or "log" in text.lower():
            # Simulated extraction of ticket ID
            result = agent.log_action("INFRA-123", "Action taken by agent")
            print(result.get("human_summary", "Jira update completed."))
        elif "create" in text.lower() or "document" in text.lower():
            result = agent.create_documentation("New Infra Doc", "Content created by agent")
            print(result.get("human_summary", "Confluence creation completed."))
    else:
        print(">> General or unrecognized intent.")

@app.command()
def config_show():
    """Display current configuration (excluding sensitive values)."""
    for k, v in os.environ.items():
        if any(secret in k.lower() for secret in ["key", "token", "password", "secret"]):
            print(f"{k}=********")
        else:
            print(f"{k}={v}")

if __name__ == "__main__":
    import os
    app()
