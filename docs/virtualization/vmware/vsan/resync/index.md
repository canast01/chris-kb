# vSAN Resync and Object Health Troubleshooting

## Checking Resync Status

```bash
# From an ESXi host in the cluster
esxcli vsan debug resync summary get
```

Or in vCenter: **vSAN** → **Skyline Health** → **Data** → **vSAN Object Health**

## Understanding Resync Types

| Type | Meaning |
|---|---|
| Repair | Rebuilding a component after a failure |
| Rebalance | Redistributing data after capacity or host changes |
| Evacuation | Migrating data for maintenance mode |
| Policy change | Applying a new storage policy |

## When Resync Is Expected

- Host just returned from maintenance mode
- Disk replacement completed
- Capacity added to the cluster
- Storage policy changed on VMs

## When Resync Is Concerning

- Resync active for more than 24 hours without progress
- Object health showing Degraded with no active resync
- Resync blocked due to capacity or network issues

## Checking Object Health

In vCenter: **vSAN** → **Virtual Objects**

- Filter by health status — investigate Degraded, Non-compliant, or Absent objects
- Note the VM name, object type, and storage policy

## Common Causes of Degraded Objects

- Host removed from cluster without full evacuation
- Disk group failure
- Network partition between hosts
- Capacity too low to meet the FTT policy

## Support Bundle Collection

If resync or object issues do not resolve after the expected timeframe:

1. Collect a vSAN support bundle from the vCenter support bundle tool
2. Include ESXi host logs from affected nodes
3. Open a VMware support case with the bundle and a timeline of events
