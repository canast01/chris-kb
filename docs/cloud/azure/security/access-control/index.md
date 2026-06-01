# Azure — Access Control


<div class="kb-summary">
Azure access control is built on Azure Role-Based Access Control (RBAC).
</div>
```
┌──────────────────────────────── Cloud Azure Security — Access Control ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Azure access control: RBAC roles, least-privilege, and access audit logging          │   │
│   │        Roles: admin (full), operator (read/modify), read-only (view); map to AD groups        │   │
│   │       Authentication: local accounts, LDAP/AD integration, and MFA for privileged users       │   │
│   │          Audit: log all admin actions; review access logs monthly; rotate credentials         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify user → assign role → enforce MFA → audit → review quarterly                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Role       │   Permissions    │       Scope       │       Auth       │   Review cycle   │   │
│   │      Admin       │    Full CRUD     │       Global      │   MFA required   │     Monthly      │   │
│   │     Operator     │   Read/modify    │      Assigned     │   MFA required   │    Quarterly     │   │
│   │    Read-only     │    View only     │      Assigned     │     Password     │    Quarterly     │   │
│   │   Service acct   │     API only     │    Specific API   │    Token/cert    │      Annual      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Security infrastructure · management network · monitoring                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Security platform overview and core concepts                      │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


 Permissions are assigned by attaching role definitions to security principals (users, groups, service principals, managed identities) at a specific scope (management group, subscription, resource group, or resource).

---

## RBAC Fundamentals

| Concept | Description |
|---|---|
| Role definition | A collection of permissions (actions, notActions, dataActions) |
| Security principal | User, group, service principal, or managed identity |
| Scope | Management group → subscription → resource group → resource (permissions inherit down) |
| Role assignment | Binds a role definition to a principal at a scope |

### Built-in Roles (Most Common)

| Role | Scope | Use |
|---|---|---|
| Owner | Any | Full access including role assignment delegation |
| Contributor | Any | Full resource management, no role assignments |
| Reader | Any | Read-only across all resources |
| User Access Administrator | Any | Manage role assignments only |
| Virtual Machine Contributor | Resource group / resource | Manage VMs, no network/storage access |
| Storage Blob Data Contributor | Storage account | Read/write/delete blob data |
| Key Vault Secrets Officer | Key Vault | Read and write secrets |
| Network Contributor | Resource group | Manage all network resources |

---

## Role Assignments

### View Existing Assignments

```bash
# All role assignments in a subscription
az role assignment list --subscription <sub-id> --output table

# Assignments for a specific principal
az role assignment list --assignee <user-upn-or-object-id> --output table

# Assignments at a specific resource group
az role assignment list --resource-group <rg-name> --output table

# Include inherited assignments from parent scopes
az role assignment list --resource-group <rg-name> --include-inherited --output table
```

### Create a Role Assignment

```bash
# Assign Contributor at resource group scope
az role assignment create \
  --role "Contributor" \
  --assignee <user-upn-or-object-id> \
  --resource-group <rg-name>

# Assign a built-in role at subscription scope
az role assignment create \
  --role "Reader" \
  --assignee <group-object-id> \
  --scope "/subscriptions/<sub-id>"

# Assign at a specific resource
az role assignment create \
  --role "Storage Blob Data Contributor" \
  --assignee <sp-object-id> \
  --scope "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<sa>"
```

### Remove a Role Assignment

```bash
az role assignment delete \
  --role "Contributor" \
  --assignee <user-upn-or-object-id> \
  --resource-group <rg-name>
```

---

## Custom Roles

Use custom roles when built-in roles are too broad. Custom roles can restrict actions to specific resource providers and operations.

```bash
# List all custom roles in the tenant
az role definition list --custom-role-only true --output table

# Create a custom role from a JSON definition
az role definition create --role-definition @custom-role.json
```

Example `custom-role.json`:

```json
{
  "Name": "VM Start Stop Only",
  "Description": "Can start and stop VMs but cannot create or delete them",
  "Actions": [
    "Microsoft.Compute/virtualMachines/start/action",
    "Microsoft.Compute/virtualMachines/deallocate/action",
    "Microsoft.Compute/virtualMachines/restart/action",
    "Microsoft.Compute/virtualMachines/read"
  ],
  "NotActions": [],
  "DataActions": [],
  "AssignableScopes": [
    "/subscriptions/<sub-id>"
  ]
}
```

```bash
# Update a custom role
az role definition update --role-definition @custom-role-updated.json

