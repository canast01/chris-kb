# Azure Storage Private Endpoints

```
┌──────────────────────────────────────────────────────────────────┐
│               Storage Private Endpoint — Traffic Flow             │
└──────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────┐
  │                   VNet (prod)                    │
  │                                                  │
  │  ┌──────────┐   DNS: stprodblobs01               │
  │  │  App VM  │────────────────────┐               │
  │  └──────────┘                   ▼               │
  │                        ┌─────────────────────┐  │
  │                        │ Private DNS Zone     │  │
  │                        │ privatelink.blob.*  │  │
  │                        │ → 10.x.x.x          │  │
  │                        └──────────┬──────────┘  │
  │                                   │              │
  │                   ┌───────────────▼───────────┐  │
  │                   │  Private Endpoint NIC      │  │
  │                   │  10.x.x.x (private IP)     │  │
  │                   └───────────────┬────────────┘  │
  └───────────────────────────────────┼───────────────┘
                                      │ Azure backbone
                                      ▼
                         ┌────────────────────────┐
                         │  Storage Account        │
                         │  Public access: Disabled│
                         └────────────────────────┘
```

## Overview

Private endpoints assign a private IP address from your VNet to an Azure Storage service, routing all traffic over the Microsoft backbone rather than the public internet. This eliminates the need for public IP access and enables granular network isolation via NSGs and UDRs.

## Creating a Private Endpoint for Storage

```bash
RG="rg-storage-prod"
SA="stprodblobs01"
VNET="vnet-prod-eastus"
SUBNET="snet-private-endpoints"
PE_NAME="pe-stprodblobs01-blob"

# Disable public network access on the storage account first
az storage account update \
  --resource-group $RG \
  --name $SA \
  --public-network-access Disabled

# Get the storage account resource ID
SA_ID=$(az storage account show \
  --resource-group $RG \
  --name $SA \
  --query "id" -o tsv)

# Get the subnet resource ID
SUBNET_ID=$(az network vnet subnet show \
  --resource-group $RG \
  --vnet-name $VNET \
  --name $SUBNET \
  --query "id" -o tsv)

# Create the private endpoint
az network private-endpoint create \
  --resource-group $RG \
  --name $PE_NAME \
  --vnet-name $VNET \
  --subnet $SUBNET \
  --private-connection-resource-id $SA_ID \
  --group-ids blob \
  --connection-name "${PE_NAME}-conn" \
  --location eastus
```

Sub-resources (group IDs) per storage service:

| Storage Service | Group ID |
|---|---|
| Blob storage | `blob` |
| Azure Files (SMB) | `file` |
| Queue storage | `queue` |
| Table storage | `table` |
| Data Lake Gen2 | `dfs` |
| Static website | `web` |

## DNS Configuration

Private endpoints require DNS resolution to return the private IP, not the public IP.

```bash
# Create a Private DNS Zone for blob storage
az network private-dns zone create \
  --resource-group $RG \
  --name "privatelink.blob.core.windows.net"

# Link the Private DNS Zone to the VNet
az network private-dns link vnet create \
  --resource-group $RG \
  --zone-name "privatelink.blob.core.windows.net" \
  --name "dns-link-vnet-prod" \
  --virtual-network $VNET \
  --registration-enabled false

# Create DNS zone group (auto-registers private endpoint DNS records)
az network private-endpoint dns-zone-group create \
  --resource-group $RG \
  --endpoint-name $PE_NAME \
  --name "dzg-${PE_NAME}" \
  --private-dns-zone "privatelink.blob.core.windows.net" \
  --zone-name "blob"

# Verify DNS resolution returns private IP (run from within the VNet)
nslookup stprodblobs01.blob.core.windows.net
# Expected: returns 10.x.x.x (private IP), not 52.x.x.x (public IP)
```

## Verifying Connectivity

```bash
# Get the private endpoint NIC and its private IP
az network private-endpoint show \
  --resource-group $RG \
  --name $PE_NAME \
  --query "customDnsConfigs[].{fqdn:fqdn, ip:ipAddresses}" \
  --output json

# Test connectivity from a VM in the VNet
# SSH or bastion to a VM in the peered VNet, then:
curl -sk -I "https://stprodblobs01.blob.core.windows.net"
# Should succeed without CORS/firewall block

# List all private endpoints in the resource group
az network private-endpoint list \
  --resource-group $RG \
  --query "[].{name:name, state:provisioningState, subnet:subnet.id}" \
  --output table
```

## Network Isolation Configuration

```bash
# Allow access only from selected VNets (service endpoints as fallback)
az storage account network-rule add \
  --resource-group $RG \
  --account-name $SA \
  --vnet-name $VNET \
  --subnet $SUBNET

# Verify network rules
az storage account show \
  --resource-group $RG \
  --name $SA \
  --query "networkRuleSet" \
  --output json

# Allow access from a specific IP range (e.g., on-prem CIDR)
az storage account network-rule add \
  --resource-group $RG \
  --account-name $SA \
  --ip-address "10.0.0.0/24"

# Set default deny action (block all public traffic)
az storage account update \
  --resource-group $RG \
  --name $SA \
  --default-action Deny
```

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| DNS returns public IP from inside VNet | DNS zone not linked to VNet | Create/verify Private DNS Zone VNet link |
| `403 AuthorizationFailure` | Network rule blocking access | Add client IP or VNet to network rules |
| `Connection refused` on private IP | Private endpoint provisioning incomplete | Check endpoint state; allow 5 minutes |
| Works from VM but not from on-prem | DNS forwarding not configured | Configure on-prem DNS to forward `*.blob.core.windows.net` to Azure DNS |
