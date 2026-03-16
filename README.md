# Infra Agents

Multi-agent infrastructure automation system powered by Antigravity and Spec-Kit.

## Features
- **Multi-Agent Orchestration**: Specialized agents for Terraform, Kubernetes, GitOps, and ITSM.
- **Token Efficiency**: Smart CLI wrappers that filter and summarize output before sending to the LLM.
- **Proxy Execution**: Ability to tunnel CLI commands through a VM (bastion host) via SSH.
- **Web Dashboard**: Simple UI for managing environment variables and API tokens.

## Setup
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your `.env` file or use the Dashboard.

## Usage
### CLI Orchestrator
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 src/orchestrator.py "How is the health of the production pods?"
```

### Dashboard
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 src/dashboard/app.py
```
Visit `http://localhost:8000` to manage your configuration.

## Project Structure
- `src/agents/`: Domain-specific agent logic.
- `src/tools/`: CLI and API interaction wrappers.
- `src/dashboard/`: FastAPI configuration UI.
- `src/utils/`: Shared logging, config, and safety utilities.
