---
tags:
  - azure
  - networking
---
# Virtual Network

<div class="kb-summary">
An Azure Virtual Network (VNet) is the fundamental building block for private networking in Azure. Resources in a VNet can communicate with each other, with on-premises networks, and with the internet, all controlled by routing and security policies.

*Applies to: Azure*
</div>

## Hub-and-Spoke VNet Topology

```d2
direction: right

onprem: "On-Premises\nExpressRoute / VPN" {shape: rectangle}
hub: "Hub VNet\nAzure Firewall · Bastion · VPN GW · DNS" {shape: rectangle}
spoke1: "Spoke VNet 1\nWorkload A — app · db" {shape: rectangle}
spoke2: "Spoke VNet 2\nWorkload B — app · db" {shape: rectangle}
spoke3: "Spoke VNet 3\nShared Services" {shape: rectangle}

```

## VNet Creation

```bash
# Create a VNet with a default subnet
az network vnet create \
  --resource-group myRG \
  --name myVNet \
  --address-prefix 10.0.0.0/16 \
  --subnet-name default \
  --subnet-prefix 10.0.0.0/24 \
  --location eastus

# Create a VNet with custom DNS servers
az network vnet create \
  --resource-group myRG \
  --name myVNet \
  --address-prefix 10.0.0.0/16 \
  --subnet-name default \
  --subnet-prefix 10.0.0.0/24 \
  --dns-servers 10.0.0.4 10.0.0.5

# List VNets in a subscription
az network vnet list \
  --output table

# Show VNet details
az network vnet show \
  --resource-group myRG \
  --name myVNet \
  --output json
```


```text title="Expected output"
{
  "newVNet": {
    "addressSpace": {
      "addressPrefixes": [
        "10.0.0.0/16"
      ]
    },
    "dnsSettings": {
      "dnsServers": []
    },
    "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet",
    "location": "eastus",
    "name": "myVNet",
    "provisioningState": "Succeeded",
    "resourceGroup": "myRG",
    "subnets": [
      {
        "addressPrefix": "10.0.0.0/24",
        "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/default",
        "name": "default",
        "provisioningState": "Succeeded"
      }
    ]
  }
}
{
  "newVNet": {
    "addressSpace": {
      "addressPrefixes": [
        "10.0.0.0/16"
      ]
    },
    "dnsSettings": {
      "dnsServers": [
        "10.0.0.4",
        "10.0.0.5"
      ]
    },
    "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet",
    "location": "eastus",
    "name": "myVNet",
    "provisioningState": "Succeeded",
    "resourceGroup": "myRG"
  }
}
Name                ResourceGroup    Location    NumSubnets    ProvisioningState
------------------  ---------------  ----------  -----------   ------------------
myVNet              myRG             eastus      1             Succeeded
prodVNet            myRG             westus2     3             Succeeded
devVNet             prodRG           eastus2     2             Succeeded
...
{
  "addressSpace": {
    "addressPrefixes": [
      "10.0.0.0/16"
    ]
  },
  "dnsSettings": {
    "dnsServers": [
      "10.0.0.4",
      "10.0.0.5"
    ]
  },
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet",
  "location": "eastus",
  "name": "myVNet",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "subnets": [
    {
      "addressPrefix": "10.0.0.0/24",
      "name": "default",
      "provisioningState": "Succeeded"
    }
  ],
  "type": "Microsoft.Network/virtual
```
## Address Space Management

```bash
# Add a second address space to an existing VNet
az network vnet update \
  --resource-group myRG \
  --name myVNet \
  --add addressSpace.addressPrefixes 10.1.0.0/16

# Update DNS server settings
az network vnet update \
  --resource-group myRG \
  --name myVNet \
  --dns-servers 10.0.0.4 10.0.0.5

# Remove a custom DNS server (reset to Azure default)
az network vnet update \
  --resource-group myRG \
  --name myVNet \
  --dns-servers ""
```


```text title="Expected output"
{
  "addressSpace": {
    "addressPrefixes": [
      "10.0.0.0/16",
      "10.1.0.0/16"
    ]
  },
  "dhcpOptions": {
    "dnsServers": []
  },
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet",
  "location": "eastus",
  "name": "myVNet",
  "provisioningState": "Succeeded",
  "subnets": [
    {
      "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/subnet-1",
      "name": "subnet-1",
      "addressPrefix": "10.0.1.0/24"
    }
  ],
  "type": "Microsoft.Network/virtualNetworks"
}
```

!!! warning "Common errors"
    **`The resource 'Microsoft.Network/virtualNetworks/myVNet' under resource group 'myRG' was not found.`** — Verify the VNet name and resource group name are correct using `az network vnet list --resource-group myRG`.
    **`Address space 10.1.0.0/16 overlaps with existing address space 10.0.0.0/16.`** — Ensure the new address space does not overlap with existing subnets; use a non-overlapping CIDR block like 10.2.0.0/16.
## VNet Peering

VNet peering connects two VNets so that resources can communicate using private IPs. Peering is non-transitive by default and can be regional or global (cross-region).

