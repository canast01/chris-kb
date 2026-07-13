---
tags:
  - aws
  - security
---
# AWS Authentication — SSO, MFA & Credentials

```bash
# List permission sets
aws sso-admin list-permission-sets \
  --instance-arn arn:aws:sso:::instance/ssoins-<id> \
  --query 'PermissionSets' --output text

# Provision credentials via SSO login (CLI)
aws sso login --profile prod
# Or configure SSO profile in ~/.aws/config:
```


```text title="Expected output"
arn:aws:sso:::permissionSet/ssoins-7a8b9c0d1e2f/ps-1a2b3c4d5e6f7g8h	arn:aws:sso:::permissionSet/ssoins-7a8b9c0d1e2f/ps-9x8y7w6v5u4t3s2r	arn:aws:sso:::permissionSet/ssoins-7a8b9c0d1e2f/ps-2k3l4m5n6o7p8q9r

Attempting to automatically open the SSO authorization page in your default browser.
If the browser does not open or you wish to use a different device to authorize this request, open the following URL:

https://device.sso.us-east-1.amazonaws.com/?user_code=ABCD-EFGH

Then enter the code when prompted in the browser (or you can paste it). If the browser does not open after a few seconds, please visit the above URL in your browser and enter the device code.

Successfully logged in. Your AWS SSO session will expire in 12 hours.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidParameterException) when calling the ListPermissionSets operation: 1 validation error detected: Value 'arn:aws:sso:::instance/ssoins-<id>' at 'instanceArn' failed to match pattern` | Replace `<id>` with the actual SSO instance ID from `aws sso-admin list-instances`. |
    | `An error occurred (AccessDeniedException) when calling the Login operation: User is not authorized to perform: sso:GetRoleCredentials` | Ensure the IAM user has `sso:GetRoleCredentials` and `sso:ListAccounts` permissions attached. |
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

```text title="Expected output"
{
    "GroupPolicyList": [
        {
            "GroupName": "Operators",
            "PolicyName": "RequireMFA",
            "PolicyDocument": "%7B%22Version%22%3A%222012-10-17%22%2C%22Statement%22%3A%5B%7B%22Sid%22%3A%22DenyAllExceptMFAManagement%22..."
        }
    ]
}
user,arn,user_creation_time,password_enabled,password_last_used,password_last_changed,password_next_rotation,mfa_active,access_key_1_active,access_key_1_last_rotated,access_key_1_last_used_date,access_key_2_active,access_key_2_last_rotated,access_key_2_last_used_date,cert_1_active,cert_1_last_rotated,cert_2_active,cert_2_last_rotated
alice.chen,arn:aws:iam::123456789012:user/alice.chen,2023-06-15T09:22:14+00:00,true,2024-01-18T14:32:00+00:00,2024-01-10T11:05:22+00:00,N/A,false,true,2024-01-12T16:48:33+00:00,2024-01-18T14:32:00+00:00,false,N/A,N/A,false,N/A,false,N/A
james.rodriguez,arn:aws:iam::123456789012:user/james.rodriguez,2023-08-22T13:17:45+00:00,true,2024-01-17T10:15:30+00:00,2024-01-09T08:42:11+00:00,N/A,false,true,2024-01-11T09:33:22+00:00,2024-01-17T10:15:30+00:00,false,N/A,N/A,false,N/A,false,N/A
marcus.thompson,arn:aws:iam::123456789012:user/marcus.thompson,2023-11-03T16:55:12+00:00,true,2024-01-16T15:48:00+00:00,2024-01-08T12:20:55+00:00,N/A,true,true,2024-01-14T11:22:44+00:00,2024-01-16T15:48:00+00:00,false,N/A,N/A,false,N/A,false,N/A
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (NoSuchEntity) when calling the PutGroupPolicy operation: The group with name Operators cannot be found.` | Create the IAM group first using `aws iam create-group --group-name Operators` before attaching the policy. |
    | `An error occurred (MalformedPolicyDocument) when calling the PutGroupPolicy operation: Invalid principal in policy: "NotAction"` | Use `"Action"` instead of `"NotAction"` in the Deny statement, or restructure the policy to explicitly list denied actions. |
    **`The
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

```text title="Expected output"
{
    "InstanceMetadataOptions": {
        "State": "pending",
        "HttpTokens": "required",
        "HttpPutResponseHopLimit": 1,
        "HttpEndpoint": "enabled"
    }
}
{
    "InstanceMetadataDefaults": {
        "HttpTokens": "required",
        "HttpPutResponseHopLimit": 1,
        "HttpEndpoint": "enabled"
    }
}
"required"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidInstanceID.NotFound) when calling the ModifyInstanceMetadataOptions operation: The instance ID 'i-0abc123' does not exist` | Verify the instance ID exists in the target region using `aws ec2 describe-instances --instance-ids i-0abc123`. |
    | `An error occurred (UnauthorizedOperation) when calling the ModifyInstanceMetadataDefaults operation: You are not authorized to perform: ec2:ModifyInstanceMetadataDefaults` | Add the `ec2:ModifyInstanceMetadataDefaults` permission to your IAM policy. |
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

```text title="Expected output"
user,arn,user_creation_time,password_enabled,password_last_used,password_last_changed,password_next_rotation,mfa_active,access_key_1_active,access_key_1_last_rotated,access_key_2_active,access_key_2_last_rotated,cert_1_active,cert_1_last_rotated
admin,arn:aws:iam::123456789012:user/admin,2022-01-15T08:22:14+00:00,true,2024-01-10T14:33:22+00:00,2023-11-20T09:15:00+00:00,2024-02-20T09:15:00+00:00,true,true,2024-01-08T10:45:33+00:00,false,,false,
svc-deploy,arn:aws:iam::123456789012:user/svc-deploy,2023-03-22T11:05:47+00:00,false,,,,false,true,2023-09-14T16:22:11+00:00,false,,false,
jenkins-ci,arn:aws:iam::123456789012:user/jenkins-ci,2023-06-10T13:18:55+00:00,false,,,,true,true,2024-01-02T07:33:44+00:00,true,2023-08-19T12:10:22+00:00,false,

New key: AKIAIOSFODNN7EXAMPLE	wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (NoSuchEntity) when calling the GetCredentialReport operation: The credential report does not exist. Please call GenerateCredentialReport.` | Run `aws iam generate-credential-report` first, then wait 5–10 seconds before retrying the get-credential-report command. |
    | `An error occurred (NoSuchEntity) when calling the DeleteAccessKey operation: The Access Key with id AKIA<old-id> cannot be found.` | Verify the correct access key ID using `aws iam list-access-keys --user-name svc-deploy` before attempting deletion. |
    | `An error occurred (AccessDenied) when calling the CreateAccessKey operation: User: arn:aws:iam::123456789012:user/svc-deploy is not authorized to perform: iam:CreateAccessKey` | Ensure your IAM user has the `iam:CreateAccessKey` permission attached via an inline or managed policy. |
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

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "User / Service" as USR
participant "AWS" as SVC
participant "Identity Provider\n(LDAP / OIDC / AD)" as IDP
participant "Token / Session Store" as TOKEN

USR -> SVC: Authentication request
SVC -> IDP: Validate credentials
IDP --> SVC: Identity confirmed
SVC -> TOKEN: Issue session token
TOKEN --> SVC: Token granted
SVC --> USR: Access allowed

@enduml
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Aws — Access Control](../access-control/)
- [Aws — Hardening](../hardening/)
- [Aws — Encryption](../encryption/)
