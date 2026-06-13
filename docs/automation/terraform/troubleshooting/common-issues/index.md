---
tags:
  - terraform
  - troubleshooting
search:
  boost: 1.5
---
# Terraform — Common Issues


<div class="kb-summary">
Common Issues reference covering Terraform Troubleshooting Decision Flow, Refresh and Reconciliation Issues, Workspace Issues, Common Error Reference.

*Applies to: Terraform 1.x*
</div>

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> B1{Provider auth\nerror?}
    S --> B2{State lock\nstuck?}
    S --> B3{Resource already\nexists error?}
    S --> B4{Plan or apply\ntimeout?}
    S --> B5{Dependency\ncycle in graph?}
    B1 -->|Yes| D1{Env vars\nset correctly?}
    D1 -->|No| R1[Common Error Reference\n— set AWS_/ARM_ env vars]
    D1 -->|Yes| R2[Terraform Troubleshooting Decision Flow\n— terraform init -upgrade]
    B2 -->|Yes| D2{Stale lock\nor active run?}
    D2 -->|Stale| R3[Common Error Reference\n— terraform force-unlock LOCK_ID]
    D2 -->|Active| R4[Workspace Issues\n— wait for concurrent run to finish]
    B3 -->|Yes| D3{Resource in\nanother state file?}
    D3 -->|Yes| R5[Common Error Reference\n— terraform state rm then import]
    D3 -->|No| R6[Terraform Troubleshooting Decision Flow\n— terraform import resource.type.name id]
    B4 -->|Yes| R7[Workspace Issues\n— check provider timeout settings]
    B5 -->|Yes| R8[Common Error Reference\n— terraform graph to visualise cycle]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8 section
    class B1,B2,B3,B4,B5,D1,D2,D3 decision
    class S start
```

---

## Before you begin

- **Access:** Provider credentials configured (`terraform login` or env vars)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Terraform Troubleshooting Decision Flow

```mermaid
flowchart TD
    failure["Terraform Error\nor Unexpected Behaviour"]
    failure --> errType{"Error category?"}
    errType -->|Provider auth| checkCreds["Check cloud credentials\naws sts get-caller-identity"]
    checkCreds -->|Invalid| fixCreds["Set AWS_ / ARM_\nenvironment variables"]
    errType -->|State locked| checkLock["Identify lock holder\n(error message shows lock ID)"]
    checkLock -->|Stale lock| forceUnlock["terraform force-unlock\n<LOCK_ID>"]
    errType -->|Resource exists in\nanother state| rmImport["terraform state rm\nthen terraform import"]
    errType -->|Provider version\nmismatch| initUpgrade["terraform init -upgrade\nupdate lock file"]
    errType -->|Cycle / dependency| graphCmd["terraform graph | dot\nvisualise dependency tree"]
    errType -->|Drift after apply| refreshOnly["terraform apply\n-refresh-only"]
    errType -->|Unknown| enableDebug["TF_LOG=DEBUG\nTF_LOG_PATH=debug.log"]
    enableDebug --> reviewLog["Review provider\nAPI call trace"]
```
```text
┌────────────────────────────────────── Terraform — Common Issues ──────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        Most frequent Terraform failures and their fixes                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Issue: Error acquiring the state lock                             │   │
│   │   Cause A: previous apply crashed → fix: terraform force-unlock <lock-id> from error message  │   │
│   │      Cause B: concurrent apply running → fix: wait for it to complete; check CI pipeline      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        Issue: Error: configuring Terraform AWS Provider                       │   │
│   │           Cause A: no credentials → fix: export AWS_PROFILE or configure OIDC in CI           │   │
│   │        Cause B: wrong region → fix: set region in provider block or AWS_DEFAULT_REGION        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Issue: Error: resource already exists                             │   │
│   │        Fix: identify resource ID from error → terraform import resource.type.name <id>        │   │
│   │  After import: terraform plan should show no changes if config matches the existing resource  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Workspace Issues

```bash
# Check current workspace
terraform workspace show

# List all workspaces
terraform workspace list

# Switch workspace
terraform workspace select staging

# Delete a workspace (must not be current; state must be empty)
terraform workspace select default
terraform workspace delete old-workspace

# Workspace-conditional logic in configuration
locals {
  is_production = terraform.workspace == "production"
}

resource "aws_instance" "web" {
  instance_type = local.is_production ? "t3.large" : "t3.micro"
}
```

## Common Error Reference

| Error message | Cause | Fix |
|---|---|---|
| `Error: No valid credential sources found` | AWS credentials missing | Set `AWS_ACCESS_KEY_ID` / configure `~/.aws/credentials` |
| `Error acquiring the state lock` | Concurrent run or stale lock | Wait for other run to finish or force-unlock |
| `Error: Provider configuration not present` | Missing provider block | Add `provider` block or `required_providers` |
| `Error: Reference to undeclared resource` | Typo in resource address | Check spelling; run `terraform state list` |
| `Error: cycle` | Circular dependency between resources | Use `depends_on` carefully; restructure dependencies |
| `Error: expected ... to be a string, got ...` | Variable type mismatch | Check `type` constraints in variable declarations |

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Terraform — Diagnostics](../diagnostics/)
- [Terraform — Escalation](../escalation/)
- [Terraform — Health Checks](../../operations/health-checks/)
