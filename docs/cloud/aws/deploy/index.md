---
tags:
  - aws
  - deployment
---
# AWS — Account and Landing Zone Setup

This guide covers building a multi-account AWS Landing Zone from scratch: AWS Organizations, IAM Identity Center, CloudTrail, AWS Config, VPC networking, IAM roles, GuardDuty, and Security Hub.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| AWS management account | Root account; used only for org-level administration |
| MFA on root | Enable before any other step |
| Identity Provider | Azure AD, Okta, or another SAML 2.0 IdP for SSO (optional but recommended) |
| Logging S3 bucket | Pre-create in a dedicated Log Archive account |
| AWS CLI | Installed and configured with management account credentials |

Before creating any accounts, define your OU structure on paper:

```text
Root
├── Infrastructure
│   └── Log Archive
│   └── Audit (Security Tooling)
├── Workloads
│   ├── Development
│   ├── Staging
│   └── Production
└── Sandbox
```

---

## Create AWS Organization and Enable AWS SSO

**Create the organization from the management account:**

```bash
aws organizations create-organization --feature-set ALL
```

**Enable all features** (required for SCPs):

```bash
aws organizations enable-all-features
```

**Enable IAM Identity Center (AWS SSO):**

1. Console → IAM Identity Center → Enable.
2. Choose your identity source:
   - **Identity Center directory** — built-in, suitable for small environments.
   - **External IdP (SAML 2.0)** — recommended for enterprise; connect Azure AD or Okta.
3. Configure attribute mappings and provision groups from your IdP.

Verify the organization:

```bash
aws organizations describe-organization
aws organizations list-accounts
```

---

## Create Accounts and OUs

**Create OUs:**

```bash
# Get the Root ID
ROOT_ID=$(aws organizations list-roots --query 'Roots[0].Id' --output text)

# Create top-level OUs
aws organizations create-organizational-unit --parent-id $ROOT_ID --name Infrastructure
aws organizations create-organizational-unit --parent-id $ROOT_ID --name Workloads
aws organizations create-organizational-unit --parent-id $ROOT_ID --name Sandbox
```

**Create member accounts:**

```bash
aws organizations create-account \
    --email log-archive@corp.com \
    --account-name "Log Archive"

aws organizations create-account \
    --email security-tooling@corp.com \
    --account-name "Security Tooling"

aws organizations create-account \
    --email dev@corp.com \
    --account-name "Development"

aws organizations create-account \
    --email prod@corp.com \
    --account-name "Production"
```

**Move accounts into OUs:**

```bash
# Get account ID and OU ID, then move
aws organizations move-account \
    --account-id <account-id> \
    --source-parent-id $ROOT_ID \
    --destination-parent-id <ou-id>
```

---

## Configure CloudTrail (All Regions)

Create an organisation-wide, multi-region trail that logs to the Log Archive account S3 bucket.

**Create the S3 bucket in the Log Archive account (run as Log Archive account):**

```bash
aws s3 mb s3://org-cloudtrail-logs-<account-id> --region us-east-1
```

