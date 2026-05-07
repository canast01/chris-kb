# VPN Gateway

Azure VPN Gateway provides encrypted connectivity between Azure VNets and on-premises networks over IPsec/IKE tunnels. It supports site-to-site (S2S), point-to-site (P2S), and VNet-to-VNet connections. For production use, deploy zone-redundant SKUs and enable active-active mode.

## VPN Gateway SKUs

| SKU          | Throughput  | Tunnels | BGP | Zone-Redundant | Notes                  |
|--------------|-------------|---------|-----|----------------|------------------------|
| Basic        | 100 Mbps    | 10      | No  | No             | Dev/test only          |
| VpnGw1       | 650 Mbps    | 30      | Yes | No             | Production entry       |
| VpnGw2       | 1 Gbps      | 30      | Yes | No             | Standard production    |
| VpnGw3       | 1.25 Gbps   | 30      | Yes | No             | High throughput        |
| VpnGw1AZ     | 650 Mbps    | 30      | Yes | Yes            | Zone-redundant         |
| VpnGw2AZ     | 1 Gbps      | 30      | Yes | Yes            | Zone-redundant         |

## Creating a VPN Gateway

```bash
# Create a GatewaySubnet (must be named GatewaySubnet)
az network vnet subnet create \
  --resource-group myRG \
  --vnet-name myVNet \
  --name GatewaySubnet \
  --address-prefix 10.0.255.0/27

# Create a public IP for the gateway
az network public-ip create \
  --resource-group myRG \
  --name vpn-gw-pip \
  --sku Standard \
  --allocation-method Static \
  --zone 1 2 3

# Create the VPN Gateway (this takes 20-45 minutes)
az network vnet-gateway create \
  --resource-group myRG \
  --name myVpnGateway \
  --vnet myVNet \
  --gateway-type Vpn \
  --vpn-type RouteBased \
  --sku VpnGw2AZ \
  --public-ip-address vpn-gw-pip \
  --location eastus
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
