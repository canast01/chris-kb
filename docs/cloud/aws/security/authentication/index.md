# AWS — Authentication


<div class="kb-summary">
Authentication reference covering Authentication Methods Overview, IAM Identity Center (SSO) Setup, MFA — Enforce for Console Users, OIDC Federation — GitHub Actions, IRSA — IAM Roles for Service Accounts (EKS) and 4 more sections.
</div>

---

## Authentication Methods Overview

| Method | Use Case | Credential Type |
|---|---|---|
| IAM User + password | AWS Console access for humans | Username/password + MFA |
| IAM User + access keys | Legacy programmatic access (avoid) | Long-lived static keys |
| IAM Role | Applications, services, cross-account | Short-lived STS tokens (1h–12h) |
| IAM Identity Center (SSO) | Federated human access via IdP | Browser SSO → short-lived credentials |
| OIDC federation | GitHub Actions, Kubernetes pods (IRSA) | No stored secrets — token exchange |
| EC2 Instance Metadata (IMDSv2) | Applications running on EC2 | Automatic role credentials via 169.254.169.254 |

---

## IAM Identity Center (SSO) Setup

```bash
# List permission sets
aws sso-admin list-permission-sets \
  --instance-arn arn:aws:sso:::instance/ssoins-<id> \
  --query 'PermissionSets' --output text

# Provision credentials via SSO login (CLI)
aws sso login --profile prod
# Or configure SSO profile in ~/.aws/config:
```
┌───────────────────────────── AWS Authentication — SSO, MFA & Credentials ─────────────────────────────┐
│                                                                                                       │
│  Authentication to AWS via IAM Identity Center SSO, MFA enforcement, and access keys.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          IAM Identity Center (SSO)           │  │               MFA Enforcement               │   │
│   │       IdP: Azure AD / Okta SAML source       │  │        Root account: hardware MFA key       │   │
│   │     Permission sets → IAM roles in accts     │  │       IAM users: TOTP or hardware MFA       │   │
│   │       Browser: AWS access portal login       │  │       SCP: deny without MFA condition       │   │
│   │         CLI: aws sso login --profile         │  │     Identity Center: MFA at portal level    │   │
│   │      Token: short-lived; no static keys      │  │    Condition: aws:MultiFactorAuthPresent    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SSO issues short-lived tokens; no long-lived access keys needed for human users.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │        Access Keys (Machine Identity)        │  │          Credential Best Practices          │   │
│   │      Use only for machine/CI workloads       │  │         No root account access keys         │   │
│   │      Prefer IAM roles over access keys       │  │          Rotate keys every 90 days          │   │
│   │      Store in Secrets Manager not code       │  │         Audit with credential report        │   │
│   │       OIDC for GitHub Actions (no key)       │  │          Deactivate before deleting         │   │
│   │       KMS for signing; not static keys       │  │        Alert on root usage via CT/CW        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS IAM global service · Identity Center regional portal · STS regional endpoints                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  IAM Identity Center= AWS SSO service managing human user access across accounts                      │
│  Permission set  = IAM policy definition assigned to users/groups in member accounts                  │
│  SAML federation = Protocol connecting corporate IdP (Azure AD/Okta) to AWS SSO                       │
│  TOTP            = Time-based One-Time Password; TOTP app (e.g. Authenticator) for MFA                │
│  Hardware MFA    = Physical YubiKey or similar device; recommended for root account                   │
│  STS             = Security Token Service; issues temporary credentials via AssumeRole                │
│  Access key      = Long-lived AKID+secret pair; avoid for human users; use SSO instead                │
│  OIDC            = OpenID Connect; allows GitHub Actions to assume roles without keys                 │
│  aws:MultiFactorAuthPresent= Condition key requiring MFA in the session                               │
│  Credential report= IAM CSV report listing users and their last key/password usage                    │
│  Root account    = AWS account root user; cannot be restricted by SCP; use sparingly                  │
│  Short-lived token= Temporary STS credential; expires after max 12h; no rotation needed               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

```bash
aws sso login --profile prod
aws s3 ls --profile prod
```

---

## MFA — Enforce for Console Users

