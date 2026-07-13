---
tags:
  - azure
  - networking
description: "Subnets segment a Virtual Network address space into smaller ranges."
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


```text title="Expected output"
{
  "serviceEndpoints": [
    {
      "service": "Microsoft.Storage",
      "locations": [
        "eastus",
        "westus"
      ]
    },
    {
      "service": "Microsoft.KeyVault",
      "locations": [
        "eastus",
        "westus"
      ]
    }
  ]
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound : Resource group 'myRG' could not be found.`** — Verify the resource group name with `az group list` and use the correct name.
    **`ResourceNotFound : The Resource 'Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet' under resource group 'myRG' was not found.`** — Confirm the VNet and subnet names exist using `az network vnet subnet list --resource-group myRG --vnet-name myVNet`.
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


```text title="Expected output"
{
  "addressPrefix": "10.0.2.0/24",
  "delegations": [
    {
      "name": "delegation",
      "properties": {
        "serviceName": "Microsoft.ContainerInstance/containerGroups"
      }
    }
  ],
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/aci-subnet",
  "name": "aci-subnet",
  "provisioningState": "Succeeded"
}
{
  "addressPrefix": "10.0.3.0/24",
  "delegations": [
    {
      "name": "delegation",
      "properties": {
        "serviceName": "Microsoft.Databricks/workspaces"
      }
    }
  ],
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/databricks-private",
  "name": "databricks-private",
  "provisioningState": "Succeeded"
}
{
  "addressPrefix": "10.0.2.0/24",
  "delegations": [],
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/aci-subnet",
  "name": "aci-subnet",
  "provisioningState": "Succeeded"
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/virtualNetworks/myVNet/subnets/aci-subnet' under resource group 'myRG' was not found.`** — Verify the subnet name, VNet name, and resource group name are correct using `az network vnet subnet list --resource-group myRG --vnet-name myVNet`.
    **`(InvalidDelegationServiceName) The delegation service name 'Microsoft.ContainerInstance/containerGroups' is not valid for this subscription.`** — Ensure the service provider is registered in your subscription with `az provider register --namespace Microsoft.ContainerInstance`.
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


```text title="Expected output"
{
  "addressPrefix": "10.0.1.0/24",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet",
  "name": "mySubnet",
  "networkSecurityGroup": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkSecurityGroups/myNSG",
    "resourceGroup": "myRG"
  },
  "provisioningState": "Succeeded",
  "routeTable": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/routeTables/myRouteTable",
    "resourceGroup": "myRG"
  },
  "serviceEndpoints": []
}
{
  "addressPrefix": "10.0.1.0/24",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet",
  "name": "mySubnet",
  "networkSecurityGroup": null,
  "provisioningState": "Succeeded",
  "routeTable": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/routeTables/myRouteTable",
    "resourceGroup": "myRG"
  },
  "serviceEndpoints": []
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/networkSecurityGroups/myNSG' under resource group 'myRG' was not found.`** — Verify the NSG name and resource group are correct with `az network nsg list --resource-group myRG`.
    **`(InvalidResourceReference) The resource '/subscriptions/.../routeTables/myRouteTable' referenced by resource '/subscriptions/.../subnets/mySubnet' does not exist.`** — Ensure the route table exists in the same resource group using `az network route-table list --resource-group myRG`.
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


```text title="Expected output"
{
  "addressPrefix": "10.0.1.0/24",
  "delegations": [],
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet",
  "ipConfigurationProfiles": [],
  "name": "mySubnet",
  "natGateway": null,
  "networkSecurityGroup": null,
  "privateEndpointNetworkPolicies": "Disabled",
  "privateLinkServiceNetworkPolicies": "Enabled",
  "provisioningState": "Succeeded",
  "purpose": null,
  "resourceGroup": "myRG",
  "routeTable": null,
  "serviceEndpoints": [],
  "type": "Microsoft.Network/virtualNetworks/subnets"
}
```

!!! warning "Common errors"
    **`The resource group 'myRG' could not be found.`** — Verify the resource group name with `az group list` and ensure you are in the correct subscription.
    **`The virtual network 'myVNet' could not be found in resource group 'myRG'.`** — Confirm the VNet name exists in the specified resource group using `az network vnet list --resource-group myRG`.
    **`The subnet 'mySubnet' could not be found in virtual network 'myVNet'.`** — List subnets with `az network vnet subnet list --resource-group myRG --vnet-name myVNet` to verify the subnet name.