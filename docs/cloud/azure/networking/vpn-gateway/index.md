---
tags:
  - azure
  - networking
---
# VPN Gateway

<div class="kb-summary">
Azure VPN Gateway provides encrypted connectivity between Azure VNets and on-premises networks over IPsec/IKE tunnels.

*Applies to: Azure*
</div>

```d2
direction: down

sitetosite_connection: "Site-to-Site Connection" {shape: rectangle}
pointtosite_configuration: "Point-to-Site Configuration" {shape: rectangle}
bgp_configuration: "BGP Configuration" {shape: rectangle}
activeactive_configuration: "Active-Active Configuration" {shape: rectangle}
monitoring: "Monitoring" {shape: rectangle}

sitetosite_connection -> pointtosite_configuration: uses
pointtosite_configuration -> bgp_configuration: uses
bgp_configuration -> activeactive_configuration: uses
activeactive_configuration -> monitoring: uses
```

## Site-to-Site Connection

```bash
# Create a local network gateway (represents on-prem)
az network local-gateway create \
  --resource-group myRG \
  --name onprem-lgw \
  --gateway-ip-address 203.0.113.1 \
  --address-prefixes 192.168.0.0/16 192.168.10.0/24

# Create the S2S connection
az network vpn-connection create \
  --resource-group myRG \
  --name s2s-connection \
  --vnet-gateway1 myVpnGateway \
  --local-gateway2 onprem-lgw \
  --shared-key "Sup3rSecr3tKey!" \
  --connection-type IPsec

# Check connection status
az network vpn-connection show \
  --resource-group myRG \
  --name s2s-connection \
  --query connectionStatus \
  --output tsv
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/myRG/providers/Microsoft.Network/localNetworkGateways/onprem-lgw",
  "location": "eastus",
  "name": "onprem-lgw",
  "resourceGroup": "myRG",
  "type": "Microsoft.Network/localNetworkGateways"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/myRG/providers/Microsoft.Network/connections/s2s-connection",
  "location": "eastus",
  "name": "s2s-connection",
  "resourceGroup": "myRG",
  "type": "Microsoft.Network/connections",
  "connectionStatus": "Connecting"
}
Connecting
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.Network/virtualNetworkGateways/myVpnGateway' under resource group 'myRG' was not found.`** — Verify the VPN gateway name matches exactly and exists in the same resource group using `az network vnet-gateway list --resource-group myRG`.
    **`InvalidAddressPrefix : The address prefix '192.168.0.0/16' is invalid.`** — Ensure CIDR notation is correct and the prefix length is between /1 and /32.
    **`BadRequest : The shared key must be between 1 and 128 characters and contain only alphanumeric characters and these special characters: @_-.`** — Remove special characters like `!` from the shared key or use only allowed characters.
## Point-to-Site Configuration

P2S allows individual clients to connect to Azure without a VPN device.

```bash
# Configure P2S on the gateway with certificate auth
az network vnet-gateway update \
  --resource-group myRG \
  --name myVpnGateway \
  --address-prefixes 172.16.0.0/24 \
  --client-protocol SSTP OpenVPN \
  --vpn-auth-type Certificate

# Add a root certificate for P2S auth
az network vnet-gateway root-cert create \
  --resource-group myRG \
  --gateway-name myVpnGateway \
  --name MyRootCert \
  --public-cert-data <base64-encoded-cert-data>
```


```text title="Expected output"
{
  "name": "myVpnGateway",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworkGateways/myVpnGateway",
  "type": "Microsoft.Network/virtualNetworkGateways",
  "location": "eastus",
  "properties": {
    "provisioningState": "Updating",
    "vpnType": "RouteBased",
    "enableBgp": false,
    "activeActive": false,
    "vpnClientConfiguration": {
      "vpnClientAddressPool": {
        "addressPrefixes": [
          "172.16.0.0/24"
        ]
      },
      "vpnClientProtocols": [
        "SSTP",
        "OpenVPN"
      ],
      "vpnAuthTypes": [
        "Certificate"
      ]
    }
  }
}
{
  "name": "MyRootCert",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworkGateways/myVpnGateway/vpnClientRootCertificates/MyRootCert",
  "type": "Microsoft.Network/virtualNetworkGateways/vpnClientRootCertificates",
  "properties": {
    "provisioningState": "Succeeded",
    "publicCertData": "MIIDXTCCAkWgAwIBAgIJAKC1/UHHo..."
  }
}
```

!!! warning "Common errors"
    **`The certificate data provided is invalid or malformed.`** — Ensure the certificate is base64-encoded and extracted from a valid .cer or .pem file without line breaks or extra whitespace.
    **`Gateway 'myVpnGateway' not found in resource group 'myRG'.`** — Verify the resource group name and gateway name are correct using `az network vnet-gateway list --resource-group myRG`.
    **`InvalidCertificateFormat: The public certificate data must be in PEM format.`** — Convert the certificate to PEM format using `openssl x509 -inform DER -in cert.cer -out cert.pem` and re-encode to base64.
## BGP Configuration

```bash
# Enable BGP on the gateway with a custom ASN
az network vnet-gateway update \
  --resource-group myRG \
  --name myVpnGateway \
  --asn 65515

# Enable BGP on the local network gateway
az network local-gateway update \
  --resource-group myRG \
  --name onprem-lgw \
  --asn 65001 \
  --bgp-peering-address 192.168.10.254

# Update the VPN connection to use BGP
az network vpn-connection update \
  --resource-group myRG \
  --name s2s-connection \
  --enable-bgp true

# Show BGP peers
az network vnet-gateway list-bgp-peer-status \
  --resource-group myRG \
  --name myVpnGateway \
  --output table
```


