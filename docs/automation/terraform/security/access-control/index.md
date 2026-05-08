# Terraform — Access Control

## State Backend Access Control

The Terraform state file contains sensitive resource attributes including passwords, private keys, and connection strings. Restrict access strictly.

### S3 Backend

```hcl
# backend.tf — encrypted S3 bucket with DynamoDB locking
terraform {
  backend "s3" {
    bucket         = "myorg-terraform-state"
    key            = "production/network/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

```json
// S3 bucket policy — restrict to the Terraform automation role only
{
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::123456789:role/terraform-automation" },
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::myorg-terraform-state/*"
    },
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::myorg-terraform-state", "arn:aws:s3:::myorg-terraform-state/*"],
      "Condition": {
        "Bool": { "aws:SecureTransport": "false" }
      }
    }
  ]
}
```

## Least Privilege IAM for Terraform

Create a dedicated IAM role for Terraform with only the permissions required for the resources it manages.

```bash
# Verify effective permissions of the Terraform role
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789:role/terraform-automation \
  --action-names s3:GetObject ec2:DescribeInstances \
  --resource-arns "*"

# List all policies attached to the Terraform role
aws iam list-attached-role-policies --role-name terraform-automation
```

## Workspace and Environment Separation

Use separate credentials and backends per environment to prevent a staging Terraform run from modifying production.

```hcl
# Use workspace-specific state paths
terraform {
  backend "s3" {
    bucket = "myorg-terraform-state"
    key    = "env/${terraform.workspace}/terraform.tfstate"
    region = "eu-west-1"
  }
}
```

## Access Control Reference

| Area | Practice |
|---|---|
| State bucket | Private, encrypted, access restricted to Terraform role |
| State locking | DynamoDB or equivalent backend locking enabled |
| IAM role | Dedicated per-environment role with least privilege |
| CI/CD | Credentials injected via secrets; not stored in code |
| Human access | Use read-only credentials for review; write credentials for planned applies only |
