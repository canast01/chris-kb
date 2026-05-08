# AWS — Standards

> Part of the [Architecture](../) section.

---

## Tagging Policy

All AWS resources must carry these mandatory tags (enforced via AWS Config + SCPs):

| Tag Key | Example Value | Notes |
|---|---|---|
| `Environment` | `prod`, `staging`, `dev` | Lowercase; no abbreviations |
| `Owner` | `infra-team` | Team name, not individual |
| `CostCentre` | `CC-1234` | Finance cost centre code |
| `Application` | `erp-frontend` | Application or service name |

AWS Config rule `required-tags` flags non-compliant resources. SCP denies creation of EC2, RDS, S3 without tags.

## Naming Convention

Pattern: `<env>-<region>-<service>-<name>`

| Resource | Example |
|---|---|
| EC2 Instance | `prod-euw1-ec2-appserver-01` |
| RDS Instance | `prod-euw1-rds-orders` |
| S3 Bucket | `corp-prod-euw1-app-assets` |
| VPC | `prod-euw1-vpc` |
| Security Group | `prod-euw1-sg-alb-inbound` |
| IAM Role | `prod-ec2-role-appserver` |

Region abbreviations: `euw1` = eu-west-1, `use1` = us-east-1, `apse1` = ap-southeast-1.

## IAM Policy Standards

| Principle | Standard |
|---|---|
| No long-lived access keys | Humans use IAM Identity Center (SSO); machines use IAM Roles |
| Least privilege | All IAM policies scoped to minimum required actions and resources |
| No wildcard `*` on actions | Exception: read-only roles; document justification |
| SCP guardrails | Deny: root access without MFA, actions outside approved regions, disabling CloudTrail |
| Permission boundary | Apply to all IAM roles created by automation |

## S3 Standards

| Setting | Requirement |
|---|---|
| Block Public Access | Enabled on all buckets (account-level + bucket-level) |
| Server-side encryption | SSE-S3 minimum; SSE-KMS for sensitive data |
| Versioning | Enabled on all buckets containing production data |
| MFA delete | Enabled on backup/compliance buckets |
| Lifecycle rules | Transition to S3-IA after 30 days, Glacier after 90 days (for archival buckets) |
| Bucket policy | Deny HTTP (require HTTPS); deny cross-account unless explicitly required |

## IAM Policy Evaluation Logic

```mermaid
flowchart TD
    request["API Request"]
    explicitDeny{"Explicit Deny\nin any policy?"}
    scpAllow{"SCP allows\nthe action?"}
    iamAllow{"IAM policy\nexplicitly allows?"}
    resourcePolicy{"Resource-based policy\nallows?"}
    defaultDeny["Default DENY\nAccess denied"]
    allow["ALLOW\nRequest proceeds"]

    request --> explicitDeny
    explicitDeny -- Yes --> defaultDeny
    explicitDeny -- No --> scpAllow
    scpAllow -- No --> defaultDeny
    scpAllow -- Yes --> iamAllow
    iamAllow -- Yes --> allow
    iamAllow -- No --> resourcePolicy
    resourcePolicy -- Yes --> allow
    resourcePolicy -- No --> defaultDeny
```

## Security Standards

| Control | Standard |
|---|---|
| CloudTrail | All-region trail in all accounts; logs to centralised S3 in log-archive account |
| Config | Enabled in all regions; conformance pack with CIS AWS Foundations Benchmark |
| GuardDuty | Enabled in all accounts via Organizations; alert forwarded to Security Tooling account |
| Security Hub | Enabled org-wide; aggregate to Security Tooling account |
| VPC Flow Logs | Enabled on all VPCs; logs to S3 or CloudWatch |
| Default VPC | Deleted from all regions on account creation |

## Approved Regions

AWS resources may only be deployed in approved regions (enforced via SCP):
- `eu-west-1` (Dublin) — primary
- `eu-west-2` (London) — secondary
- `us-east-1` — if required for global AWS services

Deploying to other regions requires an exception approved by InfoSec.

## VPC Architecture

```mermaid
flowchart TD
    subgraph vpc["VPC — 10.x.0.0/16"]
        subgraph az1["Availability Zone A"]
            pubSubA["Public Subnet /24\nALB · NAT GW"]
            privSubA["Private Subnet /24\nEC2 · ECS · Lambda"]
            isoSubA["Isolated Subnet /24\nRDS · ElastiCache"]
        end
        subgraph az2["Availability Zone B"]
            pubSubB["Public Subnet /24"]
            privSubB["Private Subnet /24"]
            isoSubB["Isolated Subnet /24"]
        end
        igw["Internet Gateway"]
        natGw["NAT Gateway"]
        sg["Security Groups\nstateful · deny-all default"]
    end
    internet["Internet"]
    onprem["On-Premises\nvia Transit Gateway"]

    internet <--> igw <--> pubSubA & pubSubB
    pubSubA --> natGw --> privSubA --> isoSubA
    pubSubB --> privSubB --> isoSubB
    onprem <--> privSubA & privSubB
```

## Network Standards

| Setting | Standard |
|---|---|
| VPC CIDR | /16 per account per region; no overlapping CIDRs across accounts |
| Subnet sizing | /24 per AZ per tier |
| NAT Gateway | One per AZ (not one per VPC) |
| Security Groups | Stateful; deny all inbound by default; explicit allow rules only |
| NACLs | Stateless; use as additional layer for subnet boundaries |
| Flow Logs | Enabled on all VPCs; ALL traffic, not REJECT only |
