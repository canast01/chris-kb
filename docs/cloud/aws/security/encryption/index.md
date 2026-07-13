---
tags:
  - aws
  - security
---
# AWS Encryption — At Rest & In Transit

```bash
# Create a CMK with key rotation enabled
aws kms create-key \
  --description "prod-s3-cmk" \
  --key-usage ENCRYPT_DECRYPT \
  --origin AWS_KMS

KEY_ID=$(aws kms list-keys --query 'Keys[0].KeyId' --output text)

# Enable annual automatic rotation
aws kms enable-key-rotation --key-id $KEY_ID

# Create an alias
aws kms create-alias \
  --alias-name alias/prod-s3-cmk \
  --target-key-id $KEY_ID

# Verify rotation is enabled
aws kms get-key-rotation-status --key-id $KEY_ID
```


```text title="Expected output"
{
    "KeyMetadata": {
        "AWSAccountId": "123456789012",
        "KeyId": "arn:aws:kms:us-east-1:123456789012:key/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "Arn": "arn:aws:kms:us-east-1:123456789012:key/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "CreationDate": "2024-01-15T14:32:18.123000+00:00",
        "Enabled": true,
        "Description": "prod-s3-cmk",
        "KeyUsage": "ENCRYPT_DECRYPT",
        "KeyState": "Enabled",
        "Origin": "AWS_KMS"
    }
}
(no output — command completes silently)
(no output — command completes silently)
{
    "KeyRotationEnabled": true
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (AccessDenied) when calling the CreateKey operation: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: kms:CreateKey` | Attach the `AWSKeyManagementServicePowerUser` policy or a custom policy with `kms:CreateKey` permission to the IAM user/role. |
    | `An error occurred (NotFoundException) when calling the GetKeyRotationStatus operation: Key 'arn:aws:kms:us-east-1:123456789012:key/invalid-key-id' does not exist` | Verify the KEY_ID variable was populated correctly by running `echo $KEY_ID` and ensure the key exists in the current region. |
```bash
# Encryption must be enabled at creation (cannot enable on existing instance)
aws rds create-db-instance \
  --db-instance-identifier prod-mysql \
  --db-instance-class db.r6g.large \
  --engine mysql \
  --engine-version 8.0 \
  --master-username admin \
  --master-user-password '<password>' \
  --storage-type gp3 \
  --allocated-storage 100 \
  --storage-encrypted \
  --kms-key-id arn:aws:kms:eu-west-1:<account>:alias/prod-rds-cmk \
  --multi-az

# Encrypt existing unencrypted RDS (snapshot → copy encrypted → restore)
aws rds create-db-snapshot \
  --db-instance-identifier prod-mysql \
  --db-snapshot-identifier prod-mysql-for-encryption
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier prod-mysql-for-encryption \
  --target-db-snapshot-identifier prod-mysql-encrypted \
  --kms-key-id arn:aws:kms:eu-west-1:<account>:alias/prod-rds-cmk
# Then restore from encrypted snapshot
```

```text title="Expected output"
{
    "DBInstance": {
        "DBInstanceIdentifier": "prod-mysql",
        "DBInstanceClass": "db.r6g.large",
        "Engine": "mysql",
        "DBInstanceStatus": "creating",
        "MasterUsername": "admin",
        "AllocatedStorage": 100,
        "StorageType": "gp3",
        "StorageEncrypted": true,
        "KmsKeyId": "arn:aws:kms:eu-west-1:123456789012:alias/prod-rds-cmk",
        "MultiAZ": true,
        "EngineVersion": "8.0.35"
    }
}

{
    "DBSnapshot": {
        "DBSnapshotIdentifier": "prod-mysql-for-encryption",
        "DBInstanceIdentifier": "prod-mysql",
        "SnapshotCreateTime": "2024-01-15T14:32:18.000Z",
        "Engine": "mysql",
        "AllocatedStorage": 100,
        "Status": "available",
        "StorageEncrypted": false
    }
}

{
    "DBSnapshot": {
        "DBSnapshotIdentifier": "prod-mysql-encrypted",
        "SourceDBSnapshotIdentifier": "prod-mysql-for-encryption",
        "SnapshotCreateTime": "2024-01-15T14:35:42.000Z",
        "Engine": "mysql",
        "AllocatedStorage": 100,
        "Status": "available",
        "StorageEncrypted": true,
        "KmsKeyId": "arn:aws:kms:eu-west-1:123456789012:alias/prod-rds-cmk"
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidParameterValue) when calling the CreateDBInstance operation: The KMS key ARN is invalid or the KMS key is not accessible.` | Verify the KMS key ARN exists in the same region and your IAM role has `kms:Decrypt` and `kms:GenerateDataKey` permissions. |
    | `An error occurred (DBSnapshotNotFound) when calling the CopyDBSnapshot operation: DBSnapshot prod-mysql-for-encryption not found.` | Ensure the source snapshot identifier matches exactly and the snapshot has finished creating (check status with `aws rds describe-db-snapshots`). |
