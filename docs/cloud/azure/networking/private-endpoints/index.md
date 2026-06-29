---
tags:
  - azure
  - networking
---
# Private Endpoints

<div class="kb-summary">
A Private Endpoint is a network interface that uses a private IP from your VNet to connect to an Azure PaaS service (e.g., Storage Account, Key Vault, SQL Database) over Azure Private Link. Traffic stays on the Microsoft backbone and never crosses the public internet.

*Applies to: Azure*
</div>

## Private Endpoint Architecture

```d2
direction: right

appVM: "Application VM\nin VNet" {shape: rectangle}
privDNS: "Private DNS Zone\nprivatelink.vaultcore.azure.net" {shape: rectangle}
pe: "Private Endpoint\nprivate IP from VNet" {shape: rectangle}
subnet: "VNet Subnet\nprivate-endpoint-network-policies = disabled" {shape: rectangle}
paasService: "Azure PaaS Service\nKey Vault · Storage · SQL" {shape: rectangle}

appVM -> privDNS
privDNS -> pe
appVM -> subnet
subnet -> pe
pe -> paasService
```

## Creating a Private Endpoint

```bash
# Disable network policy on the subnet (required before creating a private endpoint)
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --disable-private-endpoint-network-policies true

# Create a private endpoint for a Key Vault
az network private-endpoint create \
  --name pe-keyvault \
  --resource-group myRG \
  --vnet-name myVNet \
  --subnet mySubnet \
  --private-connection-resource-id /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.KeyVault/vaults/myKeyVault \
  --group-id vault \
  --connection-name pe-kv-connection \
  --location eastus

# Create a private endpoint for a Storage Account (blob)
az network private-endpoint create \
  --name pe-storage-blob \
  --resource-group myRG \
  --vnet-name myVNet \
  --subnet mySubnet \
  --private-connection-resource-id /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Storage/storageAccounts/myStorageAccount \
  --group-id blob \
  --connection-name pe-storage-connection \
  --location eastus
```


```text title="Expected output"
{
  "etag": "W/\"8f4c2a1b-9e3d-4f7a-b2c1-5d8e9a0f3c2b\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet",
  "name": "mySubnet",
  "privateEndpointNetworkPolicies": "Disabled",
  "privateLinkServiceNetworkPolicies": "Enabled",
  "provisioningState": "Succeeded"
}
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/privateEndpoints/pe-keyvault",
  "location": "eastus",
  "name": "pe-keyvault",
  "networkInterfaces": [
    {
      "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkInterfaces/pe-keyvault.nic.a1b2c3d4",
      "resourceGroup": "myRG"
    }
  ],
  "privateLinkServiceConnections": [
    {
      "groupIds": ["vault"],
      "name": "pe-kv-connection",
      "privateLinkServiceConnectionState": {
        "actionsRequired": "None",
        "description": "Auto-approved",
        "status": "Approved"
      },
      "provisioningState": "Succeeded"
    }
  ],
  "provisioningState": "Succeeded",
  "subnet": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet"
  }
}
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/privateEndpoints/pe-storage-blob",
  "location": "eastus",
  "name": "pe-storage-blob",
  "networkInterfaces": [
    {
      "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkInterfaces/pe-storage-blob.nic.e5f6g7h8",
      "resourceGroup": "myRG"
    }
  ],
  "privateLinkServiceConnections": [
    {
      "groupIds": ["blob"],
      "name": "pe-storage-connection",
      "privateLinkServiceConnectionState": {
        "actionsRequired": "None",
        "description": "Auto-approved",
        "status": "Approved"
      },
      "provisioningState": "Succeeded"
    }
  ],
  "provisioningState": "Succeeded",
  "subnet": {
    "id": "/subscriptions/12345
```
## Supported Group IDs (subresources)

| Service           | Group ID(s)                              |
|-------------------|------------------------------------------|
| Key Vault         | vault                                    |
| Storage Account   | blob, file, table, queue, dfs            |
| SQL Database      | sqlServer                                |
| Cosmos DB         | Sql, MongoDB, Cassandra, Gremlin, Table  |
| Service Bus       | namespace                                |
| Event Hub         | namespace                                |
| ACR               | registry                                 |
| App Service       | sites                                    |

