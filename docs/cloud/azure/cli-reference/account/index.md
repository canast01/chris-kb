---
tags:
  - azure
description: "Azure account CLI: az account set, az group create/list/delete, az subscription list, az policy assignment create, and resource lock management."
---
# Account, Subscriptions & Resource Groups

<div class="kb-summary">
Azure account CLI: `az account set`, `az group create/list/delete`, `az subscription list`, `az policy assignment create`, and resource lock management.

*Applies to: Azure*
</div>

> Part of the Azure CLI Reference.

---

```bash
# Login
az login
az login --service-principal -u <app_id> -p <password> --tenant <tenant>
az login --identity   # Managed identity

# Subscriptions
az account list --output table
az account show
az account set --subscription <id_or_name>

# Identity
az ad signed-in-user show
```


```text title="Expected output"
# az login
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code ABC123DEF to authenticate.

# az login --service-principal -u <app_id> -p <password> --tenant <tenant>
(no output — command completes silently)

# az login --identity
(no output — command completes silently)

# az account list --output table
Name                 CloudName    SubscriptionId                        TenantId                          State    IsDefault
-------------------  -----------  ------------------------------------  --------------------------------  -------  -----------
Production           AzureCloud   a1b2c3d4-e5f6-7890-abcd-ef1234567890  12345678-1234-1234-1234-123456789012  Enabled  True
Development          AzureCloud   f9e8d7c6-b5a4-3210-fedc-ba9876543210  12345678-1234-1234-1234-123456789012  Enabled  False
Staging              AzureCloud   5a6b7c8d-9e0f-1234-5678-9abcdef01234  12345678-1234-1234-1234-123456789012  Enabled  False

# az account show
{
  "environmentName": "AzureCloud",
  "homeTenantId": "12345678-1234-1234-1234-123456789012",
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "isDefault": true,
  "name": "Production",
  "state": "Enabled",
  "tenantId": "12345678-1234-1234-1234-123456789012",
  "user": {
    "name": "admin@company.com",
    "type": "user"
  }
}

# az account set --subscription <id_or_name>
(no output — command completes silently)

# az ad signed-in-user show
{
  "accountEnabled": true,
  "displayName": "Admin User",
  "givenName": "Admin",
  "id": "87654321-4321-4321-4321-210987654321",
  "mail": "admin@company.com",
  "surname": "User",
  "userPrincipalName": "admin@company.com"
}
```

!!! warning "Common errors"
    **`ERROR: Please run 'az login' to setup account.`** — Run `az login` to authenticate before executing other commands.
    **`ERROR: The subscription of '<subscription_id>' does not have a registered provider for namespace 'Microsoft.Compute'.`** — Register the required resource provider with `az provider register --namespace Microsoft.Compute`.
    **`ERROR: AADSTS700016: Application with identifier '<app_id>' was not found in the directory.`** — Verify the app ID, password, and tenant ID are correct and the service principal exists in the target tenant.
```bash
az group list
az group list --output table
az group show --name <rg>
az group create --name <rg> --location eastus
az group delete --name <rg> --yes
az group list --query "[].{Name:name,Location:location,State:properties.provisioningState}" --output table
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
- [Azure Identity](../../identity/index.md)
- [Azure Governance](../../governance/index.md)
