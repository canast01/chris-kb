---
tags:
  - azure
  - networking
---
# Network Security Groups

<div class="kb-summary">
Network Security Groups (NSGs) are stateful packet filters that control inbound and outbound traffic to Azure resources. They can be associated with subnets or individual network interfaces. Rules are evaluated by priority — the lowest number wins.

*Applies to: Azure*
</div>

## NSG Rule Evaluation

```d2
direction: right

traffic: "Inbound / Outbound Traffic" {shape: rectangle}
rule100: "rule100" {shape: rectangle}
allow: "ALLOW\ntraffic passes" {shape: rectangle}
deny: "DENY\ntraffic dropped" {shape: rectangle}
rule200: "rule200" {shape: rectangle}
ruleN: "ruleN" {shape: rectangle}
defaultDeny: "Default Deny-All rule\npriority 65500" {shape: rectangle}

traffic -> rule100
rule100 -> allow
rule100 -> deny
rule100 -> rule200
rule200 -> allow
rule200 -> ruleN
ruleN -> defaultDeny
defaultDeny -> deny
```

## Creating and Managing NSGs

```bash
# Create an NSG
az network nsg create \
  --resource-group myRG \
  --name myNSG \
  --location eastus

# List NSGs in a resource group
az network nsg list \
  --resource-group myRG \
  --output table

# Show all rules in an NSG
az network nsg show \
  --resource-group myRG \
  --name myNSG \
  --output json
```


```text title="Expected output"
{
  "defaultSecurityRules": [
    {
      "name": "AllowVnetInBound",
      "priority": 65000,
      "sourceAddressPrefix": "VirtualNetwork",
      "destinationAddressPrefix": "VirtualNetwork"
    },
    {
      "name": "AllowAzureLoadBalancerInBound",
      "priority": 65001,
      "sourceAddressPrefix": "AzureLoadBalancer",
      "destinationAddressPrefix": "*"
    },
    {
      "name": "DenyAllInBound",
      "priority": 65500,
      "sourceAddressPrefix": "*",
      "destinationAddressPrefix": "*"
    }
  ],
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkSecurityGroups/myNSG",
  "location": "eastus",
  "name": "myNSG",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "securityRules": [],
  "type": "Microsoft.Network/networkSecurityGroups"
}

Name    Location    ResourceGroup    ProvisioningState
------  ----------  ---------------  -------------------
myNSG   eastus      myRG             Succeeded
```

!!! warning "Common errors"
    **`ResourceGroupNotFound : Resource group 'myRG' could not be found.`** — Create the resource group first with `az group create --name myRG --location eastus`.
    **`ResourceNotFound : The Resource 'Microsoft.Network/networkSecurityGroups/myNSG' under resource group 'myRG' was not found.`** — Verify the NSG name and resource group are correct, or create the NSG before querying it.
## Inbound and Outbound Rules

```bash
# Allow HTTPS inbound from the internet
az network nsg rule create \
  --nsg-name myNSG \
  --resource-group myRG \
  --name Allow-HTTPS \
  --priority 100 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes Internet \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 443

# Allow SSH inbound from a specific management IP range
az network nsg rule create \
  --nsg-name myNSG \
  --resource-group myRG \
  --name Allow-SSH-Management \
  --priority 110 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes 10.0.0.0/24 \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 22

# Deny all other inbound traffic explicitly
az network nsg rule create \
  --nsg-name myNSG \
  --resource-group myRG \
  --name Deny-All-Inbound \
  --priority 4000 \
  --direction Inbound \
  --access Deny \
  --protocol '*' \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges '*'

# Allow outbound to Azure Monitor endpoints
az network nsg rule create \
  --nsg-name myNSG \
  --resource-group myRG \
  --name Allow-AzureMonitor-Out \
  --priority 200 \
  --direction Outbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes VirtualNetwork \
  --source-port-ranges '*' \
  --destination-address-prefixes AzureMonitor \
  --destination-port-ranges 443
```