```bash
# For MySQL/MariaDB — create parameter group with require_secure_transport=1
aws rds create-db-parameter-group \
  --db-parameter-group-name prod-mysql-tls \
  --db-parameter-group-family mysql8.0 \
  --description "Require TLS"

aws rds modify-db-parameter-group \
  --db-parameter-group-name prod-mysql-tls \
  --parameters ParameterName=require_secure_transport,ParameterValue=1,ApplyMethod=immediate

aws rds modify-db-instance \
  --db-instance-identifier prod-mysql \
  --db-parameter-group-name prod-mysql-tls \
  --apply-immediately
```

```text title="Expected output"
{
    "DBParameterGroup": {
        "DBParameterGroupName": "prod-mysql-tls",
        "DBParameterGroupFamily": "mysql8.0",
        "Description": "Require TLS",
        "DBParameterGroupArn": "arn:aws:rds:us-east-1:123456789012:pg:prod-mysql-tls",
        "ParameterGroupStatus": "creating"
    }
}
{
    "DBParameterGroup": {
        "DBParameterGroupName": "prod-mysql-tls",
        "DBParameterGroupFamily": "mysql8.0",
        "ParameterGroupStatus": "in-sync"
    }
}
{
    "DBInstance": {
        "DBInstanceIdentifier": "prod-mysql",
        "DBInstanceStatus": "modifying",
        "Engine": "mysql",
        "EngineVersion": "8.0.35",
        "DBParameterGroups": [
            {
                "DBParameterGroupName": "prod-mysql-tls",
                "ParameterApplyStatus": "pending-reboot"
            }
        ],
        "PendingModifiedValues": {
            "DBParameterGroupName": "prod-mysql-tls"
        }
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (DBParameterGroupAlreadyExists) when calling the CreateDBParameterGroup operation: DB parameter group prod-mysql-tls already exists` | Delete the existing parameter group with `aws rds delete-db-parameter-group --db-parameter-group-name prod-mysql-tls` or use a unique name. |
    | `An error occurred (InvalidDBInstanceState) when calling the ModifyDBInstance operation: DB instance prod-mysql is not in a valid state.` | Wait for the instance to reach "available" status with `aws rds describe-db-instances --db-instance-identifier prod-mysql` before applying changes. |
    | `An error occurred (InvalidParameterValue) when calling the ModifyDBParameterGroup operation: The parameter require_secure_transport cannot be modified for this DB engine version.` | Verify the parameter is supported in your MySQL version; use `aws rds describe-db-parameters --db-parameter-group-name prod-mysql-tls` to confirm availability. |
```bash
# Enable envelope encryption of Kubernetes secrets with CMK
aws eks associate-encryption-config \
  --cluster-name my-cluster \
  --encryption-config '[{
    "resources": ["secrets"],
    "provider": {
      "keyArn": "arn:aws:kms:eu-west-1:<account>:alias/prod-eks-cmk"
    }
  }]'

# Verify
aws eks describe-cluster --name my-cluster \
  --query 'cluster.encryptionConfig'
```

```text title="Expected output"
{
    "encryptionConfig": [
        {
            "resources": [
                "secrets"
            ],
            "provider": {
                "keyArn": "arn:aws:kms:eu-west-1:123456789012:alias/prod-eks-cmk"
            }
        }
    ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidParameterException) when calling the AssociateEncryptionConfig operation: Encryption config is invalid` | Verify the KMS key ARN exists and your IAM principal has `kms:CreateGrant` and `kms:DescribeKey` permissions on that key. |
    | `An error occurred (ResourceInUseException) when calling the AssociateEncryptionConfig operation: Cluster is in use and cannot be modified` | Wait for any ongoing cluster updates to complete by checking `aws eks describe-cluster --name my-cluster --query 'cluster.status'` until it returns `ACTIVE`. |
    | `An error occurred (AccessDenied) when calling the AssociateEncryptionConfig operation: User is not authorized to perform: eks:AssociateEncryptionConfig` | Add the `eks:AssociateEncryptionConfig` action to your IAM policy for the EKS cluster resource. |
```bash
# Create secret with CMK
aws secretsmanager create-secret \
  --name prod/myapp/db-password \
  --secret-string '{"username":"app","password":"<pass>"}' \
  --kms-key-id arn:aws:kms:eu-west-1:<account>:alias/prod-secrets-cmk

# Retrieve secret value
aws secretsmanager get-secret-value \
  --secret-id prod/myapp/db-password \
  --query SecretString --output text | python3 -m json.tool

# Rotate secret (enable rotation)
aws secretsmanager rotate-secret \
  --secret-id prod/myapp/db-password \
  --rotation-lambda-arn arn:aws:lambda:eu-west-1:<account>:function:RotateRDSPassword \
  --rotation-rules AutomaticallyAfterDays=30
```

