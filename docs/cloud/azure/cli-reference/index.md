---
tags:
  - azure
---
# Azure CLI Reference


<div class="kb-summary">
Commonly used Azure CLI (`az`) commands for managing compute, storage, networking, identity, and monitoring. The Azure CLI is a cross-platform tool that talks directly to Azure APIs — everything you can do in the portal, you can automate with `az`.

*Applies to: Azure*
</div>
![Azure CLI Reference](../../../assets/cloud-azure-cli-reference-index.svg)


> Requires `az login` or service principal credentials. Use `az account set --subscription <id>` to target a specific subscription.

```text
┌───────────────────────────────────────── Azure CLI Reference ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                 Azure CLI — az command-line tool for managing Azure resources                 │   │
│   │    Structured as: az <group> <command> [--options] — e.g. az vm list --resource-group myRG    │   │
│   │  Auth: az login (browser) · az login --service-principal · az account set --subscription <id> │   │
│   │              Output formats: --output json (default) | table | tsv | yaml | none              │   │
│   │      Query: --query uses JMESPath; e.g. --query "[?powerState==`VM running`].name" -o tsv     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    az CLI organises by resource type — vm, network, storage, account, backup, monitor, identity, aks  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Compute (VM/AKS)      │  │       Storage / Disks       │  │      Identity / Network     │   │
│   │    az vm list/show/start    │  │    az storage account ls    │  │    az ad user/group list    │   │
│   │    az vm stop/deallocate    │  │     az disk list/create     │  │   az role assignment list   │   │
│   │     az vm resize/create     │  │      az snapshot create     │  │     az network vnet list    │   │
│   │    az aks get-credentials   │  │   az storage blob up/down   │  │   az network nsg rule list  │   │
│   │      az vm run-command      │  │    az keyvault secret get   │  │    az monitor alert list    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Compute CLI manages VMs/AKS · Storage CLI handles blobs and disks                                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Account      │ Virtual Machines │      Storage      │    Networking    │   Backup / KV    │   │
│   │     az login     │   vm list --rg   │    blob upload    │    vnet list     │  backup item ls  │   │
│   │   account set    │  vm start/stop   │   blob download   │   nsg rule add   │  kv secret get   │   │
│   │   account list   │    vm resize     │    disk create    │     lb list      │  backup protect  │   │
│   │    sp create     │    vm run-cmd    │    snapshot cp    │   vnet peering   │   kv key list    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure Resource Manager API · Azure AD token endpoint · Azure CloudShell or local workstation         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Azure CLI v2     = Current az CLI; install via Homebrew/apt/pip; az --version to verify              │
│  az login         = Browser-based interactive login; stores token in ~/.azure/; expires after 1 hour  │
│  Service principal= Non-human identity; use az login --service-principal for automation               │
│  az account set   = Switch active subscription; use with --subscription <name or id>                  │
│  --resource-group = Required for most resource commands; shorthand --g; targets RG scope              │
│  --query          = JMESPath filter on JSON output; e.g. [].name for list of resource names           │
│  --output table   = Renders JSON as a formatted table; useful for terminal readability                │
│  az vm run-command= Execute a script inside a VM via VM agent; works without SSH or port access       │
│  az configure     = Set default resource group, output format, and location for the CLI session       │
│  CloudShell       = Browser-based shell in Azure portal; pre-authenticated; az available by default   │
│  --no-wait        = Submits a long-running operation without blocking the terminal; async execution   │
│  az find          = AI-powered CLI helper; suggests relevant commands for a given scenario            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="account/">
  <strong>Account</strong>
  <span>Login, subscription management, and service principal commands.</span>
</a>

<a class="kb-card" href="virtual-machines/">
  <strong>Virtual Machines</strong>
  <span>VM lifecycle, resize, run-command, and AKS credentials.</span>
</a>

<a class="kb-card" href="storage/">
  <strong>Storage</strong>
  <span>Storage accounts, containers, and blob upload/download.</span>
</a>

<a class="kb-card" href="disks/">
  <strong>Disks</strong>
  <span>Managed disk and snapshot management commands.</span>
</a>

<a class="kb-card" href="networking/">
  <strong>Networking</strong>
  <span>VNet, subnets, NSGs, public IPs, and load balancers.</span>
</a>

<a class="kb-card" href="identity/">
  <strong>Identity & RBAC</strong>
  <span>Users, groups, service principals, and role assignments.</span>
</a>

<a class="kb-card" href="monitor/">
  <strong>Monitor & Alerts</strong>
  <span>Activity log, metrics, alerts, and diagnostic settings.</span>
</a>

<a class="kb-card" href="key-vault/">
  <strong>Key Vault</strong>
  <span>Secrets, keys, and certificate management commands.</span>
</a>

<a class="kb-card" href="aks/">
  <strong>AKS</strong>
  <span>Cluster management, node pools, and upgrade commands.</span>
</a>

<a class="kb-card" href="backup/">
  <strong>Backup & Recovery</strong>
  <span>Recovery Services vault, backup items, and job commands.</span>
</a>

</div>

---

## Storage Accounts & Blobs

Azure Blob Storage stores unstructured data (files, backups, images) in containers within a storage account. SAS tokens grant time-limited access without sharing account keys.

```bash
# Storage accounts
az storage account list --output table
az storage account show --resource-group <rg> --name <account>
az storage account create --resource-group <rg> --name <account> --sku Standard_LRS --kind StorageV2
az storage account delete --resource-group <rg> --name <account> --yes

# Containers
az storage container list --account-name <account>
az storage container create --account-name <account> --name <container>

# Blobs
az storage blob list --account-name <account> --container-name <container>
az storage blob upload --account-name <account> --container-name <container> \
  --file <local_file> --name <blob_name>
