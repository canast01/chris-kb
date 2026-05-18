# iSCSI Targets

An iSCSI target is the storage-side endpoint — a port on an array, NAS gateway, or software target — that presents LUNs to initiators.

```
        iSCSI TARGET STRUCTURE
┌──────────────────────────────────────────────────────────┐
│  Storage Array / Target                                  │
│                                                          │
│  Target IQN: iqn.2020-01.com.purestorage:flasharray-ct0 │
│                                                          │
│  ┌───────────────────────────────────────────────────┐   │
│  │  Target Portal Group (TPG)                        │   │
│  │  ┌─────────────────┐  ┌─────────────────┐         │   │
│  │  │ Portal A        │  │ Portal B        │         │   │
│  │  │ 192.168.10.10   │  │ 192.168.20.10   │         │   │
│  │  │ :3260           │  │ :3260           │         │   │
│  │  └────────┬────────┘  └────────┬────────┘         │   │
│  └───────────┼────────────────────┼───────────────────┘   │
│              │   CHAP auth        │                       │
│              └────────┬───────────┘                       │
│                       │                                   │
│  ┌────────────────────▼──────────────────────────────┐   │
│  │  LUN Mapping (initiator IQN → LUN)                │   │
│  │  iqn.2024-01.com.example:server01 ──► LUN 0 (50G) │   │
│  │  iqn.2024-01.com.example:server02 ──► LUN 1 (100G)│   │
│  └───────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

## Target Address Format

```
iqn.2020-01.com.purestorage:flasharray-m70-ct0   (target IQN)
192.168.10.10:3260                                 (portal — IP:port)
```

TCP port 3260 is the standard iSCSI port.

## Target Portal Groups

A **Target Portal Group (TPG)** is a set of IP addresses (portals) through which a target is reachable. Arrays typically present multiple portals for load distribution and redundancy.

```bash
# Linux — show discovered targets and their portals
iscsiadm -m node -o show

# Show all portal addresses for a discovered target
iscsiadm -m node --targetname <IQN> -o show | grep portal
```

## Discovery Methods

| Method | How it works | Use case |
|---|---|---|
| **SendTargets** | Initiator queries a portal; portal returns all targets | Most common — use for dedicated storage networks |
| **iSNS** | Central iSNS server registers and serves target info | Large environments with many targets |
| **Static** | Targets entered manually | Simple/lab environments |

```bash
# Linux — SendTargets discovery
iscsiadm -m discovery -t sendtargets -p <target-ip>:3260

# Linux — list discovered targets
iscsiadm -m node

# Linux — remove stale target record
iscsiadm -m node -o delete -T <IQN> -p <ip>:3260
```

## Host / Initiator Group Mapping

All storage arrays require the initiator IQN to be registered in a host or initiator group before a LUN is visible:

| Array | Where to configure |
|---|---|
| Pure FlashArray | Storage → Hosts → Add Host (iSCSI IQN) |
| NetApp ONTAP | `igroup create -protocol iscsi -ostype vmware` |
| Dell PowerStore | Hosts → Create Host → iSCSI Initiators |
| Dell Unity | Hosts → Create Host → iSCSI Initiators |

## Verifying Target Connectivity

```bash
# Check target portal is reachable (TCP handshake)
nc -zv <target-ip> 3260

# Discover targets
iscsiadm -m discovery -t sendtargets -p <target-ip>

# Show active sessions to a target
iscsiadm -m session -P 3 | grep -A10 <IQN>
```

## Common Issues

| Symptom | Cause | Action |
|---|---|---|
| No targets returned from discovery | Wrong portal IP or TCP 3260 blocked | `nc -zv <ip> 3260` — check firewall |
| Target visible but LUN not seen | Initiator IQN not in host group | Add IQN to storage host/initiator group |
| Target disappears after reboot | Non-persistent login | Use `iscsiadm -m node -l -o automatic` |
| Multiple targets seen unexpectedly | iSNS or SendTargets returning unrelated targets | Scope discovery to dedicated storage VLAN |
