# AWS Config

AWS Config — continuous configuration tracking, compliance evaluation, and change history.

## What AWS Config Does

- Records configuration state of AWS resources at every change
- Evaluates resources against compliance rules
- Maintains configuration history and relationship graph
- Supports remediation actions for non-compliant resources

## Common CLI Commands

```bash
# List all config rules
aws configservice describe-config-rules \
  --query 'ConfigRules[*].{Name:ConfigRuleName,State:ConfigRuleState,Source:Source.Owner}' \
  --output table

# Check compliance for a specific rule
aws configservice get-compliance-details-by-config-rule \
  --config-rule-name <rule-name> \
  --compliance-types NON_COMPLIANT \
  --query 'EvaluationResults[*].{Resource:EvaluationResultIdentifier.EvaluationResultQualifier.ResourceId,Time:ResultRecordedTime}' \
  --output table

# Get compliance summary across all rules
aws configservice describe-compliance-by-config-rule \
  --query 'ComplianceByConfigRules[*].{Rule:ConfigRuleName,Status:Compliance.ComplianceType}' \
  --output table

# Get config history for a resource
aws configservice get-resource-config-history \
  --resource-type AWS::EC2::SecurityGroup \
  --resource-id <sg-id> \
  --limit 10 \
  --query 'configurationItems[*].{Time:configurationItemCaptureTime,Status:configurationItemStatus}' \
  --output table

# List all non-compliant resources across all rules
aws configservice describe-compliance-by-resource \
  --compliance-types NON_COMPLIANT \
  --query 'ComplianceByResources[*].{Type:ResourceType,ID:ResourceId,Status:Compliance.ComplianceType}' \
  --output table
```

## Common Managed Rules

| Rule | What It Checks |
|---|---|
| `restricted-ssh` | No security groups allow unrestricted inbound SSH (0.0.0.0/0:22) |
| `s3-bucket-public-read-prohibited` | S3 buckets are not publicly readable |
| `root-account-mfa-enabled` | AWS root account has MFA enabled |
| `iam-password-policy` | IAM account password policy meets requirements |
| `encrypted-volumes` | EBS volumes are encrypted |
| `rds-storage-encrypted` | RDS DB instances have storage encryption enabled |
| `cloudtrail-enabled` | CloudTrail is enabled in the account |
| `vpc-flow-logs-enabled` | VPC flow logs are enabled |

## Remediation

```bash
# Trigger automatic remediation for a rule
aws configservice start-remediation-execution \
  --config-rule-name <rule-name> \
  --resource-keys '[{"resourceType":"AWS::EC2::SecurityGroup","resourceId":"<sg-id>"}]'

# Check remediation status
aws configservice describe-remediation-execution-statuses \
  --config-rule-name <rule-name>
```

## Config Query (Advanced)

```bash
# Use AWS Config Advanced Query to find all unencrypted EBS volumes
aws configservice select-aggregate-resource-config \
  --expression "SELECT resourceId, resourceType, configuration.encrypted WHERE resourceType = 'AWS::EC2::Volume' AND configuration.encrypted = false" \
  --configuration-aggregator-name <aggregator-name>
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Rule evaluation not running | Rule trigger type | Check if periodic or change-triggered; force re-evaluation with `start-config-rules-evaluation` |
| Resources not showing in Config | Config recorder running? | `describe-configuration-recorder-status` — ensure recorder is active |
| Remediation not working | SSM Automation document | Check the document has correct permissions and the target resource is accessible |
| Missing config history | Config retention | Default: 30 days; change via `put-retention-configuration` |
