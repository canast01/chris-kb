---
tags:
  - networking
description: "By default, Azure OpenAI resources accept traffic from all public IP addresses. For production deployments, restrict access using private endpoints, VNet..."
---
# Azure OpenAI Networking

<div class="kb-summary">
By default, Azure OpenAI resources accept traffic from all public IP addresses. For production deployments, restrict access using private endpoints, VNet integration, and firewall rules.

*Applies to: Azure OpenAI*
</div>

```d2
direction: down

private_endpoints: "Private Endpoints" {shape: rectangle}
disabling_public_access: "Disabling Public Access" {shape: rectangle}
firewall_rules: "Firewall Rules" {shape: rectangle}
network_architecture_patterns: "Network Architecture Patterns" {shape: rectangle}
testing_connectivity: "Testing Connectivity" {shape: rectangle}
outbound_connectivity_for_app_servic: "Outbound Connectivity for App Services" {shape: rectangle}

private_endpoints -> disabling_public_access: uses
disabling_public_access -> firewall_rules: uses
firewall_rules -> network_architecture_patterns: uses
network_architecture_patterns -> testing_connectivity: uses
testing_connectivity -> outbound_connectivity_for_app_servic: uses
```

## Private Endpoints

Private endpoints place the Azure OpenAI resource on your VNet with a private IP address, removing exposure to the public internet.

```bash
# Create a private endpoint for the Azure OpenAI resource
az network private-endpoint create \
  --name aoai-private-ep \
  --resource-group my-rg \
  --vnet-name my-vnet \
  --subnet private-endpoints-subnet \
  --private-connection-resource-id \
    "/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource" \
  --group-id account \
  --connection-name aoai-private-connection \
  --location eastus

# Create private DNS zone for resolution
az network private-dns zone create \
  --resource-group my-rg \
  --name "privatelink.openai.azure.com"

az network private-dns link vnet create \
  --resource-group my-rg \
  --zone-name "privatelink.openai.azure.com" \
  --name aoai-dns-link \
  --virtual-network my-vnet \
  --registration-enabled false

# Add DNS record group to auto-manage A records
az network private-endpoint dns-zone-group create \
  --resource-group my-rg \
  --endpoint-name aoai-private-ep \
  --name aoai-dns-zone-group \
  --private-dns-zone "privatelink.openai.azure.com" \
  --zone-name openai
```


```text title="Expected output"
{
  "customDnsConfigs": [],
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-rg/providers/Microsoft.Network/privateEndpoints/aoai-private-ep",
  "location": "eastus",
  "name": "aoai-private-ep",
  "networkInterfaces": [
    {
      "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-rg/providers/Microsoft.Network/networkInterfaces/aoai-private-ep.nic.a1b2c3d4-e5f6-47g8",
      "resourceGroup": "my-rg"
    }
  ],
  "privateLinkServiceConnections": [
    {
      "groupIds": ["account"],
      "name": "aoai-private-connection",
      "privateLinkServiceId": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource",
      "provisioningState": "Succeeded",
      "requestMessage": null
    }
  ],
  "provisioningState": "Succeeded",
  "resourceGroup": "my-rg",
  "subnet": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-rg/providers/Microsoft.Network/virtualNetworks/my-vnet/subnets/private-endpoints-subnet"
  }
}
{
  "etag": "W/\"x9y8z7w6-v5u4-t3s2-r1q0-p9o8n7m6l5k4\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-rg/providers/Microsoft.Network/privateDnsZones/privatelink.openai.azure.com",
  "location": "global",
  "name": "privatelink.openai.azure.com",
  "provisioningState": "Succeeded",
  "resourceGroup": "my-rg",
  "type": "Microsoft.Network/privateDnsZones"
}
{
  "etag": "W/\"m5l4k3j2-i1h0-g9f8-e7d6-c5b4a3z2y1x0\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/my-rg/providers/Microsoft.Network/privateDnsZones/privatelink.openai.azure.com/virtualNetworkLinks/aoai-dns-link",
  "location": "global",
  "name": "aoai-dns-link",
  "provisioningState": "Succeeded",
  "registrationEnabled": false,
  "resourceGroup": "my
```
## Disabling Public Access

After a private endpoint is in place, disable public network access:

```bash
az cognitiveservices account update \
  --name my-aoai-resource \
  --resource-group my-rg \
  --custom-subdomain-name my-aoai-resource \
  --public-network-access Disabled
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The resource 'my-aoai-resource' could not be found in resource group 'my-rg'.` | Verify the resource name and resource group name match exactly with `az cognitiveservices account list --resource-group my-rg`. |
    | `InvalidParameter: The value of parameter publicNetworkAccess is invalid.` | Use `Enabled` or `Disabled` (case-sensitive) and ensure the resource supports network access restrictions; some older deployments may not support this parameter. |
Traffic now flows only through the private endpoint.

## Firewall Rules

If public access must remain on, restrict to known CIDR ranges:

