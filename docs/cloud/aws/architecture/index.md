# AWS — Architecture

<div class="kb-summary">
Multi-account AWS platform managed through AWS Organizations with SCPs, IAM Identity Center SSO, and Transit Gateway hub-and-spoke networking. All production workloads run in dedicated member accounts; no workloads in the management account.
</div>

```
┌────────────────────────────────────── AWS Platform Architecture ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      AWS Platform Architecture — Multi-Account Organisation with Hub-and-Spoke Networking     │   │
│   │     Management Account: AWS Organizations root · SCPs · IAM Identity Center SSO · billing     │   │
│   │    Networking: Transit Gateway hub connects spoke VPCs across accounts and on-premises via    │   │
│   │  Workload accounts: dedicated member accounts per environment (dev/staging/prod) or per team  │   │
│   │ Guardrails: SCPs (preventive) + AWS Config (detective) + Security Hub (aggregated compliance) │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Management account controls governance · networking hub connects spokes                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         How It Works        │  │         Integrations        │  │       Design Standards      │   │
│   │  Organizations: root + OUs  │  │    On-prem: DirectConnect   │  │ Account structure: OU layout│   │
│   │   IAM Identity Center: SSO  │  │  IdP: Azure AD / Okta SAML  │  │   Tagging: env+owner+team   │   │
│   │  Transit Gateway: hub-spoke │  │ Monitoring: CloudWatch/SIEM │  │  Naming: account + resource │   │
│   │  SCPs: OU-level guardrails  │  │   Security: GuardDuty+Hub   │  │ Security baselines: CIS AWS │   │
│   │  Config: resource inventory │  │  Billing: CUR + Cost Expl.  │  │  No workloads in mgmt acct  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines OU layout and networking · Integrations connect IdP and on-prem               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Account Layer   │    Networking    │      Identity     │    Guardrails    │  Observability   │   │
│   │   Mgmt account   │ Transit Gateway  │  IAM Identity Ctr │   SCPs on OUs    │  CloudTrail org  │   │
│   │  Audit account   │ VPC per account  │     SSO groups    │    AWS Config    │ CloudWatch logs  │   │
│   │ Log archive acct │  DirectConnect   │  Permission sets  │   Security Hub   │  Cost Explorer   │   │
│   │Workload accounts │  VPC Endpoints   │    MFA enforced   │  GuardDuty org   │  Budgets+alerts  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Regions · Availability Zones · Data Centres · Global backbone · DirectConnect physical ports     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Organizations = AWS service for multi-account management; root contains management account and OUs   │
│  OU            = Organisational Unit; logical grouping of accounts; SCPs applied at OU level          │
│  SCP           = Service Control Policy; preventive guardrail; restricts what actions accounts can    │
│  IAM Identity Center= AWS SSO service; assigns permission sets to users/groups in member accounts     │
│  Transit Gateway= Regional hub router; connects VPCs across accounts and to on-premises via DX/VPN    │
│  DirectConnect = Dedicated private network connection from on-premises to AWS; bypasses internet      │
│  AWS Config    = Tracks resource configuration history; evaluates rules; records compliance state     │
│  Security Hub  = Aggregates findings from GuardDuty, Inspector, Config; scores security posture       │
│  GuardDuty     = Threat detection service; analyses CloudTrail, VPC Flow Logs, DNS logs for threats   │
│  CUR           = Cost and Usage Report; detailed billing data for chargeback and FinOps analysis      │
│  Permission set= IAM Identity Center policy assigned to a user/group for a specific member account    │
│  Management account= Root of the AWS Organization; no workloads; used for billing and org-level policy│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with on-premises, identity providers, and monitoring tools.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Account structure standards, tagging, naming, and security guardrails.</span></a>
</div>

## AWS Platform Overview

![AWS Multi-Account Architecture](../../../assets/aws-overview.svg)

## Service Domains

| Domain | Key Services |
|---|---|
| Networking | VPC, Transit Gateway, Direct Connect, Route 53, ALB/NLB, CloudFront |
| Compute | EC2, Auto Scaling, EKS, ECS/Fargate, Lambda |
| Storage | S3, EBS, EFS, FSx for Windows, FSx for ONTAP |
| Database | RDS, Aurora, DynamoDB, ElastiCache |
| Security | IAM, KMS, Secrets Manager, WAF, GuardDuty, Security Hub |
| Management | CloudWatch, CloudTrail, AWS Config, Systems Manager, CloudFormation |

## Account Structure

```mermaid
graph TB
  ORG["AWS Organization\n(management account)"] --> LOG["Log Archive Account"]
  ORG --> AUDIT["Audit / Security Account"]
  ORG --> PROD["Production Account\n(workload VPC)"]
  PROD --> VPC["VPC — 10.0.0.0/16"]
  VPC --> PUB["Public Subnets\nALB · NAT GW"]
  VPC --> PRIV["Private Subnets\nEC2 · RDS · EKS"]
  PUB --> IGW["Internet Gateway"]
  PRIV --> TGW["Transit Gateway\nhub-and-spoke"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  class ORG,LOG,AUDIT,PROD ctrl
  class VPC,PUB,PRIV net
  class IGW,TGW cloud
```
