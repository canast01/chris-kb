---
tags:
  - github-actions
  - troubleshooting
search:
  boost: 1.5
---
# GitHub Actions — Common Issues

<div class="kb-summary">
GitHub Actions troubleshooting: failed steps, permission errors, runner connectivity issues, secret resolution failures, and cache invalidation problems.

*Applies to: GitHub Actions*
</div>

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
common_failures: "Common Failures" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> common_failures: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
common_failures -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "Common Failures\n— adjust on.branches or on.paths filter" {shape: rectangle}
R2: "Common Failures\n— merge workflow file to default branch" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Common Failures\n— check repo vs env vs org secret scope" {shape: rectangle}
R4: "Common Failures\n— verify step can access secrets context" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "Common Failures\n— add working-directory: or cd in step" {shape: rectangle}
R6: "Common Failures\n— check artifact path glob matches files" {shape: rectangle}
D4: "D4" {shape: rectangle}
R7: "Common Failures\n— fix runs-on label or register runner" {shape: rectangle}
R8: "Common Failures\n— restart runner service on host" {shape: rectangle}
B5: "B5" {shape: rectangle}
R9: "Common Failures\n— add permissions: block with required scopes" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}
B4: "B4" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
D4 -> R7
D4 -> R8
B5 -> R9
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Common Failures

```d2
direction: right

failure: "Workflow failure\nor unexpected behaviour" {shape: rectangle}
noTrigger: "noTrigger" {shape: rectangle}
checkPaths: "Check on.paths filter\nDoes it match the changed files?" {shape: rectangle}
stepFail: "stepFail" {shape: rectangle}
permErr: "Resource not accessible\n→ Add permissions: block to job" {shape: rectangle}
ctxErr: "Context access invalid\n→ Fix ${{ }} expression syntax" {shape: rectangle}
exitErr: "Exit code 1\n→ Check step output in logs" {shape: rectangle}
secretErr: "Secret is empty\n→ Check repo vs env vs org scope" {shape: rectangle}
wdErr: "No such file\n→ Add working-directory: or cd" {shape: rectangle}

failure -> noTrigger
noTrigger -> checkPaths
noTrigger -> stepFail
stepFail -> permErr
stepFail -> ctxErr
stepFail -> exitErr
stepFail -> secretErr
stepFail -> wdErr
```

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [GitHub Actions — Diagnostics](../diagnostics/)
- [GitHub Actions — Escalation](../escalation/)
- [GitHub Actions — Health Checks](../../operations/health-checks/)
