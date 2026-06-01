# AWS — Access Control


<div class="kb-summary">
Access Control reference covering IAM Fundamentals, Least-Privilege Policy Design, Cross-Account Access, Resource-Based Policies, Permission Boundary and 4 more sections.
</div>

---

## IAM Fundamentals

| Concept | Description |
|---|---|
| IAM User | Long-lived identity with access keys or password; avoid for services |
| IAM Role | Temporary credentials via STS; use for EC2, Lambda, ECS, cross-account |
| IAM Group | Collection of users sharing policies; cannot be used as a principal |
| IAM Policy | JSON document defining Allow/Deny on actions/resources |
| Permission Boundary | Max permissions a role/user can ever have, regardless of attached policies |
| SCP (Service Control Policy) | Org-level guardrail — applies to entire accounts, not individual principals |

---

## Least-Privilege Policy Design

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3ReadSpecificBucket",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-prod-bucket",
        "arn:aws:s3:::my-prod-bucket/*"
      ]
    }
  ]
}
```
┌─────────────────────────── AWS Access Control — Least-Privilege IAM Design ───────────────────────────┐
│                                                                                                       │
│  Layered access control using IAM policies, SCPs, permission boundaries, and resource policies.       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Policy Types                 │  │               Evaluation Order              │   │
│   │       Identity: user/role/group policy       │  │       1. Explicit deny anywhere → DENY      │   │
│   │      Resource: bucket/key/queue policy       │  │             2. SCP denies → DENY            │   │
│   │           SCP: org-level guardrail           │  │        3. Permission boundary limits        │   │
│   │       Permission boundary: max allowed       │  │       4. Session policy reduces scope       │   │
│   │       Session: temporary scoped token        │  │    5. Identity or resource allows → ALLOW   │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Default deny: no explicit allow means denied; all policy types must allow for access.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Least Privilege Design            │  │            Access Analysis Tools            │   │
│   │         Start with managed policies          │  │        IAM Access Analyzer: findings        │   │
│   │       Generate policy from CloudTrail        │  │          CloudTrail: last-used data         │   │
│   │     Remove unused permissions quarterly      │  │        Credential report: stale keys        │   │
│   │        Conditions: IP, time, MFA, tag        │  │       Config rule: no wildcard actions      │   │
│   │    Tag-based access: aws:RequestedRegion     │  │          Security Hub: IAM findings         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS IAM control plane · Global IAM service · Regional enforcement at API endpoints                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Explicit deny   = Deny statement that overrides any allow; highest priority in evaluation            │
│  SCP             = Service Control Policy; org-level ceiling; cannot grant new permissions            │
│  Permission boundary= IAM policy limiting the maximum permissions an entity can have                  │
│  Resource policy = Policy attached to a resource (S3 bucket, KMS key) controlling access              │
│  Session policy  = Policy passed with AssumeRole to further restrict the session                      │
│  Default deny    = No explicit allow = implicit deny; AWS denies by default                           │
│  IAM condition   = Policy element adding constraints: IP, MFA, time, tag, region                      │
│  Access Analyzer = Service that identifies cross-account or public resource access                    │
│  Policy generator= Tool that analyses CloudTrail to generate least-privilege policy                   │
│  aws:RequestedRegion= Condition key restricting actions to specified AWS regions                      │
│  Credential report= CSV of all IAM users with last sign-in and key usage timestamps                   │
│  Wildcard action = iam:* or s3:* in a policy grants all actions — avoid in production                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Resource-Based Policies

For S3, KMS, SQS, Lambda — attached to the resource, not the principal. Grant access without requiring IAM role assumptions.

```bash
# S3 bucket policy — allow specific role from another account
aws s3api put-bucket-policy --bucket my-bucket --policy '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<account-id>:role/DataProcessingRole"
      },
      "Action": ["s3:GetObject","s3:PutObject"],
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}'

# Deny public access to all buckets
aws s3control put-public-access-block \
  --account-id <account-id> \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

---

## Permission Boundary

```bash
# Create boundary policy (max permissions this role can have)
aws iam create-policy \
  --policy-name DeveloperBoundary \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": ["ec2:*","s3:*","rds:Describe*","cloudwatch:*"],
        "Resource": "*"
      },
      {
        "Effect": "Deny",
        "Action": ["iam:*","organizations:*","account:*"],
        "Resource": "*"
      }
    ]
  }'

# Apply boundary when creating role
aws iam create-role \
  --role-name DeveloperRole \
  --assume-role-policy-document file://trust.json \
  --permissions-boundary arn:aws:iam::<account>:policy/DeveloperBoundary
```

---

## Policy Simulation

```bash
# Test whether a role can perform specific actions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::<account>:role/DeveloperRole \
  --action-names s3:PutObject s3:DeleteObject ec2:TerminateInstances iam:CreateUser \
  --resource-arns "arn:aws:s3:::my-bucket/*" \
  --query 'EvaluationResults[*].[EvalActionName,EvalDecision]' \
  --output table
```

---

## Access Advisor — Identify Unused Permissions

```bash
# Generate access advisor report for a role
JOB_ID=$(aws iam generate-service-last-accessed-details \
  --arn arn:aws:iam::<account>:role/DeveloperRole \
  --query 'JobId' --output text)

sleep 5

aws iam get-service-last-accessed-details --job-id $JOB_ID \
  --query 'ServicesLastAccessed[?TotalAuthenticatedEntities==`0`].[ServiceName,ServiceNamespace]' \
  --output table
# Services never accessed — candidates for removal from the policy
```

---

## AWS Organizations — SCPs

```bash
# List SCPs attached to an OU
aws organizations list-policies-for-target \
  --target-id ou-xxxx-yyyyyyyy \
  --filter SERVICE_CONTROL_POLICY \
  --query 'Policies[*].[Name,Id,Description]' \
  --output table

# Common SCP — deny leaving the organization
# Apply at root or management account level:
# {
#   "Effect": "Deny",
#   "Action": "organizations:LeaveOrganization",
#   "Resource": "*"
# }
```

---

## Audit — Privilege Review

```bash
# Users with AdministratorAccess
aws iam list-entities-for-policy \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess \
  --query '[PolicyUsers[*].UserName,PolicyRoles[*].RoleName,PolicyGroups[*].GroupName]' \
  --output table

# Roles with * on * (broad permissions) — review manually
aws iam list-roles --query 'Roles[*].RoleName' --output text | \
  tr '\t' '\n' | while read role; do
    POLICIES=$(aws iam list-attached-role-policies --role-name "$role" \
      --query 'AttachedPolicies[*].PolicyArn' --output text 2>/dev/null)
    echo "$role: $POLICIES"
  done
```
