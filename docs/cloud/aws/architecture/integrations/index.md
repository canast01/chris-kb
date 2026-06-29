---
tags:
  - architecture
  - aws
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

## IAM Identity Center (SSO)

```bash
# List permission sets
aws sso-admin list-permission-sets --instance-arn <sso-instance-arn>

# List account assignments for a permission set
aws sso-admin list-account-assignments --instance-arn <sso-arn> \
    --account-id <account-id> --permission-set-arn <permission-set-arn>
```

## CloudTrail to SIEM

Centralise CloudTrail logs to the log-archive account:

```bash
# Verify CloudTrail is enabled in all regions
aws cloudtrail describe-trails --include-shadow-trails

# Verify log delivery is healthy
aws cloudtrail get-trail-status --name <trail-name> | jq '{LatestDeliveryTime, LatestDeliveryError}'
```

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
