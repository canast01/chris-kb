---
tags:
  - azure
  - security
description: "Azure access control is built on Azure Role-Based Access Control (RBAC)."
---
# Azure — Access Control

<div class="kb-summary">
Azure access control is built on Azure Role-Based Access Control (RBAC).

*Applies to: Azure*
</div>

 Permissions are assigned by attaching role definitions to security principals (users, groups, service principals, managed identities) at a specific scope (management group, subscription, resource group, or resource).

---

```d2
direction: down

auth: "Azure\nAuthentication" {shape: rectangle}
rbac_fundamentals: "RBAC Fundamentals" {shape: rectangle}
role_assignments: "Role Assignments" {shape: rectangle}
custom_roles: "Custom Roles" {shape: rectangle}
managed_identities: "Managed Identities" {shape: rectangle}
service_principals: "Service Principals" {shape: rectangle}
privileged_identity_management_pim: "Privileged Identity Management (PIM)" {shape: rectangle}
resources: Protected Resources {shape: cylinder}

auth -> rbac_fundamentals: grants
rbac_fundamentals -> resources: access
auth -> role_assignments: grants
role_assignments -> resources: access
auth -> custom_roles: grants
custom_roles -> resources: access
auth -> managed_identities: grants
managed_identities -> resources: access
auth -> service_principals: grants
service_principals -> resources: access
auth -> privileged_identity_management_pim: grants
privileged_identity_management_pim -> resources: access
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

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


```text title="Expected output"
RoleDefinitionName             Scope
---------------------------    -----------------------------------------------
Owner                          /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
Contributor                    /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
Reader                         /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
Storage Blob Data Contributor  /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg
Virtual Machine Contributor    /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/dev-rg
...

RoleDefinitionName    Scope
------------------    -----------------------------------------------
Contributor           /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
Reader                /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg

RoleDefinitionName             Scope
---------------------------    -----------------------------------------------
Owner                          /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg
Contributor                    /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg
Storage Blob Data Reader       /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg

