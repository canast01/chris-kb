---
tags:
  - troubleshooting
  - terraform
  - automation
  - known-issues
---
# Terraform / OpenTofu — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Terraform and Terraform Enterprise bugs, error codes, and workarounds covering state management, provider errors, and locking.

*Applies to: Terraform 1.5.x / 1.9.x, TFE (Terraform Enterprise)*
</div>

```text
┌──────────────────────────────────────── Terraform / OpenTofu ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Infrastructure-as-code: declarative state-driven provisioning via providers          │   │
│   │           Protocols: HTTPS to provider APIs · HTTPS to remote state backend (S3/TFE)          │   │
│   │                   Management: terraform CLI / Terraform Enterprise (TFE) UI                   │   │
│   │           plan -> diff against state -> apply -> provider API calls -> state updated          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            State            │  │      State file + lock      │  │    S3/TFE/Consul backend    │   │
│   │          Providers          │  │    AWS/Azure/vSphere etc.   │  │       Plugin binaries       │   │
│   │          Execution          │  │       CLI / TFE agent       │  │     Local or remote runs    │   │
│   │           Modules           │  │    Registry / Git source    │  │      Reusable IaC units     │   │
│   │          Workspace          │  │        TFE workspace        │  │    Per-environment state    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  State backend   │  Stores tfstate  │       HTTPS       │    IAM/Token     │  Lock vs. races  │   │
│   │ Provider plugin  │ API translation  │ Provider-specific │   Cloud creds    │Versioned, cached │   │
│   │    TFE agent     │ Remote execution │    HTTPS to TFE   │   Agent token    │  On-prem access  │   │
│   │ Module registry  │Shared IaC modules│     HTTPS/Git     │ Token (priv reg) │ Public + private │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: CLI/agent host running terraform - state backend - target cloud/on-prem APIs               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  State file     = JSON record mapping resources to real infrastructure IDs                            │
│  State lock     = prevents two concurrent applies from corrupting the same state                      │
│  Provider       = plugin translating HCL resources into API calls for a platform                      │
│  Plan           = dry-run diff between desired config and current state                               │
│  Apply          = executes the plan, calling provider APIs to reach desired state                     │
│  Drift          = real infrastructure diverges from what state file records                           │
│  Module         = reusable bundle of resources with input variables and outputs                       │
│  TFE            = Terraform Enterprise; self-hosted remote run/state platform                         │
│  Workspace      = isolated state + variable set, typically one per environment                        │
│  Agent pool     = group of self-hosted runners executing TFE runs in private networks                 │
│  Parallelism    = max concurrent resource operations per apply (default 10)                           │
│  force-unlock   = manually clears a stuck state lock after confirming no other run                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Terraform errors appear in `terraform plan` / `terraform apply` output.
- TFE run errors appear in TFE UI → Workspace → Runs.
- State issues are the most dangerous — always backup state before manual state manipulation.

## State and Locking

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Error acquiring the state lock` | All | Previous run crashed without releasing lock | Force unlock: `terraform force-unlock <lock-id>` (confirm no other operation running) | N/A |
| `State file outdated — refresh required` | All | State file diverged from actual infrastructure | Run `terraform refresh` to re-sync state with reality | N/A |
| `Error loading state` — backend unreachable | All | S3 bucket or TFE not reachable | Verify backend connectivity (TCP 443 to S3/TFE); check credentials | N/A |

## Provider Errors

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Provider produced inconsistent result after apply` | All | Provider bug or timing issue (resource not ready) | Add `depends_on` or `time_sleep`; check provider GitHub issues | Depends on provider |
| `Error: 429 Too Many Requests` from cloud provider | All | Terraform parallelism too high for provider rate limits | Reduce parallelism: `terraform apply -parallelism=5` | N/A |
| `Error configuring Terraform AWS Provider: no valid credential sources found` | All | AWS credentials not available in execution environment | Set `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` or use IAM role | N/A |

## TFE (Enterprise)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| TFE agent not connecting | TFE | TCP 443 from agent to TFE blocked | Verify TCP 443 from agent host to TFE; check agent token is valid | N/A |
| Run stuck in `Planning` | TFE | Agent not available in agent pool | Check TFE → Settings → Agent Pools; ensure agent is online | N/A |

## See also

- [Terraform — Common Issues](common-issues.md)
- [Ansible — Known Issues](../../ansible/troubleshooting/known-issues/)
- [GitHub Actions — Known Issues](../../github-actions/troubleshooting/known-issues/)
