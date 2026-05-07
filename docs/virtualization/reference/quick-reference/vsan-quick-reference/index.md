# vSAN Quick Reference
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
