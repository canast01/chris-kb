---
tags:
  - aws
  - security
---
# AWS Security Hardening — CIS Baseline

```bash
# Check root account has no access keys
aws iam get-account-summary \
  --query 'SummaryMap.[AccountAccessKeysPresent,AccountMFAEnabled]'
# Expected: AccountAccessKeysPresent=0, AccountMFAEnabled=1

# MFA for root must be enabled via Console — cannot be set via CLI
```


```text title="Expected output"
[
    0,
    1
]
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (AccessDenied) when calling the GetAccountSummary operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: iam:GetAccountSummary` | Attach the `IAMReadOnlyAccess` policy or `iam:GetAccountSummary` permission to the IAM user running this command. |
    | `Unable to locate credentials` | Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables. |
```bash
# Enable GuardDuty
DETECTOR_ID=$(aws guardduty create-detector \
  --enable \
  --finding-publishing-frequency FIFTEEN_MINUTES \
  --features '[
    {"Name":"S3_DATA_EVENTS","Status":"ENABLED"},
    {"Name":"EKS_AUDIT_LOGS","Status":"ENABLED"},
    {"Name":"MALWARE_PROTECTION","Status":"ENABLED"},
    {"Name":"RDS_LOGIN_EVENTS","Status":"ENABLED"},
    {"Name":"LAMBDA_NETWORK_LOGS","Status":"ENABLED"}
  ]' \
  --query 'DetectorId' --output text)

echo "Detector ID: $DETECTOR_ID"

# Export findings to S3 (for SIEM)
aws guardduty create-publishing-destination \
  --detector-id $DETECTOR_ID \
  --destination-type S3 \
  --destination-properties \
    DestinationArn=arn:aws:s3:::my-security-findings,KmsKeyArn=arn:aws:kms:eu-west-1:<account>:alias/guardduty-cmk
```

```text title="Expected output"
Detector ID: 12a34b5c6d7e8f9g0h1i2j3k4l5m6n7o

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidParameterException) when calling the CreateDetector operation: 1 validation error detected: Value at 'features' failed a custom validation constraint: Duplicate feature name` | Remove duplicate feature entries from the features array, ensuring each feature name appears only once. |
    | `An error occurred (InvalidParameterException) when calling the CreatePublishingDestination operation: The S3 bucket does not exist or you do not have permission to access it` | Verify the S3 bucket exists in the same region and the AWS credentials have `s3:GetBucketLocation` and `s3:ListBucket` permissions. |
    | `An error occurred (InvalidParameterException) when calling the CreatePublishingDestination operation: The KMS key ARN is invalid or the key does not exist` | Confirm the KMS key exists in the specified region (eu-west-1) and the GuardDuty service principal has `kms:Decrypt` and `kms:GenerateDataKey` permissions via the key policy. |
```bash
# Enable Security Hub
aws securityhub enable-security-hub \
  --enable-default-standards \
  --control-finding-generator SECURITY_CONTROL

# Enable CIS AWS Foundations Benchmark
aws securityhub batch-enable-standards \
  --standards-subscription-requests \
    StandardsArn=arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0

# List failed controls
aws securityhub get-findings \
  --filters '{
    "ComplianceStatus": [{"Value":"FAILED","Comparison":"EQUALS"}],
    "WorkflowStatus": [{"Value":"NEW","Comparison":"EQUALS"}],
    "SeverityLabel": [{"Value":"CRITICAL","Comparison":"EQUALS"}]
  }' \
  --query 'Findings[*].[Title,SeverityLabel,ProductName]' \
  --output table
```

```text title="Expected output"
{
    "HubArn": "arn:aws:securityhub:us-east-1:123456789012:hub/default",
    "RepeatableHubArn": "arn:aws:securityhub:us-east-1:123456789012:hub/default"
}
{
    "StandardsSubscriptionRequests": [
        {
            "StandardsArn": "arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0",
            "StandardsSubscriptionRequestArn": "arn:aws:securityhub:us-east-1:123456789012:subscription/cis-aws-foundations-benchmark/v/1.2.0/123e4567-e89b-12d3-a456-426614174000",
            "StandardsStatus": "PENDING"
        }
    ],
    "FailedCount": 0
}
-----------------------------------
|                    Title                    | SeverityLabel |     ProductName      |
|---------------------------------------------|---------------|----------------------|
| S3 bucket public read access blocked        | CRITICAL      | Security Hub         |
| CloudTrail logging not enabled              | CRITICAL      | Security Hub         |
| IAM password policy not configured          | CRITICAL      | Security Hub         |
| VPC Flow Logs not enabled                   | CRITICAL      | Security Hub         |
| KMS key rotation not enabled                | CRITICAL      | Security Hub         |
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ResourceConflictException) when calling the EnableSecurityHub operation: Security Hub is already enabled in this account.` | Run `aws securityhub describe-hub` to verify it's already active, then skip the enable command. |
    | `An error occurred (InvalidInputException) when calling the BatchEnableStandards operation: StandardsArn is invalid` | Verify the benchmark version exists in your region with `aws securityhub describe-standards` and use the correct ARN. |
    | `An error occurred (AccessDeniedException) when calling the GetFindings operation: User is not authorized to perform: securityhub:GetFindings` | Attach the `SecurityHubReadOnlyAccess` policy or equivalent to your IAM user/role. |
