---
tags:
  - github-actions
  - operations
---
# GitHub Actions — Operations



<div class="kb-summary">
GitHub Actions — Operations reference: CLI Reference, Health Checks, Procedures, Install & Upgrade, and 2 more.

*Applies to: GitHub Actions*
</div>

```text
┌───────────────────────────────────── GitHub Actions — Operations ─────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  GitHub Actions operations: runner management, workflow monitoring, billing, secret rotation  │   │
│   │        Self-hosted runner: install runner agent, register to org, manage as OS service        │   │
│   │   Monitor: job queuing time, runner availability, billing minutes, failure rate per workflow  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Runner Operations               │  │             Workflow Operations             │   │
│   │         Register self-hosted runner          │  │           Monitor job queue times           │   │
│   │         Update runner agent software         │  │              Re-run failed jobs             │   │
│   │            Scale runner pool size            │  │            Cancel stuck workflows           │   │
│   │             Rotate runner tokens             │  │          Update pinned action SHAs          │   │
│   │           Monitor runner disk/CPU            │  │            Review billing minutes           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │Runner groups   = org-level grouping; restrict which repos can use specific self-hosted runners│   │
│   │   Actions Runner Controller (ARC) = Kubernetes operator for auto-scaling self-hosted runners  │   │
│   │   Billing minutes = GitHub-hosted runner usage billed per minute; free tier: 2000 min/month   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Commands, syntax, and quick reference.</span></a>
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Routine checks, service validation, and status verification.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Day-to-day operational tasks and how-to guides.</span></a>
<a class="kb-card" href="install-upgrade/"><strong>Install & Upgrade</strong><span>Installation, upgrade, patching, and decommission.</span></a>
<a class="kb-card" href="backup-restore/"><strong>Backup & Restore</strong><span>Backup configuration, restore procedures, and validation.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts and reusable code.</span></a>
</div>

