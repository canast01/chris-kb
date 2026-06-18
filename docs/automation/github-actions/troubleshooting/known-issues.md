---
tags:
  - troubleshooting
  - github-actions
  - automation
  - known-issues
---
# GitHub Actions — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known GitHub Actions bugs, error codes, and workarounds covering self-hosted runners, workflow failures, and secrets.

*Applies to: GitHub Actions (cloud), GitHub Enterprise self-hosted runners*
</div>

```text
┌─────────────────────────────────────────── GitHub Actions ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          CI/CD platform — cloud-hosted or self-hosted runners executing workflow YAML         │   │
│   │                  Protocols: HTTPS (TCP 443) to github.com · webhook callbacks                 │   │
│   │                  Management: Settings -> Actions (repo/org/enterprise level)                  │   │
│   │            Trigger -> Runner pickup -> Job steps -> Artifacts/Logs -> Status check            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Trigger           │  │        Workflow YAML        │  │     on: push/PR/schedule    │   │
│   │           Compute           │  │ Hosted / self-hosted runner │  │     Labels match runs-on    │   │
│   │           Identity          │  │     GITHUB_TOKEN / OIDC     │  │        Scoped per job       │   │
│   │           Secrets           │  │     Repo/org/env secrets    │  │        Masked in logs       │   │
│   │          Artifacts          │  │   actions/upload-artifact   │  │   90-day default retention  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  Hosted runner   │ Ephemeral VM/job │       HTTPS       │   GITHUB_TOKEN   │  GitHub-managed  │   │
│   │Self-hosted runner│ Customer compute │  HTTPS out (443)  │   Runner token   │Long-lived process│   │
│   │       OIDC       │ Cloud federation │       HTTPS       │    JWT claims    │  No static keys  │   │
│   │   Environments   │  Deploy gating   │        N/A        │    Reviewers     │ Protection rules │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: GitHub-hosted VM fleet (cloud) or customer-owned self-hosted runner hosts                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Workflow       = YAML file in .github/workflows defining triggers, jobs, and steps                   │
│  Runner         = the machine (hosted or self-hosted) that executes a job                             │
│  runs-on        = label selecting which runner picks up a job (e.g. ubuntu-latest)                    │
│  GITHUB_TOKEN   = auto-generated per-job token scoped to the triggering repository                    │
│  OIDC           = OpenID Connect; lets workflows get short-lived cloud creds, no secrets              │
│  Secret         = encrypted value set at repo/org/environment scope, masked in logs                   │
│  Environment    = named deployment target with optional required reviewers/wait timer                 │
│  Artifact       = file(s) uploaded by a job for later jobs or download, time-limited                  │
│  Matrix build   = one job definition fanned out across a grid of input variables                      │
│  Self-hosted    = customer-managed runner; needs outbound 443 to github.com, no inbound               │
│  Concurrency    = group key limiting/cancelling overlapping workflow runs                             │
│  Reusable wflow = workflow called by another workflow via workflow_call                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- GitHub Actions errors appear in the workflow run UI → expand failed step.
- Self-hosted runner logs: `<runner-dir>/_diag/Runner_*.log`.
- Most self-hosted runner issues are outbound connectivity (TCP 443 to github.com) or permissions.

## Self-Hosted Runners

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Runner shows `Offline` in GitHub | Any | Runner service stopped or TCP 443 to github.com blocked | Restart runner: `./svc.sh start` (Linux) or Services.msc (Windows); verify TCP 443 outbound | N/A |
| Runner idle — jobs not picked up | Any | Runner labels don't match workflow `runs-on` label | Match runner labels in Settings → Actions → Runners to workflow `runs-on` | N/A |
| `Error: Process completed with exit code 1` — generic | Any | Script error in job step | Check step output; add `set -e` to bash scripts for early exit on error | N/A |

## Secrets and Permissions

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Secret shows `***` in log but job fails with auth error | Any | Secret value incorrect or missing from environment level | Check secret is set at correct scope (repo/org/env); update value | N/A |
| `Resource not accessible by integration` — GitHub API call | Any | GITHUB_TOKEN lacks required permission | Add permission to workflow: `permissions: {contents: read, issues: write}` | N/A |

## Workflow Failures

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Workflow not triggering on push | Any | Branch filter or path filter not matching; or workflow YAML syntax error | Validate YAML; check `on.push.branches` filter | N/A |
| Job stuck in `Queued` indefinitely | Any | No available runner matching labels | Check runner availability in Settings → Actions → Runners | N/A |

## See also

- [GitHub Actions — Common Issues](common-issues/)
- [Ansible — Known Issues](../../ansible/troubleshooting/known-issues.md)
- [Terraform — Known Issues](../../terraform/troubleshooting/known-issues.md)
