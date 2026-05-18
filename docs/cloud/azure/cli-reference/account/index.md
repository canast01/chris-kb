# Account, Subscriptions & Resource Groups

> Part of the Azure CLI Reference.

```
┌──────────────────────────────────────────────────────────────┐
│                  Account CLI Flow                            │
│                                                              │
│  ┌────────────┐   az login    ┌────────────────────────────┐ │
│  │  User /    │──────────────►│  Entra ID Token            │ │
│  │  Service   │               │  (access + refresh)        │ │
│  │  Principal │               └──────────────┬─────────────┘ │
│  └────────────┘                              │               │
│                                              ▼               │
│                               ┌────────────────────────────┐ │
│  az account list              │  Subscription List         │ │
│  az account show  ◄──────────►│  (tenant scope)            │ │
│  az account set               └──────────────┬─────────────┘ │
│                                              │               │
│                                              ▼               │
│                               ┌────────────────────────────┐ │
│                               │  Active Subscription       │ │
│                               │  (all az commands target   │ │
│                               │   this subscription)       │ │
│                               └────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

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

```bash
az group list
az group list --output table
az group show --name <rg>
az group create --name <rg> --location eastus
az group delete --name <rg> --yes
az group list --query "[].{Name:name,Location:location,State:properties.provisioningState}" --output table
```
