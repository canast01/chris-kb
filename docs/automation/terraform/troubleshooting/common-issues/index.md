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

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
terraform_troubleshooting_decision_f: "Terraform Troubleshooting Decision Flow" {shape: rectangle}
workspace_issues: "Workspace Issues" {shape: rectangle}
common_error_reference: "Common Error Reference" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> terraform_troubleshooting_decision_f: investigate
symptom -> workspace_issues: investigate
symptom -> common_error_reference: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
terraform_troubleshooting_decision_f -> resolution
workspace_issues -> resolution
common_error_reference -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "Common Error Reference\n— set AWS_/ARM_ env vars" {shape: rectangle}
R2: "Terraform Troubleshooting Decision Flow\n— terraform init -upgrade" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Common Error Reference\n— terraform force-unlock LOCK_ID" {shape: rectangle}
R4: "Workspace Issues\n— wait for concurrent run to finish" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "Common Error Reference\n— terraform state rm then import" {shape: rectangle}
R6: "Terraform Troubleshooting Decision Flow\n— terraform import resource.type.name id" {shape: rectangle}
B4: "B4" {shape: rectangle}
R7: "Workspace Issues\n— check provider timeout settings" {shape: rectangle}
B5: "B5" {shape: rectangle}
R8: "Common Error Reference\n— terraform graph to visualise cycle" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
B4 -> R7
B5 -> R8
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

```d2
direction: right

failure: "Terraform Error\nor Unexpected Behaviour" {shape: rectangle}
errType: "Error category?" {shape: rectangle}
checkCreds: "Check cloud credentials\naws sts get-caller-identity" {shape: rectangle}
fixCreds: "Set AWS_ / ARM_\nenvironment variables" {shape: rectangle}
checkLock: "Identify lock holder\n(error message shows lock ID" {shape: rectangle}
forceUnlock: "terraform force-unlock\n<LOCK_ID>" {shape: rectangle}
rmImport: "terraform state rm\nthen terraform import" {shape: rectangle}
initUpgrade: "terraform init -upgrade\nupdate lock file" {shape: rectangle}
graphCmd: "terraform graph | dot\nvisualise dependency tree" {shape: rectangle}
refreshOnly: "terraform apply\n-refresh-only" {shape: rectangle}
enableDebug: "TF_LOG=DEBUG\nTF_LOG_PATH=debug.log" {shape: rectangle}
reviewLog: "Review provider\nAPI call trace" {shape: rectangle}

failure -> errType
errType -> checkCreds
checkCreds -> fixCreds
errType -> checkLock
checkLock -> forceUnlock
errType -> rmImport
errType -> initUpgrade
errType -> graphCmd
errType -> refreshOnly
errType -> enableDebug
enableDebug -> reviewLog
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


```text title="Expected output"
default
  staging
* production

staging

(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: workspace "old-workspace" does not exist`** — Verify the workspace name with `terraform workspace list` before attempting deletion.
    **`Error: Cannot delete the currently selected workspace`** — Switch to a different workspace with `terraform workspace select default` before deleting the target workspace.
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
