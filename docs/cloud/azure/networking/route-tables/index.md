---
tags:
  - azure
  - networking
description: "Azure Route Tables (User Defined Routes / UDRs) override Azure's default system routes"
---
# Route Tables

<div class="kb-summary">
Azure Route Tables (User Defined Routes / UDRs) override Azure's default system routes

*Applies to: Azure*
</div>

```d2
direction: down

adding_user_defined_routes: "Adding User Defined Routes" {shape: rectangle}
next_hop_types: "Next Hop Types" {shape: rectangle}
bgp_route_propagation: "BGP Route Propagation" {shape: rectangle}
associating_a_route_table_with_a_sub: "Associating a Route Table with a Subnet" {shape: rectangle}
viewing_effective_routes: "Viewing Effective Routes" {shape: rectangle}
forced_tunnelling_design: "Forced Tunnelling Design" {shape: rectangle}

adding_user_defined_routes -> next_hop_types: uses
next_hop_types -> bgp_route_propagation: uses
bgp_route_propagation -> associating_a_route_table_with_a_sub: uses
associating_a_route_table_with_a_sub -> viewing_effective_routes: uses
viewing_effective_routes -> forced_tunnelling_design: uses
```

## Adding User Defined Routes

```bash
# Route all internet traffic through an NVA (forced tunnelling)
az network route-table route create \
  --resource-group myRG \
  --route-table-name myRouteTable \
  --name route-to-nva \
  --address-prefix 0.0.0.0/0 \
  --next-hop-type VirtualAppliance \
  --next-hop-ip-address 10.0.0.4

# Route on-prem traffic through VPN gateway
az network route-table route create \
  --resource-group myRG \
  --route-table-name myRouteTable \
  --name route-onprem \
  --address-prefix 192.168.0.0/16 \
  --next-hop-type VirtualNetworkGateway

# Route traffic to a specific subnet via the VNet (keep local)
az network route-table route create \
  --resource-group myRG \
  --route-table-name myRouteTable \
  --name route-local-subnet \
  --address-prefix 10.0.2.0/24 \
  --next-hop-type VnetLocal

# Drop traffic to a specific range (blackhole)
az network route-table route create \
  --resource-group myRG \
  --route-table-name myRouteTable \
  --name blackhole-route \
  --address-prefix 10.99.0.0/16 \
  --next-hop-type None
```


```text title="Expected output"
{
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/routeTables/myRouteTable/routes/route-to-nva",
  "name": "route-to-nva",
  "nextHopIpAddress": "10.0.0.4",
  "nextHopType": "VirtualAppliance",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG"
}
{
  "etag": "W/\"b2c3d4e5-f6g7-48h9-i0j1-k2l3m4n5o6p7\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/routeTables/myRouteTable/routes/route-onprem",
  "name": "route-onprem",
  "nextHopType": "VirtualNetworkGateway",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG"
}
{
  "etag": "W/\"c3d4e5f6-g7h8-49i0-j1k2-l3m4n5o6p7q8\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/routeTables/myRouteTable/routes/route-local-subnet",
  "name": "route-local-subnet",
  "nextHopType": "VnetLocal",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG"
}
{
  "etag": "W/\"d4e5f6g7-h8i9-50j0-k1l2-m3n4o5p6q7r8\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/routeTables/myRouteTable/routes/blackhole-route",
  "name": "blackhole-route",
  "nextHopType": "None",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG"
}
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.Network/routeTables/myRouteTable' under resource group 'myRG' was not found.`** — Verify the route table exists in the correct resource group with `az network route-table show --resource-group myRG --name myRouteTable`.
    **`InvalidNextHopIpAddress : The next hop IP address '10.0.0.4' is not valid for the next hop type 'VirtualAppliance'.`** — Ensure the NVA IP address exists within your VNet address space and the NVA is deployed and running
## Next Hop Types

| Next Hop Type          | Description                                          |
|------------------------|------------------------------------------------------|
| VirtualNetworkGateway  | Send to VPN or ExpressRoute gateway                  |
| VnetLocal              | Stay within the VNet (override default)              |
| Internet               | Route to public internet                             |
| VirtualAppliance       | Forward to a firewall / NVA at a specific IP         |
| None                   | Drop packets (blackhole)                             |

## BGP Route Propagation

When a VNet is connected to a VPN or ExpressRoute gateway, on-prem routes are propagated via BGP to all subnets. Disable this on subnets where you want only UDRs to apply (e.g., Gateway subnet should keep BGP enabled; workload subnets can disable it to enforce NVA routing).

```bash
# Disable BGP route propagation on a route table
az network route-table update \
  --resource-group myRG \
  --name myRouteTable \
  --disable-bgp-route-propagation true

# Verify BGP propagation state
az network route-table show \
  --resource-group myRG \
  --name myRouteTable \
  --query disableBgpRoutePropagation \
  --output tsv
```


