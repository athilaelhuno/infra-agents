# Phase 0: Research - Infra Automation Agents

## Outline & Tasks

Based on the technical context and the user's specific request to optimize token usage while building CLI-driven infrastructure agents, the following areas require clear architectural decisions:

1. **Token Efficiency vs. Reliability**: How to minimize tokens when agents read outputs from verbose tools like `kubectl` or `terraform plan`?
2. **LLM Framework Selection**: Should we use LangChain, AutoGen, Pydantic-AI, or native API calls for the orchestrator?
3. **Proxy Execution Implementation**: How to efficiently Pipe CLI commands through an SSH VM?
4. **Dashboard Framework**: Lightweight UI for configuration management.

## Findings & Decisions

### Decision 1: Token Optimization Strategy for CLI Tool Outputs
- **Observation**: CLI tools like `kubectl describe pod` or `terraform plan` can produce thousands of lines of output, easily consuming large amounts of context window tokens and causing hallucinations.
- **Decision**: Implement a **Filtering Wrapper Pattern**.
- **Rationale**: Instead of returning raw stdout to the LLM agent, the Python `tools/` layer will pre-filter the output. For example, a `kube_get_failing_pods` tool will run `kubectl get pods -A | grep -v Runnings`, and parse the result returning only the names and namespaces of failing pods as a concise JSON. A `tf_plan_summary` tool will parse the terraform plan output returning only the counts of resources to add/change/destroy instead of the full diff, unless specifically requested.
- **Alternatives considered**: Passing full stdout (wastes tokens), fine-tuning smaller models (too complex for this project scope), simple truncation (risks cutting off the actual error at the end of the log).

### Decision 2: LLM Framework Selection
- **Observation**: The project needs a multi-agent routing system but wants to stay lightweight.
- **Decision**: Native Python API calls (using the official OpenAI/Anthropic/Google SDKs) combined with **Pydantic/LiteLLM** for tool calling schemas.
- **Rationale**: Frameworks like LangChain or AutoGen introduce significant abstraction overhead and often use hidden prompts that consume extra tokens invisibly. By using native SDKs with strict Pydantic schemas for the tool inputs, we have 100% control over the prompt and the token usage.
- **Alternatives considered**: AutoGen (great for multi-agent, but harder to control exact token spend), LangChain (bloated for simple tool-calling routers), purely native standard library (requires too much boilerplate for tool definition).

### Decision 3: ITSM Integration Approach
...
### Decision 4: Proxy Execution Implementation
- **Observation**: Commands like `kubectl` need to run on a network that can reach the cluster, often requiring a jump host.
- **Decision**: Use **SSH-based Command Execution (Paramiko/Fabric)**.
- **Rationale**: Instead of a full-blown agent on the VM, we will use a Python library to execute the commands via SSH directly from the central orchestrator. This centralizes the logic and simplifies the VM requirement (only needs SSH access).
- **Alternatives considered**: Remote agents (too heavy), HTTP proxies (complex to set up for all tools).

### Decision 5: Dashboard Framework
- **Observation**: Need a simple UI for editing `.env` and variables.
- **Decision**: **FastAPI + Jinja2 Templates**.
- **Rationale**: Minimal, fast, and stays within the Python ecosystem. No need for a complex frontend framework like React for a simple configuration page.
- **Alternatives considered**: Streamlit (fast but less control over layout), Flask (great but FastAPI is more modern/type-safe).
