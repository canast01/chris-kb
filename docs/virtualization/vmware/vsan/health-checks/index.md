# vSAN Health and Object Compliance
## vSAN Skyline Health

Access via vCenter → **Host and Clusters** → Select cluster → **vSAN** → **Skyline Health**

Review all health categories:
- Network
- Physical disk
- Data
- Cluster
- Hardware compatibility

## Disk Group Health

- Confirm all disk groups show as Healthy
- Check for any degraded or absent disk groups
- Review individual disk status — confirm no failed or at-risk disks

## Object Health

Access via **vSAN** → **Virtual Objects**

- Confirm all objects show as Healthy or Compliant
- Investigate any objects showing Degraded, Non-compliant, or Absent

## Storage Policy Compliance

- Objects should meet their assigned storage policy
- Non-compliant objects may indicate insufficient capacity or a disk failure

## Resync Status

- Active resyncs are normal after failures or maintenance
- Monitor resync progress — extended resyncs can indicate capacity or performance issues
- Avoid taking additional hosts into maintenance while resync is active

## Capacity Usage

- Recommended: keep usable vSAN capacity below 70%
- Review thin-provisioned disk growth
- Remove stale snapshots that consume vSAN space

## Network Health

- Confirm vSAN VMkernel adapters are active on all hosts
- Confirm vSAN traffic is on the correct VLAN
- Test connectivity between hosts using vmkping if network health shows errors

## Common Causes of Degraded Objects

- Host placed into maintenance mode without full migration
- Disk failure
- Network partition
- Insufficient capacity to meet FTT policy
- Stretched cluster site issue

## When to Open a VMware Support Case

- Degraded objects that do not recover after the host returns
- Disk group failure with no clear hardware cause
- Skyline Health showing persistent errors after corrective actions
- vSAN objects stuck in resync for extended periods
