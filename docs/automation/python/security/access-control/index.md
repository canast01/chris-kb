---
tags:
  - python
  - security
description: "Access Control reference covering Least Privilege Access Model, AWS IAM Least Privilege, Access Policies Reference."
---
# Python Automation — Access Control

<div class="kb-summary">
Access Control reference covering Least Privilege Access Model, AWS IAM Least Privilege, Access Policies Reference.

*Applies to: Python 3.x*
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Least Privilege Access Model

```d2
direction: right

script: "Python Script\n(automation job" {shape: rectangle}
svcAccount: "Dedicated Service Account\n(linux: automation user" {shape: rectangle}
iamRole: "IAM Role / API Token\n(scoped to task" {shape: rectangle}
readOnly: "Read-Only Permissions\n(for reporting scripts" {shape: rectangle}
writePerms: "Write Permissions\n(only for change scripts" {shape: rectangle}
auditLog: "Audit Log\n(quarterly review" {shape: rectangle}

script -> svcAccount
svcAccount -> iamRole
iamRole -> readOnly
iamRole -> writePerms
svcAccount -> auditLog
iamRole -> auditLog
```

```bash
# Verify effective permissions for an IAM role
aws sts get-caller-identity
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789:role/automation-role \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/*
```


```text title="Expected output"
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/automation-admin"
}
{
    "EvaluationResults": [
        {
            "EvalActionName": "s3:GetObject",
            "EvalResourceName": "arn:aws:s3:::my-bucket/*",
            "EvalDecision": "allowed",
            "MatchedStatements": [
                {
                    "SourceStatement": "arn:aws:iam::123456789012:role/automation-role inline policy"
                }
            ],
            "EvalDecisionDetails": {},
            "ResourceSpecificResults": []
        }
    ]
}
```

!!! warning "Common errors"
    **`An error occurred (NoSuchEntity) when calling the SimulatePrincipalPolicy operation: The role with name automation-role cannot be found.`** — Verify the role name and account ID match exactly, then check that the role exists in the target account using `aws iam get-role --role-name automation-role`.
    **`An error occurred (AccessDenied) when calling the SimulatePrincipalPolicy operation: User: arn:aws:iam::123456789012:user/automation-admin is not authorized to perform: iam:SimulatePrincipalPolicy`** — Add the `iam:SimulatePrincipalPolicy` permission to your current user's IAM policy.
## Access Policies Reference

| Principle | Practice |
|---|---|
| Least privilege | Grant only the permissions the script actually needs |
| Separation of duties | Read-only scripts use read-only tokens; write scripts use write tokens |
| Token scoping | Scope API tokens to specific resources, not entire platforms |
| Account isolation | Use a dedicated service account — never a personal account |
| Regular review | Audit script credentials and permissions quarterly |

---

## See also

- [Python — Authentication](../authentication/)
- [Python — Hardening](../hardening/)
- [Python — Encryption](../encryption/)