```bash
# Create Config recorder
aws configservice put-configuration-recorder \
  --configuration-recorder '{
    "name": "default",
    "roleARN": "arn:aws:iam::<account>:role/AWSConfigRole",
    "recordingGroup": {
      "allSupported": true,
      "includeGlobalResourceTypes": true
    }
  }'

# Create delivery channel
aws configservice put-delivery-channel \
  --delivery-channel '{
    "name": "default",
    "s3BucketName": "my-config-bucket",
    "configSnapshotDeliveryProperties": {
      "deliveryFrequency": "TwentyFour_Hours"
    }
  }'

aws configservice start-configuration-recorder --configuration-recorder-name default
```

```text title="Expected output"
{
    "ConfigurationRecorderArn": "arn:aws:config:us-east-1:123456789012:config-recorder/default"
}
{
    "DeliveryChannelArn": "arn:aws:config:us-east-1:123456789012:delivery-channel/default"
}
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidParameterValueException) when calling the PutConfigurationRecorder operation: The role ARN is invalid or does not have the required permissions.` | Ensure the IAM role exists, has the AWSConfigRoleForConfigServicePrincipal trust relationship, and is in the same account as specified in the ARN. |
    | `An error occurred (NoSuchBucketException) when calling the PutDeliveryChannel operation: The S3 bucket does not exist.` | Create the S3 bucket with `aws s3 mb s3://my-config-bucket` and ensure it is in the same region as your Config recorder. |
    | `An error occurred (NoAvailableConfigurationRecorderException) when calling the StartConfigurationRecorder operation: Configuration recorder 'default' does not exist.` | Verify the configuration recorder was created successfully by running `aws configservice describe-configuration-recorders` before starting it. |
```bash
aws s3control put-public-access-block \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Verify
aws s3control get-public-access-block \
  --account-id $(aws sts get-caller-identity --query Account --output text)
```

```text title="Expected output"
{
    "PublicAccessBlockConfiguration": {
        "BlockPublicAcls": true,
        "IgnorePublicAcls": true,
        "BlockPublicPolicy": true,
        "RestrictPublicBuckets": true
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (AccessDenied) when calling the PutPublicAccessBlock operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: s3:PutAccountPublicAccessBlock` | Attach the `AmazonS3FullAccess` policy or a custom policy with `s3:PutAccountPublicAccessBlock` permission to the IAM user/role. |
    | `Unable to locate credentials` | Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables. |
    | `An error occurred (NoSuchPublicAccessBlockConfiguration) when calling the GetPublicAccessBlock operation: The public access block configuration does not exist` | Run the `put-public-access-block` command first before attempting to retrieve the configuration. |
```bash
# Delete default VPC (if not in use — irreversible)
DEFAULT_VPC=$(aws ec2 describe-vpcs \
  --filters Name=isDefault,Values=true \
  --query 'Vpcs[0].VpcId' --output text)

# Before deleting, detach/delete IGW and subnets
aws ec2 describe-internet-gateways \
  --filters "Name=attachment.vpc-id,Values=$DEFAULT_VPC" \
  --query 'InternetGateways[0].InternetGatewayId' --output text | \
  xargs -I{} aws ec2 detach-internet-gateway --internet-gateway-id {} --vpc-id $DEFAULT_VPC
# Then delete subnets, then VPC

# Enable VPC Flow Logs
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-0abc123 \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name /aws/vpc/flowlogs \
  --deliver-logs-permission-arn arn:aws:iam::<account>:role/VPCFlowLogsRole
```
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyUnapprovedRegions",
      "Effect": "Deny",
      "NotAction": [
        "iam:*",
        "organizations:*",
        "support:*",
        "budgets:*",
        "account:*",
        "sts:*",
        "cloudfront:*",
        "route53:*",
        "waf::*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": ["eu-west-1","eu-central-1","us-east-1"]
        }
      }
    }
  ]
}
```

```d2
direction: down

network_controls: "Network Controls" {shape: rectangle}
os_hardening: "OS Hardening" {shape: rectangle}
application_security: "Application Security" {shape: rectangle}
audit_monitoring: "Audit & Monitoring" {shape: rectangle}

network_controls -> os_hardening: hardens
os_hardening -> application_security: hardens
application_security -> audit_monitoring: hardens
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
- [Aws — Access Control](../access-control/)
- [Aws — Encryption](../encryption/)