RoleDefinitionName             Scope
---------------------------    -----------------------------------------------
Owner                          /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg
Contributor                    /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
Reader                         /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
Storage Blob Data Reader       /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg
```

!!! warning "Common errors"
    **`ERROR: The subscription '<sub-id>' could not be found.`** — Verify the subscription
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


```text title="Expected output"
{
  "canDelegate": false,
  "id": "/subscriptions/12a4b5c6-d7e8-4f9a-b0c1-2d3e4f5a6b7c/resourceGroups/prod-rg/providers/Microsoft.Authorization/roleAssignments/8f9a0b1c-2d3e-4f5a-6b7c-8d9e0f1a2b3c",
  "name": "8f9a0b1c-2d3e-4f5a-6b7c-8d9e0f1a2b3c",
  "principalId": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "principalType": "User",
  "roleDefinitionId": "/subscriptions/12a4b5c6-d7e8-4f9a-b0c1-2d3e4f5a6b7c/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c",
  "scope": "/subscriptions/12a4b5c6-d7e8-4f9a-b0c1-2d3e4f5a6b7c/resourceGroups/prod-rg",
  "type": "Microsoft.Authorization/roleAssignments"
}
{
  "canDelegate": false,
  "id": "/subscriptions/12a4b5c6-d7e8-4f9a-b0c1-2d3e4f5a6b7c/providers/Microsoft.Authorization/roleAssignments/c5d6e7f8-9a0b-1c2d-3e4f-5a6b7c8d9e0f",
  "name": "c5d6e7f8-9a0b-1c2d-3e4f-5a6b7c8d9e0f",
  "principalId": "f1e2d3c4-b5a6-4978-8c7d-6e5f4a3b2c1d",
  "principalType": "Group",
  "roleDefinitionId": "/subscriptions/12a4b5c6-d7e8-4f9a-b0c1-2d3e4f5a6b7c/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7",
  "scope": "/subscriptions/12a4b5c6-d7e8-4f9a-b0c1-2d3e4f5a6b7c",
  "type": "Microsoft.Authorization/roleAssignments"
}
{
  "canDelegate": false,
  "id": "/subscriptions/12a4b5c6-d7e8-4f9a-b0c1-2d3e4f5a6b7c/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/prodstg001/providers/Microsoft.Authorization/roleAssignments/1a
```
### Remove a Role Assignment

```bash
az role assignment delete \
  --role "Contributor" \
  --assignee <user-upn-or-object-id> \
  --resource-group <rg-name>
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`The provided information does not match any role assignments.`** — Verify the exact role name with `az role definition list --query "[].name"`, assignee identity with `az ad user show --id <upn>`, and resource group name with `az group list`.
    **`The user does not have permission to perform action 'Microsoft.Authorization/roleAssignments/delete' over scope '/subscriptions/<sub-id>/resourceGroups/<rg-name>'.`** — Ensure your account has Owner or User Access Administrator role on the resource group or subscription.
---

## Custom Roles

Use custom roles when built-in roles are too broad. Custom roles can restrict actions to specific resource providers and operations.

```bash
# List all custom roles in the tenant
az role definition list --custom-role-only true --output table

# Create a custom role from a JSON definition
az role definition create --role-definition @custom-role.json
```


```text title="Expected output"
Name                                    Type       Description
──────────────────────────────────────  ─────────  ──────────────────────────────────────
Virtual Machine Operator                CustomRole Manage virtual machines and snapshots
Network Security Manager                CustomRole Manage NSGs and firewall rules
Database Administrator Custom           CustomRole Administer SQL databases
Storage Blob Reader Extended            CustomRole Read and list storage blobs
Kubernetes Cluster Auditor               CustomRole Audit AKS cluster operations

{
  "name": "Virtual Machine Operator",
  "id": "a1b2c3d4-e5f6-47a8-9b1c-2d3e4f5a6b7c",
  "type": "CustomRole",
  "permissions": [
    {
      "actions": [
        "Microsoft.Compute/virtualMachines/read",
        "Microsoft.Compute/virtualMachines/start/action"
      ],
      "notActions": []
    }
  ],
  "assignableScopes": [
    "/subscriptions/12345678-1234-1234-1234-123456789012"
  ]
}
```

!!! warning "Common errors"
    **`ERROR: (InvalidInput) The role definition file '@custom-role.json' does not exist.`** — Verify the JSON file path is correct and exists in the current working directory using `ls -la custom-role.json`.
    **`ERROR: (Forbidden) The user does not have permission to create role definitions at scope '/subscriptions/...'.`** — Ensure your account has Owner or User Access Administrator role on the subscription using `az role assignment list --assignee <your-email>`.
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


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`The role definition file '@custom-role-updated.json' does not exist.`** — Verify the JSON file path is correct and exists in the current working directory with `ls -la custom-role-updated.json`.
    **`Cannot delete role definition 'VM Start Stop Only'. There are still 3 role assignments using this role.`** — Remove all role assignments for this custom role using `az role assignment delete --role "VM Start Stop Only"` before attempting deletion.
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


```text title="Expected output"
{
  "identity": {
    "principalId": "a7b2c9d4-e1f6-4a8b-9c3d-2e5f7a1b4c6d",
    "tenantId": "72f988bf-86f1-41af-91ab-2d7cd011db47",
    "type": "SystemAssigned"
  },
  "name": "myvm",
  "resourceGroup": "myresourcegroup"
}
{
  "clientId": "f8e3d2c1-9a7b-4e6f-8c2d-1a5b9e3f7c4d",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourcegroups/myresourcegroup/providers/microsoft.managedidentity/userassignedidentities/myidentity",
  "location": "eastus",
  "name": "myidentity",
  "principalId": "b9c3d4e5-f1a2-4b6c-8d9e-0f2a3b4c5d6e",
  "resourceGroup": "myresourcegroup"
}
{
  "identity": {
    "principalId": "a7b2c9d4-e1f6-4a8b-9c3d-2e5f7a1b4c6d",
    "tenantId": "72f988bf-86f1-41af-91ab-2d7cd011db47",
    "type": "UserAssigned, SystemAssigned",
    "userAssignedIdentities": {
      "/subscriptions/12345678-1234-1234-1234-123456789012/resourcegroups/myresourcegroup/providers/microsoft.managedidentity/userassignedidentities/myidentity": {
        "clientId": "f8e3d2c1-9a7b-4e6f-8c2d-1a5b9e3f7c4d",
        "principalId": "b9c3d4e5-f1a2-4b6c-8d9e-0f2a3b4c5d6e"
      }
    }
  },
  "name": "myvm"
}
{
  "canDelegate": false,
  "condition": null,
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/roleAssignments/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "principalId": "b9c3d4e5-f1a2-4b6c-8d9e-0f2a3b4c5d6e",
  "principalType": "ServicePrincipal",
  "roleDefinitionId": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/roleDefinitions/4633458b-17de-408a-b874-0445c86300d1",
  "scope": "/subscriptions/12345678
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


```text title="Expected output"
{
  "appId": "a7f3c2e1-9b4d-4e8f-b2c6-1d5a9e3f7c2b",
  "displayName": "sp-pipeline-prod",
  "password": "Ew8Q~7mK9nL2pQ5rS8tU1vW4xY6zA3bC5dE7fG9h",
  "tenant": "72f988bf-86f1-41af-91ab-2d7cd011db47"
}

DisplayName                 AppId                                 CreatedDateTime
--------------------------- ------------------------------------- -----------------------
sp-pipeline-prod            a7f3c2e1-9b4d-4e8f-b2c6-1d5a9e3f7c2b 2024-01-15T10:32:44Z
sp-pipeline-staging         b8e4d3f2-0c5e-5f9g-c3d7-2e6b0f4g8d3c 2024-01-10T14:18:22Z

{
  "appId": "a7f3c2e1-9b4d-4e8f-b2c6-1d5a9e3f7c2b",
  "password": "Kx9P~2mN8qL5sT1uV4wX7yZ0aB3cD6eF8gH1jK4l",
  "tenant": "72f988bf-86f1-41af-91ab-2d7cd011db47"
}
```

!!! warning "Common errors"
    **`No subscriptions found. Please run 'az login' to set up account.`** — Run `az login` and ensure you have access to the target subscription before creating the service principal.
    **`The service principal with object id '<id>' does not have authorization to perform action 'Microsoft.Authorization/roleAssignments/write'.`** — Ensure your user account has Owner or User Access Administrator role on the subscription or resource group before assigning roles to the service principal.
    **`Service principal '<sp-app-id>' not found.`** — Verify the service principal exists by running `az ad sp list --display-name "<name>"` and use the correct appId from the output.
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


```text title="Expected output"
{
  "value": [
    {
      "id": "/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8/providers/Microsoft.Authorization/roleEligibilityScheduleInstances/550e8400-e29b-41d4-a716-446655440000",
      "name": "550e8400-e29b-41d4-a716-446655440000",
      "type": "Microsoft.Authorization/roleEligibilityScheduleInstances",
      "properties": {
        "scope": "/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8",
        "roleDefinitionId": "/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8/providers/Microsoft.Authorization/roleDefinitions/8e3af657-a8ff-443c-a75c-2fe8c4bcb635",
        "principalId": "a1b2c3d4-e5f6-4a5b-9c8d-7e6f5a4b3c2d",
        "principalType": "User",
        "roleEligibilityScheduleId": "660f9511-f40c-52e5-b827-557766551111",
        "memberType": "Inherited",
        "status": "Provisioned"
      }
    },
    {
      "id": "/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8/providers/Microsoft.Authorization/roleEligibilityScheduleInstances/661f9512-f41c-53e6-c938-668877662222",
      "name": "661f9512-f41c-53e6-c938-668877662222",
      "type": "Microsoft.Authorization/roleEligibilityScheduleInstances",
      "properties": {
        "scope": "/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8",
        "roleDefinitionId": "/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c",
        "principalId": "a1b2c3d4-e5f6-4a5b-9c8d-7e6f5a4b3c2d",
        "principalType": "User",
        "roleEligibilityScheduleId": "772g0623-g52d-64f7-d049-779988773333",
        "memberType": "Direct",
        "status": "Provisioned"
      }
    }
  ]
}
```

!!! warning "Common errors"
    **`ERROR: The subscription '<sub-id>' could not be found.`**
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


```text title="Expected output"
Id                                   DisplayName                Type
------------------------------------  -----------------------  ------
/providers/Microsoft.Management/managementGroups/mg-prod
mg-prod                              Microsoft.Management/managementGroups
/providers/Microsoft.Management/managementGroups/mg-dev
mg-dev                               Microsoft.Management/managementGroups
/providers/Microsoft.Management/managementGroups/mg-staging
mg-staging                           Microsoft.Management/managementGroups

{
  "canDelegate": false,
  "id": "/providers/Microsoft.Management/managementGroups/mg-prod/providers/Microsoft.Authorization/roleAssignments/a7f3c2e1-9b4d-4f8a-b2c5-d1e6f7a8b9c0",
  "name": "a7f3c2e1-9b4d-4f8a-b2c5-d1e6f7a8b9c0",
  "principalId": "f2e8c1a9-7d4b-4e6f-9a2c-3b5d8e1f7a4c",
  "principalType": "Group",
  "roleDefinitionId": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7",
  "scope": "/providers/Microsoft.Management/managementGroups/mg-prod",
  "type": "Microsoft.Authorization/roleAssignments"
}
```

!!! warning "Common errors"
    **`The provided information does not map to a management group.`** — Verify the management group name exists by running `az account management-group list` and use the exact DisplayName value.
    **`Principal with object id <group-object-id> does not exist in the directory.`** — Confirm the group object ID is correct by running `az ad group show --group <group-name> --query objectId` in the target Azure AD tenant.
    **`Authorization failed for template deployment.`** — Ensure your user account has Owner or User Access Administrator role on the management group scope before assigning roles to others.
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


```text title="Expected output"
Principal,Role,Scope,PrincipalType
alice@contoso.com,Contributor,/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8,User
svc-automation@contoso.com,Owner,/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8,ServicePrincipal
bob@contoso.com,Reader,/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8/resourceGroups/prod-rg,User
devops-team@contoso.com,Contributor,/subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8/resourceGroups/dev-rg,Group

PrincipalName                    RoleDefinitionName    Scope
svc-automation@contoso.com       Owner                 /subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8
admin@contoso.com                Owner                 /subscriptions/12a4b5c6-d7e8-4f9a-b1c2-d3e4f5a6b7c8

Time                 OperationName                                      Status    ResourceGroup
2024-01-15T14:32:18  Microsoft.Authorization/roleAssignments/write      Succeeded prod-rg
2024-01-14T09:47:52  Microsoft.Authorization/roleAssignments/write      Succeeded dev-rg
2024-01-12T16:21:09  Microsoft.Authorization/roleAssignments/write      Succeeded prod-rg
```

!!! warning "Common errors"
    **`ERROR: The following arguments are required: --resource-group/-g`** — Add `--resource-group <name>` or use `--all` flag to query across all subscriptions.
    **`KeyError: 'principalName'`** — Some role assignments may lack a principalName field; add error handling with `a.get("principalName", "N/A")` in the Python script.
Conduct quarterly access reviews:
- Remove assignments for departed users
- Validate service principal secrets are rotated
- Confirm no standing Owner assignments outside break-glass accounts
- Validate PIM eligible assignments match current team membership

---

## See also

- [Azure — Authentication](../authentication/)
- [Azure — Hardening](../hardening/)
- [Azure — Encryption](../encryption/)