```text title="Expected output"
{
    "ARN": "arn:aws:secretsmanager:eu-west-1:123456789012:secret:prod/myapp/db-password-AbCdE",
    "Name": "prod/myapp/db-password",
    "VersionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
{
  "username": "app",
  "password": "<pass>"
}
{
    "ARN": "arn:aws:secretsmanager:eu-west-1:123456789012:secret:prod/myapp/db-password-AbCdE",
    "Name": "prod/myapp/db-password",
    "VersionId": "b2c3d4e5-f6a7-8901-bcde-f12345678901"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (InvalidParameterException) when calling the CreateSecret operation: The KMS key ARN provided is invalid or you do not have permission to use it.` | Verify the CMK ARN exists in the target region and your IAM role has `kms:Decrypt` and `kms:GenerateDataKey` permissions. |
    | `An error occurred (ResourceNotFoundException) when calling the GetSecretValue operation: Secrets Manager can't find the specified secret.` | Confirm the secret name matches exactly (case-sensitive) and exists in the current AWS region. |
    | `An error occurred (InvalidParameterException) when calling the RotateSecret operation: The Lambda function does not have permission to access the secret.` | Add a resource-based policy to the Lambda function allowing `secretsmanager:GetSecretValue` and ensure the rotation function has the correct IAM execution role. |
```bash
# Request a public ACM certificate (DNS validation)
aws acm request-certificate \
  --domain-name example.com \
  --subject-alternative-names "*.example.com" \
  --validation-method DNS \
  --region eu-west-1

# Get DNS validation records
aws acm describe-certificate \
  --certificate-arn arn:aws:acm:eu-west-1:<account>:certificate/<id> \
  --query 'Certificate.DomainValidationOptions[*].[DomainName,ResourceRecord.Name,ResourceRecord.Value]' \
  --output table

# Import existing certificate (from external CA)
aws acm import-certificate \
  --certificate fileb://cert.pem \
  --private-key fileb://key.pem \
  --certificate-chain fileb://chain.pem \
  --region eu-west-1
```

```text title="Expected output"
{
    "CertificateArn": "arn:aws:acm:eu-west-1:123456789012:certificate/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6"
}
---------------------------------------------------------------------------
| DomainName      | ResourceRecord.Name                    | ResourceRecord.Value                                    |
|---------------------------------------------------------------------------
| example.com     | _a1b2c3d4e5f6g7h8.example.com.         | _9x8y7w6v5u4t3s2r1q0p9o8n7m6l5k4j.acm-validations.aws. |
| *.example.com   | _a1b2c3d4e5f6g7h8.example.com.         | _9x8y7w6v5u4t3s2r1q0p9o8n7m6l5k4j.acm-validations.aws. |
---------------------------------------------------------------------------
{
    "CertificateArn": "arn:aws:acm:eu-west-1:123456789012:certificate/b2c3d4e5-f6g7-48h9-i0j1-k2l3m4n5o6p7"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `An error occurred (ValidationException) when calling the RequestCertificate operation: Domain name is invalid or does not exist` | Verify the domain name is correctly spelled and publicly resolvable via DNS. |
    | `An error occurred (CertificateAlreadyExists) when calling the ImportCertificate operation: Certificate with the same domain name already exists` | Delete or retire the existing certificate in ACM before importing a replacement. |
    | `An error occurred (InvalidParameterException) when calling the DescribeCertificate operation: Invalid ARN` | Replace the placeholder `<account>` and `<id>` with actual AWS account ID and certificate ID from the request-certificate output. |
```bash
# S3 buckets without default encryption
aws s3api list-buckets --query 'Buckets[*].Name' --output text | \
  tr '\t' '\n' | while read bucket; do
    ENC=$(aws s3api get-bucket-encryption --bucket "$bucket" \
      --query 'ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm' \
      --output text 2>/dev/null || echo "NONE")
    echo "$bucket: $ENC"
  done

# EBS volumes not encrypted
aws ec2 describe-volumes \
  --filters "Name=encrypted,Values=false" \
  --query 'Volumes[*].[VolumeId,Size,State,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# RDS instances not encrypted
aws rds describe-db-instances \
  --query 'DBInstances[?StorageEncrypted==`false`].[DBInstanceIdentifier,Engine,StorageEncrypted]' \
  --output table
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

- [Aws — Hardening](../hardening/)
- [Aws — Authentication](../authentication/)
- [Aws — Access Control](../access-control/)
