# Network

> Part of the Dell Data Domain CLI Reference.

## Interface Status

```bash
# All interfaces — IP, speed, state
net show all

# Interface configuration (IP, netmask, MTU, bonding)
net show config

# Network settings summary
net show settings

# Interface statistics (rx/tx, errors, drops)
net show stats
```

## Interface Configuration

```bash
# Configure an interface IP
net config eth1 <ip_address> netmask <mask>

# Bring an interface up or down
net enable eth1
net disable eth1
```

## Routing

```bash
# Current routing table
net route show

# Add a host route
net route add host <destination_ip> gateway <gateway_ip> dev <interface>

# Add a network route
net route add net <network_ip> netmask <mask> gateway <gateway_ip>

# Delete a route
net route del host <destination_ip>
```

## DNS

```bash
# Hosts file entries
net hosts show

# Add a static host entry
net config hosts add <ip_address> <hostname>

# DNS server configuration
net show settings | grep -i dns
```

## NTP

```bash
# NTP server list
ntp show

# NTP sync status
ntp status

# Add NTP server
ntp add timeserver <ntp_ip>

# Remove NTP server
ntp del timeserver <ntp_ip>
```

## Ping and Connectivity Testing

```bash
# Ping from Data Domain
net ping <destination_ip>
net ping <destination_ip> count 10

# Traceroute
net traceroute <destination_ip>
```

## Bonding / LACP

```bash
# Show bonding configuration
net config bond show

# Create a bond
net config bond create bond0 <eth1> <eth2> lacp
```

## Firewall

```bash
# Show open ports and firewall rules
net config firewall show
```
