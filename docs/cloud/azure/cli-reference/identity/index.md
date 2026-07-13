---
tags:
  - azure
description: "Azure identity CLI: az ad user/group/sp, az role assignment create, az policy definition create, az keyvault set-policy, and managed identity assignment."
---
# Identity & RBAC

<div class="kb-summary">
Azure identity CLI: `az ad user/group/sp`, `az role assignment create`, `az policy definition create`, `az keyvault set-policy`, and managed identity assignment.

*Applies to: Azure*
</div>

> Part of the Azure CLI Reference.

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


```text title="Expected output"
DisplayName                          UserPrincipalName                    ObjectId
-----------------------------------  ------------------------------------  ------------------------------------
Alice Johnson                        alice.johnson@contoso.com            a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d
Bob Smith                            bob.smith@contoso.com               b2c3d4e5-f6a7-4b5c-8d9e-1f2a3b4c5d6e
Carol White                          carol.white@contoso.com             c3d4e5f6-a7b8-4c5d-8e9f-2a3b4c5d6e7f

GroupId                              DisplayName
-----------------------------------  ------------------------------------
d4e5f6a7-b8c9-4d5e-8f9a-3b4c5d6e7f8a  Engineering
e5f6a7b8-c9d0-4e5f-8f9a-4c5d6e7f8a9b  Finance
f6a7b8c9-d0e1-4f5g-8g9a-5d6e7f8a9b0c  Marketing

ObjectId                              DisplayName                          AppId
-----------------------------------  ------------------------------------  ------------------------------------
g7b8c9d0-e1f2-4g5h-8h9b-6e7f8a9b0c1d  my-app-service-principal            a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c
h8c9d0e1-f2g3-4h5i-8i9c-7f8a9b0c1d2e  monitoring-sp                       b2c3d4e5-f6a7-47b9-9c0d-2e3f4a5b6c7d

AppId                                DisplayName
-----------------------------------  ------------------------------------
i9d0e1f2-g3h4-4i5j-8j9d-8a9b0c1d2e3f  web-api-app
j0e1f2g3-h4i5-4j5k-8k9e-9b0c1d2e3f4a  desktop-client-app
```

!!! warning "Common errors"
    **`The following arguments are required: --id`** — Provide the user's UPN or object ID with the `--id` parameter (e.g., `az ad user show --id alice.johnson@contoso.com`).
    **`Invalid password. Passwords must be at least 8 characters and contain uppercase, lowercase, numbers and special characters.`** — Use a strong password meeting complexity requirements or omit `--password` to have Azure generate one.
    **`No subscriptions found in the current account.`** — Run `az account set --subscription <subscription_id>` to set the active subscription before creating service principals.
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

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```

## See also

- [Azure CLI Reference](../index.md)
- [Azure Security](../../security/index.md)
- [Azure Identity](../../identity/index.md)
