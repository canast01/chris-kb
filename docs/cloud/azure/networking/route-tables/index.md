# Route Tables

Azure Route Tables (User Defined Routes / UDRs) override Azure's default system routes, allowing you to control how traffic is directed within and out of your VNet. Common uses include forced tunnelling through a firewall NVA, BGP propagation control, and hub-spoke routing.

## Creating a Route Table

```bash
# Create a route table
az network route-table create \
  --resource-group myRG \
  --name myRouteTable \
  --location eastus \
  --disable-bgp-route-propagation false

# Show route table details
az network route-table show \
  --resource-group myRG \
  --name myRouteTable \
  --output json

# List all route tables in a resource group
az network route-table list \
  --resource-group myRG \
  --output table
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
