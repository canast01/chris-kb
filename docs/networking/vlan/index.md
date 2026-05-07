# VLANs

VLANs segment network traffic into logical broadcast domains. In an enterprise infrastructure, separate VLANs are standard practice for management, storage (iSCSI, NFS), replication, vMotion, backup, SAN, and production traffic.

## View VLANs (Cisco IOS/NX-OS)

```bash
show vlan brief
show vlan id <id>
show interfaces trunk
show interface <int> status
```

## Create a VLAN

```bash
vlan <id>
  name <vlan_name>
```

## Assign a Port to a VLAN (Access Port)

```bash
interface <int>
  switchport mode access
  switchport access vlan <id>
```

## Configure a Trunk Port

```bash
interface <int>
  switchport mode trunk
  switchport trunk allowed vlan <id1>,<id2>
  switchport trunk native vlan <native_id>
```

## Add / Remove VLANs on a Trunk

```bash
switchport trunk allowed vlan add <id>
switchport trunk allowed vlan remove <id>
```

## VLAN Validation

After creating or modifying VLANs:

```bash
# Confirm VLAN exists
show vlan brief | include <id>

# Confirm port is in correct VLAN
show interface <int> status

# Confirm VLAN crosses trunk
show interfaces trunk | include <id>

# End-to-end test
ping <ip_on_same_vlan>
```

## Common VLAN Use Cases

| VLAN | Traffic Type | Notes |
|---|---|---|
| Management | OOB switch/server management | Strictly controlled access |
| Storage | iSCSI, NFS | Jumbo frames (MTU 9000) required |
| vMotion | VMware live migration | Dedicated, no other traffic |
| Replication | SRDF, SnapMirror, vSphere replication | May share with storage |
| Backup | Backup agents and media servers | High-bandwidth bursts |
| Production | Application traffic | Standard MTU (1500) |

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Host unreachable | VLAN on trunk? | `show interfaces trunk` |
| VLAN not in FLOGI / iSCSI | Wrong VLAN on port | Check access or trunk assignment |
| Native VLAN mismatch | CDP/LLDP log | Match native VLAN on both trunk ends |
| VLAN not propagated | VTP or manual config | Check VTP domain or add VLAN manually |
