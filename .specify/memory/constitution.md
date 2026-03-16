<!--
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- Modified principles: Replaced placeholders with 5 core infra-agent principles.
- Added sections: Security & Credentials Management, Development Workflow & Review.
- Removed sections: N/A
- Templates requiring updates: ✅ None required at this stage.
- Follow-up TODOs: None.
-->

# infra-agents Constitution

## Core Principles

### I. Agent Independence & Single Responsibility
Each agent within the system focuses on a singular domain (e.g., Terraform, Kubernetes, GitOps, Jira, Confluence, GitLab). Agents must communicate through clear, decoupled interfaces and avoid overstepping into another agent's domain.

### II. Infrastructure as Code (IaC) Strictness
All infrastructure states must be defined in code (Terraform, Terragrunt, Kubernetes manifests). Agents should avoid imperative or manual changes unless explicitly requested for emergency troubleshooting.

### III. Idempotency & Safety Guards
Agents must treat "dry-run" or "plan" as the default state. **CRITICAL: No command that creates, updates, or deletes resources can be executed without explicit user confirmation.**

### IV. Observability & Traceability
All actions must be summarized in human-readable format.

### V. GitOps-First Alignment
For Kubernetes deployments, agents should prefer updating state repositories to trigger FluxCD reconciliations, rather than modifying cluster state directly, preserving the GitOps source of truth.

## Security & Credentials Management

Agents MUST NOT log or expose plaintext secrets, tokens, or credentials in outputs or incident tickets. Access to Google Cloud Platform (GCP), GitLab, and Kubernetes should use short-lived tokens, Workload Identity, or secure secret injection methods (e.g., SOPS).

## Development Workflow, Review & Automation

Automated module creation or significant configuration changes MUST result in a Merge Request (MR) in GitLab for human review. Agents must create comprehensive documentation in Confluence and link related Jira tickets to the MR description.

## Governance

This Constitution supersedes all ad-hoc instructions or temporary practices. Adding new capabilities or agents to the `infra-agents` system requires ensuring they adhere to these core principles. Any deviation must be justified and documented.

**Version**: 1.0.0 | **Ratified**: 2026-03-16 | **Last Amended**: 2026-03-16