Apply a bucket policy that allows CloudTrail to write from the management account:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSCloudTrailAclCheck",
      "Effect": "Allow",
      "Principal": {"Service": "cloudtrail.amazonaws.com"},
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::org-cloudtrail-logs-<account-id>"
    },
    {
      "Sid": "AWSCloudTrailWrite",
      "Effect": "Allow",
      "Principal": {"Service": "cloudtrail.amazonaws.com"},
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::org-cloudtrail-logs-<account-id>/AWSLogs/*"
    }
  ]
}
```

**Create the organisation trail (run as management account):**

```bash
aws cloudtrail create-trail \
    --name org-trail \
    --s3-bucket-name org-cloudtrail-logs-<account-id> \
    --is-multi-region-trail \
    --is-organization-trail \
    --enable-log-file-validation

aws cloudtrail start-logging --name org-trail
```

Verify:

```bash
aws cloudtrail get-trail-status --name org-trail
```

`IsLogging` should be `true`.

---

## Configure AWS Config

Enable AWS Config in each account and region to record configuration changes and evaluate compliance rules.

```bash
# Create Config delivery channel and recorder (per account, per region)
aws configservice put-configuration-recorder \
    --configuration-recorder name=default,roleARN=arn:aws:iam::<account-id>:role/AWSConfigRole

aws configservice put-delivery-channel \
    --delivery-channel name=default,s3BucketName=org-config-logs-<account-id>

aws configservice start-configuration-recorder --configuration-recorder-name default
```

**Enable CIS benchmark conformance pack:**

```bash
aws configservice put-conformance-pack \
    --conformance-pack-name CIS-AWS-Foundations \
    --template-s3-uri s3://aws-configurules-us-east-1/packages/CIS_Top_20.yaml
```

Verify compliance status:

```bash
aws configservice describe-conformance-pack-compliance \
    --conformance-pack-name CIS-AWS-Foundations
```

---

## Set Up VPC and Networking

Create a standard VPC with public and private subnets across two Availability Zones.

```bash
# Create VPC
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 \
    --query 'Vpc.VpcId' --output text)
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-hostnames

# Create subnets
aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 \
    --availability-zone us-east-1a --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=Public-1a}]'

aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 \
    --availability-zone us-east-1b --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=Public-1b}]'

aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.11.0/24 \
    --availability-zone us-east-1a --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=Private-1a}]'

aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.12.0/24 \
    --availability-zone us-east-1b --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=Private-1b}]'

# Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID

# NAT Gateway (requires Elastic IP)
EIP_ALLOC=$(aws ec2 allocate-address --domain vpc --query 'AllocationId' --output text)
aws ec2 create-nat-gateway --subnet-id <public-subnet-1a-id> --allocation-id $EIP_ALLOC
```

---

## Configure IAM Roles and SCPs

**Create job-function IAM roles:**

```bash
aws iam create-role --role-name InfraAdmin \
    --assume-role-policy-document file://trust-policy.json

aws iam attach-role-policy --role-name InfraAdmin \
    --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

**Apply a Deny-region SCP to restrict to approved regions only:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonApprovedRegions",
      "Effect": "Deny",
      "NotAction": [
        "iam:*", "organizations:*", "support:*", "cloudfront:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": ["us-east-1", "eu-west-1"]
        }
      }
    }
  ]
}
```

```bash
aws organizations create-policy \
    --name DenyNonApprovedRegions \
    --type SERVICE_CONTROL_POLICY \
    --content file://deny-regions-scp.json

aws organizations attach-policy \
    --policy-id <policy-id> \
    --target-id <workloads-ou-id>
```

---

## Enable GuardDuty

Enable GuardDuty as an organisation-level service so all member accounts are automatically enrolled.

```bash
# Enable in management account (designate Security Tooling as delegated admin first)
aws guardduty create-detector --enable --finding-publishing-frequency FIFTEEN_MINUTES

# Designate delegated admin
aws guardduty enable-organization-admin-account --admin-account-id <security-tooling-account-id>
```

Configure findings export to S3:

```bash
aws guardduty update-detector \
    --detector-id <detector-id> \
    --finding-publishing-frequency FIFTEEN_MINUTES
```

Verify:

```bash
aws guardduty list-detectors
aws guardduty get-detector --detector-id <detector-id>
```

`Status` should be `ENABLED`.

---

## Configure Security Hub

Security Hub aggregates findings from GuardDuty, Config, Inspector, and third-party tools.

```bash
# Enable Security Hub
aws securityhub enable-security-hub \
    --enable-default-standards \
    --control-finding-generator SECURITY_CONTROL

# Verify enabled standards
aws securityhub describe-standards-subscriptions
```

Enable the CIS AWS Foundations standard explicitly if not auto-enabled:

```bash
aws securityhub batch-enable-standards \
    --standards-subscription-requests \
    StandardsArn=arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.4.0
```

Review initial findings:

```bash
aws securityhub get-findings \
    --filters '{"SeverityLabel":[{"Value":"CRITICAL","Comparison":"EQUALS"}]}' \
    --query 'Findings[].{Title:Title,Severity:Severity.Label,AccountId:AwsAccountId}' \
    --output table
```

Address all `CRITICAL` findings before workloads are deployed into the accounts.
