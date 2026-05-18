# AWS — Hardening

```
┌──────────────────────────────────────────────────────────┐
│            AWS Hardening Checklist (Priority)            │
├──────────────────────────────────────────────────────────┤
│  CRITICAL                                                │
│  ├── Root account: no access keys, MFA enabled          │
│  ├── IMDSv2 required on all EC2 instances               │
│  ├── S3 Block Public Access (account level)             │
│  └── CloudTrail: all-region, S3 + CloudWatch Logs       │
├──────────────────────────────────────────────────────────┤
│  HIGH                                                    │
│  ├── GuardDuty enabled (all features + S3/EKS)          │
│  ├── Security Hub + CIS Benchmark standard enabled      │
│  ├── AWS Config recording all resource types            │
│  ├── No IAM users with AdministratorAccess (use roles)  │
│  ├── Access keys rotated ≤ 90 days                      │
│  └── IAM password policy: length ≥ 14, rotation 90d    │
├──────────────────────────────────────────────────────────┤
│  MEDIUM                                                  │
│  ├── VPC Flow Logs enabled                              │
│  └── Default VPC deleted or unused                      │
└──────────────────────────────────────────────────────────┘
  GuardDuty ──► Security Hub ──► Findings Dashboard
  Config    ──► Security Hub ──► Compliance Score
```

---

## Account Hardening Checklist

| Control | CLI Verification | Priority |
|---|---|---|
| Root account — no access keys | `aws iam get-account-summary` → AccountAccessKeysPresent = 0 | Critical |
| Root account — MFA enabled | Console only; check credential report | Critical |
| IMDSv2 required on all EC2 | `aws ec2 describe-instance-metadata-options` | Critical |
| S3 Block Public Access (account level) | `aws s3control get-public-access-block --account-id <id>` | Critical |
| CloudTrail — all regions, S3 + CloudWatch | `aws cloudtrail describe-trails` | Critical |
| GuardDuty enabled | `aws guardduty list-detectors` | High |
| Security Hub enabled | `aws securityhub describe-hub` | High |
| AWS Config enabled | `aws configservice describe-configuration-recorders` | High |
| No users with AdministratorAccess (use roles) | `aws iam list-entities-for-policy --policy-arn ...AdministratorAccess` | High |
| Access key rotation ≤ 90 days | Credential report | High |
| Password policy — length ≥ 14, complexity, rotation | `aws iam get-account-password-policy` | High |
| VPC Flow Logs enabled | `aws ec2 describe-flow-logs` | Medium |
| Default VPC deleted or unused | `aws ec2 describe-vpcs --filters Name=isDefault,Values=true` | Medium |

---

## Root Account Protection

```bash
# Check root account has no access keys
aws iam get-account-summary \
  --query 'SummaryMap.[AccountAccessKeysPresent,AccountMFAEnabled]'
# Expected: AccountAccessKeysPresent=0, AccountMFAEnabled=1

# MFA for root must be enabled via Console — cannot be set via CLI
```

---

## IAM Password Policy

```bash
aws iam update-account-password-policy \
  --minimum-password-length 14 \
  --require-symbols \
  --require-numbers \
  --require-uppercase-characters \
  --require-lowercase-characters \
  --allow-users-to-change-password \
  --max-password-age 90 \
  --password-reuse-prevention 12 \
  --hard-expiry

aws iam get-account-password-policy
```

---

## CloudTrail — Multi-Region with CloudWatch

```bash
# Create S3 bucket for CloudTrail logs
aws s3api create-bucket \
  --bucket my-org-cloudtrail-logs \
  --region eu-west-1 \
  --create-bucket-configuration LocationConstraint=eu-west-1

# Enable versioning + server-side encryption on the bucket
aws s3api put-bucket-versioning \
  --bucket my-org-cloudtrail-logs \
  --versioning-configuration Status=Enabled

# Create multi-region trail
aws cloudtrail create-trail \
  --name org-management-trail \
  --s3-bucket-name my-org-cloudtrail-logs \
  --include-global-service-events \
  --is-multi-region-trail \
  --enable-log-file-validation \
  --cloud-watch-logs-log-group-arn arn:aws:logs:eu-west-1:<account>:log-group:CloudTrail \
  --cloud-watch-logs-role-arn arn:aws:iam::<account>:role/CloudTrailCloudWatchRole

aws cloudtrail start-logging --name org-management-trail

# Verify
aws cloudtrail get-trail-status --name org-management-trail \
  --query '[IsLogging,LatestDeliveryTime,LatestCloudWatchLogsDeliveryTime]'
```

---

## GuardDuty — Enable All Features

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

---

## Security Hub — Enable and Standards

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

---

## AWS Config — Enable Recording

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

---

## S3 — Block Public Access (Account Level)

```bash
aws s3control put-public-access-block \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Verify
aws s3control get-public-access-block \
  --account-id $(aws sts get-caller-identity --query Account --output text)
```

---

## VPC — Security Controls

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

---

## Restrict Region Usage (SCP)

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

Apply this SCP via AWS Organizations to restrict which regions accounts can operate in.
