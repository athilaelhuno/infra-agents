# Implementation Plan: infra-automation-agents

**Branch**: `001-infra-automation-agents` | **Date**: 2026-03-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-infra-automation-agents/spec.md`

## Summary

The project consists of implementing an automation system using multiple agents to manage infrastructure operations. We will add a **lightweight Web Dashboard** (using Flask or FastAPI) to manage configuration and secrets. To handle restricted environments, we will implement a **Proxy Execution Engine** that allows agents to route CLI commands through a VM using SSH tunnels.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `pydantic`, `typer`, `subprocess`, `requests`, `fastapi` (for the dashboard), `paramiko` (for SSH proxying).
**Storage**: Local encrypted file or Vault (for secrets) + `.env`.
**Testing**: `pytest`.
**Target Platform**: Linux/macOS.
**Project Type**: CLI + Web Dashboard + Agent Orchestrator.
**Performance Goals**: Minimal LLM token context usage; quick execution of local CLI commands.
**Constraints**: Must not log or expose secrets. Must rely on robust CLI parsing instead of heavy JSON/API payload processing by the LLM.
**Scale/Scope**: Manageable set of ~5 distinct agent personas routing to ~15-20 specific CLI tool wrappers.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Agent Independence & Single Responsibility**: PASS. We will separate the logic into distinct Python modules per agent domain (e.g., `agents/terraform.py`, `agents/k8s.py`).
- **II. Infrastructure as Code (IaC) Strictness**: PASS. Tools provided to agents will be strictly wrapper commands around established IaC tools.
- **III. Idempotency & Safety Guards**: PASS. Write operations will implement a dry-run flag or explicit confirmation step.
- **IV. Observability & Traceability**: PASS. Standard Python `logging` module will be used to track all agent tool calls.
- **V. GitOps-First Alignment**: PASS. K8s agents will default to updating GitLab repos and monitoring Flux.
- **Security & Credentials**: PASS. Use environment variables and standard credential managers (e.g., `gcloud auth`, `~/.kube/config`); no hardcoded secrets.

## Phase 0: Research

*See `research.md` for specific architectural decisions on token usage optimization and CLI wrapping.*

## Phase 1: Design

*See `data-model.md` for tool schemas and `quickstart.md` for setup instructions.*

## Project Structure

### Documentation (this feature)

```text
specs/001-infra-automation-agents/
├── plan.md              # This file
├── research.md          # Token optimization and CLI wrapping strategy
├── data-model.md        # Agent state and tool schemas
├── quickstart.md        # How to run the orchestrator
└── tasks.md             # Implementation steps
```

### Source Code (repository root)

```text
src/
├── orchestrator.py      # Main entry point and user prompt router
├── dashboard/           # Web UI for configuration
│   ├── app.py           # FastAPI/Flask app
│   └── templates/       # HTML for config editing
├── agents/              # Individual agent domains
│   ├── terraform.py
│   ├── kubernetes.py
│   ├── gitops.py
│   └── itsm.py
├── tools/               # CLI wrappers and execution logic
│   ├── shell_runner.py  # Local shell execution
│   ├── proxy_runner.py  # SSH-based execution on VM
│   ├── tf_tools.py
│   ├── kube_tools.py
│   └── glab_tools.py
└── utils/
    ├── config.py        # Config & Secret loader
    ├── logger.py
    └── safety.py

tests/
├── unit/
│   ├── test_agents.py
│   └── test_tools.py
└── integration/
    └── test_cli_wrappers.py
```

**Structure Decision**: A modular Python CLI structure where `src/orchestrator.py` routes user intent to specific `agents/`, which in turn use strictly defined `tools/` that wrap native CLI binaries.

## Complexity Tracking

No violations of the Constitution observed; project structure is kept flat and modular to adhere to the separation of concerns.
