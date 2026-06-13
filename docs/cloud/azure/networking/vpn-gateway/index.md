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
```text
┌─────────────────────────────────────── Cloud Azure Networking ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Azure: Cloud Azure Networking platform                            │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                     Management: Cloud Azure Networking management console                     │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Networking infrastructure · management network · monitoring                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Networking platform overview and core concepts                    │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