## DNS Configuration

Private endpoints require DNS to resolve the service FQDN to the private IP. Azure automatically creates DNS records if you link the private DNS zone.

```bash
# Create a private DNS zone for Key Vault
az network private-dns zone create \
  --resource-group myRG \
  --name "privatelink.vaultcore.azure.net"

# Link the private DNS zone to the VNet
az network private-dns link vnet create \
  --resource-group myRG \
  --zone-name "privatelink.vaultcore.azure.net" \
  --name myVNetLink \
  --virtual-network myVNet \
  --registration-enabled false

# Create a DNS zone group on the private endpoint (auto-registers DNS record)
az network private-endpoint dns-zone-group create \
  --resource-group myRG \
  --endpoint-name pe-keyvault \
  --name default \
  --private-dns-zone /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net \
  --zone-name privatelink.vaultcore.azure.net
```


```text title="Expected output"
{
  "etag": "W/\"1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net",
  "location": "global",
  "name": "privatelink.vaultcore.azure.net",
  "resourceGroup": "myRG",
  "type": "Microsoft.Network/privateDnsZones"
}
{
  "etag": "W/\"9z8y7x6w-5v4u-3t2s-1r0q-9p8o7n6m5l4k\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net/virtualNetworkLinks/myVNetLink",
  "name": "myVNetLink",
  "registrationEnabled": false,
  "resourceGroup": "myRG",
  "virtualNetwork": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet"
  }
}
{
  "etag": "W/\"5a4b3c2d-1e0f-9g8h-7i6j-5k4l3m2n1o0p\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/privateEndpoints/pe-keyvault/privateDnsZoneGroups/default",
  "name": "default",
  "privateDnsZoneConfigs": [
    {
      "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/privateEndpoints/pe-keyvault/privateDnsZoneGroups/default/privateDnsZoneConfigs/privatelink.vaultcore.azure.net",
      "name": "privatelink.vaultcore.azure.net",
      "privateDnsZoneId": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net"
    }
  ]
}
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Network/privateEndpoints/pe-keyvault' under resource group 'myRG' was not found.`** — Create the private endpoint `pe-keyvault` before creating the DNS zone group, or verify the endpoint name matches exactly.
    **`InvalidResourceId: Provided resource id is invalid.`** — Replace `<sub-id>` with your actual subscription ID from `az account show --query id -o tsv`.
## Approving a Private Endpoint Connection

For services with manual approval, the connection must be approved by the resource owner.

```bash
# List pending private endpoint connections on a Key Vault
az network private-endpoint-connection list \
  --resource-group myRG \
  --name myKeyVault \
  --type Microsoft.KeyVault/vaults \
  --output table

# Approve a pending connection
az network private-endpoint-connection approve \
  --resource-group myRG \
  --resource-name myKeyVault \
  --name <connection-name> \
  --type Microsoft.KeyVault/vaults \
  --description "Approved by infra team"

# Reject a connection
az network private-endpoint-connection reject \
  --resource-group myRG \
  --resource-name myKeyVault \
  --name <connection-name> \
  --type Microsoft.KeyVault/vaults \
  --description "Rejected - not approved"
```


