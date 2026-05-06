# Systems Manager (SSM)

> Part of the AWS CLI Reference.

---

```bash
# Session (no SSH needed)
aws ssm start-session --target <instance_id>

# Run command
aws ssm send-command --instance-ids <id> --document-name "AWS-RunShellScript" --parameters commands="uptime"
aws ssm list-command-invocations --command-id <cmd_id> --details

# Parameter Store
aws ssm get-parameter --name /my/param --with-decryption
aws ssm put-parameter --name /my/param --value "value" --type SecureString
aws ssm get-parameters-by-path --path /my/
```
