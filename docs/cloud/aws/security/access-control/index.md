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

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`An error occurred (NoSuchBucket) when calling the PutBucketPolicy operation: The specified bucket does not exist`** — Verify the bucket name is correct and exists in the current AWS region with `aws s3 ls`.
    **`An error occurred (InvalidPrincipal) when calling the PutBucketPolicy operation: Invalid principal in policy`** — Ensure the cross-account role ARN is correctly formatted and the role actually exists in the target account.
    **`An error occurred (AccessDenied) when calling the PutPublicAccessBlock operation: User: arn:aws:iam::<account-id>:user/<user> is not authorized to perform: s3:PutAccountPublicAccessBlock`** — Add `s3:PutAccountPublicAccessBlock` permission to your IAM user or role policy.
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

```text title="Expected output"
{
    "Policy": {
        "PolicyName": "DeveloperBoundary",
        "PolicyId": "ANPA7K3Q9M2X5LBVWC8F",
        "Arn": "arn:aws:iam::487291847562:policy/DeveloperBoundary",
        "Path": "/",
        "DefaultVersionId": "v1",
        "AttachmentCount": 0,
        "PermissionsBoundaryUsageCount": 0,
        "IsAttachable": true,
        "Description": "",
        "CreateDate": "2024-01-15T14:32:18+00:00",
        "UpdateDate": "2024-01-15T14:32:18+00:00"
    }
}
{
    "Role": {
        "Path": "/",
        "RoleName": "DeveloperRole",
        "RoleId": "AROA5N8PQRST2UVWXYZ9",
        "Arn": "arn:aws:iam::487291847562:role/DeveloperRole",
        "CreateDate": "2024-01-15T14:32:22+00:00",
        "AssumeRolePolicyDocument": "%7B%22Version%22%3A%222012-10-17%22%2C...",
        "PermissionsBoundary": {
            "PermissionsBoundaryType": "PermissionsBoundary",
            "PermissionsBoundaryArn": "arn:aws:iam::487291847562:policy/DeveloperBoundary"
        },
        "MaxSessionDuration": 3600
    }
}
```

!!! warning "Common errors"
    **`An error occurred (NoSuchEntity) when calling the CreateRole operation: The trust.json file does not exist`** — Ensure the trust.json file exists in the current directory with valid assume-role-policy-document JSON.
    **`An error occurred (InvalidInput) when calling the CreateRole operation: Invalid ARN specified in the request`** — Replace `<account>` with your actual AWS account ID (12-digit number).
    **`An error occurred (EntityAlreadyExists) when calling the CreatePolicy operation: Policy DeveloperBoundary already exists`** — Use a unique policy name or delete the existing policy with `aws iam delete-policy --policy-arn arn:aws:iam::ACCOUNT:policy/DeveloperBoundary` first.
```bash
# Test whether a role can perform specific actions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::<account>:role/DeveloperRole \
  --action-names s3:PutObject s3:DeleteObject ec2:TerminateInstances iam:CreateUser \
  --resource-arns "arn:aws:s3:::my-bucket/*" \
  --query 'EvaluationResults[*].[EvalActionName,EvalDecision]' \
  --output table
```

```text title="Expected output"
---------------------------------
|      EvalActionName      | EvalDecision |
|---------------------------------|
| s3:PutObject             | allowed      |
| s3:DeleteObject          | allowed      |
| ec2:TerminateInstances   | implicitDeny |
| iam:CreateUser           | implicitDeny |
---------------------------------
```

!!! warning "Common errors"
    **`An error occurred (NoSuchEntity) when calling the SimulatePrincipalPolicy operation: The role with name DeveloperRole cannot be found.`** — Verify the role name exists in your AWS account and the ARN is correctly formatted with the correct account ID.
    
    **`An error occurred (InvalidInput) when calling the SimulatePrincipalPolicy operation: 1 validation error detected: Value 'arn:aws:s3:::my-bucket/*' at 'resourceArns' failed to satisfy constraint`** — Ensure all resource ARNs are valid; S3 bucket ARNs must use the format `arn:aws:s3:::bucket-name` or `arn:aws:s3:::bucket-name/*` for objects.
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

```text title="Expected output"
DQNP7K9M2X5L8Q3R
ServiceName                          ServiceNamespace
---------------------------------    ---------------------------------
AWS CloudFormation                   cloudformation
AWS Systems Manager                  ssm
Amazon Macie                          macie2
AWS Glue                              glue
Amazon Kinesis                        kinesis
(no output — command completes silently)
```

!!! warning "Common errors"
    **`An error occurred (NoSuchEntity) when calling the GenerateServiceLastAccessedDetails operation: The role with name DeveloperRole cannot be found.`** — Verify the role name exists in your AWS account and use the correct ARN format.
    **`An error occurred (AccessDenied) when calling the GenerateServiceLastAccessedDetails operation: User: arn:aws:iam::<account>:user/admin is not authorized to perform: iam:GenerateServiceLastAccessedDetails`** — Add `iam:GenerateServiceLastAccessedDetails` and `iam:GetServiceLastAccessedDetails` permissions to your IAM user or role.
    **`InvalidInput`** — Increase the sleep duration to 10-15 seconds if the job hasn't completed; the report generation is asynchronous and may not be ready immediately.
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

```text title="Expected output"
-------------------------------------------
|                 Name                 |            Id            |        Description        |
|----------------------------------------------|------|------|
| DenyLeavingOrganization              | p-xxxxxxxxxx             | Prevent member account exit |
| RestrictedS3Access                   | p-yyyyyyyyyy             | Limit S3 bucket operations  |
| DenyRootAccountUsage                 | p-zzzzzzzzzz             | Block root user activities  |
| EnforceEncryption                    | p-aaaaaaaaaaa            | Require encryption in transit|
-------------------------------------------
```

!!! warning "Common errors"
    **`An error occurred (TargetNotFoundException) when calling the ListPoliciesForTarget operation: You provided an invalid target id.`** — Verify the OU ID format matches `ou-xxxx-yyyyyyyy` and exists in your organization with `aws organizations list-organizational-units-for-parent --parent-id r-xxxx`.
    
    **`An error occurred (AccessDeniedException) when calling the ListPoliciesForTarget operation: User is not authorized to perform: organizations:ListPolicies`** — Ensure your IAM user or role has the `organizations:ListPolicies` permission attached in the management account.
    
    **`An error occurred (PolicyTypeNotEnabledException) when calling the ListPoliciesForTarget operation: SERVICE_CONTROL_POLICY is not enabled in this organization.`** — Enable SCPs by running `aws organizations enable-policy-type --root-id r-xxxx --policy-type SERVICE_CONTROL_POLICY` in the management account.
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
