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

```text
┌────────────────────────── GitHub Actions — Event-Driven CI/CD Architecture ───────────────────────────┐
│                                                                                                       │
│  Workflows defined in .github/workflows/*.yml trigger on events; jobs run                             │
│  in parallel on hosted or self-hosted runners; artifacts bridge job data.                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Workflow Triggers               │  │                Job Execution                │   │
│   │          push: branch/tag patterns           │  │          Jobs: parallel by default          │   │
│   │           pull_request: PR events            │  │           needs: serial dependency          │   │
│   │          schedule: cron expression           │  │         runs-on: hosted or self-host        │   │
│   │         workflow_dispatch: manual UI         │  │          matrix: fan-out test grid          │   │
│   │        repository_dispatch: API call         │  │         concurrency: cancel prev run        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Each job gets a fresh runner environment; checkout step clones the repo.                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   Runners                    │  │            Artifacts and Outputs            │   │
│   │        GitHub-hosted: ubuntu/win/mac         │  │        upload-artifact: persist files       │   │
│   │        Self-hosted: on-prem or cloud         │  │       download-artifact: between jobs       │   │
│   │       Self-hosted: labels for routing        │  │            outputs: string values           │   │
│   │         Larger runners: premium SKUs         │  │           cache: restore/save keys          │   │
│   │        Runner groups: org-level RBAC         │  │           secrets: encrypted vault          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  GitHub.com infrastructure for hosted runners; self-hosted: any VM/bare-metal                         │
│  running the actions/runner agent with outbound HTTPS to api.github.com.                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Workflow      = YAML file in .github/workflows/; one or more jobs                                    │
│  Event         = trigger: push, PR, schedule, dispatch, or repository event                           │
│  Job           = set of steps running on one runner; isolated environment                             │
│  Step          = shell command or action reference within a job                                       │
│  Runner        = compute that executes a job; ephemeral or persistent                                 │
│  Action        = reusable unit; marketplace or local composite/JS/Docker                              │
│  matrix        = strategy for fanning out jobs across param combinations                              │
│  needs         = job dependency; downstream job waits for upstream                                    │
│  concurrency   = prevents duplicate runs; cancel-in-progress for PRs                                  │
│  artifact      = file(s) persisted from a job; available for 90 days                                  │
│  OIDC          = OpenID Connect; grant cloud access without stored secrets                            │
│  Secrets       = encrypted repo/org values; injected as env vars at runtime                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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

