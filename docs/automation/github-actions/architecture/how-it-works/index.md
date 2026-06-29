---
tags:
  - architecture
  - github-actions
---
# GitHub Actions — How It Works

<div class="kb-summary">
GitHub Actions is an event-driven CI/CD and automation platform embedded directly into GitHub repositories. It executes workflows in response to repository events, schedules, or external triggers.

*Applies to: GitHub Actions*
</div>

---

## Core Execution Model

```d2
direction: right

E: "Repository Event" {shape: rectangle}
W: "Workflow Triggered" {shape: rectangle}
Q: "Job Queue" {shape: rectangle}
R1: "Runner 1\nJob A" {shape: rectangle}
R2: "Runner 2\nJob B" {shape: rectangle}
S1: "Step 1: Checkout" {shape: rectangle}
S2: "Step 2: Build" {shape: rectangle}
S3: "Step 3: Test" {shape: rectangle}
S4: "Step 1: Lint" {shape: rectangle}
S5: "Step 2: Scan" {shape: rectangle}
A: "Upload Artifact" {shape: rectangle}
NOTIFY: "Notification / Downstream Jobs" {shape: rectangle}

E -> W
W -> Q
Q -> R1
Q -> R2
R1 -> S1
R1 -> S2
R1 -> S3
R2 -> S4
R2 -> S5
S3 -> A
S5 -> A
A -> NOTIFY
```

| Scope | Registration Level | Shared Across |
|---|---|---|
| Repository | Single repository settings | That repo only |
| Organisation | Organisation settings | All repos granted access |
| Enterprise | Enterprise settings | All orgs in the enterprise |

!!! warning "Self-Hosted Runner Security"
    Never run self-hosted runners on public repositories — a forked PR can execute arbitrary code on the host.

---

## Concurrency

Concurrency groups prevent duplicate workflow runs for the same logical scope.

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

---

## Artifacts

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: dist-package
    path: dist/
    retention-days: 30

- uses: actions/download-artifact@v4
  with:
    name: dist-package
    path: dist/
```

| Limit | Value |
|---|---|
| Default retention | 90 days |
| Maximum size per artifact | 10 GB |

---

## Platform Limits

| Limit | GitHub Free | GitHub Team | GitHub Enterprise |
|---|---|---|---|
| Concurrent jobs (Linux, hosted) | 20 | 60 | 180 |
| Job execution timeout | 6 hours | 6 hours | 6 hours |
| Artifact storage included | 500 MB | 2 GB | 50 GB |
| Cache storage per repository | 10 GB | 10 GB | 10 GB |
| Secrets per repository | 100 | 100 | 100 |

---

## See also

- [Github Actions — Design Standards](../design-standards/)
- [Github Actions — Integrations](../integrations/)
- [Github Actions — Deploy](../../deploy/)
