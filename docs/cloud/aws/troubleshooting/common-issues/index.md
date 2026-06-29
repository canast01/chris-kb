---
tags:
  - aws
  - troubleshooting
search:
  boost: 1.5
---
# AWS Troubleshooting — Common Issues

```bash
# View the stack events to identify the failed resource
aws cloudformation describe-stack-events \
  --stack-name my-stack \
  --query 'StackEvents[?ResourceStatus==`UPDATE_FAILED`].[LogicalResourceId,ResourceStatusReason]' \
  --output table

# Continue rollback (skip specific resources if they're blocking)
aws cloudformation continue-update-rollback \
  --stack-name my-stack \
  --resources-to-skip LogicalResourceId1 LogicalResourceId2
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "EC2 Issues — SG and NACL check" {shape: rectangle}
D2: "D2" {shape: rectangle}
R2: "IAM Issues — bucket policy and BPA" {shape: rectangle}
D3: "D3" {shape: rectangle}
R3: "Storage Issues — RDS connectivity" {shape: rectangle}
D4: "D4" {shape: rectangle}
R4: "IAM Issues — execution role and concurrency" {shape: rectangle}
D5: "D5" {shape: rectangle}
R5: "Networking Issues — resource quota or policy" {shape: rectangle}
R6: "Verify resolution" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}

D1 -> R1
D2 -> R2
D3 -> R3
D4 -> R4
D5 -> R5
R1 -> R6
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Aws — Diagnostics](../diagnostics/)
- [Aws — Escalation](../escalation/)
- [Aws — Health Checks](../../operations/health-checks/)
