# Python Automation — Access Control

## Least Privilege Access Model

```mermaid
graph TD
    script["Python Script\n(automation job)"]
    svcAccount["Dedicated Service Account\n(linux: automation user)"]
    iamRole["IAM Role / API Token\n(scoped to task)"]
    readOnly["Read-Only Permissions\n(for reporting scripts)"]
    writePerms["Write Permissions\n(only for change scripts)"]
    auditLog["Audit Log\n(quarterly review)"]

    script --> svcAccount
    svcAccount --> iamRole
    iamRole --> readOnly
    iamRole --> writePerms
    svcAccount --> auditLog
    iamRole --> auditLog
```

## Least Privilege

Automation scripts should run with the minimum permissions required to complete their task.

- Use a dedicated service account or IAM role — not a personal account
- Scope API tokens to specific resources and actions (e.g. read-only unless writes are needed)
- Rotate tokens on a schedule; revoke tokens when a script is retired
- Audit which scripts use which credentials at least quarterly

## Service Accounts

```bash
# Create a dedicated Linux user for automation scripts
sudo useradd -r -s /usr/sbin/nologin automation

# Run a cron job as the automation user
sudo -u automation crontab -e

# Restrict access to the script directory
chown -R automation:automation /opt/automation/scripts
chmod 750 /opt/automation/scripts
```

```python
# Verify the script is running as the expected user at startup
import os, sys

EXPECTED_USER = "automation"
if os.getlogin() != EXPECTED_USER:
    sys.exit(f"ERROR: This script must run as '{EXPECTED_USER}', not '{os.getlogin()}'")
```

## AWS IAM Least Privilege

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-automation-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

```bash
# Verify effective permissions for an IAM role
aws sts get-caller-identity
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789:role/automation-role \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/*
```

## Access Policies Reference

| Principle | Practice |
|---|---|
| Least privilege | Grant only the permissions the script actually needs |
| Separation of duties | Read-only scripts use read-only tokens; write scripts use write tokens |
| Token scoping | Scope API tokens to specific resources, not entire platforms |
| Account isolation | Use a dedicated service account — never a personal account |
| Regular review | Audit script credentials and permissions quarterly |
