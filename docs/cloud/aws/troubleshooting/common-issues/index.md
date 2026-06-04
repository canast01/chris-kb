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