az storage blob download --account-name <account> --container-name <container> \
  --name <blob_name> --file <local_file>
az storage blob delete --account-name <account> --container-name <container> --name <blob_name>

# SAS token (time-limited access URL)
az storage container generate-sas --account-name <account> --name <container> \
  --permissions rwdl --expiry 2025-12-31
```

---

## Networking

Manage virtual networks, subnets, network security groups (NSGs), public IPs, and load balancers. VNets are the private network space in Azure — subnets segment them further.

```bash
# VNets
az network vnet list --output table
az network vnet show --resource-group <rg> --name <vnet>
az network vnet create --resource-group <rg> --name <vnet> --address-prefixes 10.0.0.0/16

# Subnets
az network vnet subnet list --resource-group <rg> --vnet-name <vnet> --output table
az network vnet subnet create --resource-group <rg> --vnet-name <vnet> \
  --name <subnet> --address-prefixes 10.0.1.0/24

# Network Security Groups (NSGs — virtual firewalls)
az network nsg list --resource-group <rg> --output table
az network nsg create --resource-group <rg> --name <nsg>
az network nsg rule create --resource-group <rg> --nsg-name <nsg> --name Allow-SSH \
  --priority 100 --protocol Tcp --destination-port-range 22 --access Allow

# Public IPs
az network public-ip list --output table
az network public-ip create --resource-group <rg> --name <pip> --allocation-method Static

# Load balancer
az network lb list --output table
```

---

## Identity & RBAC

Manage Azure Active Directory users, groups, service principals, and role-based access control. Service principals are non-human identities used by apps and automation.

```bash
# Users
az ad user list --output table
az ad user show --id <user_upn>
az ad user create --display-name "Name" --user-principal-name user@domain.com --password <pass>

# Groups
az ad group list --output table
az ad group show --group <group>
az ad group member list --group <group>

# Service principals (automation identities)
az ad sp list --output table
az ad sp show --id <app_id>
az ad sp create-for-rbac --name <name> --role Contributor --scopes /subscriptions/<sub_id>

# App registrations
az ad app list --output table
az ad app show --id <app_id>

# Role assignments (RBAC — who can do what on which resource)
az role assignment list --assignee <user_or_sp>
az role assignment list --scope /subscriptions/<sub_id>/resourceGroups/<rg>
az role assignment create --assignee <user_or_sp> --role "Contributor" --scope <resource_id>
az role assignment delete --assignee <user_or_sp> --role "Contributor" --scope <resource_id>

# Role definitions
az role definition list --output table
az role definition show --name "Contributor"
```

---

## Monitor & Alerts

Query the activity log (who did what), pull resource metrics (CPU, network), and manage alerts and diagnostic settings.

```bash
# Activity log (audit trail of all operations)
az monitor activity-log list --max-events 50
az monitor activity-log list --resource-group <rg> --offset 24h

# Metrics (CPU, network, disk IOPS, etc.)
az monitor metrics list --resource <resource_id> --metric "Percentage CPU"
az monitor metrics list-definitions --resource <resource_id>

# Alerts
az monitor alert list --resource-group <rg>
az monitor action-group list

# Diagnostic settings (route logs and metrics to Log Analytics, storage, or Event Hub)
az monitor diagnostic-settings list --resource <resource_id>
az monitor diagnostic-settings create --name <name> --resource <resource_id> \
  --workspace <workspace_id> --metrics '[{"category":"AllMetrics","enabled":true}]'
```

---

## Key Vault

Azure Key Vault stores secrets (passwords, connection strings), cryptographic keys, and certificates centrally — applications retrieve them at runtime instead of embedding them in code.

```bash
# Vaults
az keyvault list --output table
az keyvault show --name <vault>

# Secrets
az keyvault secret list --vault-name <vault>
az keyvault secret show --vault-name <vault> --name <secret>
az keyvault secret set --vault-name <vault> --name <secret> --value <value>
az keyvault secret delete --vault-name <vault> --name <secret>

# Keys
az keyvault key list --vault-name <vault>
az keyvault key show --vault-name <vault> --name <key>

# Certificates
az keyvault certificate list --vault-name <vault>
az keyvault certificate show --vault-name <vault> --name <cert>
```

---

## AKS

Azure Kubernetes Service (AKS) is Azure's managed Kubernetes offering. It manages the control plane — you manage workloads with `kubectl` after fetching credentials with `az aks get-credentials`.

```bash
# Clusters
az aks list --output table
az aks show --resource-group <rg> --name <cluster>

# Credentials (configures kubectl to point to this cluster)
az aks get-credentials --resource-group <rg> --name <cluster>
az aks get-credentials --resource-group <rg> --name <cluster> --admin

# Scale node pool
az aks scale --resource-group <rg> --name <cluster> --node-count 5

# Upgrade
az aks get-upgrades --resource-group <rg> --name <cluster>
az aks upgrade --resource-group <rg> --name <cluster> --kubernetes-version <version>

# Node pools
az aks nodepool list --resource-group <rg> --cluster-name <cluster>
```

---

## Backup & Recovery

Azure Backup stores recovery points in Recovery Services vaults. Use these commands to check backup status, review jobs, and trigger on-demand backups.

```bash
# Recovery Services vaults
az backup vault list --output table
az backup vault show --resource-group <rg> --name <vault>

# Backup items (protected resources)
az backup item list --resource-group <rg> --vault-name <vault> --output table

# Jobs
az backup job list --resource-group <rg> --vault-name <vault> --output table
az backup job wait --resource-group <rg> --vault-name <vault> --name <job_id>

# On-demand backup
az backup protection backup-now --resource-group <rg> --vault-name <vault> \
  --container-name <container> --item-name <item> --retain-until <date>
```
