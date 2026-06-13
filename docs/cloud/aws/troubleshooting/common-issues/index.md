---
tags:
  - aws
  - troubleshooting
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
```text
┌───────────────────────────────── AWS Troubleshooting — Common Issues ─────────────────────────────────┐
│                                                                                                       │
│  Common AWS issues and their resolution patterns across EC2, networking, IAM, and storage.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  EC2 Issues                  │  │              Networking Issues              │   │
│   │     Cannot connect SSH: check SG port 22     │  │        No internet: check IGW + route       │   │
│   │     Instance unreachable: status checks      │  │      Private cannot reach internet: NAT     │   │
│   │       High CPU: CloudWatch CPU metric        │  │       Cross-VPC: peering + routes set       │   │
│   │     Disk full: extend EBS or clean logs      │  │      DNS not resolving: check VPC attr      │   │
│   │        Out of memory: check processes        │  │       ELB 502: target unhealthy check       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Check SG, NACL, route table, and IGW in order for networking issues.                                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  IAM Issues                  │  │                Storage Issues               │   │
│   │     AccessDenied: check CT + policy sim      │  │      S3 403: check bucket policy + BPA      │   │
│   │         SCP blocking: check org SCPs         │  │      EBS perf: IOPS exhausted check CW      │   │
│   │     Role assume fail: trust policy check     │  │        RDS slow: Performance Insights       │   │
│   │       Credential expired: re-login SSO       │  │      EFS mount fail: check SG port 2049     │   │
│   │      MFA required: check condition key       │  │       Snapshot failed: IAM permission       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS EC2 host hardware · Regional network fabric · CloudTrail audit infrastructure                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Status check    = EC2 system check (AWS infra) or instance check (OS); both must pass                │
│  AccessDenied    = IAM explicit deny, missing allow, SCP block, or boundary restriction               │
│  Policy simulator= IAM tool testing policy evaluation for a given principal and action                │
│  BPA             = Block Public Access; S3 setting preventing public access                           │
│  Trust policy    = IAM role policy allowing specific principals to call AssumeRole                    │
│  SCP blocking    = Service Control Policy at org level blocking the API action                        │
│  ELB 502         = Bad Gateway; target returned invalid response; check app health                    │
│  VPC DNS attrs   = enableDnsHostnames + enableDnsSupport; must be on for DNS to work                  │
│  IOPS exhausted  = Volume throughput limit hit; upgrade to gp3 with higher IOPS                       │
│  Performance Insights= RDS tool showing wait events and top SQL for slow queries                      │
│  NFS port 2049   = EFS mount requires TCP 2049 open in mount target security group                    │
│  Credential expired= SSO tokens expire; run aws sso login to refresh                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
