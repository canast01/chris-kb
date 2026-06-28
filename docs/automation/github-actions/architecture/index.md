---
tags:
  - architecture
  - github-actions
---
# GitHub Actions — Architecture

<div class="kb-summary">
Event-driven CI/CD platform embedded in GitHub repositories; workflows defined in YAML trigger on push, PR, schedule, or API call; jobs run in parallel on hosted or self-hosted runners; artifacts and outputs bridge job data.

*Applies to: GitHub Actions*
</div>

![GitHub Actions — Architecture — Diagram](../../../assets/automation-github-actions-architecture-diagram.svg)
![GitHub Actions Architecture](../../../assets/github-actions-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Events, workflows, jobs, steps, runners, concurrency, and artifacts.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Integration with other platforms and external systems.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing guidelines, design standards, and best practices.</span>
</a>

</div>

## GitHub-Hosted Runner Specs

| Label | OS | vCPU | RAM |
|---|---|---|---|
| `ubuntu-24.04` / `ubuntu-latest` | Ubuntu 24.04 LTS | 4 | 16 GB |
| `ubuntu-22.04` | Ubuntu 22.04 LTS | 4 | 16 GB |
| `windows-2022` / `windows-latest` | Windows Server 2022 | 4 | 16 GB |
| `macos-15` / `macos-latest` | macOS 15 (ARM, M1) | 4 | 14 GB |

## Core Execution Model

