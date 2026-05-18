# vSAN Quick Reference

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       vSAN Health Flow                                  │
│                                                                         │
│  Physical Disks ──► Disk Group ──► vSAN Datastore ──► VM Objects       │
│  (cache + cap)      (per host)     (cluster-wide)      (FTT policy)     │
│                                                                         │
├───────────────────────────────────────────────────────────────────────── │
│  Check Sequence                │  Key Commands                         │
├────────────────────────────────┼───────────────────────────────────────┤
│ 1. Skyline Health (all green?) │ esxcli vsan health cluster list       │
│ 2. Resync active?              │ esxcli vsan debug resync summary get  │
│ 3. Object compliance?          │ vCenter → Cluster → vSAN → Objects   │
│ 4. Disk group up?              │ esxcli vsan storage list              │
│ 5. Network OK between hosts?   │ vmkping -I vmk2 <peer-vsan-vmk-ip>  │
├────────────────────────────────┴───────────────────────────────────────┤
│  Policy: RAID-1 FTT=1 minimum  │  Throttle resync: -p 25 during maint │
└─────────────────────────────────────────────────────────────────────────┘
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

## Ping vSAN VMkernel Between Hosts

```bash
# From ESXi host, ping another host's vSAN VMkernel
vmkping -I vmk2 <target-vsan-vmk-ip>

# Test jumbo frames if MTU is 9000
vmkping -I vmk2 -s 8972 -d <target-vsan-vmk-ip>
```

## Common Issues

| Symptom | First Check |
|---|---|
| Object degraded | Skyline Health → check disk group and host state |
| Resync not completing | Capacity usage, network health, host maintenance state |
| Disk group offline | Physical disk health in iDRAC |
| Network partition | vSAN VMkernel reachability between hosts |
| Capacity warning | Snapshot growth, thin provisioning, stale templates |
