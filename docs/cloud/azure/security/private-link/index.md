---
tags:
  - azure
  - security
description: "Azure Private Link enables private connectivity to Azure PaaS services (Storage, Key Vault, SQL, etc.) over a private endpoint in your VNet — eliminating..."
---
# Azure — Private Link

<div class="kb-summary">
Azure Private Link enables private connectivity to Azure PaaS services (Storage, Key Vault, SQL, etc.) over a private endpoint in your VNet — eliminating exposure to the public internet.

*Applies to: Azure*
</div>

```d2
direction: down

concepts: "Concepts" {shape: rectangle}
traffic_flow: "Traffic Flow" {shape: rectangle}
creating_a_private_endpoint: "Creating a Private Endpoint" {shape: rectangle}
dns_configuration: "DNS Configuration" {shape: rectangle}
private_dns_zones_by_service: "Private DNS Zones by Service" {shape: rectangle}
validating_connectivity: "Validating Connectivity" {shape: rectangle}

concepts -> traffic_flow: uses
traffic_flow -> creating_a_private_endpoint: uses
creating_a_private_endpoint -> dns_configuration: uses
dns_configuration -> private_dns_zones_by_service: uses
private_dns_zones_by_service -> validating_connectivity: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Concepts

| Term | Definition |
|---|---|
| **Private Link Service** | The Azure PaaS service resource being accessed privately |
| **Private Endpoint** | A NIC with a private IP in your VNet, connected to the Private Link Service |
| **Private DNS Zone** | Azure DNS zone that resolves the service's public FQDN to the private IP |
| **DNS zone link** | Association between the Private DNS Zone and a VNet |

## Traffic Flow

```text
App (in VNet) → resolves storage.blob.core.windows.net
                → Private DNS Zone overrides → 10.1.0.5 (private endpoint IP)
                → Traffic stays within VNet / Azure backbone
                → Never traverses internet
```

Without Private Link, resolution returns a public IP and traffic exits to the internet (even if using a service endpoint).

## Creating a Private Endpoint

```bash
# Example: Key Vault private endpoint

# 1. Disable public access on the vault
az keyvault update \
  --name <vault-name> \
  --resource-group <rg> \
  --public-network-access Disabled

# 2. Create the private endpoint
az network private-endpoint create \
  --name "<vault-name>-pe" \
  --resource-group <rg> \
  --vnet-name <vnet-name> \
  --subnet <subnet-name> \
  --private-connection-resource-id \
    /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name> \
  --group-id vault \
  --connection-name "<vault-name>-connection"

# 3. Get the private endpoint NIC IP
PE_IP=$(az network private-endpoint show \
  --name "<vault-name>-pe" \
  --resource-group <rg> \
  --query 'customDnsConfigs[0].ipAddresses[0]' --output tsv)

echo "Private endpoint IP: $PE_IP"
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cde/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/mykeyvault",
  "name": "mykeyvault",
  "properties": {
    "publicNetworkAccess": "Disabled"
  }
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cde/resourceGroups/prod-rg/providers/Microsoft.Network/privateEndpoints/mykeyvault-pe",
  "name": "mykeyvault-pe",
  "properties": {
    "provisioningState": "Succeeded",
    "privateLinkServiceConnections": [
      {
        "name": "mykeyvault-connection",
        "properties": {
          "provisioningState": "Succeeded",
          "privateLinkServiceId": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cde/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/mykeyvault",
          "groupIds": ["vault"]
        }
      }
    ]
  }
}
Private endpoint IP: 10.1.2.45
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.KeyVault/vaults/<vault-name>' under resource group '<rg>' was not found.`** — Verify the vault name and resource group name are correct and the vault exists in the specified subscription.
    **`(InvalidResourceId) The provided resource ID is invalid or the resource does not exist.`** — Ensure the subscription ID, resource group name, and vault name in the private-connection-resource-id parameter match exactly with the actual resource.
    **`(BadRequest) The subnet '<subnet-name>' does not have the 'Microsoft.Network/virtualNetworks/subnets/join/action' permission.`** — Verify the subnet exists in the specified vnet and that the service principal has network permissions to create private endpoints.
