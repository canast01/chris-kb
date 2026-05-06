# Storage — Aggregates & Disks

> Part of the [NetApp ONTAP CLI Reference](../).

---

## Storage — Aggregates & Disks

```bash
# Aggregates
storage aggregate show
storage aggregate show -state online
storage aggregate show -fields aggr-name,node,size,availsize,usedsize,state
storage aggregate show-space
storage aggregate show-space -aggregate <aggr>
storage aggregate modify -aggregate <aggr> -maxraidsize <n>

# Disks
storage disk show
storage disk show -broken
storage disk show -fields disk,bay,node,container-type,disk-type,rpm,size,position
storage disk unfail -disk <disk>
storage disk assign -disk <disk> -owner <node>
```
