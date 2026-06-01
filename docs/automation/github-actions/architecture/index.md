# GitHub Actions — Architecture

<div class="kb-summary">
Event-driven CI/CD platform embedded in GitHub repositories; workflows defined in YAML trigger on push, PR, schedule, or API call; jobs run in parallel on hosted or self-hosted runners; artifacts and outputs bridge job data.
</div>

```text
┌──────────────────────────────────── GitHub Actions — Architecture ────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     GitHub Actions architecture: GitHub.com hosts the control plane; runners execute jobs     │   │
│   │       Self-hosted runners poll GitHub Actions API over HTTPS — no inbound port required       │   │
│   │       Runner groups: org or repo-level; assign self-hosted runners to specific workflows      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 How It Works                 │  │               Design Standards              │   │
│   │          Push → trigger → queue job          │  │              Pin actions to SHA             │   │
│   │         Runner picks up job via poll         │  │         Minimal permissions in token        │   │
│   │          Steps execute sequentially          │  │          Use environments for prod          │   │
│   │        Results reported to GitHub UI         │  │           Cache deps, not secrets           │   │
│   │           Logs streamed live to UI           │  │         Matrix over copy-paste jobs         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Physical: GitHub-hosted runners are ephemeral VMs; self-hosted are VMs or bare-metal on-prem │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
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


