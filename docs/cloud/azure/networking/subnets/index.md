---
tags:
  - azure
  - networking
---
# Subnets

<div class="kb-summary">
Subnets segment a Virtual Network address space into smaller ranges.

*Applies to: Azure*
</div>

```d2
direction: down

service_endpoints: "Service Endpoints" {shape: rectangle}
subnet_delegation: "Subnet Delegation" {shape: rectangle}
nsg_and_route_table_association: "NSG and Route Table Association" {shape: rectangle}
private_endpoint_network_policies: "Private Endpoint Network Policies" {shape: rectangle}

service_endpoints -> subnet_delegation: uses
subnet_delegation -> nsg_and_route_table_association: uses
nsg_and_route_table_association -> private_endpoint_network_policies: uses
```

## Service Endpoints

Service endpoints extend VNet identity to Azure PaaS services, ensuring traffic flows over the Azure backbone rather than the public internet.

```bash
# Enable service endpoints for Storage and Key Vault on a subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --service-endpoints Microsoft.Storage Microsoft.KeyVault

# List service endpoints on a subnet
az network vnet subnet show \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --query serviceEndpoints \
  --output json
```

## Subnet Delegation

Delegation allows certain Azure services (e.g., Azure Container Instances, Azure NetApp Files, Azure Databricks) to inject resources directly into a subnet.

```bash
# Delegate a subnet to Azure Container Instances
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name aci-subnet \
  --delegations Microsoft.ContainerInstance/containerGroups

# Delegate to Azure Databricks
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name databricks-private \
  --delegations Microsoft.Databricks/workspaces

# Remove a delegation
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name aci-subnet \
  --remove delegations
```

## NSG and Route Table Association

```bash
# Associate an NSG with a subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --network-security-group myNSG

# Associate a route table with a subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --route-table myRouteTable

# Disassociate NSG from a subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --network-security-group ""
```

## Private Endpoint Network Policies

```bash
# Disable private endpoint network policies (required before creating a private endpoint)
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --disable-private-endpoint-network-policies true

# Show all subnet properties
az network vnet subnet show \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --output json
```
