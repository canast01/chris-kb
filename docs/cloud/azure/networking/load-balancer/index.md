---
tags:
  - azure
  - networking
---
# Load Balancer

<div class="kb-summary">
Azure Load Balancer is a Layer 4 (TCP/UDP) load balancer for distributing inbound traffic to backend VMs or scale sets.

*Applies to: Azure*
</div>

```d2
direction: down

frontend_ips: "Frontend IPs" {shape: rectangle}
backend_pools: "Backend Pools" {shape: rectangle}
health_probes: "Health Probes" {shape: rectangle}
load_balancing_rules: "Load Balancing Rules" {shape: rectangle}
inbound_nat_rules: "Inbound NAT Rules" {shape: rectangle}
sku_comparison: "SKU Comparison" {shape: rectangle}

frontend_ips -> backend_pools: uses
backend_pools -> health_probes: uses
health_probes -> load_balancing_rules: uses
load_balancing_rules -> inbound_nat_rules: uses
inbound_nat_rules -> sku_comparison: uses
```

## Frontend IPs

```bash
# Add an additional frontend IP (internal, for private load balancing)
az network lb frontend-ip create \
  --resource-group myRG \
  --lb-name myLB \
  --name myInternalFrontend \
  --vnet-name myVNet \
  --subnet mySubnet \
  --private-ip-address 10.0.1.100 \
  --private-ip-address-version IPv4

# List frontend IP configs
az network lb frontend-ip list \
  --resource-group myRG \
  --lb-name myLB \
  --output table
```


```text title="Expected output"
{
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/loadBalancers/myLB/frontendIPConfigurations/myInternalFrontend",
  "name": "myInternalFrontend",
  "privateIpAddress": "10.0.1.100",
  "privateIpAddressVersion": "IPv4",
  "privateIpAllocationMethod": "Static",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "subnet": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet"
  },
  "type": "Microsoft.Network/loadBalancers/frontendIPConfigurations"
}

Name                    PrivateIpAddress    PrivateIpAllocationMethod    ProvisioningState
----------------------  ------------------  ---------------------------  -------------------
myPublicFrontend        N/A                 Dynamic                      Succeeded
myInternalFrontend      10.0.1.100          Static                       Succeeded
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/loadBalancers/myLB' under resource group 'myRG' was not found.`** — Verify the load balancer name and resource group exist with `az network lb list --resource-group myRG`.
    **`(InvalidParameter) The subnet 'mySubnet' does not exist in virtual network 'myVNet'.`** — Confirm the subnet name is correct by running `az network vnet subnet list --resource-group myRG --vnet-name myVNet`.
    **`(InvalidParameter) The private IP address 10.0.1.100 is not within the address space of subnet mySubnet.`** — Ensure the private IP falls within the subnet's address range using `az network vnet subnet show --resource-group myRG --vnet-name myVNet --name mySubnet`.
## Backend Pools

```bash
# Add a VM NIC to the backend pool
az network lb address-pool address add \
  --resource-group myRG \
  --lb-name myLB \
  --pool-name myBackendPool \
  --name vm1-ip \
  --vnet /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet \
  --ip-address 10.0.1.4

# Add a second address
az network lb address-pool address add \
  --resource-group myRG \
  --lb-name myLB \
  --pool-name myBackendPool \
  --name vm2-ip \
  --vnet /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet \
  --ip-address 10.0.1.5

# List backend pool addresses
az network lb address-pool address list \
  --resource-group myRG \
  --lb-name myLB \
  --pool-name myBackendPool \
  --output table
```


```text title="Expected output"
{
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/loadBalancers/myLB/backendAddressPools/myBackendPool/addresses/vm1-ip",
  "ipAddress": "10.0.1.4",
  "name": "vm1-ip",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "type": "Microsoft.Network/loadBalancers/backendAddressPools/addresses",
  "virtualNetwork": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet"
}
{
  "etag": "W/\"b2c3d4e5-f6g7-48h9-i0j1-k2l3m4n5o6p7\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/loadBalancers/myLB/backendAddressPools/myBackendPool/addresses/vm2-ip",
  "ipAddress": "10.0.1.5",
  "name": "vm2-ip",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "type": "Microsoft.Network/loadBalancers/backendAddressPools/addresses",
  "virtualNetwork": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet"
}
Name      IpAddress    VirtualNetwork
--------  -----------  -----------------------------------------------
vm1-ip    10.0.1.4     /subscriptions/.../virtualNetworks/myVNet
vm2-ip    10.0.1.5     /subscriptions/.../virtualNetworks/myVNet
```

!!! warning "Common errors"
    **`(BadRequest) The virtual network resource id is invalid or does not exist.`** — Verify the subscription ID and virtual network name in the `--vnet` parameter match your actual Azure resources.
    **`(NotFound) The load balancer 'myLB' does not exist in resource group 'myRG'.`** — Confirm the load balancer name and resource group are correct using `az network lb list --resource-group myRG`.
    **`(Conflict) The address 'vm1-ip' already exists in the backend pool.`** — Use a unique name for each backend address or remove the existing address first with `az network lb address-pool address remove`.
## Health Probes

```bash
# Create a TCP health probe on port 80
az network lb probe create \
  --resource-group myRG \
  --lb-name myLB \
  --name myHealthProbe \
  --protocol Tcp \
  --port 80 \
  --interval 15 \
  --threshold 2

# Create an HTTP probe with a custom path
az network lb probe create \
  --resource-group myRG \
  --lb-name myLB \
  --name httpProbe \
  --protocol Http \
  --port 80 \
  --path /health \
  --interval 15 \
  --threshold 2
```


