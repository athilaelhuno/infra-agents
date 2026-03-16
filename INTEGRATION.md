# Integration Guide: Multi-Project Support

This document explains how to integrate `infra-agents` as a centralized automation engine across multiple target projects.

## 🏗 Architecture Selection
You can use `infra-agents` in two ways:
1. **Centralized Engine (Recommended)**: Keep `infra-agents` in its own repo and point to target projects.
2. **Submodule/Sidecar**: Include `infra-agents` as a folder inside each project.

## 🚀 Step 1: Configuration per Project
Create an `infra-agents.yml` (or `.env.project`) in each target project to define:
- `WORKING_DIR`: Path to Terraform modules.
- `K8S_NAMESPACE`: Target namespace.
- `PROXY_HOST`: If that project requires a specific bastion.

## 🛠 Step 2: Running with Context
The orchestrator now supports a `--project-root` (or `-p`) flag. This allows you to run the agents from anywhere while targeting a specific project.

```bash
# Run from the infra-agents directory targeting Project A
python src/orchestrator.py -p "/path/to/project-a" "plan terraform"

# Run targeting Project B (which might have its own .kubeconfig)
python src/orchestrator.py -p "/path/to/project-b" "check pod health"
```

## 🧠 Step 3: Analysis & Decision Flow
To enable the "Analysis based on what I want to do" capability:
1. **Context Loading**: The agent reads the target project's root to find `infra/` folders, `.git` repos, or `.kubeconfig` files.
2. **Intent Discovery**: The LLM analyzes the prompt + project context to select the right tool.
3. **Execution Gate**: Based on Phase 9, it generates a Plan and asks for your approval before modifying anything in the target project.

## 📋 Integration Checklist
- [ ] Install `infra-agents` dependencies in your environment.
- [ ] Set up a global `.env` with shared credentials (GCP/Jira).
- [ ] Define project-specific overrides in the target repository.
- [ ] Alias the orchestrator: `alias ia='python /path/to/infra-agents/src/orchestrator.py'`