```bash
# Create peering from VNet A to VNet B
az network vnet peering create \
  --resource-group myRG \
  --name vnetA-to-vnetB \
  --vnet-name vnetA \
  --remote-vnet /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/vnetB \
  --allow-vnet-access true \
  --allow-forwarded-traffic true

# Create peering from VNet B to VNet A (peering is not automatically bidirectional)
az network vnet peering create \
  --resource-group myRG \
  --name vnetB-to-vnetA \
  --vnet-name vnetB \
  --remote-vnet /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/vnetA \
  --allow-vnet-access true \
  --allow-forwarded-traffic true

# List peerings for a VNet
az network vnet peering list \
  --resource-group myRG \
  --vnet-name vnetA \
  --output table
```


```text title="Expected output"
{
  "allowForwardedTraffic": true,
  "allowGatewayTransit": false,
  "allowVirtualNetworkAccess": true,
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/vnetA/virtualNetworkPeerings/vnetA-to-vnetB",
  "name": "vnetA-to-vnetB",
  "peeringState": "Initiated",
  "provisioningState": "Succeeded",
  "remoteVirtualNetwork": {
    "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/vnetB"
  },
  "resourceGroup": "myRG"
}
{
  "allowForwardedTraffic": true,
  "allowGatewayTransit": false,
  "allowVirtualNetworkAccess": true,
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/vnetB/virtualNetworkPeerings/vnetB-to-vnetA",
  "name": "vnetB-to-vnetA",
  "peeringState": "Connected",
  "provisioningState": "Succeeded",
  "remoteVirtualNetwork": {
    "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/vnetA"
  },
  "resourceGroup": "myRG"
}
Name            ResourceGroup    PeeringState    ProvisioningState
--------------  ---------------  ---------------  -------------------
vnetA-to-vnetB  myRG             Connected        Succeeded
```

!!! warning "Common errors"
    **`The remote virtual network with id '/subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/vnetB' does not exist.`** — Verify the subscription ID, resource group name, and VNet name in the remote-vnet resource ID are correct.
    **`(BadRequest) Peering between virtual networks in different subscriptions is not supported for this operation.`** — Ensure both VNets are in the same subscription, or use cross-subscription peering with appropriate permissions.
## Peering Flags

| Flag                         | Effect                                                  |
|------------------------------|---------------------------------------------------------|
| `--allow-vnet-access`        | Allow traffic between peered VNets                     |
| `--allow-forwarded-traffic`  | Accept forwarded traffic from the remote VNet's NVA    |
| `--allow-gateway-transit`    | Allow remote VNet to use this VNet's gateway            |
| `--use-remote-gateways`      | Use the remote VNet's gateway (hub-spoke pattern)       |

## VNet DNS Settings

| DNS Mode          | Configuration                                            |
|-------------------|----------------------------------------------------------|
| Azure default     | No DNS servers set — uses 168.63.129.16                  |
| Custom DNS        | Set VM/on-prem DNS IPs in VNet DNS server settings       |
| Private DNS zone  | Link the zone to the VNet for automatic resolution       |

```bash
# Check effective DNS configuration
az network vnet show \
  --resource-group myRG \
  --name myVNet \
  --query "dhcpOptions.dnsServers" \
  --output json
```


```text title="Expected output"
[
  "10.0.1.4",
  "10.0.1.5"
]
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name with `az group list` and ensure you're authenticated to the correct subscription.
    **`ResourceNotFound`** — Confirm the virtual network name exists in the specified resource group using `az network vnet list --resource-group myRG`.
## Checking Available Address Space

```bash
# Check addresses available in a VNet
az network vnet check-ip-address \
  --resource-group myRG \
  --name myVNet \
  --ip-address 10.0.1.100

# List all subnets and their prefixes
az network vnet subnet list \
  --resource-group myRG \
  --vnet-name myVNet \
  --output table
```


```text title="Expected output"
{
  "available": true
}
Name      AddressPrefix    ProvisioningState    Purpose
---------  ---------------  -------------------  -----------------------
subnet-1   10.0.1.0/24      Succeeded            Regular
subnet-2   10.0.2.0/24      Succeeded            Regular
subnet-3   10.0.3.0/24      Succeeded            Regular
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/virtualNetworks/myVNet' under resource group 'myRG' was not found.`** — Verify the VNet name and resource group name are correct with `az network vnet list --resource-group myRG`.
    **`(InvalidParameter) The provided IP address '10.0.1.100' is not valid for CIDR notation validation.`** — Ensure the IP address is in valid dotted-decimal format (e.g., 10.0.1.100, not 10.0.1.100/32).
## Tagging and Governance

```bash
# Tag a VNet for environment tracking
az network vnet update \
  --resource-group myRG \
  --name myVNet \
  --set tags.environment=production tags.owner=network-team

# Delete a VNet (removes all subnets — use with caution)
az network vnet delete \
  --resource-group myRG \
  --name myVNet \
  --yes
```


```text title="Expected output"
(no output — command completes silently)
Request successful. Deleting virtual network 'myVNet'...
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/virtualNetworks/myVNet' under resource group 'myRG' was not found.`** — Verify the VNet name and resource group name are correct with `az network vnet list --resource-group myRG`.
    **`(AuthorizationFailed) The client 'user@example.com' with object id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have authorization to perform action 'Microsoft.Network/virtualNetworks/delete' over scope '/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet'.`** — Request the Network Contributor or Owner role for the resource group from your subscription administrator.