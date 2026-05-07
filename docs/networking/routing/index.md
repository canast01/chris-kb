# Routing

## Overview

Routing determines how traffic moves between subnets. All storage replication, backup traffic, vMotion, and cloud connectivity depend on correct routing.

## View Route Table

**Linux:**
```bash
ip route show
ip route get <destination_ip>    # show which route would be used
```

**Windows:**
```cmd
route print
```

**Cisco IOS / NX-OS:**
```bash
show ip route
show ip route <destination>
show ip route summary
```

## Default Gateway

```bash
# Linux — confirm default route
ip route show default

# Windows
route print 0.0.0.0
```

## OSPF

```bash
# Check OSPF neighbor state
show ip ospf neighbor

# Verify OSPF routes
show ip route ospf

# OSPF interface status
show ip ospf interface brief
```

All OSPF neighbors should be in `FULL` state. `EXSTART`, `EXCHANGE`, or stuck `2WAY` indicates an adjacency issue.

## BGP

```bash
# BGP summary (neighbor states)
show bgp summary
show bgp neighbors <ip>

# BGP routes
show bgp
show bgp routes
```

## Static Routes

```bash
# Linux — add a static route
ip route add <network>/<prefix> via <gateway>

# Persist (add to /etc/network/interfaces or nmcli)
nmcli connection modify <conn> +ipv4.routes "<network>/<prefix> <gateway>"
```

## Path Tracing

```bash
traceroute <destination>    # Linux
tracert <destination>       # Windows
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| No route to host | `ip route get <dest>` | Add missing static route or fix OSPF |
| OSPF neighbor stuck | MTU mismatch or auth | Match MTU and OSPF auth config |
| Default gateway unreachable | Physical link and ARP | Check interface and ARP table |
| Asymmetric routing | `traceroute` both directions | Review route policy |