```bash
# Attach policy that denies all actions unless MFA is present
# Apply this to IAM groups used for human console access:
aws iam put-group-policy \
  --group-name Operators \
  --policy-name RequireMFA \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "DenyAllExceptMFAManagement",
        "Effect": "Deny",
        "NotAction": [
          "iam:CreateVirtualMFADevice",
          "iam:EnableMFADevice",
          "iam:GetUser",
          "iam:ListMFADevices",
          "iam:ListVirtualMFADevices",
          "iam:ResyncMFADevice",
          "sts:GetSessionToken"
        ],
        "Resource": "*",
        "Condition": {
          "BoolIfExists": {"aws:MultiFactorAuthPresent": "false"}
        }
      }
    ]
  }'

# Check which users have MFA enabled
aws iam generate-credential-report && sleep 10
aws iam get-credential-report --output text | base64 -d | \
  awk -F',' 'NR==1 || $8!="true"' | column -t -s','
# Shows users without MFA enabled
```

---

## OIDC Federation — GitHub Actions

No stored secrets: GitHub issues an OIDC token, AWS validates it and returns temporary credentials.

```bash
# Create OIDC provider for GitHub
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1

# Create trust policy for the role
cat > github-trust.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<account>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:myorg/myrepo:*"
        }
      }
    }
  ]
}
EOF

aws iam create-role --role-name GitHubActionsDeployRole \
  --assume-role-policy-document file://github-trust.json
```

```yaml
# GitHub Actions workflow — assume role
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::<account>:role/GitHubActionsDeployRole
    aws-region: eu-west-1
```

---

## IRSA — IAM Roles for Service Accounts (EKS)

```bash
# Enable OIDC provider for EKS cluster
eksctl utils associate-iam-oidc-provider \
  --cluster my-cluster --approve

# Get OIDC issuer URL
OIDC_URL=$(aws eks describe-cluster --name my-cluster \
  --query 'cluster.identity.oidc.issuer' --output text)

# Create trust policy for a K8s service account
OIDC_ID=$(echo $OIDC_URL | cut -d'/' -f5)
cat > irsa-trust.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<account>:oidc-provider/oidc.eks.eu-west-1.amazonaws.com/id/$OIDC_ID"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.eu-west-1.amazonaws.com/id/$OIDC_ID:sub": "system:serviceaccount:my-namespace:my-service-account"
        }
      }
    }
  ]
}
EOF

aws iam create-role --role-name eks-my-app-role \
  --assume-role-policy-document file://irsa-trust.json
```

```yaml
# Annotate Kubernetes service account to link the role
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-account
  namespace: my-namespace
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::<account>:role/eks-my-app-role
```

---

## IMDSv2 — Enforce on EC2

IMDSv2 requires a session token for metadata access, preventing SSRF-based credential theft.

```bash
# Enforce IMDSv2 on existing instance
aws ec2 modify-instance-metadata-options \
  --instance-id i-0abc123 \
  --http-tokens required \
  --http-endpoint enabled

# Enforce IMDSv2 at launch (default for all new instances in account)
aws ec2 modify-instance-metadata-defaults \
  --http-tokens required \
  --region eu-west-1

# Verify
aws ec2 describe-instance-metadata-options \
  --instance-id i-0abc123 \
  --query 'InstanceMetadataOptions.HttpTokens'
```

---

## Access Key Management

```bash
# List all access keys across all users (via credential report)
aws iam get-credential-report --output text | base64 -d | \
  awk -F',' 'NR==1 || $9=="true" || $14=="true"' | \
  column -t -s','
# Shows users with active access keys

# Rotate an access key (create new, update application, delete old)
NEW_KEY=$(aws iam create-access-key --user-name svc-deploy \
  --query 'AccessKey.[AccessKeyId,SecretAccessKey]' --output text)
echo "New key: $NEW_KEY"
# Update application config with new key, then:
aws iam delete-access-key --user-name svc-deploy --access-key-id AKIA<old-id>

# Disable old key before deleting (safer)
aws iam update-access-key \
  --user-name svc-deploy \
  --access-key-id AKIA<old-id> \
  --status Inactive
```

---

## Break-Glass Account

```bash
# Create a break-glass user (used only when SSO/IdP is unavailable)
aws iam create-user --user-name break-glass-admin

# Attach AdministratorAccess
aws iam attach-user-policy \
  --user-name break-glass-admin \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Enable MFA — configure TOTP device via Console (cannot be done via CLI alone)
# Store TOTP seed + password in offline vault (not in AWS Secrets Manager)

# CloudTrail alert: break-glass login triggers SNS → PagerDuty
# Create CloudWatch alarm on metric filter for user: "break-glass-admin"
```
---

## Related Reference

- [Standard SAML Configuration](../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