```text title="Expected output"
Name                                          Provisioning State    Connection State
--------------------------------------------  --------------------  ------------------
pe-conn-prod-eastus-20240115                  Succeeded             Pending
pe-conn-staging-westus-20240114               Succeeded             Pending
pe-conn-dev-eastus-20240110                   Succeeded             Approved

PrivateEndpointConnectionProperties:
  id: /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Microsoft.KeyVault/vaults/myKeyVault/privateEndpointConnections/pe-conn-prod-eastus-20240115
  name: pe-conn-prod-eastus-20240115
  type: Microsoft.Network/privateEndpointConnections
  provisioningState: Succeeded
  privateEndpoint:
    id: /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Microsoft.Network/privateEndpoints/pe-prod-eastus
  privateLinkServiceConnectionState:
    status: Approved
    description: Approved by infra team
    actionsRequired: None

PrivateEndpointConnectionProperties:
  id: /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Microsoft.KeyVault/vaults/myKeyVault/privateEndpointConnections/pe-conn-staging-westus-20240114
  name: pe-conn-staging-westus-20240114
  type: Microsoft.Network/privateEndpointConnections
  provisioningState: Succeeded
  privateLinkServiceConnectionState:
    status: Rejected
    description: Rejected - not approved
    actionsRequired: None
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.KeyVault/vaults/myKeyVault' under resource group 'myRG' was not found.`** — Verify the Key Vault name and resource group name are correct using `az keyvault list --resource-group myRG`.
    **`InvalidResourceName: The resource name '<connection-name>' is invalid or does not exist.`** — Replace `<connection-name>` with the actual connection name from the list output (e.g., `pe-conn-prod-eastus-20240115`).
    **`AuthorizationFailed: The client 'user@contoso.com' with object id 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d' does not have permission to perform action 'Microsoft.Network/privateEndpointConnections/write' over scope '/subscriptions/...'.`** — Ensure your user account has the Network Contributor or Owner role on the Key Vault's resource group.
## Network Policy for Private Endpoints

```bash
# Verify network policies are disabled on the subnet
az network vnet subnet show \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --query privateEndpointNetworkPolicies \
  --output tsv

# List all private endpoints in a resource group
az network private-endpoint list \
  --resource-group myRG \
  --output table

# Show private endpoint NIC and IP
az network private-endpoint show \
  --resource-group myRG \
  --name pe-keyvault \
  --query "customDnsConfigs" \
  --output json
```


```text title="Expected output"
Disabled
Name                ResourceGroup    PrivateLinkServiceId                                                                    PrivateEndpointId
------------------  ---------------  --------------------------------------------------------------------------------------  ------------------------------------
pe-keyvault         myRG             /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Micr...  /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Micr...
pe-storage          myRG             /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Micr...  /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Micr...
pe-sqldb            myRG             /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Micr...  /subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myRG/providers/Micr...
[
  {
    "fqdn": "keyvault.privatelink.vaultcore.azure.net",
    "ipAddresses": [
      "10.0.1.42"
    ]
  }
]
```

!!! warning "Common errors"
    **`(ResourceNotFound) No registered resource provider found for location 'eastus' and API version '2021-02-01' for type 'subnets'.`** — Verify the resource group name and VNet name are correct, and the subnet exists in the specified region.
    **`(AuthorizationFailed) The client 'user@contoso.com' with object id 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d' does not have authorization to perform action 'Microsoft.Network/virtualNetworks/subnets/read'.`** — Ensure your Azure account has Network Contributor or higher role assigned to the resource group.
    **`(InvalidResourceName) The name 'pe-keyvault' is invalid. It must begin with a letter or underscore, contain only letters, numbers, underscores, and hyphens, and end with a letter or number.`** — Rename the private endpoint to follow Azure naming conventions (alphanumeric, hyphens, and underscores only).
## Verification

```bash
# From a VM in the VNet, verify DNS resolves to private IP
# ssh into VM, then:
nslookup myKeyVault.vault.azure.net
# Expected: returns 10.x.x.x (private IP), not a public IP
```


```text title="Expected output"
Server:         168.63.129.16
Address:        168.63.129.16#53

Non-authoritative answer:
Name:   myKeyVault.vault.azure.net
Address: 10.42.1.15
Address: 10.42.1.16
```

!!! warning "Common errors"
    **`** server can't find myKeyVault.vault.azure.net: NXDOMAIN`** — Verify the private endpoint is created in the correct VNet and the private DNS zone is linked to your VNet.
    **`Non-authoritative answer: Name: myKeyVault.vault.azure.net Address: 52.xxx.xxx.xxx`** — The DNS is resolving to a public IP instead of private; confirm the private DNS zone (vault.azure.net) is linked to your VNet and the private endpoint A record exists.