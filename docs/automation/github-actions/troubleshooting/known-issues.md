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
┌────────────────────────────── Automation Github Actions Troubleshooting ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Github Actions: Automation Github Actions Troubleshooting platform              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │            Management: Automation Github Actions Troubleshooting management console           │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Automation Github Actions Troubleshooting infrastructure · management network · monitor  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Github Actions     = Automation Github Actions Troubleshooting platform overview and core concept  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
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

- [GitHub Actions — Common Issues](common-issues.md)
- [Ansible — Known Issues](../../ansible/troubleshooting/known-issues/)
- [Terraform — Known Issues](../../terraform/troubleshooting/known-issues/)
