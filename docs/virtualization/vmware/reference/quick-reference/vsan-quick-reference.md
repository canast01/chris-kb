---
tags:
  - reference
  - vsan
  - vsphere-8
---
# vSAN Quick Reference

<div class="kb-summary">
vSAN Quick Reference reference covering Fast Health Checks, Common Commands, Ping vSAN VMkernel Between Hosts, Common Issues.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

fast_health_checks: "Fast Health Checks" {shape: rectangle}
common_commands: "Common Commands" {shape: rectangle}
ping_vsan_vmkernel_between_hosts: "Ping vSAN VMkernel Between Hosts" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}

fast_health_checks -> common_commands: uses
common_commands -> ping_vsan_vmkernel_between_hosts: uses
ping_vsan_vmkernel_between_hosts -> common_issues: uses
```

## Fast Health Checks

- vSAN Skyline Health → vCenter → Cluster → vSAN → Skyline Health
- Object Health → vCenter → Cluster → vSAN → Virtual Objects
- Resync Status → vCenter → Cluster → vSAN → Resyncing Components

## Common Commands

```bash
# Check vSAN cluster info
esxcli vsan cluster get

# Check vSAN network configuration
esxcli vsan network list

# Check vSAN disks
esxcli vsan storage list

# Check vSAN resync summary
esxcli vsan debug resync summary get
```


```text title="Expected output"
Cluster UUID                : 52d4a8f0-1234-5678-abcd-ef1234567890
Cluster Dominance           : 1
Node UUID                   : a1b2c3d4-5678-90ab-cdef-1234567890ab
Subcluster Master           : true
Current Master              : a1b2c3d4-5678-90ab-cdef-1234567890ab
Cluster Size                : 3
Health State                : healthy

Interface vmk0              : 192.168.1.100
Interface vmk1              : 192.168.1.101
Multicast Address           : 224.1.1.1
Multicast Port              : 23451
Network Mode                : unicast

Disk Group 0
   Physical Disk 0          : naa.5001405a1b2c3d4e
   Physical Disk 1          : naa.5001405a1b2c3d4f
Disk Group 1
   Physical Disk 0          : naa.5001405a1b2c3d50

Resync Objects              : 12
Resync Data (MB)            : 2048
Estimated Time (seconds)    : 180
```

!!! warning "Common errors"
    **`vsan cluster get: Unknown command or namespace`** — Ensure vSAN is licensed and enabled on the cluster; run `esxcli vsan cluster list` to verify vSAN is active.
    **`Error: Unable to connect to vSAN cluster`** — Verify the ESXi host is part of a vSAN cluster and network connectivity exists between cluster nodes on the vSAN network.
    **`Permission denied`** — Run the command as root or with appropriate vSAN administrator privileges on the ESXi host.
## Ping vSAN VMkernel Between Hosts

```bash
# From ESXi host, ping another host's vSAN VMkernel
vmkping -I vmk2 <target-vsan-vmk-ip>

# Test jumbo frames if MTU is 9000
vmkping -I vmk2 -s 8972 -d <target-vsan-vmk-ip>
```


```text title="Expected output"
PING 192.168.100.45 (192.168.100.45): 56 data bytes
64 bytes from 192.168.100.45: icmp_seq=0 ttl=64 time=0.542 ms
64 bytes from 192.168.100.45: icmp_seq=1 ttl=64 time=0.518 ms
64 bytes from 192.168.100.45: icmp_seq=2 ttl=64 time=0.531 ms
64 bytes from 192.168.100.45: icmp_seq=3 ttl=64 time=0.525 ms
--- 192.168.100.45 statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 0.518/0.529/0.542 ms

PING 192.168.100.45 (192.168.100.45): 8972 data bytes
8972 bytes from 192.168.100.45: icmp_seq=0 ttl=64 time=1.203 ms
8972 bytes from 192.168.100.45: icmp_seq=1 ttl=64 time=1.187 ms
8972 bytes from 192.168.100.45: icmp_seq=2 ttl=64 time=1.195 ms
--- 192.168.100.45 statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
```

!!! warning "Common errors"
    **`Unknown interface vmk2`** — Verify the correct VMkernel interface name with `esxcli network ip interface list` and use the correct interface (e.g., vmk1, vmk3).
    **`100% packet loss`** — Check that the target vSAN VMkernel IP is reachable and that vSAN network connectivity is established between hosts.
    **`Packet size too large for link MTU`** — Reduce the packet size with `-s` flag or verify that jumbo frames (MTU 9000) are configured on both the ESXi host and physical switch.
## Common Issues

| Symptom | First Check |
|---|---|
| Object degraded | Skyline Health → check disk group and host state |
| Resync not completing | Capacity usage, network health, host maintenance state |
| Disk group offline | Physical disk health in iDRAC |
| Network partition | vSAN VMkernel reachability between hosts |
| Capacity warning | Snapshot growth, thin provisioning, stale templates |