```text title="Expected output"
{
  "access": "Allow",
  "destinationAddressPrefix": "*",
  "destinationPortRange": "443",
  "direction": "Inbound",
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkSecurityGroups/myNSG/securityRules/Allow-HTTPS",
  "name": "Allow-HTTPS",
  "priority": 100,
  "protocol": "Tcp",
  "provisioningState": "Succeeded",
  "sourceAddressPrefix": "Internet",
  "sourcePortRange": "*",
  "type": "Microsoft.Network/networkSecurityGroups/securityRules"
}
{
  "access": "Allow",
  "destinationAddressPrefix": "*",
  "destinationPortRange": "22",
  "direction": "Inbound",
  "etag": "W/\"b2c3d4e5-f6g7-48h9-i0j1-k2l3m4n5o6p7\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkSecurityGroups/myNSG/securityRules/Allow-SSH-Management",
  "name": "Allow-SSH-Management",
  "priority": 110,
  "protocol": "Tcp",
  "provisioningState": "Succeeded",
  "sourceAddressPrefix": "10.0.0.0/24",
  "sourcePortRange": "*",
  "type": "Microsoft.Network/networkSecurityGroups/securityRules"
}
{
  "access": "Deny",
  "destinationAddressPrefix": "*",
  "destinationPortRange": "*",
  "direction": "Inbound",
  "etag": "W/\"c3d4e5f6-g7h8-49i0-j1k2-l3m4n5o6p7q8\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkSecurityGroups/myNSG/securityRules/Deny-All-Inbound",
  "name": "Deny-All-Inbound",
  "priority": 4000,
  "protocol": "*",
  "provisioningState": "Succeeded",
  "sourceAddressPrefix": "*",
  "sourcePortRange": "*",
  "type": "Microsoft.Network/networkSecurityGroups/securityRules"
}
{
  "access": "Allow",
  "destinationAddressPrefix": "AzureMonitor",
  "destinationPortRange": "443",
  "direction": "Outbound",
  "etag": "W/\"d4e5f6g7-h8i9-50j0-k1l2
```
## Rule Priority and Default Rules

| Priority Range | Guideline                                   |
|----------------|---------------------------------------------|
| 100–999        | Critical allow rules (specific sources)     |
| 1000–3999      | Broader allow rules                         |
| 4000–4096      | Explicit deny rules                         |
| 65000–65500    | Azure default rules (cannot be deleted)     |

Default rules that exist in every NSG:

| Rule Name                     | Direction | Action | Notes                              |
|-------------------------------|-----------|--------|------------------------------------|
| AllowVNetInBound              | Inbound   | Allow  | Allow traffic from same VNet/peered VNets |
| AllowAzureLoadBalancerInBound | Inbound   | Allow  | Allow load balancer health probes  |
| DenyAllInBound                | Inbound   | Deny   | Block everything else              |
| AllowVNetOutBound             | Outbound  | Allow  | Allow traffic to same VNet         |
| AllowInternetOutBound         | Outbound  | Allow  | Allow outbound to internet         |
| DenyAllOutBound               | Outbound  | Deny   | Block everything else              |

## Application Security Groups (ASGs)

ASGs group VMs logically so NSG rules can reference the group name instead of IP ranges, simplifying rule management as VMs scale.

```bash
# Create an ASG for web servers
az network asg create \
  --resource-group myRG \
  --name web-servers-asg

# Associate a NIC with an ASG
az network nic update \
  --resource-group myRG \
  --name myVM-nic \
  --application-security-groups web-servers-asg

# Allow HTTPS inbound to the ASG
az network nsg rule create \
  --nsg-name myNSG \
  --resource-group myRG \
  --name Allow-HTTPS-to-WebServers \
  --priority 120 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes Internet \
  --source-port-ranges '*' \
  --destination-asgs web-servers-asg \
  --destination-port-ranges 443
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/myRG/providers/Microsoft.Network/applicationSecurityGroups/web-servers-asg",
  "location": "eastus",
  "name": "web-servers-asg",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "tags": null,
  "type": "Microsoft.Network/applicationSecurityGroups"
}
(no output — command completes silently)
{
  "access": "Allow",
  "description": null,
  "destinationAddressPrefixes": [],
  "destinationApplicationSecurityGroups": [
    {
      "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/myRG/providers/Microsoft.Network/applicationSecurityGroups/web-servers-asg",
      "resourceGroup": "myRG"
    }
  ],
  "destinationPortRanges": [
    "443"
  ],
  "direction": "Inbound",
  "etag": "W/\"a1b2c3d4-e5f6-7890-abcd-ef1234567890\"",
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/myRG/providers/Microsoft.Network/networkSecurityGroups/myNSG/securityRules/Allow-HTTPS-to-WebServers",
  "name": "Allow-HTTPS-to-WebServers",
  "priority": 120,
  "protocol": "Tcp",
  "provisioningState": "Succeeded",
  "sourceAddressPrefixes": [
    "Internet"
  ],
  "sourcePortRanges": [
    "*"
  ]
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/networkSecurityGroups/myNSG' under resource group 'myRG' was not found.`** — Verify the NSG name matches an existing NSG in the resource group using `az network nsg list --resource-group myRG`.
    **`(InvalidResourceReference) The referenced application security group '/subscriptions/.../web-servers-asg' does not exist.`** — Ensure the ASG was created successfully in the same resource group before creating the NSG rule.
    **`(BadRequest) The NIC 'myVM-nic' does not exist in resource group 'myRG'.`** — Confirm the NIC name is correct by listing NICs with `az network nic list --resource-group myRG`.
