---
tags:
  - aws
  - learning-path
---
# AWS — Learning Path

<div class="kb-summary">
Recommended reading order for AWS. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: AWS*
</div>

```text
┌───────────────────────────────────────── AWS — Learning Path ─────────────────────────────────────────┐
│                                                                                                       │
│    5 stages in order: Architecture → Deploy → Operations → Security → Troubleshoot                    │
│                                                                                                       │
│   ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│   │  Architecture  │  │     Deploy     │  │    Operations   │  │    Security    │  │  Troubleshoot  │ │
│   │                │  │                │  │                 │  │                │  │                │ │
│   │  How It Works  │  │ Initial Setup  │  │  Health Checks  │  │ Access Control │  │ Common Issues  │ │
│   │Design Standards│  │Install/Upgrade │  │  CLI Reference  │  │ Authentication │  │  Diagnostics   │ │
│   │  Integrations  │  │                │  │    Procedures   │  │   Encryption   │  │   Escalation   │ │
│   │                │  │                │  │ Backup & Restore│  │   Hardening    │  │                │ │
│   │                │  │                │  │     Scripts     │  │                │  │                │ │
│   └────────────────┘  └────────────────┘  └─────────────────┘  └────────────────┘  └────────────────┘ │
│                                                                                                       │
│    Stage 1 (Architecture) builds understanding. Stage 3 (Operations) is daily work. Troubleshoot last.│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```
| Stage | Focus | Time investment |
|-------|-------|----------------|
| 1 — Architecture | Account model, VPC, IAM fundamentals | 4–6 h |
| 2 — Deployment | IaC, AMI lifecycle, patching | 2–3 h |
| 3 — Operations | CloudWatch, backups, runbooks | ongoing |
| 4 — Security | IAM hardening, compliance, encryption | 3–4 h |
| 5 — Troubleshooting | CloudTrail, Flow Logs, support | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand AWS's global infrastructure model, core service relationships, and how accounts, VPCs, and IAM interact before touching anything in the console.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — regions, AZs, edge locations, and the shared responsibility model; every service is a regional or global API endpoint called over TLS
- [Design Standards](../architecture/design-standards/) — multi-account strategy via AWS Organizations, landing zone patterns (Control Tower), VPC CIDR allocation, and tagging conventions for cost attribution
- [Integrations](../architecture/integrations/) — on-premises connectivity via Direct Connect and Site-to-Site VPN; IAM Identity Center (SSO) for federated access across all accounts

**Key concepts before moving on**:

- Every resource lives in a region and optionally an AZ; IAM, Route 53, and CloudFront are global services
- IAM evaluates policies in default-deny — an explicit deny always wins regardless of any allow
- VPC CIDR ranges cannot be changed after creation; get the address plan right the first time
- SCPs in Organizations restrict what even account-level admin roles can do — they are a hard ceiling

**Why first**: Every AWS decision — subnet sizing, IAM scope, cost — flows from account and network architecture. Get this wrong and everything else is harder to fix.

---

## Stage 2 — Deployment

**Goal**: Know how resources are provisioned and governed repeatably before managing any production workloads.

**Read**:

- [Deploy](../deploy/) — CloudFormation, CDK, and AWS CLI provisioning patterns; StackSets for multi-account/multi-region deployment; Service Catalog for governed self-service
- [Install & Upgrade](../operations/install-upgrade/) — AMI lifecycle via EC2 Image Builder, patch baselines in Systems Manager Patch Manager, and SSM Distributor for package distribution

**Deployment principles**:

- Never click-create production resources — use IaC (CloudFormation or Terraform) from day one
- Use CloudFormation change sets to preview all resource mutations before applying
- Test patch baselines in non-production before enabling auto-approval in production accounts
- Tag every resource at creation time; retrofitting tags to thousands of existing resources is painful

---

## Stage 3 — Operations

**Goal**: Run AWS environments confidently — monitoring costs, health, and platform state on every shift.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; CloudWatch dashboards, AWS Health events, alarm thresholds, and Trusted Advisor critical findings
- [CLI Reference](../operations/cli-reference/) — `aws ec2`, `aws s3`, `aws iam`, `aws rds`, `aws cloudwatch`, `aws ssm` patterns; `--query` JMESPath filtering and `--output table` for readability
- [Procedures](../operations/procedures/) — runbooks: EC2 instance recovery, EBS snapshot restore, account vending via Control Tower, RDS failover to read replica
- [Backup & Restore](../operations/backup-restore/) — AWS Backup vaults, backup plan schedules and retention periods, cross-region copy jobs, and restore testing cadence
- [Scripts](../operations/scripts/) — scripts for cost tag enforcement, stale resource cleanup, Security Hub finding suppression, and compliance report generation

**Daily rhythm**: Health Checks first → review CloudWatch alarms → verify Backup job outcomes → check Cost Explorer for anomalous spend.

---

## Stage 4 — Security

**Goal**: Enforce least-privilege access and continuous compliance across all accounts and regions.

**Read**:

- [Access Control](../security/access-control/) — IAM identity-based and resource-based policies, permission boundaries, SCPs, and the multi-layer policy evaluation logic
- [Authentication](../security/authentication/) — IAM Identity Center with external IdP federation (Entra ID, Okta), MFA enforcement via SCP, and role assumption patterns for cross-account access
- [Encryption](../security/encryption/) — KMS key management (AWS-managed vs customer-managed), S3 default encryption, EBS encryption, and Secrets Manager vs Parameter Store
- [Hardening](../security/hardening/) — Security Hub standards (CIS, AWS Foundational), GuardDuty findings triage, Inspector scan baselines, and Config rules for continuous drift detection

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose failures quickly using AWS-native tooling without guessing across service boundaries.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — EC2 connectivity failures (security group vs NACL vs route table), S3 permission errors, RDS slow queries, IAM `AccessDenied` denial diagnosis
- [Diagnostics](../troubleshooting/diagnostics/) — CloudTrail event lookup, VPC Flow Logs analysis, CloudWatch Logs Insights queries, and `aws iam simulate-principal-policy` for permission debugging
- [Escalation](../troubleshooting/escalation/) — opening AWS Support cases (severity selection, required evidence), Trusted Advisor, Service Quotas increase requests, and TAM escalation path

**Why last**: Troubleshooting makes most sense once you know the normal operating state and what correct AWS behaviour looks like across IAM, networking, and compute.

---

## See also

- [Aws — Deploy](../deploy/)
- [Aws — Procedures](../operations/procedures/)
- [Aws — Common Issues](../troubleshooting/common-issues/)