```text title="Expected output"
{
  "bgpSettings": {
    "asn": 65515,
    "bgpPeeringAddress": "10.0.0.30",
    "peerWeight": 0
  },
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworkGateways/myVpnGateway",
  "name": "myVpnGateway",
  "provisioningState": "Succeeded"
}
{
  "bgpSettings": {
    "asn": 65001,
    "bgpPeeringAddress": "192.168.10.254"
  },
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/localNetworkGateways/onprem-lgw",
  "name": "onprem-lgw",
  "provisioningState": "Succeeded"
}
{
  "connectionStatus": "Connected",
  "enableBgp": true,
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/connections/s2s-connection",
  "name": "s2s-connection",
  "provisioningState": "Succeeded"
}
Neighbor    ASN    IP              State      ConnectedDuration
----------  -----  ---------------  ---------  -------------------
192.168.10.254  65001  192.168.10.254   Connected  0:15:32
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.Network/virtualNetworkGateways/myVpnGateway' under resource group 'myRG' was not found.`** — Verify the gateway name and resource group exist using `az network vnet-gateway list --resource-group myRG`.
    **`(BadRequest) BGP is not supported for this gateway SKU.`** — Upgrade the VPN gateway to a SKU that supports BGP (Standard, HighPerformance, or VpnGw1 and above) using `az network vnet-gateway update --sku VpnGw1`.
    **`(BadRequest) The BGP peering address 192.168.10.254 is not in the same address space as the local network gateway.`** — Ensure the BGP peering address falls within the address space defined for the local network gateway.
## Active-Active Configuration

Active-active mode uses two public IPs and two BGP sessions to provide higher availability.

```bash
# Create a second public IP for active-active
az network public-ip create \
  --resource-group myRG \
  --name vpn-gw-pip2 \
  --sku Standard \
  --allocation-method Static

# Enable active-active mode
az network vnet-gateway update \
  --resource-group myRG \
  --name myVpnGateway \
  --public-ip-addresses vpn-gw-pip vpn-gw-pip2 \
  --enable-active-active true
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/myRG/providers/Microsoft.Network/publicIPAddresses/vpn-gw-pip2",
  "location": "eastus",
  "name": "vpn-gw-pip2",
  "publicIpAddressVersion": "IPv4",
  "publicIpAllocationMethod": "Static",
  "resourceGroup": "myRG",
  "sku": {
    "name": "Standard",
    "tier": "Regional"
  },
  "ipAddress": "203.0.113.45"
}
{
  "activeActive": true,
  "bgpSettings": {
    "asn": 65515,
    "bgpPeeringAddress": "10.0.0.30",
    "peerWeight": 0
  },
  "enableBgp": false,
  "gatewayType": "Vpn",
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworkGateways/myVpnGateway",
  "name": "myVpnGateway",
  "provisioningState": "Succeeded",
  "publicIpAddresses": [
    "203.0.113.44",
    "203.0.113.45"
  ]
}
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Network/publicIPAddresses/vpn-gw-pip2' under resource group 'myRG' was not found.`** — Verify the resource group name matches and the public IP doesn't already exist in a different RG.
    **`InvalidApiVersionParameter: The api-version '2021-02-01' is not valid for this operation.`** — Update the Azure CLI to the latest version with `az upgrade`.
    **`BadRequest: The gateway 'myVpnGateway' does not support active-active mode with the current SKU.`** — Ensure the VPN gateway uses a HighPerformance, VpnGw2, or higher SKU that supports active-active.
## Monitoring

```bash
# List gateway connections and their states
az network vpn-connection list \
  --resource-group myRG \
  --output table

# Get VPN gateway metrics (tunnel bandwidth)
az monitor metrics list \
  --resource /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.Network/virtualNetworkGateways/myVpnGateway \
  --metric "TunnelIngressBytes" "TunnelEgressBytes" \
  --interval PT5M \
  --aggregation Total \
  --output table
```


```text title="Expected output"
Name                    ResourceGroup    ConnectionType    RoutingWeight    ConnectionStatus
site-to-site-conn-01    myRG             IPSec             10               Connected
site-to-site-conn-02    myRG             IPSec             20               Disconnected
vnet-to-vnet-conn       myRG             Vnet2Vnet         0                Connected
p2s-connection          myRG             ExpressRoute      5                Connected

Timestamp                          TunnelIngressBytes    TunnelEgressBytes
2024-01-15T14:00:00+00:00         1247856               892341
2024-01-15T14:05:00+00:00         1356742               945123
2024-01-15T14:10:00+00:00         1189234               823456
2024-01-15T14:15:00+00:00         1502341               1087654
```

!!! warning "Common errors"
    **`The resource 'Microsoft.Network/virtualNetworkGateways/myVpnGateway' under resource group 'myRG' was not found.`** — Verify the gateway name and resource group name match exactly, and confirm the gateway exists with `az network vnet-gateway list --resource-group myRG`.
    **`Metrics data not available for the specified time range.`** — Extend the time range using `--start-time` and `--end-time` parameters, or wait for metrics to be populated (typically 5–10 minutes after gateway creation).