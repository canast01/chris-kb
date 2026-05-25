# Identity & RBAC

> Part of the Azure CLI Reference.

```text
┌──────────────────────────────────────────────────────────────┐
│                    Identity CLI Flow                         │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                   Entra ID                             │  │
│  │  az ad user list/create     az ad group list/create    │  │
│  │  az ad sp create-for-rbac   az ad app list             │  │
│  └───────────────────────┬────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                Role Assignment                         │  │
│  │  az role assignment create                             │  │
│  │      --assignee  <user / group / sp>                   │  │
│  │      --role      "Contributor" / custom                │  │
│  │      --scope     /subscriptions/<id>/...               │  │
│  └───────────────────────┬────────────────────────────────┘  │
│                          │ inherits down                     │
│          ┌───────────────┼──────────────────┐                │
│          ▼               ▼                  ▼                │
│   Mgmt Group     Subscription        Resource Group          │
└──────────────────────────────────────────────────────────────┘
```

---

```bash
# Users
az ad user list --output table
az ad user show --id <user_upn>
az ad user create --display-name "Name" --user-principal-name user@domain.com --password <pass>

# Groups
az ad group list --output table
az ad group show --group <group>
az ad group member list --group <group>

# Service principals
az ad sp list --output table
az ad sp show --id <app_id>
az ad sp create-for-rbac --name <name> --role Contributor --scopes /subscriptions/<sub_id>

# App registrations
az ad app list --output table
az ad app show --id <app_id>
```

```bash
# Role assignments
az role assignment list --assignee <user_or_sp>
az role assignment list --scope /subscriptions/<sub_id>/resourceGroups/<rg>
az role assignment create --assignee <user_or_sp> --role "Contributor" --scope <resource_id>
az role assignment delete --assignee <user_or_sp> --role "Contributor" --scope <resource_id>

# Role definitions
az role definition list --output table
az role definition show --name "Contributor"
```
