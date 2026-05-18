# AWS — Access Control

```
┌──────────────────────────────────────────────────────────┐
│           IAM Policy Evaluation Order                    │
└──────────────────────────────────────────────────────────┘

  Principal makes API request
           │
           ▼
  ┌─────────────────┐   Explicit Deny?  ──► DENY
  │  SCP check      │
  │  (Org-level)    │   Not allowed?    ──► DENY
  └────────┬────────┘
           ▼
  ┌─────────────────┐   Explicit Deny?  ──► DENY
  │  Permission     │
  │  Boundary       │   Not in boundary?──► DENY
  └────────┬────────┘
           ▼
  ┌─────────────────┐   Explicit Deny?  ──► DENY
  │  Identity-based │
  │  Policy (IAM)   │
  └────────┬────────┘
           ▼
  ┌─────────────────┐   Explicit Deny?  ──► DENY
  │  Resource-based │
  │  Policy (S3/KMS)│   No Allow found? ──► DENY
  └────────┬────────┘
           │  All checks passed
           ▼
         ALLOW ✓
```

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

Attach to a role, not a user. Use resource ARNs, not `*`, wherever possible.

---

## IAM Role for EC2 (Instance Profile)

```bash
# Create a trust policy for EC2
cat > trust-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create the role
aws iam create-role \
  --role-name ec2-app-role \
  --assume-role-policy-document file://trust-policy.json

# Attach a policy
aws iam attach-role-policy \
  --role-name ec2-app-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Create instance profile and link role
aws iam create-instance-profile --instance-profile-name ec2-app-profile
aws iam add-role-to-instance-profile \
  --instance-profile-name ec2-app-profile \
  --role-name ec2-app-role

# Attach to running instance
aws ec2 associate-iam-instance-profile \
  --instance-id i-0abc123 \
  --iam-instance-profile Name=ec2-app-profile
```

---

## Cross-Account Access

```bash
# In the target account — create role with trust for source account
cat > cross-account-trust.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::<source-account-id>:root"},
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {"sts:ExternalId": "my-external-id"}
      }
    }
  ]
}
EOF

aws iam create-role \
  --role-name CrossAccountReadRole \
  --assume-role-policy-document file://cross-account-trust.json

# In the source account — assume the target role
aws sts assume-role \
  --role-arn arn:aws:iam::<target-account>:role/CrossAccountReadRole \
  --role-session-name audit-session \
  --external-id my-external-id
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
