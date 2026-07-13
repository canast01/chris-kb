---
tags:
  - architecture
  - aws
description: "AWS integration patterns: Active Directory Connector, VPC peering and PrivateLink, API Gateway service mesh, EventBridge routing, and on-premises Direct..."
---
# AWS — Integrations

<div class="kb-summary">
AWS integration patterns: Active Directory Connector, VPC peering and PrivateLink, API Gateway service mesh, EventBridge routing, and on-premises Direct Connect.

*Applies to: AWS*
</div>

---

## S3 Object Lifecycle

```d2
direction: right

upload: "Object Upload\nS3 Standard" {shape: rectangle}
ia: "S3 Standard-IA\nafter 30 days" {shape: rectangle}
glacier: "S3 Glacier\nafter 90 days" {shape: rectangle}
deepArchive: "S3 Glacier Deep Archive\nafter 180 days (optional" {shape: rectangle}
expire: "Expiration\ndelete after retention period" {shape: rectangle}

upload -> ia
ia -> glacier
glacier -> deepArchive
deepArchive -> expire
```

**AD Connector** (proxy authentication to on-premises AD without replication):
```bash
aws ds create-ad-connector --name corp.local --password <svc-account-pwd> \
    --connect-settings VpcId=<vpc>,SubnetIds=<sub1>,<sub2>,CustomerDnsIps=<dc1-ip>,<dc2-ip>,CustomerUserName=svc_aws_connector
```


```text title="Expected output"
{
    "DirectoryId": "d-9067c8a2f1",
    "Name": "corp.local",
    "Status": "Creating",
    "Type": "ADConnector",
    "CreationDateTime": 1699564823.0,
    "VpcSettings": {
        "VpcId": "vpc-0a3f8c2e1b9d4f6a",
        "SubnetIds": [
            "subnet-0e2b1f4a8c3d9e7b",
            "subnet-1f3c2g5b9d4e0f8c"
        ],
        "SecurityGroupId": "sg-0d7e4c1a2f9b3e6d",
        "AvailabilityZones": [
            "us-east-1a",
            "us-east-1b"
        ]
    },
    "ConnectSettings": {
        "CustomerDnsIps": [
            "10.50.10.5",
            "10.50.10.6"
        ],
        "CustomerUserName": "svc_aws_connector",
        "SubnetIds": [
            "subnet-0e2b1f4a8c3d9e7b",
            "subnet-1f3c2g5b9d4e0f8c"
        ]
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidParameterException) when calling the CreateAdConnector operation: The password does not meet complexity requirements` | Ensure the service account password meets AWS AD Connector requirements (minimum 8 characters, uppercase, lowercase, number, and special character). |
    | `An error occurred (InvalidParameterException) when calling the CreateAdConnector operation: The specified subnet is not available in the VPC` | Verify both subnets exist in the specified VPC and are in different availability zones. |
    | `An error occurred (InvalidParameterException) when calling the CreateAdConnector operation: The specified DNS IP is not reachable` | Confirm the customer DNS IPs are reachable from the specified subnets and that security groups allow DNS traffic (port 53). |
## IAM Identity Center (SSO)

```bash
# List permission sets
aws sso-admin list-permission-sets --instance-arn <sso-instance-arn>

# List account assignments for a permission set
aws sso-admin list-account-assignments --instance-arn <sso-arn> \
    --account-id <account-id> --permission-set-arn <permission-set-arn>
```


```text title="Expected output"
{
    "PermissionSets": [
        "arn:aws:sso:::permissionSet/sso-instance-d-9067b21e64/ps-a1b2c3d4e5f6g7h8",
        "arn:aws:sso:::permissionSet/sso-instance-d-9067b21e64/ps-x9y8z7w6v5u4t3s2",
        "arn:aws:sso:::permissionSet/sso-instance-d-9067b21e64/ps-m2n3o4p5q6r7s8t9"
    ]
}
{
    "AccountAssignments": [
        {
            "AccountId": "123456789012",
            "PermissionSetArn": "arn:aws:sso:::permissionSet/sso-instance-d-9067b21e64/ps-a1b2c3d4e5f6g7h8",
            "PrincipalType": "USER",
            "PrincipalId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        },
        {
            "AccountId": "123456789012",
            "PermissionSetArn": "arn:aws:sso:::permissionSet/sso-instance-d-9067b21e64/ps-a1b2c3d4e5f6g7h8",
            "PrincipalType": "GROUP",
            "PrincipalId": "b2c3d4e5-f6a7-8901-bcde-f12345678901"
        }
    ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ValidationException) when calling the ListPermissionSets operation: 1 validation error detected: Value '<sso-instance-arn>' at 'instanceArn' failed to match pattern` | Replace `<sso-instance-arn>` with the actual SSO instance ARN (format: `arn:aws:sso:::instance/sso-instance-xxxxxxxx`). |
    | `An error occurred (ResourceNotFoundException) when calling the ListAccountAssignments operation: Permission set arn:aws:sso:::permissionSet/... does not exist` | Verify the permission set ARN exists by running the first command and copying an ARN from the output. |
    | `An error occurred (AccessDeniedException) when calling the ListPermissionSets operation: User is not authorized to perform: sso:ListPermissionSets` | Ensure your IAM user/role has `sso:ListPermissionSets` and `sso:ListAccountAssignments` permissions attached. |
## CloudTrail to SIEM

Centralise CloudTrail logs to the log-archive account:

```bash
# Verify CloudTrail is enabled in all regions
aws cloudtrail describe-trails --include-shadow-trails

# Verify log delivery is healthy
aws cloudtrail get-trail-status --name <trail-name> | jq '{LatestDeliveryTime, LatestDeliveryError}'
```


