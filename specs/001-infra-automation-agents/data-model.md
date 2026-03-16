# Data Model & Interfaces: Infra Automation Agents

## Agent Contexts

To maintain single-responsibility and avoid credential leakage, each agent operates with an injected `Context` object.

### 1. `TerraformContext`
- **Purpose**: Defines the working directory, workspace, and expected variables for Terraform/Terragrunt runs.
- **Fields**:
  - `working_dir: str` (e.g., `/infra/environments/prod`)
  - `backend_type: str` (e.g., `gcs`)
  - `vars: dict` (key-value pairs of TF_VARs)

### 2. `KubernetesContext`
- **Purpose**: Defines the target cluster and namespace for `kubectl` or `flux` operations.
- **Fields**:
  - `kubeconfig_path: str`
  - `context_name: str`
  - `namespace: str` (default: `default`)

### 4. `ProxyContext`
- **Purpose**: Defines the remote host and credentials for command proxying.
- **Fields**:
  - `host: str`
  - `user: str`
  - `ssh_key_path: str`

### 5. `Configuration`
- **Purpose**: Represents the persistent state of tokens and environment variables.
- **Fields**:
  - `variables: dict[str, str]`
  - `secrets: dict[str, str]` (encrypted at rest)

## Tool Interface Contracts

All tools wrap underlying CLI executions or API calls. They accept strictly typed Pydantic models.

### `tf_plan`
```python
class TFPlanInput(BaseModel):
    working_dir: str
    target_resources: Optional[List[str]] = None

# Returns a JSON summary: {"add": int, "change": int, "destroy": int, "critical_changes": list}
```

### `kube_get_failing_resources`
```python
class KubeFailingInput(BaseModel):
    namespace: Optional[str] = None
    resource_type: str = "pods" # pods, deployments, kustomizations

# Returns list of {"name": "...", "namespace": "...", "status": "...", "age": "..."}
```

### `jira_update_ticket`
```python
class JiraUpdateInput(BaseModel):
    ticket_id: str
    comment: str
    transition_state: Optional[str] = None
```

## State Machine / Orchestrator Flow

1. **User Request**: Orchestrator LLM receives user intent.
2. **Routing**: Orchestrator determines which agent (Terraform, K8s, GitOps, ITSM) handles the domain.
3. **Execution**: Selected agent formulates the tool calls based on the context.
4. **Tool Wrapper**: The Python tool wrapper translates the call to the native CLI, captures `stdout/stderr`, parses the text into structured data.
5. **Synthesis**: The agent summarizes the result and routes back to the orchestrator or directly to the user/ITSM tracker.