## DNS Configuration

### Private DNS Zone setup

```bash
# Create private DNS zone for Key Vault
az network private-dns zone create \
  --resource-group <rg> \
  --name "privatelink.vaultcore.azure.net"

# Link DNS zone to VNet
az network private-dns link vnet create \
  --resource-group <rg> \
  --zone-name "privatelink.vaultcore.azure.net" \
  --name "<vnet-name>-link" \
  --virtual-network <vnet-name> \
  --registration-enabled false

# Add A record pointing to private endpoint IP
az network private-dns record-set a create \
  --resource-group <rg> \
  --zone-name "privatelink.vaultcore.azure.net" \
  --name <vault-name>

az network private-dns record-set a add-record \
  --resource-group <rg> \
  --zone-name "privatelink.vaultcore.azure.net" \
  --record-set-name <vault-name> \
  --ipv4-address "$PE_IP"
```


```text title="Expected output"
{
  "etag": "W/\"a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net",
  "location": "global",
  "name": "privatelink.vaultcore.azure.net",
  "resourceGroup": "myResourceGroup",
  "type": "Microsoft.Network/privateDnsZones"
}
{
  "etag": "W/\"b2c3d4e5-f6g7-4h8i-9j0k-1l2m3n4o5p6q\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net/virtualNetworkLinks/prod-vnet-link",
  "name": "prod-vnet-link",
  "registrationEnabled": false,
  "resourceGroup": "myResourceGroup",
  "virtualNetwork": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/prod-vnet"
  }
}
{
  "etag": "W/\"c3d4e5f6-g7h8-4i9j-0k1l-2m3n4o5p6q7r\"",
  "fqdn": "myvault.privatelink.vaultcore.azure.net.",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net/A/myvault",
  "name": "myvault",
  "resourceGroup": "myResourceGroup",
  "ttl": 3600,
  "type": "Microsoft.Network/privateDnsZones/A"
}
{
  "aRecords": [
    {
      "ipv4Address": "10.2.5.42"
    }
  ],
  "etag": "W/\"d4e5f6g7-h8i9-4j0k-1l2m-3n4o5p6q7r8s\"",
  "fqdn": "myvault.privatelink.vaultcore.azure.net.",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net/A/myvault",
  "name": "myvault",
  "resourceGroup": "myResourceGroup",
  "ttl": 3600,
  "type": "Microsoft.Network/privateDnsZones/A"
}
```

!!! warning "Common errors"
    **`ResourceNot
### Auto-registration via `privateDnsZoneGroup`

```bash
# Attach private DNS zone group to the endpoint (auto-registers the A record)
az network private-endpoint dns-zone-group create \
  --endpoint-name "<vault-name>-pe" \
  --resource-group <rg> \
  --name "default" \
  --private-dns-zone /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net \
  --zone-name "privatelink.vaultcore.azure.net"
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateEndpoints/myvault-pe/privateDnsZoneGroups/default",
  "name": "default",
  "privateDnsZoneConfigs": [
    {
      "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateEndpoints/myvault-pe/privateDnsZoneGroups/default/privateDnsZoneConfigs/privatelink.vaultcore.azure.net",
      "name": "privatelink.vaultcore.azure.net",
      "privateDnsZoneId": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net",
      "recordSets": [
        {
          "fqdn": "myvault.privatelink.vaultcore.azure.net",
          "ipAddresses": [
            "10.0.1.5"
          ],
          "recordType": "A"
        }
      ]
    }
  ],
  "resourceGroup": "myResourceGroup",
  "type": "Microsoft.Network/privateEndpoints/privateDnsZoneGroups"
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/privateEndpoints/vault-name-pe' under resource group 'myResourceGroup' was not found.`** — Verify the private endpoint name matches exactly and exists in the specified resource group with `az network private-endpoint list -g <rg>`.
    **`(InvalidResourceId) The provided resource ID is invalid.`** — Ensure the private DNS zone resource ID path is correct and the zone exists by running `az network private-dns zone list -g <rg>`.
    **`(BadRequest) The private endpoint 'vault-name-pe' does not have a network interface attached.`** — Wait a few moments for the private endpoint to fully provision before attaching the DNS zone group.
