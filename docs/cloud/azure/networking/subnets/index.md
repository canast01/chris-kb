# Subnets

Subnets segment a Virtual Network address space into smaller ranges.

```text
┌───────────────────────────────────────────────────────────┐
│               VNet  10.0.0.0/16                           │
│                                                           │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │  web-subnet      │  │  app-subnet      │               │
│  │  10.0.1.0/24     │  │  10.0.2.0/24     │               │
│  │                  │  │                  │               │
│  │  NSG: web-nsg    │  │  NSG: app-nsg    │               │
│  │  RT:  web-rt     │  │  RT:  app-rt     │               │
│  └──────────────────┘  └──────────────────┘               │
│                                                           │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │  db-subnet       │  │  GatewaySubnet   │               │
│  │  10.0.3.0/24     │  │  10.0.255.0/27   │               │
│  │                  │  │  (VPN/ER GW)     │               │
│  │  Delegation:     │  │  no NSG required │               │
│  │  (optional)      │  │                  │               │
│  └──────────────────┘  └──────────────────┘               │
│                                                           │
│  Azure reserves 5 IPs per subnet (first 4 + last 1)       │
└───────────────────────────────────────────────────────────┘
``` Each subnet can have an NSG, route table, service endpoints, and delegations independently configured. Azure reserves 5 addresses in each subnet (first 4 and last 1).

## Subnet Sizing

Azure reserves 5 IP addresses per subnet, so the usable host count is `2^(32-prefix) - 5`.

| CIDR     | Total IPs | Usable IPs | Notes                              |
|----------|-----------|------------|------------------------------------|
| /29      | 8         | 3          | Minimum for most services          |
| /28      | 16        | 11         | Small workload subnet              |
| /27      | 32        | 27         | Medium subnet                      |
| /26      | 64        | 59         | Standard workload subnet           |
| /24      | 256       | 251        | Large subnet, common for VM pools  |
| /23      | 512       | 507        | AKS node pool minimum recommended  |

## Creating Subnets

```bash
# Create a subnet in an existing VNet
az network vnet subnet create \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --address-prefix 10.0.1.0/24

# Create multiple subnets at VNet creation time
az network vnet create \
  --resource-group myRG \
  --name myVNet \
  --address-prefix 10.0.0.0/16 \
  --subnet-name default \
  --subnet-prefix 10.0.0.0/24

# Add additional subnets
az network vnet subnet create \
  --resource-group myRG \
  --vnet-name myVNet \
  --name app-subnet \
  --address-prefix 10.0.1.0/24

az network vnet subnet create \
  --resource-group myRG \
  --vnet-name myVNet \
  --name db-subnet \
  --address-prefix 10.0.2.0/24

az network vnet subnet create \
  --resource-group myRG \
  --vnet-name myVNet \
  --name GatewaySubnet \
  --address-prefix 10.0.255.0/27

# List subnets
az network vnet subnet list \
  --resource-group myRG \
  --vnet-name myVNet \
  --output table
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