```text title="Expected output"
(no output — command completes silently)
true
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name with `az group list` and ensure you are in the correct subscription.
    **`RouteTableNotFound`** — Confirm the route table exists in the specified resource group using `az network route-table list --resource-group myRG`.
## Associating a Route Table with a Subnet

```bash
# Associate route table with a subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --route-table myRouteTable

# Disassociate route table from a subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --route-table ""
```


```text title="Expected output"
{
  "addressPrefix": "10.0.1.0/24",
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet",
  "name": "mySubnet",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "routeTable": {
    "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/myRG/providers/Microsoft.Network/routeTables/myRouteTable",
    "resourceGroup": "myRG"
  }
}
{
  "addressPrefix": "10.0.1.0/24",
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet",
  "name": "mySubnet",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "routeTable": null
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/routeTables/myRouteTable' under resource group 'myRG' was not found.`** — Verify the route table name and resource group are correct using `az network route-table list --resource-group myRG`.
    **`(InvalidResourceReference) The resource '/subscriptions/.../routeTables/myRouteTable' does not exist.`** — Ensure the route table exists in the same resource group and region as the virtual network before associating it.
## Viewing Effective Routes

```bash
# Show effective routes on a VM NIC (includes system and UDR routes)
az network nic show-effective-route-table \
  --resource-group myRG \
  --name myVM-nic \
  --output table

# Show routes defined in the route table
az network route-table route list \
  --resource-group myRG \
  --route-table-name myRouteTable \
  --output table
```


```text title="Expected output"
Name                 State    Source                Address Prefix    Next Hop Type       Next Hop IP
-------------------  -------  --------------------  ----------------  ------------------  ---------------
default              Active   Default               0.0.0.0/0         Internet
myCustomRoute        Active   User                  10.0.0.0/8        VirtualAppliance    10.1.2.50
system_route_1       Active   Default               10.0.0.0/16       VnetLocal
AzureLoadBalancer    Active   Default               168.63.129.16/32  AzureLoadBalancer

Name             Address Prefix    Next Hop Type       Next Hop IP    Provisioning State
---------------  ----------------  ------------------  ---------------  -------------------
prodRoute        192.168.0.0/16    VirtualAppliance    10.1.2.50      Succeeded
devRoute         172.16.0.0/12     Internet                            Succeeded
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Network/networkInterfaces/myVM-nic' under resource group 'myRG' was not found.`** — Verify the NIC name matches the actual network interface attached to the VM using `az network nic list --resource-group myRG`.
    **`ResourceNotFound: The Resource 'Microsoft.Network/routeTables/myRouteTable' under resource group 'myRG' was not found.`** — Confirm the route table name and resource group are correct with `az network route-table list --resource-group myRG`.
## Forced Tunnelling Design

Forced tunnelling routes all internet-bound traffic from a subnet through an on-premises network or NVA for inspection. The VPN or ExpressRoute gateway subnet must NOT have a UDR with 0.0.0.0/0 — only workload subnets should have that route.

```bash
# Create route table for workload subnet with forced tunnel
az network route-table create \
  --resource-group myRG \
  --name workload-rt \
  --disable-bgp-route-propagation true

az network route-table route create \
  --resource-group myRG \
  --route-table-name workload-rt \
  --name forced-tunnel \
  --address-prefix 0.0.0.0/0 \
  --next-hop-type VirtualAppliance \
  --next-hop-ip-address 10.0.0.4

az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name workload-subnet \
  --route-table workload-rt
```


```text title="Expected output"
{
  "disableBgpRoutePropagation": true,
  "etag": "W/\"a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/routeTables/workload-rt",
  "location": "eastus",
  "name": "workload-rt",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "routes": [],
  "subnets": null,
  "tags": null,
  "type": "Microsoft.Network/routeTables"
}
{
  "addressPrefix": "0.0.0.0/0",
  "etag": "W/\"b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e\"",
  "hasBgpOverride": false,
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/routeTables/workload-rt/routes/forced-tunnel",
  "name": "forced-tunnel",
  "nextHopIpAddress": "10.0.0.4",
  "nextHopType": "VirtualAppliance",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "type": "Microsoft.Network/routeTables/routes"
}
{
  "addressPrefix": "10.0.0.0/24",
  "delegations": [],
  "etag": "W/\"c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/workload-subnet",
  "name": "workload-subnet",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "routeTable": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/routeTables/workload-rt"
  }
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/virtualNetworks/myVNet' under resource group 'myRG' was not found.`** — Verify the VNet name and resource group exist using `az network vnet list --resource-group myRG`.
    **`(InvalidNextHopIpAddress) The next hop IP address '10.0.0.4' is not valid for the specified next hop type.`** — Ensure the next-hop IP address exists on a network interface in the VNet and is reachable from the subnet.