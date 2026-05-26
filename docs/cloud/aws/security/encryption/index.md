# AWS — Encryption

---

## Encryption Coverage Overview

| Service | At Rest | In Transit |
|---|---|---|
| S3 | SSE-S3 (default), SSE-KMS (recommended), SSE-C | TLS 1.2+ enforced via bucket policy |
| EBS | KMS-managed CMK or AWS-managed key | N/A (within AWS fabric) |
| RDS | KMS at instance creation | TLS enforced via parameter group |
| Secrets Manager | KMS (CMK or AWS-managed) | TLS always |
| EKS secrets (etcd) | KMS envelope encryption | TLS (in-cluster) |
| DynamoDB | AWS-owned key (default), CMK optional | TLS always |
| SQS/SNS | SSE-SQS or CMK | TLS always |

---

## KMS — Customer Managed Key (CMK)

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
┌──────────────────────────────── AWS Encryption — At Rest & In Transit ────────────────────────────────┐
│                                                                                                       │
│  Encryption at rest via KMS keys; in transit via TLS; key management and rotation policy.             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              At-Rest Encryption              │  │            In-Transit Encryption            │   │
│   │          S3: SSE-S3, SSE-KMS, SSE-C          │  │          ALB/NLB: TLS 1.2+ policies         │   │
│   │           EBS: AES-256 via KMS CMK           │  │        API calls: HTTPS/TLS enforced        │   │
│   │       RDS: encryption at creation only       │  │       S3: enforce-HTTPS bucket policy       │   │
│   │         DynamoDB: enabled by default         │  │         VPN: IPSec tunnel encryption        │   │
│   │       EFS / FSx / ElastiCache: KMS opt       │  │        DirectConnect: MACsec Layer 2        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Use CMKs over AWS-managed keys for full control, key policy, and cross-account access.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Key Management                │  │            Encryption in Practice           │   │
│   │        CMK: customer-managed KMS key         │  │       S3 bucket policy: deny non-HTTPS      │   │
│   │        Key policy: who can use/admin         │  │       EBS default encryption: account       │   │
│   │        Annual auto-rotation available        │  │          RDS: encrypt before launch         │   │
│   │     Cross-region: copy snapshot with key     │  │        Config rule: encrypted-volumes       │   │
│   │      Secrets Manager: KMS envelope enc       │  │      Security Hub: encryption findings      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS KMS HSMs (FIPS 140-2 Level 3) · S3 encryption hardware · TLS termination nodes                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CMK             = Customer-Managed Key; KMS key fully controlled by the customer                     │
│  AWS-managed key = Managed by AWS per service; auto-rotate annually; less control                     │
│  Envelope encryption= Data encrypted with data key; data key encrypted with CMK                       │
│  SSE-KMS         = S3 server-side encryption using a KMS key; auditable in CloudTrail                 │
│  SSE-S3          = S3 server-side encryption with AWS-managed S3 key; no KMS audit                    │
│  SSE-C           = S3 encryption with customer-provided key; AWS does not store key                   │
│  Key rotation    = Annual automatic replacement of key material; aliases unchanged                    │
│  Key policy      = Resource-based policy on CMK defining who can use/manage the key                   │
│  Cross-region copy= Snapshot copied to another region must be re-encrypted with region key            │
│  MACsec          = Layer 2 encryption on dedicated Direct Connect connections                         │
│  TLS policy      = ALB security policy selecting supported TLS versions and ciphers                   │
│  EBS default enc = Account-level setting encrypting all new EBS volumes automatically                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## EBS — Encrypted Volume

```bash
# Enable EBS encryption by default for all new volumes in region
aws ec2 enable-ebs-encryption-by-default --region eu-west-1

# Verify
aws ec2 get-ebs-encryption-by-default --region eu-west-1

# Create encrypted EBS volume with CMK
aws ec2 create-volume \
  --availability-zone eu-west-1a \
  --size 100 \
  --volume-type gp3 \
  --encrypted \
  --kms-key-id arn:aws:kms:eu-west-1:<account>:alias/prod-ebs-cmk

# Encrypt an existing unencrypted volume (via snapshot copy)
SNAP_ID=$(aws ec2 create-snapshot --volume-id vol-<unencrypted> \
  --description "pre-encrypt" --query SnapshotId --output text)
aws ec2 copy-snapshot \
  --source-region eu-west-1 \
  --source-snapshot-id $SNAP_ID \
  --encrypted \
  --kms-key-id alias/prod-ebs-cmk \
  --region eu-west-1
```

---

## RDS — Encryption at Rest

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

---

## RDS — Enforce TLS

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

---

## EKS — Secrets Encryption at Rest

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

---

## Secrets Manager — CMK

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

---

## ACM — TLS Certificate

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

---

## Audit — Unencrypted Resources

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
