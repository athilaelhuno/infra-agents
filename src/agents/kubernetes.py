from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from src.tools import kube_tools
from src.utils.logger import logger

class KubernetesContext(BaseModel):
    namespace: str = "default"
    cluster_ctx: Optional[str] = None

class KubernetesAgent:
    def __init__(self, context: KubernetesContext):
        self.context = context

    def check_health(self) -> Dict:
        logger.info(f"KubernetesAgent: Checking health in namespace {self.context.namespace}")
        return kube_tools.kube_get_failing_pods(self.context.namespace)

    def troubleshoot_pod(self, pod_name: str) -> Dict:
        logger.info(f"KubernetesAgent: Troubleshooting pod {pod_name}")
        return kube_tools.kube_describe_resource("pod", pod_name, self.context.namespace)
