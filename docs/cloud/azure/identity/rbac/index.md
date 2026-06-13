---
title: RBAC
tags:
  - azure
---

# Azure — RBAC


<div class="kb-summary">
Azure Role-Based Access Control (RBAC) is the authorisation system for Azure resources. Every access decision evaluates: **who** (principal) has **what** (role) on **which** (scope).
</div>
```text
┌──────────────────────────────────────── Cloud Azure Identity ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Azure: Cloud Azure Identity platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                      Management: Cloud Azure Identity management console                      │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
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
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Identity infrastructure · management network · monitoring                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Identity platform overview and core concepts                      │
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


## RBAC Model

```text
Scope hierarchy (broader → narrower):
  Management Group
    └── Subscription
          └── Resource Group
                └── Resource
```

A role assignment at a broader scope is inherited by all narrower scopes beneath it.

## Key Concepts

| Term | Definition |
|---|---|
| **Security principal** | User, group, service principal, or managed identity receiving access |
| **Role definition** | Named collection of permissions (actions, dataActions, notActions) |
| **Scope** | The boundary at which the role applies |
| **Role assignment** | The binding of principal + role + scope |

## Built-in Roles — Common Ones

| Role | What it grants |
|---|---|
| **Owner** | Full control including the ability to delegate access |
| **Contributor** | Create/modify resources; cannot manage access |
| **Reader** | Read-only across all resource types |
| **User Access Administrator** | Can manage role assignments; cannot modify resources |
| **Storage Blob Data Contributor** | Read/write/delete blob containers and data |
| **Key Vault Secrets User** | Read secrets from Key Vault (data plane) |
| **Virtual Machine Contributor** | Manage VMs; no network or storage access |
| **Network Contributor** | Manage networking; no resource access |
| **Monitoring Reader** | Read monitoring data, metrics, logs |

## Managing Role Assignments

### Azure CLI

```bash
# List all assignments in a subscription
az role assignment list --all --output table

# List assignments for a specific principal
az role assignment list --assignee <object-id-or-upn> --all

# Assign a built-in role at resource group scope
az role assignment create \
  --assignee <user-upn-or-object-id> \
  --role "Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg-name>

# Assign to a managed identity at resource scope
az role assignment create \
  --assignee <managed-identity-object-id> \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account>

# Remove a role assignment
az role assignment delete \
  --assignee <object-id> \
  --role "Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg-name>

# List all built-in role definitions
az role definition list --custom-role-only false --output table
```

### PowerShell

```powershell
# List assignments for a user
Get-AzRoleAssignment -SignInName user@domain.com

# Assign role at resource group scope
New-AzRoleAssignment `
  -ObjectId <object-id> `
  -RoleDefinitionName "Contributor" `
  -ResourceGroupName <rg-name>

# Remove assignment
Remove-AzRoleAssignment `
  -ObjectId <object-id> `
  -RoleDefinitionName "Contributor" `
  -ResourceGroupName <rg-name>
```

## Custom Role Definitions

```json
{
  "Name": "VM Operator (Read + Start/Stop)",
  "Description": "Can read VMs and start or stop them",
  "Actions": [
    "Microsoft.Compute/virtualMachines/read",
    "Microsoft.Compute/virtualMachines/start/action",
    "Microsoft.Compute/virtualMachines/deallocate/action",
    "Microsoft.Compute/virtualMachines/restart/action",
    "Microsoft.Resources/subscriptions/resourceGroups/read"
  ],
  "NotActions": [],
  "DataActions": [],
  "NotDataActions": [],
  "AssignableScopes": ["/subscriptions/<sub-id>"]
}
```

```bash
# Create, update, delete custom role
az role definition create --role-definition @custom-role.json
az role definition update --role-definition @custom-role.json
az role definition delete --name "VM Operator (Read + Start/Stop)"
```

## Data Plane vs Control Plane

Control plane (management) and data plane (data) are separate in Azure RBAC.

| Action type | Example | Role needed |
|---|---|---|
| Control plane | Create/delete storage account | Storage Account Contributor |
| Data plane | Read blob data | Storage Blob Data Reader |

A user with Storage Account Contributor cannot read blob data without an explicit data-plane role assignment.

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| `AuthorizationFailed` despite role assignment | Assignment propagation delay (up to 10 min) | Wait; verify with `az role assignment list --assignee` |
| Resource inaccessible despite subscription-level role | Resource has deny assignment from Blueprint or policy | Check: `az role assignment list --include-deny-assignments --all` |
| Data access denied despite control-plane role | Control and data planes are separate | Assign the matching data-plane role |
| Custom role not visible in portal | Assignable scopes doesn't include target subscription | Update `AssignableScopes` in the role definition |
| Service principal lacks access after role assignment | Assignment targets wrong object ID (use SP object ID, not app ID) | Verify: `az ad sp show --id <app-id> --query id` |
