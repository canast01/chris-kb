---
tags:
  - aws
  - troubleshooting
search:
  boost: 1.5
---
# AWS Troubleshooting — Common Issues
![AWS Troubleshooting — Common Issues](../../../../assets/cloud-aws-troubleshooting-common-issues-index.svg)


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


## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> D1{EC2 instance\nunreachable?}
    S --> D2{S3 access\ndenied?}
    S --> D3{RDS connection\nrefused?}
    S --> D4{Lambda\nthrottling?}
    S --> D5{CloudFormation\nstack rollback?}
    D1 --> R1[EC2 Issues — SG and NACL check]
    D2 --> R2[IAM Issues — bucket policy and BPA]
    D3 --> R3[Storage Issues — RDS connectivity]
    D4 --> R4[IAM Issues — execution role and concurrency]
    D5 --> R5[Networking Issues — resource quota or policy]
    R1 --> R6[Verify resolution]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6 section
    class D1,D2,D3,D4,D5 decision
    class S start
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
