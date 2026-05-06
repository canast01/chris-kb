# Azure CLI Reference

Commonly used Azure CLI (`az`) commands for managing compute, storage, networking, identity, and monitoring.

> Requires `az login` or service principal credentials. Use `az account set --subscription <id>` to target a specific subscription.

---

## Account & Subscription

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

---

## Resource Groups

```bash
az group list
az group list --output table
az group show --name <rg>
az group create --name <rg> --location eastus
az group delete --name <rg> --yes
az group list --query "[].{Name:name,Location:location,State:properties.provisioningState}" --output table
```

---

## Virtual Machines

```bash
# List
az vm list --output table
az vm list --resource-group <rg> --output table
az vm list --resource-group <rg> --show-details --output table

# Start / stop / restart
az vm start --resource-group <rg> --name <vm>
az vm stop --resource-group <rg> --name <vm>
az vm deallocate --resource-group <rg> --name <vm>
az vm restart --resource-group <rg> --name <vm>

# Details
az vm show --resource-group <rg> --name <vm>
az vm get-instance-view --resource-group <rg> --name <vm>

# Create
az vm create --resource-group <rg> --name <vm> --image Ubuntu2204 --size Standard_D2s_v3 \
  --admin-username azureuser --ssh-key-values ~/.ssh/id_rsa.pub

# Resize
az vm resize --resource-group <rg> --name <vm> --size Standard_D4s_v3

# Run command
az vm run-command invoke --resource-group <rg> --name <vm> --command-id RunShellScript \
  --scripts "uptime"

# Open port
az vm open-port --resource-group <rg> --name <vm> --port 22
```

---

## Disks & Snapshots

```bash
# Managed disks
az disk list --resource-group <rg> --output table
az disk show --resource-group <rg> --name <disk>
az disk create --resource-group <rg> --name <disk> --size-gb 128 --sku Premium_LRS
az disk delete --resource-group <rg> --name <disk> --yes

# Attach disk to VM
az vm disk attach --resource-group <rg> --vm-name <vm> --name <disk>
az vm disk detach --resource-group <rg> --vm-name <vm> --name <disk>

# Snapshots
az snapshot list --resource-group <rg> --output table
az snapshot create --resource-group <rg> --name <snap> --source <disk_id>
az snapshot delete --resource-group <rg> --name <snap>
```

---

## Storage Accounts & Blobs

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
az storage blob upload --account-name <account> --container-name <container> --file <local_file> --name <blob_name>
az storage blob download --account-name <account> --container-name <container> --name <blob_name> --file <local_file>
az storage blob delete --account-name <account> --container-name <container> --name <blob_name>

# SAS token
az storage container generate-sas --account-name <account> --name <container> \
  --permissions rwdl --expiry 2025-12-31
```

---

## Networking

```bash
# VNets
az network vnet list --output table
az network vnet show --resource-group <rg> --name <vnet>
az network vnet create --resource-group <rg> --name <vnet> --address-prefixes 10.0.0.0/16

# Subnets
az network vnet subnet list --resource-group <rg> --vnet-name <vnet> --output table
az network vnet subnet create --resource-group <rg> --vnet-name <vnet> --name <subnet> --address-prefixes 10.0.1.0/24

# NSGs
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

## Azure Active Directory (Entra ID)

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

---

## RBAC

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

---

## Monitor & Alerts

```bash
# Activity log
az monitor activity-log list --max-events 50
az monitor activity-log list --resource-group <rg> --offset 24h

# Metrics
az monitor metrics list --resource <resource_id> --metric "Percentage CPU"
az monitor metrics list-definitions --resource <resource_id>

# Alerts
az monitor alert list --resource-group <rg>
az monitor action-group list

# Diagnostic settings
az monitor diagnostic-settings list --resource <resource_id>
az monitor diagnostic-settings create --name <name> --resource <resource_id> \
  --workspace <workspace_id> --metrics '[{"category":"AllMetrics","enabled":true}]'
```

---

## Key Vault

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

```bash
# Clusters
az aks list --output table
az aks show --resource-group <rg> --name <cluster>

# Credentials
az aks get-credentials --resource-group <rg> --name <cluster>
az aks get-credentials --resource-group <rg> --name <cluster> --admin

# Scale
az aks scale --resource-group <rg> --name <cluster> --node-count 5

# Upgrade
az aks get-upgrades --resource-group <rg> --name <cluster>
az aks upgrade --resource-group <rg> --name <cluster> --kubernetes-version <version>

# Node pools
az aks nodepool list --resource-group <rg> --cluster-name <cluster>
```

---

## Backup & Recovery

```bash
# Recovery Services vaults
az backup vault list --output table
az backup vault show --resource-group <rg> --name <vault>

# Backup items
az backup item list --resource-group <rg> --vault-name <vault> --output table

# Jobs
az backup job list --resource-group <rg> --vault-name <vault> --output table
az backup job wait --resource-group <rg> --vault-name <vault> --name <job_id>

# On-demand backup
az backup protection backup-now --resource-group <rg> --vault-name <vault> \
  --container-name <container> --item-name <item> --retain-until <date>
```
