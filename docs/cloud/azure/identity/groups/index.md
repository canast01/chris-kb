# Azure — Groups

Entra ID (Azure AD) groups are the primary mechanism for managing access at scale.

```
┌──────────────────────────────────────────────────────────────┐
│                  Entra ID Group Flow                         │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Security Group  (type: security, assignable to role)│    │
│  │                                                      │    │
│  │  Members ──► users / nested groups / service prncpls │    │
│  └──────────────────────────┬─────────────────────────┘     │
│                             │                                │
│                             ▼ role assignment                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  RBAC Role Assignment                                │    │
│  │  Group ──► "Contributor" ──► /subscriptions/.../rg   │    │
│  └──────────────────────────┬─────────────────────────┘     │
│                             │                                │
│                             ▼ access scope                   │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Resource Group / Resource  (inherited by all members│    │
│  │  including transitive nested group membership)       │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
``` Assign roles and permissions to groups rather than individual users.

## Group Types

| Type | Assignable to Azure roles | Use case |
|---|---|---|
| **Security group** | Yes | Azure RBAC, app access, conditional access |
| **Microsoft 365 group** | No | Collaboration (Teams, SharePoint, Exchange) |
| **Distribution group** | No | Email distribution lists only |

For Azure RBAC and resource access, always use Security groups.

## Membership Types

| Type | How members are added | License required |
|---|---|---|
| **Assigned** | Manually by admin | None |
| **Dynamic user** | Rule-based on user attributes | Entra ID P1 or P2 |
| **Dynamic device** | Rule-based on device attributes | Entra ID P1 or P2 |

## Managing Groups

### Azure CLI

```bash
# List all groups
az ad group list --output table

# Get group details
az ad group show --group <group-name-or-object-id>

# Create a security group
az ad group create \
  --display-name "storage-prod-readers" \
  --mail-nickname "storage-prod-readers"

# Add a member
az ad group member add \
  --group <group-object-id> \
  --member-id <user-or-group-object-id>

# Remove a member
az ad group member remove \
  --group <group-object-id> \
  --member-id <user-object-id>

# List members
az ad group member list --group <group-object-id> --output table

# Check membership (direct or transitive)
az ad group member check \
  --group <group-object-id> \
  --member-id <user-object-id>

# Delete group
az ad group delete --group <group-object-id>
```

### PowerShell

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

```
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

```bash
# Create dynamic group
az ad group create \
  --display-name "dynamic-engineers" \
  --mail-nickname "dynamic-engineers" \
  --group-types "DynamicMembership" \
  --membership-rule '(user.department -eq "Engineering")' \
  --membership-rule-processing-state "On"
```

Dynamic group updates can take up to 24 hours after a rule or attribute change.

## Nested Groups

Security groups can be nested — a group can be a member of another group. Azure RBAC honours transitive membership.

```bash
# Add group-B as a member of group-A
az ad group member add \
  --group <group-A-object-id> \
  --member-id <group-B-object-id>
```

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| User not receiving access after being added | RBAC propagation delay (up to 10 min) | Wait; verify with `az ad group member check` |
| Dynamic group not updating | Rule evaluation delay or invalid rule syntax | Test rule in Entra Portal → Groups → Dynamic membership rules → Validate rules |
| Cannot assign group to Azure role | Group is not a security group (e.g., M365 group) | Recreate as security group |
| Transitive access not working | PIM eligible group memberships are not transitive | Activate eligible membership before relying on nested access |
| Group deletion didn't remove access immediately | Token caching — existing tokens remain valid until expiry | Wait for token TTL (typically 1 hour) |