# Delete a custom role (remove all assignments first)
az role definition delete --name "VM Start Stop Only"
```

---

## Managed Identities

Managed identities allow Azure resources (VMs, App Services, AKS pods) to authenticate to other Azure services without storing credentials.

| Type | Lifecycle | Use Case |
|---|---|---|
| System-assigned | Tied to the resource; deleted with resource | Single-resource identity |
| User-assigned | Independent lifecycle; assigned to multiple resources | Shared identity across resources |

```bash
# Enable system-assigned managed identity on a VM
az vm identity assign \
  --name <vm-name> \
  --resource-group <rg-name>

# Create a user-assigned managed identity
az identity create \
  --name <identity-name> \
  --resource-group <rg-name>

# Assign user-assigned identity to a VM
az vm identity assign \
  --name <vm-name> \
  --resource-group <rg-name> \
  --identities <identity-resource-id>

# Grant the managed identity access to a Key Vault
az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee <managed-identity-object-id> \
  --scope <key-vault-resource-id>
```

---

## Service Principals

Service principals are application identities for automation, CI/CD pipelines, and cross-service authentication.

```bash
# Create a service principal with Contributor access (returns client ID and secret)
az ad sp create-for-rbac \
  --name "sp-pipeline-prod" \
  --role "Contributor" \
  --scopes "/subscriptions/<sub-id>/resourceGroups/<rg-name>"

# List service principals
az ad sp list --display-name "sp-pipeline" --output table

# Reset credentials for a service principal
az ad sp credential reset --name <sp-app-id>

# Delete a service principal
az ad sp delete --id <sp-app-id>
```

Use certificate-based authentication for service principals in production — avoid client secrets where possible. Rotate secrets on a schedule (90 days maximum).

---

## Privileged Identity Management (PIM)

PIM provides just-in-time (JIT) activation of privileged roles. Instead of permanent Owner/Contributor assignments, users activate the role for a limited period (1–8 hours) with optional MFA and justification.

```bash
# List eligible assignments for current user
az rest \
  --method GET \
  --url "https://management.azure.com/subscriptions/<sub-id>/providers/Microsoft.Authorization/roleEligibilityScheduleInstances?api-version=2020-10-01"

# Activate a PIM role via Portal: Entra ID → PIM → Azure Resources → Eligible Assignments → Activate
```

**PIM governance rules:**
- Owner role: maximum 4-hour activation, require MFA + justification
- Contributor: maximum 8-hour activation, require justification
- All permanent Owner assignments must go through PIM — no standing Owner except break-glass accounts
- Break-glass accounts: two accounts, permanently assigned Global Administrator, not managed by PIM, monitored by alerts on sign-in

---

## Management Group RBAC

Roles assigned at a management group scope inherit to all subscriptions and resource groups within it.

```bash
# List management groups
az account management-group list --output table

# Assign Reader to an entire management group (e.g., for a security team)
az role assignment create \
  --role "Reader" \
  --assignee <group-object-id> \
  --scope "/providers/Microsoft.Management/managementGroups/<mg-name>"
```

Use management group scope for:
- Security team Reader access across all subscriptions
- Network Contributor for the network team across all network resource groups
- Cost Management Reader for FinOps visibility

---

## Access Review and Auditing

```bash
# Export all role assignments to CSV for review
az role assignment list --all --output json | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
print('Principal,Role,Scope,PrincipalType')
for a in data:
    print(f'{a[\"principalName\"]},{a[\"roleDefinitionName\"]},{a[\"scope\"]},{a[\"principalType\"]}')
"

# Find all Owner assignments (should be minimal)
az role assignment list --all \
  --query "[?roleDefinitionName=='Owner']" \
  --output table

# Check role assignment changes in Activity Log
az monitor activity-log list \
  --offset 30d \
  --query "[?operationName.value=='Microsoft.Authorization/roleAssignments/write']" \
  --output table
```

Conduct quarterly access reviews:
- Remove assignments for departed users
- Validate service principal secrets are rotated
- Confirm no standing Owner assignments outside break-glass accounts
- Validate PIM eligible assignments match current team membership
