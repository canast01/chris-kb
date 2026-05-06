# Identity & Access (IAM / STS)

> Part of the AWS CLI Reference.

---

```bash
# Current identity
aws sts get-caller-identity

# IAM users
aws iam list-users
aws iam get-user --user-name <user>
aws iam create-user --user-name <user>
aws iam delete-user --user-name <user>

# IAM groups
aws iam list-groups
aws iam add-user-to-group --user-name <user> --group-name <group>

# IAM roles
aws iam list-roles
aws iam get-role --role-name <role>
aws iam create-role --role-name <role> --assume-role-policy-document file://trust.json
aws iam attach-role-policy --role-name <role> --policy-arn <arn>

# Access keys
aws iam list-access-keys --user-name <user>
aws iam create-access-key --user-name <user>
aws iam delete-access-key --user-name <user> --access-key-id <id>

# Assume role
aws sts assume-role --role-arn <arn> --role-session-name session1
```