## NSG Flow Logs

NSG Flow Logs record accepted and denied traffic for compliance analysis and troubleshooting.

```bash
# Enable NSG flow logs (v2 with traffic analytics)
az network watcher flow-log create \
  --location eastus \
  --name myFlowLog \
  --nsg myNSG \
  --storage-account /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Storage/storageAccounts/myStorageAccount \
  --workspace /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.OperationalInsights/workspaces/myWorkspace \
  --interval 10 \
  --traffic-analytics true \
  --resource-group myRG
```


```text title="Expected output"
{
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "flowAnalyticsConfiguration": {
    "networkWatcherFlowAnalyticsConfiguration": {
      "enabled": true,
      "trafficAnalyticsInterval": 10,
      "workspaceResourceId": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.OperationalInsights/workspaces/myWorkspace",
      "workspaceRegion": "eastus",
      "workspaceId": "a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6"
    }
  },
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkWatchers/NetworkWatcher_eastus/flowLogs/myFlowLog",
  "location": "eastus",
  "name": "myFlowLog",
  "provisioningState": "Succeeded",
  "resourceGroup": "myRG",
  "retentionPolicy": {
    "days": 0,
    "enabled": false
  },
  "storageId": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Storage/storageAccounts/myStorageAccount",
  "targetResourceId": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkSecurityGroups/myNSG",
  "type": "Microsoft.Network/networkWatchers/flowLogs"
}
```

!!! warning "Common errors"
    **`The resource with name 'myNSG' and type 'networkSecurityGroups' could not be found in resource group 'myRG'.`** — Verify the NSG name and resource group are correct using `az network nsg list --resource-group myRG`.
    **`The specified storage account does not exist or you do not have permission to access it.`** — Ensure the storage account exists in the same region and subscription, and the user has Storage Blob Data Contributor role on it.
    **`The workspace resource ID is invalid or the workspace does not exist.`** — Confirm the Log Analytics workspace exists and use `az monitor log-analytics workspace list --resource-group myRG` to get the correct resource ID.
## Associating NSGs

```bash
# Associate NSG with a subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myVNet \
  --name mySubnet \
  --network-security-group myNSG

# Associate NSG with a NIC
az network nic update \
  --resource-group myRG \
  --name myVM-nic \
  --network-security-group myNSG
```


```text title="Expected output"
{
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworks/myVNet/subnets/mySubnet",
  "name": "mySubnet",
  "networkSecurityGroup": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkSecurityGroups/myNSG",
    "resourceGroup": "myRG"
  },
  "provisioningState": "Succeeded",
  "type": "Microsoft.Network/virtualNetworks/subnets"
}
{
  "dnsSettings": {
    "appliedDnsServers": [],
    "dnsServers": []
  },
  "enableAcceleratedNetworking": false,
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkInterfaces/myVM-nic",
  "ipConfigurations": [...],
  "name": "myVM-nic",
  "networkSecurityGroup": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/networkSecurityGroups/myNSG",
    "resourceGroup": "myRG"
  },
  "provisioningState": "Succeeded",
  "type": "Microsoft.Network/networkInterfaces"
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/networkSecurityGroups/myNSG' under resource group 'myRG' was not found.`** — Verify the NSG exists in the correct resource group using `az network nsg list --resource-group myRG`.
    **`(InvalidResourceReference) The resource '/subscriptions/.../subnets/mySubnet' does not exist.`** — Confirm the subnet name and virtual network name are correct and exist in the specified resource group.
    **`(AuthorizationFailed) The client 'user@example.com' with object id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have permission to perform action 'Microsoft.Network/networkSecurityGroups/join/action'.`** — Ensure your Azure account has Network Contributor or higher role assigned to the resource group.