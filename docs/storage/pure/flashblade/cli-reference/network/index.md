# Network

> Part of the [Pure FlashBlade CLI Reference](../).

## Network Interfaces

```bash
# List all interfaces (data, management, replication)
purefb network-interface show

# Specific interface detail
purefb network-interface show --name <if_name>

# Interface state (connected, disconnected, speed)
purefb network-interface show | grep -E "Name|Speed|State|Address"
```

## Subnets

Subnets define the network layout for data and replication traffic:

```bash
# List subnets
purefb subnet show

# Create a subnet
purefb subnet create \
    --name <subnet_name> \
    --prefix <cidr> \
    --gateway <gateway_ip>

# Delete a subnet
purefb subnet delete --name <subnet_name>
```

## DNS

```bash
# View DNS configuration
purefb dns show

# Update DNS servers
purefb dns update --nameservers <ns1_ip>,<ns2_ip>

# Update search domain
purefb dns update --search <search_domain>
```

## NTP

```bash
# Current NTP configuration and sync status
purefb ntp show

# Set NTP servers
purefb ntp update --ntpservers <ntp1_ip>,<ntp2_ip>
```

## VIPs (Virtual IPs) for NFS/SMB

FlashBlade uses VIPs for client data access. VIPs float between blades for availability:

```bash
# List VIPs
purefb vip show

# Create a VIP (floats across blades for the specified services)
purefb vip create \
    --name <vip_name> \
    --address <vip_ip> \
    --subnet <subnet_name> \
    --services <nfs,smb>
```

## Routing

```bash
# Static routes
purefb static-route show

# Add a static route
purefb static-route create \
    --address <destination_cidr> \
    --gateway <gateway_ip>
```

## Network Troubleshooting

```bash
# Interface errors and statistics
purefb network-interface show --detailed | grep -i error

# Ping from FlashBlade
purefb ping --to <destination_ip>

# DNS resolution test
purefb dns-lookup --name <hostname>
```

## Common Issues

| Issue | Check | Command |
|---|---|---|
| NFS mount fails | VIP exists and reachable? | `purefb vip show` |
| DNS not resolving | DNS servers configured? | `purefb dns show` |
| Interface down | Physical link? | `purefb network-interface show` |
| Replication not connecting | Remote array management IP reachable? | `purefb remote-array show` |
