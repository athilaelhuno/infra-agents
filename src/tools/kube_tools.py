from typing import List, Dict, Optional
from src.tools.shell_runner import run_command
from src.tools.proxy_runner import run_ssh_command
from src.utils.logger import logger
from src.utils.safety import human_readable_summary

def kube_get_failing_pods(namespace: str = "default", proxy_config: Optional[Dict] = None) -> Dict:
    """
    Returns a filtered list of non-running pods + human summary.
    """
    cmd_str = f"kubectl get pods -n {namespace} --no-headers"
    
    if proxy_config:
        result = run_ssh_command(
            host=proxy_config['host'],
            user=proxy_config['user'],
            key_path=proxy_config['key_path'],
            command=cmd_str
        )
    else:
        result = run_command(cmd_str.split())
    
    failing_pods = []
    if result.success:
        lines = result.stdout.strip().split("\n")
        for line in lines:
            parts = line.split()
            if len(parts) >= 3:
                name, ready, status = parts[0], parts[1], parts[2]
                if status != "Running" and status != "Completed":
                    failing_pods.append({
                        "name": name,
                        "status": status,
                        "ready": ready
                    })
    
    h_summary = human_readable_summary(
        f"K8S POD HEALTH ({namespace})",
        f"Found {len(failing_pods)} failing pods." if result.success else result.stderr,
        result.success
    )
    
    return {
        "failing_pods": failing_pods,
        "human_summary": h_summary,
        "success": result.success
    }

def kube_describe_resource(resource_type: str, name: str, namespace: str = "default") -> Dict:
    """
    Describes a resource and returns a sampled output + human summary.
    """
    cmd = ["kubectl", "describe", resource_type, name, "-n", namespace]
    result = run_command(cmd)
    
    output = result.stdout
    if result.success and len(output) > 2000:
        output = output[:500] + "\n... [truncated] ...\n" + output[-1000:]
    
    h_summary = human_readable_summary(
        f"K8S DESCRIBE {resource_type.upper()} {name}",
        output if result.success else result.stderr,
        result.success
    )
    
    return {
        "output": output,
        "human_summary": h_summary,
        "success": result.success
    }