```text title="Expected output"
{
    "trailList": [
        {
            "Name": "org-audit-trail",
            "S3BucketName": "cloudtrail-logs-prod-us-east-1",
            "IncludeGlobalServiceEvents": true,
            "IsMultiRegionTrail": true,
            "HomeRegion": "us-east-1",
            "HasCustomEventSelectors": true,
            "HasInsightSelectors": false,
            "IsOrganizationTrail": true
        },
        {
            "Name": "regional-trail-eu-west-1",
            "S3BucketName": "cloudtrail-logs-prod-eu-west-1",
            "IncludeGlobalServiceEvents": false,
            "IsMultiRegionTrail": false,
            "HomeRegion": "eu-west-1",
            "HasCustomEventSelectors": false,
            "HasInsightSelectors": true,
            "IsOrganizationTrail": false
        }
    ]
}
{
  "LatestDeliveryTime": "2024-01-15T14:32:18Z",
  "LatestDeliveryError": null
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (TrailNotFoundException) when calling the DescribeTrails operation: Unknown trail: <trail-name>` | Verify the trail name exists in the current region with `aws cloudtrail describe-trails --region <region>`. |
    | `An error occurred (InvalidCloudTrailARNException) when calling the GetTrailStatus operation: Invalid CloudTrail ARN` | Use the exact trail name (not ARN) with `get-trail-status`, or provide the full ARN with the `--name` parameter. |
Stream to Splunk/Elastic via Kinesis Firehose:
1. Create Kinesis Data Firehose delivery stream to SIEM endpoint
2. Configure CloudWatch Logs subscription filter → Kinesis Firehose
3. Or use EventBridge → Lambda → SIEM API for enriched forwarding

## AWS Backup

```bash
# List backup plans
aws backup list-backup-plans

# Create backup plan for EC2 and RDS
aws backup create-backup-plan --backup-plan '{
  "BackupPlanName": "prod-daily",
  "Rules": [{
    "RuleName": "Daily",
    "TargetBackupVaultName": "prod-vault",
    "ScheduleExpression": "cron(0 2 * * ? *)",
    "DeleteAfterDays": 30
  }]
}'

# Enable cross-account backup (to log-archive account)
aws backup put-backup-vault-access-policy --backup-vault-name prod-vault --policy file://vault-policy.json
```


```text title="Expected output"
{
    "BackupPlansList": [
        {
            "BackupPlanArn": "arn:aws:backup:us-east-1:123456789012:backup-plan:a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "BackupPlanName": "prod-daily",
            "CreationDate": 1704067200.0,
            "LastUpdatedDate": 1704067200.0,
            "VersionId": "1"
        },
        {
            "BackupPlanArn": "arn:aws:backup:us-east-1:123456789012:backup-plan:f9e8d7c6-b5a4-3210-fedc-ba9876543210",
            "BackupPlanName": "legacy-weekly",
            "CreationDate": 1703462400.0,
            "LastUpdatedDate": 1703462400.0,
            "VersionId": "2"
        }
    ]
}
{
    "BackupPlanArn": "arn:aws:backup:us-east-1:123456789012:backup-plan:9f8e7d6c-5b4a-3210-fedc-ba9876543210",
    "BackupPlanId": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
    "CreationDate": 1704153600.0,
    "VersionId": "1"
}
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidParameterException) when calling the CreateBackupPlan operation: Invalid backup vault name` | Ensure the target backup vault exists first using `aws backup create-backup-vault --backup-vault-name prod-vault`. |
    | `An error occurred (AccessDenied) when calling the PutBackupVaultAccessPolicy operation: User is not authorized to perform: backup:PutBackupVaultAccessPolicy` | Add `backup:PutBackupVaultAccessPolicy` permission to your IAM role's backup policy. |
    | `An error occurred (InvalidParameterException) when calling the PutBackupVaultAccessPolicy operation: Invalid policy document` | Validate the JSON syntax in `vault-policy.json` and ensure it contains a valid principal ARN for the cross-account role. |
## CloudFormation Stack Lifecycle

```d2
direction: right

template: "Template\nJSON / YAML" {shape: rectangle}
validate: "Validate\naws cloudformation validate-template" {shape: rectangle}
createStack: "CREATE_IN_PROGRESS\nresource provisioning" {shape: rectangle}
complete: "CREATE_COMPLETE\nstack outputs available" {shape: rectangle}
update: "UPDATE_IN_PROGRESS\nchange set execution" {shape: rectangle}
rollback: "ROLLBACK_IN_PROGRESS\nfailure detected" {shape: rectangle}
deleteStack: "DELETE_IN_PROGRESS\nresource teardown" {shape: rectangle}

template -> validate
validate -> createStack
createStack -> complete
complete -> update
update -> complete
createStack -> rollback
update -> rollback
complete -> deleteStack
```

## GitHub Actions + OIDC

No static access keys — use OIDC federation:

```yaml
# .github/workflows/deploy.yml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::<account-id>:role/github-actions-deploy
    aws-region: eu-west-1
```

IAM trust policy for the role:
```json
{
  "Condition": {
    "StringEquals": {
      "token.actions.githubusercontent.com:sub": "repo:org/repo:ref:refs/heads/main"
    }
  }
}
```

## Terraform Remote State

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "corp-terraform-state-prod"
    key            = "prod/vpc/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "corp-terraform-locks"
    encrypt        = true
  }
}
```

One state bucket per environment; versioning and MFA-delete enabled on state bucket.

---

## See also

- [Aws — Design Standards](../design-standards/)