## Private DNS Zones by Service

| Service | Private DNS Zone |
|---|---|
| Key Vault | `privatelink.vaultcore.azure.net` |
| Storage (blob) | `privatelink.blob.core.windows.net` |
| Storage (file) | `privatelink.file.core.windows.net` |
| Storage (queue) | `privatelink.queue.core.windows.net` |
| Azure SQL | `privatelink.database.windows.net` |
| Azure Container Registry | `privatelink.azurecr.io` |
| AKS API server | `<guid>.privatelink.<region>.azmk8s.io` |
| Event Hub / Service Bus | `privatelink.servicebus.windows.net` |
| App Service | `privatelink.azurewebsites.net` |

## Validating Connectivity

```bash
# From a VM in the VNet — verify DNS resolves to private IP
nslookup <vault-name>.vault.azure.net
# Should return 10.x.x.x (private IP), not 52.x.x.x (public)

# Test TCP connectivity to private endpoint
nc -zv <vault-name>.vault.azure.net 443

# From outside the VNet (on-premises via VPN/ExpressRoute)
nslookup <vault-name>.vault.azure.net <dns-server-in-vnet>
```


```text title="Expected output"
Server:  168.63.129.16
Address:  168.63.129.16#53

Non-authoritative answer:
Name:	contoso-vault.vault.azure.net
Address: 10.42.3.15

Connection to contoso-vault.vault.azure.net 443 port [tcp/https] succeeded!

Server:  10.42.1.4
Address:  10.42.1.4#53

Non-authoritative answer:
Name:	contoso-vault.vault.azure.net
Address: 10.42.3.15
```

!!! warning "Common errors"
    **`nslookup: can't resolve '(null)': Name or service not known`** — Replace `<vault-name>` and `<dns-server-in-vnet>` with actual values; do not run the template literally.
    **`Connection to contoso-vault.vault.azure.net 443 port [tcp/https] timed out.`** — Verify the private endpoint exists in the VNet, the Network Security Group allows outbound 443, and the VM has network connectivity to the subnet hosting the private endpoint.
    **`Address: 52.231.x.x`** — DNS is resolving to the public IP instead of private; check that private DNS zone is linked to the VNet and the private endpoint is properly registered in Azure DNS.
## On-Premises Access via ExpressRoute / VPN

For on-premises hosts to reach private endpoints, they must:

1. Route traffic over ExpressRoute or VPN to the VNet.
2. Resolve the service FQDN to the private IP — either:
   - Configure on-prem DNS to forward the `privatelink.*` zone to Azure DNS (168.63.129.16), or
   - Add a static A record in on-prem DNS for the service FQDN pointing to the private endpoint IP.

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| Service still resolves to public IP | Private DNS zone not linked to VNet | Verify: `az network private-dns link vnet list --zone-name <zone>` |
| 403 from VM in same VNet | Public access disabled but endpoint connection not approved | Check endpoint connection state: `az network private-endpoint show` → `privateLinkServiceConnectionState.status` should be `Approved` |
| On-prem hosts cannot reach private endpoint | DNS not forwarding to Azure; traffic not routing via VPN/ER | Set up DNS conditional forwarder for `privatelink.*` zones to 168.63.129.16 |
| Endpoint works but traffic slow | NSG on endpoint subnet blocking or hairpinning | Verify NSG allows traffic from app subnet to private endpoint subnet on required port |
| Multiple VNets need access | DNS zone only linked to one VNet | Link the private DNS zone to each VNet that needs resolution |
