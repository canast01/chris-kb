---
tags:
  - azure
---
# Azure Storage Private Endpoints

<div class="kb-summary">
Azure Storage Private Endpoints reference covering Overview, Creating a Private Endpoint for Storage, DNS Configuration, Verifying Connectivity, Network Isolation Configuration and 1 more sections.

*Applies to: Azure*
</div>

```d2
direction: down

creating_a_private_endpoint_for_stor: "Creating a Private Endpoint for Storage" {shape: rectangle}
dns_configuration: "DNS Configuration" {shape: rectangle}
verifying_connectivity: "Verifying Connectivity" {shape: rectangle}
network_isolation_configuration: "Network Isolation Configuration" {shape: rectangle}
troubleshooting: "Troubleshooting" {shape: rectangle}

creating_a_private_endpoint_for_stor -> dns_configuration: uses
dns_configuration -> verifying_connectivity: uses
verifying_connectivity -> network_isolation_configuration: uses
network_isolation_configuration -> troubleshooting: uses
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


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01",
  "name": "stprodblobs01",
  "publicNetworkAccess": "Disabled",
  "type": "Microsoft.Storage/storageAccounts"
}
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-storage-prod/providers/Microsoft.Network/virtualNetworks/vnet-prod-eastus/subnets/snet-private-endpoints
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-storage-prod/providers/Microsoft.Network/privateEndpoints/pe-stprodblobs01-blob",
  "location": "eastus",
  "name": "pe-stprodblobs01-blob",
  "privateLinkServiceConnections": [
    {
      "name": "pe-stprodblobs01-blob-conn",
      "privateLinkServiceId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01",
      "requestMessage": "",
      "status": "Approved"
    }
  ],
  "provisioningState": "Succeeded",
  "resourceGroup": "rg-storage-prod"
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Storage/storageAccounts/stprodblobs01' under resource group 'rg-storage-prod' was not found.`** — Verify the storage account name and resource group exist with `az storage account show --resource-group $RG --name $SA`.
    **`(InvalidResourceId) The subnet 'snet-private-endpoints' does not exist in virtual network 'vnet-prod-eastus'.`** — Confirm the subnet name and VNET name are correct by running `az network vnet subnet list --resource-group $RG --vnet-name $VNET`.
    **`(BadRequest) Private endpoint cannot be created in a subnet that has a Network Security Group with deny rules for the storage service.`** — Review and adjust NSG rules on the subnet to allow private endpoint traffic, or temporarily associate a permissive NSG.
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


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-prod-eastus/providers/Microsoft.Network/privateDnsZones/privatelink.blob.core.windows.net",
  "location": "global",
  "name": "privatelink.blob.core.windows.net",
  "resourceGroup": "rg-prod-eastus",
  "type": "Microsoft.Network/privateDnsZones"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-prod-eastus/providers/Microsoft.Network/privateDnsZones/privatelink.blob.core.windows.net/virtualNetworkLinks/dns-link-vnet-prod",
  "name": "dns-link-vnet-prod",
  "registrationEnabled": false,
  "resourceGroup": "rg-prod-eastus",
  "virtualNetwork": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-prod-eastus/providers/Microsoft.Network/virtualNetworks/vnet-prod",
  "virtualNetworkLinkStatus": "Succeeded"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-prod-eastus/providers/Microsoft.Network/privateEndpoints/pe-blob-prod/privateDnsZoneGroups/dzg-pe-blob-prod",
  "name": "dzg-pe-blob-prod",
  "privateDnsZoneConfigs": [
    {
      "id": "blob",
      "privateDnsZoneId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-prod-eastus/providers/Microsoft.Network/privateDnsZones/privatelink.blob.core.windows.net",
      "recordSetName": "stprodblobs01"
    }
  ],
  "resourceGroup": "rg-prod-eastus"
}
Server:  10.0.0.4
Address:  10.0.0.4#53

Name:	stprodblobs01.blob.core.windows.net
Address: 10.2.1.15
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Network/privateDnsZones/privatelink.blob.core.windows.net' under resource group 'rg-prod-eastus' was not found.`** — Run the first `az network private-dns zone create` command before attempting to link or create the zone group.
    **`InvalidResourceReference: The private endpoint 'pe-blob-prod' does not exist in resource group 'rg-prod-eastus'.`** — Ensure the private endpoint
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


```text title="Expected output"
[
  {
    "fqdn": "stprodblobs01.blob.core.windows.net",
    "ip": [
      "10.2.1.45"
    ]
  }
]
HTTP/1.1 200 OK
Content-Length: 0
Content-Type: application/octet-stream
Date: Wed, 15 Jan 2025 14:32:18 GMT
Server: Windows-Azure-Blob/1.0 Microsoft-HTTPAPI/2.0

Name                          State              Subnet
------------------------------  -----------------  -----------------------------------------------
stprodblobs01-pe              Succeeded          /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Network/virtualNetworks/prod-vnet/subnets/pe-subnet
stprodfiles01-pe              Succeeded          /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Network/virtualNetworks/prod-vnet/subnets/pe-subnet
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.Network/privateEndpoints/stprodblobs01-pe' under resource group 'prod-rg' was not found.`** — Verify the private endpoint name matches exactly and the resource group variable `$RG` is set correctly with `echo $RG`.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to curl to skip certificate verification, or ensure the private DNS zone is properly linked to the VNet so the FQDN resolves to the private IP.
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


```text title="Expected output"
{
  "bypass": "AzureServices",
  "defaultAction": "Allow",
  "ipRules": [
    {
      "action": "Allow",
      "value": "10.0.0.0/24"
    }
  ],
  "virtualNetworkRules": [
    {
      "action": "Allow",
      "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Network/virtualNetworks/prod-vnet/subnets/storage-subnet",
      "state": "Succeeded"
    }
  ]
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`The subnet 'storage-subnet' under virtual network 'prod-vnet' does not have 'Microsoft.Storage' service endpoint enabled.`** — Enable the service endpoint on the subnet with `az network vnet subnet update --resource-group $RG --vnet-name $VNET --name $SUBNET --service-endpoints Microsoft.Storage`.
    **`The resource group '$RG' could not be found.`** — Verify the resource group name is correct and exists in your subscription with `az group list --query "[].name"`.
    **`The storage account '$SA' could not be found in the specified resource group.`** — Confirm the storage account name and resource group are correct with `az storage account list --resource-group $RG --query "[].name"`.
## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| DNS returns public IP from inside VNet | DNS zone not linked to VNet | Create/verify Private DNS Zone VNet link |
| `403 AuthorizationFailure` | Network rule blocking access | Add client IP or VNet to network rules |
| `Connection refused` on private IP | Private endpoint provisioning incomplete | Check endpoint state; allow 5 minutes |
| Works from VM but not from on-prem | DNS forwarding not configured | Configure on-prem DNS to forward `*.blob.core.windows.net` to Azure DNS |
