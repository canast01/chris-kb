# Secrets Manager

AWS Secrets Manager — secrets storage, rotation, and lifecycle management.

## Key Concepts

| Concept | Description |
|---|---|
| Secret | Stored credential, API key, or config value |
| Rotation | Automatic periodic secret rotation using a Lambda function |
| Secret version | Immutable value; multiple versions stored per secret |
| AWSCURRENT | Label for the current active version |
| AWSPENDING | Label for the version being rotated in |
| AWSPREVIOUS | Label for the previous version (kept for rollback) |

## Common CLI Commands

```bash
# List secrets
aws secretsmanager list-secrets \
  --query 'SecretList[*].{Name:Name,LastChanged:LastChangedDate,RotationEnabled:RotationEnabled}' \
  --output table

# Get a secret value
aws secretsmanager get-secret-value \
  --secret-id <secret-name-or-arn> \
  --query 'SecretString' \
  --output text

# Create a new secret
aws secretsmanager create-secret \
  --name "prod/app/db-password" \
  --secret-string '{"username":"app","password":"secret-value"}' \
  --kms-key-id alias/aws/secretsmanager

# Update an existing secret
aws secretsmanager put-secret-value \
  --secret-id "prod/app/db-password" \
  --secret-string '{"username":"app","password":"new-secret-value"}'

# Rotate secret immediately (if rotation is configured)
aws secretsmanager rotate-secret \
  --secret-id "prod/app/db-password"

# Describe secret (rotation config, version info)
aws secretsmanager describe-secret --secret-id <secret-name>
```

## Retrieve Secret Value in Code

**Python (boto3):**
```python
import boto3
import json

client = boto3.client('secretsmanager', region_name='eu-west-1')
response = client.get_secret_value(SecretId='prod/app/db-password')
secret = json.loads(response['SecretString'])
db_password = secret['password']
```

**PowerShell:**
```powershell
$secret = Get-SECSecretValue -SecretId 'prod/app/db-password'
$values = $secret.SecretString | ConvertFrom-Json
$password = $values.password
```

## Rotation Setup

```bash
# Enable automatic rotation (using AWS-managed Lambda for RDS)
aws secretsmanager rotate-secret \
  --secret-id "prod/app/db-password" \
  --rotation-lambda-arn arn:aws:lambda:<region>:<account>:function:SecretsManagerRDSRotation \
  --rotation-rules AutomaticallyAfterDays=30

# Check rotation status
aws secretsmanager describe-secret --secret-id <secret-name> \
  --query '{RotationEnabled:RotationEnabled,LastRotatedDate:LastRotatedDate,NextRotationDate:NextRotationDate}'
```

## Access Control

```json
// IAM policy — allow application to read a specific secret
{
  "Effect": "Allow",
  "Action": ["secretsmanager:GetSecretValue"],
  "Resource": "arn:aws:secretsmanager:<region>:<account>:secret:prod/app/*"
}
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| `AccessDenied` on `GetSecretValue` | IAM policy | Add `secretsmanager:GetSecretValue` and `kms:Decrypt` for the KMS key |
| Rotation failing | Lambda logs | Check CloudWatch Logs for the rotation Lambda function |
| Secret not rotating on schedule | Rotation enabled? | Verify `RotationEnabled=true`; check rotation Lambda health |
| App using old password | Version stage | Ensure app is fetching `AWSCURRENT` version, not caching the old value |
