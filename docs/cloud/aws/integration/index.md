# AWS Integration
## Direct Connect + VPN

On-premises to AWS connectivity:

```bash
# Check Direct Connect connection status
aws directconnect describe-connections --query 'connections[*].[connectionId,connectionName,connectionState]'

# Check Virtual Interface BGP state
aws directconnect describe-virtual-interfaces --query 'virtualInterfaces[*].[virtualInterfaceId,bgpPeers]'

# Verify Transit Gateway route tables
aws ec2 describe-transit-gateway-route-tables
aws ec2 search-transit-gateway-routes --transit-gateway-route-table-id <tgw-rtb-id> --filters "Name=state,Values=active"
```

VPN is configured as a backup to Direct Connect with lower BGP preference (AS-Path prepend or local preference).

## Active Directory

**AWS Managed Microsoft AD** (new deployments):
```bash
# Create managed AD
aws ds create-microsoft-ad --name corp.local --password <pwd> --vpc-settings VpcId=<vpc>,SubnetIds=<sub1>,<sub2>
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