```text title="Expected output"
{
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/loadBalancers/myLB/probes/myHealthProbe",
  "intervalInSeconds": 15,
  "loadBalancingRules": [],
  "name": "myHealthProbe",
  "numberOfProbes": 2,
  "port": 80,
  "protocol": "Tcp",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "type": "Microsoft.Network/loadBalancers/probes"
}
{
  "etag": "W/\"b2c3d4e5-f6g7-48h9-i0j1-k2l3m4n5o6p7\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/loadBalancers/myLB/probes/httpProbe",
  "intervalInSeconds": 15,
  "loadBalancingRules": [],
  "name": "httpProbe",
  "numberOfProbes": 2,
  "port": 80,
  "protocol": "Http",
  "provisioningState": "Succeeded",
  "requestPath": "/health",
  "resourceGroup": "myRG",
  "type": "Microsoft.Network/loadBalancers/probes"
}
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.Network/loadBalancers/myLB' under resource group 'myRG' was not found.`** — Verify the load balancer name and resource group exist using `az network lb list --resource-group myRG`.
    **`InvalidParameter : The value of parameter 'port' is invalid.`** — Ensure the port number is between 1 and 65535 and matches a port your backend pool is listening on.
## Load Balancing Rules

```bash
# Create a load balancing rule for HTTPS
az network lb rule create \
  --resource-group myRG \
  --lb-name myLB \
  --name HTTPS-Rule \
  --protocol Tcp \
  --frontend-port 443 \
  --backend-port 443 \
  --frontend-ip-name myFrontendIP \
  --backend-pool-name myBackendPool \
  --probe-name myHealthProbe \
  --idle-timeout 4 \
  --enable-tcp-reset true

# List all LB rules
az network lb rule list \
  --resource-group myRG \
  --lb-name myLB \
  --output table
```


```text title="Expected output"
{
  "backendPort": 443,
  "enableFloatingIp": false,
  "enableTcpReset": true,
  "frontendIpConfiguration": {
    "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/myRG/providers/Microsoft.Network/loadBalancers/myLB/frontendIPConfigurations/myFrontendIP",
    "resourceGroup": "myRG"
  },
  "frontendPort": 443,
  "idleTimeoutInMinutes": 4,
  "loadDistribution": "Default",
  "name": "HTTPS-Rule",
  "probe": {
    "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/myRG/providers/Microsoft.Network/loadBalancers/myLB/probes/myHealthProbe"
  },
  "protocol": "Tcp",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG"
}

Name          Protocol    Frontend Port    Backend Port    Backend Pool      Probe
------------  ----------  ---------------  ---------------  ----------------  ----------------
HTTPS-Rule    Tcp         443              443              myBackendPool     myHealthProbe
HTTP-Rule     Tcp         80               80               myBackendPool     myHealthProbe
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/loadBalancers/myLB' under resource group 'myRG' was not found.`** — Verify the load balancer name and resource group exist using `az network lb list --resource-group myRG`.
    **`(InvalidResourceReference) The referenced resource '/subscriptions/.../frontendIPConfigurations/myFrontendIP' does not exist.`** — Confirm the frontend IP configuration name matches an existing one with `az network lb frontend-ip list --resource-group myRG --lb-name myLB`.
    **`(InvalidResourceReference) The referenced resource '/subscriptions/.../backendAddressPools/myBackendPool' does not exist.`** — Create the backend pool first with `az network lb address-pool create --resource-group myRG --lb-name myLB --name myBackendPool`.
## Inbound NAT Rules

Inbound NAT rules map a specific frontend port to a backend VM port for direct access (e.g., SSH/RDP).

```bash
# Create an inbound NAT rule for SSH to vm1
az network lb inbound-nat-rule create \
  --resource-group myRG \
  --lb-name myLB \
  --name ssh-vm1 \
  --protocol Tcp \
  --frontend-port 2201 \
  --backend-port 22 \
  --frontend-ip-name myFrontendIP
```


```text title="Expected output"
{
  "backendPort": 22,
  "enableFloatingIp": false,
  "enableTcpReset": false,
  "frontendIpConfiguration": {
    "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cde/resourceGroups/myRG/providers/Microsoft.Network/loadBalancers/myLB/frontendIPConfigurations/myFrontendIP",
    "resourceGroup": "myRG"
  },
  "frontendPort": 2201,
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cde/resourceGroups/myRG/providers/Microsoft.Network/loadBalancers/myLB/inboundNatRules/ssh-vm1",
  "idleTimeoutInMinutes": 4,
  "name": "ssh-vm1",
  "protocol": "Tcp",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "type": "Microsoft.Network/loadBalancers/inboundNatRules"
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/loadBalancers/myLB' under resource group 'myRG' was not found.`** — Verify the load balancer name and resource group exist using `az network lb list --resource-group myRG`.
    **`(InvalidResourceReference) The resource '/subscriptions/.../frontendIPConfigurations/myFrontendIP' does not exist.`** — Confirm the frontend IP configuration name matches exactly with `az network lb frontend-ip list --resource-group myRG --lb-name myLB`.
## SKU Comparison

| Feature                 | Basic SKU    | Standard SKU         |
|-------------------------|--------------|----------------------|
| Availability zones      | No           | Yes (zone-redundant) |
| SLA                     | None         | 99.99%               |
| Backend pool type       | Availability set | Any VM/VMSS       |
| Secure by default       | No           | Yes (requires NSG)   |
| Diagnostics             | Limited      | Full metrics/logs    |
| HTTPS probes            | No           | Yes                  |
