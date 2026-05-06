# NSX-T CLI Reference

Commonly used NSX-T Manager and Edge CLI commands for managing overlays, routing, and distributed firewall.

> NSX Manager and Edge Node CLIs are accessed via SSH. Log in as `admin`.

---

## NSX Manager — System

```bash
# System status
get managers
get clusters
get services
get service http
get service manager

# Version
get version

# Nodes
get nodes
get node interfaces
get node interface eth0

# Appliance management
set appliance gw-route <prefix> <gw>
set appliance ui <start|stop>
```

---

## Transport Nodes & Fabric

```bash
# Transport nodes
get transport-nodes
get transport-node <id>
get transport-node <id> status

# Host node connectivity
get transport-zone
get transport-zone <name>

# Tunnel endpoints
get tunnel endpoints
get tunnel status
```

---

## Logical Switches & Segments

```bash
# Segments (NSX-T)
get logical-switches
get logical-switch <id>
get logical-switch <id> status
get logical-switch <id> stats

# Ports
get logical-ports
get logical-port <id>
get logical-port <id> status
```

---

## Tier-0 and Tier-1 Gateways

```bash
# List gateways (NSX Manager)
get logical-routers

# On an Edge Node — enter router context
vrf <logical-router-id>

# Show routes
get route
get route detail
get bgp neighbor summary
get bgp neighbor <neighbor_ip>
get bgp neighbor <neighbor_ip> routes

# Forwarding table
get forwarding

# Interfaces
get interfaces
get interface <name>
```

---

## Edge Nodes

```bash
# Connect to Edge Node via SSH (admin)
get services
get service dataplane
get service router

# System
get node
get node cpu-usage
get node memory

# Uplinks
get interfaces
get interface fp-eth0

# Routing
vrf <lr_id>
get route
get forwarding
get bgp neighbor summary

# Connectivity tests
ping <ip>
traceroute <ip>
curl http://<ip>
```

---

## Distributed Firewall (DFW) — NSX Manager

```bash
# DFW rules overview (via NSX Manager shell)
nsxcli
get firewall stats
get dfw stats

# From ESXi host — inspect DFW
summarize-dvfilter
vsipioctl getrules -f <filter_name>
vsipioctl getaddrsets -f <filter_name>
vsipioctl getstats -f <filter_name>
```

---

## NAT & Load Balancing

```bash
# NAT rules on Edge
vrf <lr_id>
get nat rules

# Load balancer
get load-balancer status
get load-balancer virtual-servers
get load-balancer pools
```

---

## Diagnostics & Troubleshooting

```bash
# Central CLI (run from NSX Manager against any node)
nsxcli -u admin

# Traceflow (Manager UI / API primarily, CLI helper)
get traceflows

# Packet capture on Edge
debug packet capture interface fp-eth0 count 500
debug packet capture interface nsx-geneve count 500

# Log levels
set service manager logging-level debug
set service manager logging-level info

# System logs
get logs
get log manager follow
```

---

## IPAM / IP Pools

```bash
get ip-pools
get ip-pool <id>
get ip-pool <id> allocations
```

---

## Certificates

```bash
get certificates
get certificate <id>
get trust-objects
```

---

## Backup & Restore

```bash
get backup status
set backup schedule daily time 02:00
backup manual
get backup history
```
