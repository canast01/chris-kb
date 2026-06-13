---
tags:
  - github-actions
  - operations
---
# GitHub Actions — Install & Upgrade

```bash
cd /opt/actions-runner   # or wherever the runner is installed
./config.sh --version
```
```text
┌───────────────────────────────── GitHub Actions — Install & Upgrade ──────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  GitHub Actions is a hosted service — no server-side installation; manage self-hosted runners │   │
│   │    Self-hosted runner install: download from GitHub, configure, register, run as OS service   │   │
│   │   Runner updates: GitHub-hosted auto-update weekly; self-hosted manual or auto-update policy  │   │
│   │        ARC (Actions Runner Controller): Kubernetes-based auto-scaling runner deployment       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Self-Hosted Runner Setup           │  │            ARC Setup (Kubernetes)           │   │
│   │       1. Settings → Actions → Runners        │  │          helm install arc oci://...         │   │
│   │          2. Download runner package          │  │      kubectl apply -f runnerdeployment      │   │
│   │         3. ./config.sh --url --token         │  │          Set minRunners/maxRunners          │   │
│   │           4. sudo ./svc.sh install           │  │           Configure runner labels           │   │
│   │            5. sudo ./svc.sh start            │  │           Verify runners register           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ARC             = Actions Runner Controller; Kubernetes operator managing ephemeral runner pods│   │
│   │  Runner version  = must be within 30 days of latest; GitHub stops routing jobs to old runners │   │
│   │     Ephemeral     = --ephemeral flag: runner deregisters after each job; clean env per run    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```yaml
on: workflow_dispatch
jobs:
  validate:
    runs-on: [self-hosted, <runner-label>]
    steps:
      - run: echo "Runner version check"
      - run: cat /opt/actions-runner/.runner
```
