---
tags:
  - aws
  - security
---
# AWS Access Control — Least-Privilege IAM Design

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
```bash
# Test whether a role can perform specific actions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::<account>:role/DeveloperRole \
  --action-names s3:PutObject s3:DeleteObject ec2:TerminateInstances iam:CreateUser \
  --resource-arns "arn:aws:s3:::my-bucket/*" \
  --query 'EvaluationResults[*].[EvalActionName,EvalDecision]' \
  --output table
```
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

```d2
direction: down

auth: "AWS\nAuthentication" {shape: rectangle}
administrator: "Administrator" {shape: rectangle}
operator: "Operator" {shape: rectangle}
auditor: "Auditor" {shape: rectangle}
readonly: "Read-Only" {shape: rectangle}
resources: Protected Resources {shape: cylinder}

auth -> administrator: grants
administrator -> resources: access
auth -> operator: grants
operator -> resources: access
auth -> auditor: grants
auditor -> resources: access
auth -> readonly: grants
readonly -> resources: access
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Aws — Authentication](../authentication/)
- [Aws — Hardening](../hardening/)
- [Aws — Encryption](../encryption/)
