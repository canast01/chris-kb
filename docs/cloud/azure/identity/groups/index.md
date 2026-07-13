---
tags:
  - azure
description: "Entra ID (Azure AD) groups are the primary mechanism for managing access at scale."
---
# Azure — Groups

<div class="kb-summary">
Entra ID (Azure AD) groups are the primary mechanism for managing access at scale.

*Applies to: Azure*
</div>

```d2
direction: down

powershell: "PowerShell" {shape: rectangle}
dynamic_membership_rules: "Dynamic Membership Rules" {shape: rectangle}
nested_groups: "Nested Groups" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}

powershell -> dynamic_membership_rules: uses
dynamic_membership_rules -> nested_groups: uses
nested_groups -> common_issues: uses
```

## PowerShell

```powershell
# List groups
Get-AzADGroup | Select-Object DisplayName, Id, SecurityEnabled

# Create group
New-AzADGroup -DisplayName "storage-prod-readers" -MailNickname "storage-prod-readers" -SecurityEnabled

# Add member
Add-AzADGroupMember -TargetGroupObjectId <group-id> -MemberObjectId <user-id>

# List members
Get-AzADGroupMember -GroupObjectId <group-id>
```

## Dynamic Membership Rules

Dynamic groups evaluate rules against user attributes and update membership automatically.

```bash
# All users in a department
(user.department -eq "Engineering")

# Users by job title
(user.jobTitle -contains "Engineer")

# Country + company
(user.country -eq "AU") and (user.companyName -eq "Contoso")

# Custom extension attribute
(user.extensionAttribute1 -eq "prod-access")

# All guest users
(user.userType -eq "Guest")
```


```text title="Expected output"
(no output — these are Azure AD dynamic group membership rule expressions, not executable commands)
```

!!! warning "Common errors"
    **`Syntax error: unexpected token 'eq'`** — Ensure the rule is entered in the Azure Portal's "Dynamic membership rules" editor or via Microsoft Graph API, not executed as a bash command.
    **`Property 'jobTitle' is not a valid user property`** — Verify the attribute name exists in your Azure AD schema; use `user.jobTitle` (camelCase) rather than `user.job_title` or other variations.
    **`The rule contains an unsupported operator or property`** — Confirm you are using supported operators (`-eq`, `-ne`, `-contains`, `-notContains`, `-startsWith`, `-notStartsWith`) and valid user object properties documented in Azure AD.
```bash
# Create dynamic group
az ad group create \
  --display-name "dynamic-engineers" \
  --mail-nickname "dynamic-engineers" \
  --group-types "DynamicMembership" \
  --membership-rule '(user.department -eq "Engineering")' \
  --membership-rule-processing-state "On"
```


```text title="Expected output"
{
  "displayName": "dynamic-engineers",
  "id": "a7c2f891-4e3a-4b9c-8d1f-2e5a9c3b7f4a",
  "mailNickname": "dynamic-engineers",
  "mailEnabled": false,
  "securityEnabled": true,
  "groupTypes": [
    "DynamicMembership"
  ],
  "membershipRule": "(user.department -eq \"Engineering\")",
  "membershipRuleProcessingState": "On",
  "createdDateTime": "2024-01-15T10:32:47.123Z"
}
```

!!! warning "Common errors"
    **`Error: Invalid membership rule syntax`** — Verify the membership rule uses correct Azure AD query syntax (e.g., property names are case-sensitive and must match Azure AD schema).
    **`Error: Insufficient privileges to create groups`** — Ensure your Azure AD account has the Directory.ReadWrite.All permission or Group.Create permission in the target tenant.
    **`Error: Mail nickname 'dynamic-engineers' is already in use`** — Choose a unique mail-nickname value that doesn't conflict with existing groups or distribution lists.
Dynamic group updates can take up to 24 hours after a rule or attribute change.

## Nested Groups

Security groups can be nested — a group can be a member of another group. Azure RBAC honours transitive membership.

```bash
# Add group-B as a member of group-A
az ad group member add \
  --group <group-A-object-id> \
  --member-id <group-B-object-id>
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: The following arguments are required: --group, --member-id`** — Ensure both `<group-A-object-id>` and `<group-B-object-id>` are replaced with actual Azure AD object IDs (run `az ad group list --query "[].{name:displayName, id:objectId}"` to retrieve them).
    **`Error: Authorization_RequestDenied: Insufficient privileges to complete the operation.`** — Verify your Azure CLI account has the "Groups Administrator" or "Directory Administrator" role in the target Azure AD tenant.
## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| User not receiving access after being added | RBAC propagation delay (up to 10 min) | Wait; verify with `az ad group member check` |
| Dynamic group not updating | Rule evaluation delay or invalid rule syntax | Test rule in Entra Portal → Groups → Dynamic membership rules → Validate rules |
| Cannot assign group to Azure role | Group is not a security group (e.g., M365 group) | Recreate as security group |
| Transitive access not working | PIM eligible group memberships are not transitive | Activate eligible membership before relying on nested access |
| Group deletion didn't remove access immediately | Token caching — existing tokens remain valid until expiry | Wait for token TTL (typically 1 hour) |