```bash
# Allow only specific IP ranges
az cognitiveservices account network-rule add \
  --name my-aoai-resource \
  --resource-group my-rg \
  --ip-address "203.0.113.0/24"

# Allow traffic from a specific VNet subnet
az cognitiveservices account network-rule add \
  --name my-aoai-resource \
  --resource-group my-rg \
  --vnet-name my-vnet \
  --subnet app-subnet

# Set default action to Deny
az cognitiveservices account update \
  --name my-aoai-resource \
  --resource-group my-rg \
  --default-action Deny
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource",
  "name": "my-aoai-resource",
  "type": "Microsoft.CognitiveServices/accounts",
  "location": "eastus",
  "sku": {
    "name": "S0"
  },
  "kind": "OpenAI",
  "properties": {
    "networkAcls": {
      "defaultAction": "Deny",
      "virtualNetworkRules": [
        {
          "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/my-rg/providers/Microsoft.Network/virtualNetworks/my-vnet/subnets/app-subnet",
          "state": "Succeeded"
        }
      ],
      "ipRules": [
        {
          "value": "203.0.113.0/24",
          "action": "Allow"
        }
      ]
    },
    "provisioningState": "Succeeded"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `(ResourceNotFound) The Resource 'Microsoft.CognitiveServices/accounts/my-aoai-resource' under resource group 'my-rg' was not found.` | Verify the resource name and resource group name match exactly with `az cognitiveservices account list -g my-rg`. |
    | `(InvalidParameter) The subnet 'app-subnet' does not exist in virtual network 'my-vnet'.` | Confirm the subnet exists in the VNet using `az network vnet subnet list -g my-rg --vnet-name my-vnet`. |
    | `(InvalidParameter) The IP address '203.0.113.0/24' is not a valid CIDR notation.` | Use valid CIDR notation (e.g., `203.0.113.0/24` or `203.0.113.5/32` for a single IP). |
## Network Architecture Patterns

| Pattern | Use Case | Pros | Cons |
|---|---|---|---|
| Public endpoint + API key | Development | Simple setup | No network isolation |
| Public endpoint + IP allowlist | Internal tools | Easy, no VNet required | Requires static IPs |
| Private endpoint + VNet | Production workloads | Full isolation | Requires DNS config |
| Private endpoint + Azure API Management | Multi-team API gateway | Centralised auth, routing | Added complexity |

## Testing Connectivity

```bash
# From within the VNet, resolve the private endpoint
nslookup my-aoai-resource.openai.azure.com
# Should return a 10.x.x.x or 172.x.x.x private IP

# Test from inside the VNet
curl -s \
  "https://my-aoai-resource.openai.azure.com/openai/deployments?api-version=2024-02-01" \
  -H "api-key: $AZURE_OPENAI_API_KEY" | jq '.data[].id'

# From outside the VNet (should fail with private endpoint + public disabled)
curl -v "https://my-aoai-resource.openai.azure.com/openai/models?api-version=2024-02-01" \
  -H "api-key: $AZURE_OPENAI_API_KEY"
# Expected: connection refused or 403 PublicAccessDisabled
```


```text title="Expected output"
Server:		10.0.0.4
Address:	10.0.0.4#53

Name:	my-aoai-resource.openai.azure.com
Address: 10.1.2.45

"gpt-4-deployment"
"gpt-35-turbo-deployment"
"text-embedding-ada-002"

*   Trying 10.1.2.45:443...
* Connected to my-aoai-resource.openai.azure.com (10.1.2.45) port 443 (#0)
* TLSv1.2 (OUT), TLS handshake, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Server hello (1):
* TLSv1.2 (IN), TLS handshake, Certificate (11):
* TLSv1.2 (IN), TLS handshake, Finished (20):
< HTTP/1.1 403 Forbidden
< Content-Type: application/json
{"error":{"code":"PublicAccessDisabled","message":"Public access is disabled for this resource."}}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to my-aoai-resource.openai.azure.com port 443: Connection refused` | Verify the private endpoint is created and the DNS A record points to the correct private IP (10.x.x.x or 172.x.x.x range). |
    | `nslookup: can't find my-aoai-resource.openai.azure.com: NXDOMAIN` | Ensure the private DNS zone is linked to the VNet and the private endpoint is registered in the zone. |
    | `"error":{"code":"InvalidAuthenticationToken"}` | Confirm the `$AZURE_OPENAI_API_KEY` environment variable is set and contains a valid API key from the Azure OpenAI resource. |
## Outbound Connectivity for App Services

When deploying applications on Azure App Service or Azure Functions, use VNet Integration to route outbound calls through the VNet:

```bash
az webapp vnet-integration add \
  --name my-app \
  --resource-group my-rg \
  --vnet my-vnet \
  --subnet app-subnet
```


```text title="Expected output"
Integrating webapp 'my-app' with vnet 'my-vnet' and subnet 'app-subnet'...
{
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/my-rg/providers/Microsoft.Web/sites/my-app/virtualNetworkConnections/my-vnet_app-subnet",
  "name": "my-vnet_app-subnet",
  "resourceGroup": "my-rg",
  "subnet": {
    "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/my-rg/providers/Microsoft.Network/virtualNetworks/my-vnet/subnets/app-subnet",
    "name": "app-subnet"
  },
  "vnet": {
    "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/my-rg/providers/Microsoft.Network/virtualNetworks/my-vnet",
    "name": "my-vnet"
  },
  "type": "Microsoft.Web/sites/virtualNetworkConnections"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound: The Resource 'Microsoft.Web/sites/my-app' under resource group 'my-rg' was not found.` | Verify the webapp name and resource group exist with `az webapp list -g my-rg`. |
    | `InvalidResourceId: The subnet 'app-subnet' does not exist in vnet 'my-vnet'.` | Confirm the subnet name with `az network vnet subnet list --vnet-name my-vnet -g my-rg`. |
    | `BadRequest: The subnet must have a service endpoint or delegation for Microsoft.Web.` | Add the Microsoft.Web service endpoint to the subnet using `az network vnet subnet update --vnet-name my-vnet -n app-subnet -g my-rg --service-endpoints Microsoft.Web`. |
Ensure the subnet has `Microsoft.CognitiveServices` service endpoint enabled if using service endpoints instead of private endpoints.
