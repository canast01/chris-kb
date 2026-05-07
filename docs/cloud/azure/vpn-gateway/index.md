# VPN Gateway

Azure VPN Gateway — site-to-site VPN, point-to-site VPN, and VNet-to-VNet connectivity.
## Connection Types

| Type | Use Case |
|---|---|
| Site-to-Site (S2S) | On-premises network → Azure VNet via IPsec/IKE |
| Point-to-Site (P2S) | Individual client → Azure VNet (remote access) |
| VNet-to-VNet | Azure VNet → Azure VNet in same or different regions |
| ExpressRoute co-existence | VPN as failover for ExpressRoute |

## Common Azure CLI Commands

```bash
# List VPN gateways
az network vnet-gateway list -g <rg> \
  --query '[*].{Name:name,SKU:sku.name,VPN:vpnType,BGP:enableBgp,State:provisioningState}' -o table

# List VPN connections
az network vpn-connection list -g <rg> \
  --query '[*].{Name:name,State:connectionStatus,SharedKey:sharedKey,Protocol:ipsecPolicies}' -o table

# Check connection status
az network vpn-connection show -g <rg> -n <connection-name> \
  --query '{State:connectionStatus,IngressBytes:ingressBytesTransferred,EgressBytes:egressBytesTransferred}'

# Reset gateway (clears stuck tunnels)
az network vnet-gateway reset -g <rg> -n <gateway-name>

# Reset a specific connection
az network vpn-connection reset -g <rg> -n <connection-name>
```

## Create S2S VPN Connection

```bash
# 1. Create Local Network Gateway (represents on-premises)
az network local-gateway create -g <rg> -n <lgw-name> \
  --gateway-ip-address <on-prem-public-ip> \
  --local-address-prefixes 10.0.0.0/8

# 2. Create VPN Connection
az network vpn-connection create -g <rg> -n <conn-name> \
  --vnet-gateway1 <azure-gw-name> \
  --local-gateway2 <lgw-name> \
  --shared-key <pre-shared-key> \
  --connection-type IPsec
```

## IKE / IPsec Policy

```bash
# Set custom IKE/IPsec policy on a connection
az network vpn-connection ipsec-policy add -g <rg> \
  --connection-name <conn-name> \
  --ike-encryption AES256 \
  --ike-integrity SHA256 \
  --dh-group DHGroup14 \
  --ipsec-encryption AES256 \
  --ipsec-integrity SHA256 \
  --pfs-group PFS2048 \
  --sa-lifetime 3600 \
  --sa-max-size 102400000
```

## Diagnostic Logs

```bash
# Enable gateway diagnostic logging
az monitor diagnostic-settings create \
  --name vpn-diag \
  --resource <gateway-resource-id> \
  --logs '[{"category":"GatewayDiagnosticLog","enabled":true},{"category":"TunnelDiagnosticLog","enabled":true}]' \
  --workspace <log-analytics-workspace-id>
```

**KQL — check tunnel events:**
```kql
AzureDiagnostics
| where Category == "TunnelDiagnosticLog"
| project TimeGenerated, operationName_s, status_s, remoteIP_s, message_s
| sort by TimeGenerated desc
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Tunnel stuck at Connecting | IKE phase 1 mismatch | Verify encryption/auth/DH group matches on both sides |
| Tunnel connected but no traffic | Routing / firewall | Check routes exist on both sides; check on-prem firewall allows VPN subnet |
| Intermittent drops | Dead peer detection | Ensure on-prem device sends DPD keepalives |
| High latency through tunnel | Gateway SKU | Upgrade gateway SKU; check bandwidth limit |
| P2S clients can't resolve DNS | DNS settings | Add Azure DNS resolver IP (168.63.129.16) to P2S DNS config |
