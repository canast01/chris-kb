# Transport Nodes & Fabric

> Part of the [NSX-T CLI Reference](../).

## Transport Nodes (NSX Manager CLI)

```bash
nsxcli

# List all transport nodes (ESXi hosts + Edge nodes)
get transport-nodes

# Detail for a specific transport node
get transport-node <id>

# Operational status (UP/DOWN/DEGRADED)
get transport-node <id> status

# Summary status for all nodes
get transport-node-status
```

## Transport Zones

```bash
# List transport zones (overlay and VLAN backed)
get transport-zone

# Detail for a specific zone
get transport-zone <name>

# Which transport nodes are in a zone
get transport-nodes | grep <zone_name>
```

## Tunnel Endpoints (TEPs)

```bash
# List all TEP IPs and associated hosts
get tunnel endpoints

# Tunnel status between all TEP pairs
get tunnel status

# Tunnel to a specific remote TEP
get tunnel status <remote_tep_ip>
```

## ESXi Host Fabric Verification

SSH to the ESXi host:

```bash
# NSX VIBs installed
esxcli software vib list | grep -i nsx

# VDS and NSX Port ID mapping
net-vdl2 -M all -s 0

# TEP VMkernel IP and state
esxcli network ip interface ipv4 get | grep -A2 vmk

# TEP uplink binding
esxcli network ip interface list | grep -i nsx
```

## Edge Node Fabric Status

SSH to Edge node:

```bash
# Edge interfaces (uplinks + overlay)
get interfaces

# Geneve overlay interface
get interface nsx-geneve

# Uplink state
get interface fp-eth0
get interface fp-eth1
```

## Common Issues

| Symptom | Check |
|---|---|
| Transport node status DEGRADED | `get transport-node <id> status` — check VIB version mismatch |
| Tunnel DOWN between two hosts | `get tunnel status` — check TEP IP reachability and MTU ≥ 1600 |
| ESXi host not joining fabric | `esxcli software vib list | grep nsx` — VIB may have failed install |
| BFD session flapping | Underlay MTU or path instability — check physical switch |
| Segment VMs can't communicate | `get logical-switch <id> status` + `get tunnel status` between both host TEPs |

## Maintenance Mode Workflow

```bash
# Before putting ESXi host in maintenance mode:
# 1. Check no active vSAN resync
esxcli vsan debug resync list

# 2. Verify NSX DFW is not the sole enforcement point for a segment
nsxcli
get transport-node <id> status

# 3. After host in maintenance mode — confirm tunnels reconverged
get tunnel status
```
