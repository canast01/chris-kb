# Diagnostics & Troubleshooting

> Part of the [NSX-T CLI Reference](../).

## Central CLI (NSX Manager)

```bash
# Connect to NSX Manager via SSH then enter nsxcli
nsxcli

# Or run a single command without interactive mode
nsxcli -c "get managers"
```

## Traceflow

Traceflow injects a probe packet to trace its path through the logical network.

```bash
# List active traceflows
get traceflows

# Traceflow is primarily launched from NSX Manager UI:
# Plan & Troubleshoot → Traceflow
# Or via API: POST /api/v1/traceflows
```

## Packet Capture on Edge Node

SSH to the Edge node, then:

```bash
# Capture on uplink (physical interface)
debug packet capture interface fp-eth0 count 500

# Capture on Geneve overlay interface
debug packet capture interface nsx-geneve count 500

# Capture with filter (BPF syntax)
debug packet capture interface fp-eth0 filter "host 10.0.0.1" count 200

# Write to file for Wireshark analysis
debug packet capture interface fp-eth0 file /tmp/cap.pcap count 1000
```

## Log Management

```bash
# View recent logs
get logs

# Follow logs in real time
get log manager follow

# Set log level (Edge or Manager node)
set service manager logging-level debug
set service manager logging-level info      # reset after troubleshooting

# NSX log file locations (SSH to node)
ls /var/log/vmware/nsx-*/
tail -f /var/log/vmware/nsx-manager/manager.log
tail -f /var/log/vmware/nsx-edge/edge.log
```

## Connectivity Tests

```bash
# Ping from NSX Manager node
vrf <lr_id>
ping <destination_ip>
ping <destination_ip> repeat 100 size 1400

# Traceroute through overlay
traceroute <destination_ip>

# Test DNS resolution from Edge
nslookup <hostname>
```

## BGP and Routing Diagnostics

```bash
# Check BGP session state (run on Edge in gateway VRF)
vrf <lr_id>
get bgp neighbor summary

# BGP route counts per neighbor
get bgp neighbor <neighbor_ip>

# Advertised routes to a peer
get bgp neighbor <neighbor_ip> advertised-routes

# Received routes from a peer
get bgp neighbor <neighbor_ip> routes

# Full forwarding table
get forwarding

# Check for route to a specific prefix
get route <prefix>/<mask>
```

## Health and Cluster Status

```bash
# NSX Manager cluster health
get managers
get clusters
get cluster status

# Corfu DB (control plane) status
get corfu-cluster status

# Individual service status
get service manager
get service http
get service controller

# Transport node connectivity
get transport-nodes
get transport-node-status
```

## Common Diagnostic Scenarios

| Symptom | Commands |
|---|---|
| VM can't reach gateway | `vsipioctl getrules` on source ESXi host — check DFW drop |
| BGP session down | `vrf <id>` → `get bgp neighbor summary` on Edge |
| Tunnel flapping | `get tunnel status` — check underlay MTU (needs ≥ 1600 for Geneve) |
| Segment not reachable | `get logical-switch <id> status` — check replication mode |
| High CPU on Edge | `get service dataplane stats` — check connection table |
| Manager UI unreachable | `get service http` + `get cluster status` on Manager node |
