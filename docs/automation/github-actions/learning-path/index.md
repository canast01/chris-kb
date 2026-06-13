# GitHub Actions — Learning Path

<div class="kb-summary">
Recommended reading order for GitHub Actions. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌─────────────────────────────────── GitHub Actions — Learning Path ────────────────────────────────────┐
│                                                                                                       │
│    5 stages in order: Architecture → Deploy → Operations → Security → Troubleshoot                    │
│                                                                                                       │
│   ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│   │  Architecture  │  │     Deploy     │  │    Operations   │  │    Security    │  │  Troubleshoot  │ │
│   │                │  │                │  │                 │  │                │  │                │ │
│   │  How It Works  │  │ Initial Setup  │  │  Health Checks  │  │ Access Control │  │ Common Issues  │ │
│   │Design Standards│  │Install/Upgrade │  │  CLI Reference  │  │ Authentication │  │  Diagnostics   │ │
│   │  Integrations  │  │                │  │    Procedures   │  │   Encryption   │  │   Escalation   │ │
│   │                │  │                │  │ Backup & Restore│  │   Hardening    │  │                │ │
│   │                │  │                │  │     Scripts     │  │                │  │                │ │
│   └────────────────┘  └────────────────┘  └─────────────────┘  └────────────────┘  └────────────────┘ │
│                                                                                                       │
│    Stage 1 (Architecture) builds understanding. Stage 3 (Operations) is daily work. Troubleshoot last.│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```
| Stage | Focus | Time investment |
|-------|-------|----------------|
| 1 — Architecture | Event model, job graph, runner lifecycle | 3–4 h |
| 2 — Deployment | Self-hosted runners, environments, OIDC | 2–3 h |
| 3 — Operations | Runner health, workflow monitoring, CLI | ongoing |
| 4 — Security | Permissions, secrets, action pinning, OIDC | 2–3 h |
| 5 — Troubleshooting | Debug logs, runner diagnostics, OIDC errors | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand how GitHub Actions orchestrates workflows — event triggers, job dependency graphs, runner allocation, and the context/expression model — before building production CI/CD pipelines.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — event model (`push`, `pull_request`, `workflow_dispatch`, `schedule`, `workflow_call`), job dependency graph (`needs:`), step execution order, and GitHub-hosted vs self-hosted runner isolation and lifecycle
- [Design Standards](../architecture/design-standards/) — workflow file naming (`/.github/workflows/`), job and step naming conventions, matrix strategy design for cross-platform testing, and reusable workflow (`workflow_call`) patterns for DRY automation
- [Integrations](../architecture/integrations/) — OIDC token exchange with AWS/Azure/GCP for credential-free cloud access, GitHub Packages for artifact storage, GitHub Environments for deployment targets with protection rules, and external webhooks

**Key concepts before moving on**:

- Each job runs in a fresh runner (GitHub-hosted) or a reused runner (self-hosted) — there is no shared filesystem between jobs without artefact upload/download
- The `GITHUB_TOKEN` scoped to a repository has a default permission set that may need expanding with the `permissions:` block
- Secrets are masked in logs but only after they are referenced; do not construct secrets from multiple concatenated strings that individually appear in logs
- `pull_request_target` runs in the context of the base branch with write access — it is dangerous when used with untrusted forks

**Why first**: GitHub Actions workflows execute against real infrastructure. A clear mental model of runner isolation, secret scoping, and job concurrency prevents accidental parallel deploys and secret exposure.

---

## Stage 2 — Deployment

**Goal**: Set up self-hosted runners, configure environments with protection rules, and establish a safe CI/CD promotion workflow from the start.

**Read**:

- [Deploy](../deploy/) — self-hosted runner registration (`./config.sh --url ... --token ...`), runner group assignment, environment creation with required reviewers and deployment branch policies, and OIDC provider setup in AWS/Azure
- [Install & Upgrade](../operations/install-upgrade/) — runner software auto-update configuration, action version pinning with commit SHA refs (`uses: actions/checkout@<SHA>`), and `actions/runner` release monitoring

**Deployment principles**:

- Pin third-party actions to full commit SHAs, not tags — tags are mutable and can be updated to deliver malicious code
- Use GitHub Environments with required reviewer approval gates for all deployments to production
- Register self-hosted runners as a service (systemd / Windows service) so they survive server reboots automatically

---

## Stage 3 — Operations

**Goal**: Monitor workflow health, manage runner capacity, and maintain reliable CI/CD pipelines across repositories.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; runner connectivity status in Settings → Actions → Runners, queued job depth, workflow failure rate over the past 24 hours, and environment deployment history
- [CLI Reference](../operations/cli-reference/) — `gh workflow list`, `gh workflow run`, `gh run list`, `gh run view`, `gh run watch`, `gh secret set`, `gh variable set` commands for workflow and secret management
- [Procedures](../operations/procedures/) — re-running failed jobs (`gh run rerun`), cancelling stuck workflows, rotating repository and organisation secrets, and adding a new reusable workflow to the shared library
- [Backup & Restore](../operations/backup-restore/) — workflow files are in Git (backed up with the repository), secret rotation runbook, and self-hosted runner rebuild from an Infrastructure-as-Code script
- [Scripts](../operations/scripts/) — composite actions for common steps (checkout + setup + cache), workflow dispatch wrapper scripts, runner health polling, and workflow run duration reporting

**Daily rhythm**: Runner status → queued job depth → overnight workflow failures → environment deployment history review.

---

## Stage 4 — Security

**Goal**: Prevent secret exposure, restrict workflow permissions, and enforce code-review gates on production deployments.

**Read**:

- [Access Control](../security/access-control/) — `permissions:` block to scope `GITHUB_TOKEN` to minimum required (e.g. `contents: read`), environment protection rules (required reviewers, branch policies), and runner group access controls
- [Authentication](../security/authentication/) — OIDC for AWS/Azure/GCP authentication from runners (no long-lived secrets), `secrets` vs `vars` context distinction, and GitHub Apps tokens vs PATs for machine access
- [Encryption](../security/encryption/) — GitHub encrypted secrets (AES-256 at rest), OIDC token audience and subject claim scoping, and log masking for secret values referenced in steps
- [Hardening](../security/hardening/) — avoiding `pull_request_target` with untrusted fork content, pinning actions to SHA, enabling minimum `GITHUB_TOKEN` permissions at the organisation level, and CodeQL code scanning as a required status check

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose workflow failures, runner issues, and permission errors without re-running blindly against production deployments.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — runner offline (service stopped or network blocked), OIDC token exchange failure (audience mismatch or trust policy), environment approval timeout, matrix job partial failure, and expression evaluation errors
- [Diagnostics](../troubleshooting/diagnostics/) — enabling `ACTIONS_STEP_DEBUG=true` and `ACTIONS_RUNNER_DEBUG=true` secrets, downloading full job logs via `gh run download`, inspecting runner `_diag/` log files, and verifying OIDC subject claims against the cloud trust policy
- [Escalation](../troubleshooting/escalation/) — GitHub Support ticket creation via github.com/contact/support (include run URL and runner ID), `actions/runner` GitHub repository for self-hosted runner bugs, and community GitHub Actions forums for workflow syntax questions

**Why last**: Troubleshooting makes most sense once you understand the event model, runner lifecycle, job concurrency controls, and secret scoping under normal workflow execution.
