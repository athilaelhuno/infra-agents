# Tasks Priority & Breakdown

**Feature Runbook**: infra-automation-agents | **Branch**: 001-infra-automation-agents
**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)

## 📋 Phase 1: Setup

These tasks establish the project scaffolding based on the Implementation Plan structure.

- [x] T001 Initialize Git repository, python env, and `requirements.txt`
- [x] T002 Create root project structure (`src/`, `tests/`)
- [x] T003 Setup basic utility modules (`src/utils/logger.py`, `src/utils/safety.py`)

## 🧱 Phase 2: Foundational

These tasks build the core orchestrator and base CLI wrapper mechanisms. 

- [x] T004 Build the `src/tools/shell_runner.py` to securely wrap subprocess calls and capture stdout/err.
- [x] T005 Implement the `src/orchestrator.py` entrypoint using Typer for CLI parsing.
- [ ] T006 Implement base LLM integration in `src/orchestrator.py` using standard API calls and Pydantic schemas.

## 🚀 Phase 3: User Story 1 - Multi-Agent Infrastructure Provisioning (P1)

**Goal**: Provision infrastructure by communicating with a Terraform/Terragrunt agent.
**Independent Test**: Request the agent to provision a simple Terraform module and verify it correctly parses `terraform plan` outputs.

- [x] T007 [P] [US1] Build `src/tools/tf_tools.py` with `tf_plan` and `tf_apply` wrappers.
- [x] T008 [P] [US1] Create `src/agents/terraform.py` encapsulating the TerraformContext.
- [x] T009 [US1] Wire the orchestrator to route IaC intents to the Terraform Agent.

- [x] Phase 3: Story 1 (Terraform)
- [x] Phase 6: Story 4 (UI)
- [x] Phase 7: Story 5 (Proxy)
- [/] Phase 8: Polish
## 🚀 Phase 4: User Story 2 - Automated Kubernetes & GitOps Management (P1)

**Goal**: Manage and troubleshoot Kubernetes deployments via a GitOps agent.
**Independent Test**: Ask the agent to read FluxCD kustomizations and check pod health for a specific namespace.

- [x] T010 [P] [US2] Build `src/tools/kube_tools.py` to wrap `kubectl` (e.g., getting pods, describing resources).
- [x] T011 [P] [US2] Build `src/tools/gitops_tools.py` to wrap `flux` commands and Git actions over manifests.
- [x] T012 [P] [US2] Create `src/agents/kubernetes.py` encapsulating the KubernetesContext.
- [x] T013 [P] [US2] Create `src/agents/gitops.py` to manage repository manipulation.
- [x] T014 [US2] Wire the orchestrator to route K8s/GitOps intents to these agents.

## 🚀 Phase 5: User Story 3 - ITSM and Documentation Sync (P2)

**Goal**: Link operations to Jira tickets and document them in Confluence.
**Independent Test**: Trigger the agent to update a Jira ticket and summarize logs in a Confluence page using REST APIs.

- [x] T015 [P] [US3] Build `src/tools/itsm_tools.py` to implement Python `requests` calls for Jira.
- [x] T016 [P] [US3] Extend `src/tools/itsm_tools.py` for Confluence API integration.
- [x] T017 [P] [US3] Create `src/agents/itsm.py` encapsulating the ITSMContext.
- [x] T018 [US3] Wire the orchestrator to route ticketing and documentation intents to the ITSM agent.

## 🚀 Phase 6: User Story 4 - Configuration & Secret Management UI (P2)

**Goal**: Centralized web interface for managing secrets.
**Independent Test**: Update a variable in the UI and check if it's updated in the agent's memory.

- [x] T019 [P] [US4] Create `src/utils/config.py` for safe loading/saving of env and secrets.
- [x] T020 [P] [US4] Build a simple FastAPI app in `src/dashboard/app.py`.
- [x] T021 [US4] Implement a configuration page with Jinja2 templates.

## 🚀 Phase 7: User Story 5 - Remote Proxy Execution (P1)

**Goal**: Pipe CLI commands through an SSH VM.
**Independent Test**: Configure a test host and run `uname -a` on that host via the orchestrator.

- [x] T022 [P] [US5] Implement `src/tools/proxy_runner.py` using Paramiko to execute commands over SSH.
- [x] T023 [US5] Integrate proxy_runner into `src/tools/tf_tools.py` and `src/tools/kube_tools.py` as an optional execution path.

## ✨ Phase 8: Polish

- [x] T024 Ensure all agent prompts are token-optimized (Filter verbosity on stdout).
- [x] T025 Run `pytest` on all tools to verify JSON parsing stability.
- [x] T026 Add final README documentation for running the CLI and Dashboard.

## 🔄 Dependencies

The orchestrator and shell_runner (Phase 2) block all specific agents (Phase 3-5). However, specific tool wrappers (e.g. `kube_tools.py` and `tf_tools.py`) can be built in parallel. Story 1 and Story 2 can be developed independently of each other once Phase 2 is complete.

## 🔀 Parallel Opportunities

- **T007 & T008 & T010 & T011 & T015**: All tool wrappers and their respective agent data models can be built concurrently by different developers or AI passes, since they don't depend on each other.

## 🎯 Implementation Strategy

1. **MVP Scope** (Phases 1-3): Build the core router and just the Terraform agent. If we can correctly run `terraform plan` and read it without blowing up the context window, the architectural assumption is validated.
2. **Expansion**: Move on to Kubernetes and GitOps (Phase 4).
3. **Integration**: Add the ITSM hooks (Phase 5) to link the automation to project tracking.
