# Datastore Inventory

> Part of the [Inventory](../) reference.

---

## Overview

Track all datastores presented to the vSphere environment. Update this inventory after any datastore creation, expansion, removal, or re-presentation event.

## Datastore Inventory Table

| Datastore Name | Type | Capacity (TB) | Free (TB) | % Used | Hosts Mounted | Backing Array | Protocol | VMFS Version | Notes |
|---|---|---|---|---|---|---|---|---|---|
| ds-prod-powermax-fc-01 | VMFS | 20 | 8 | 60% | All prod compute hosts | Dell PowerMax 2500 | FC | VMFS 6 | General production VMs |
| ds-prod-powermax-fc-02 | VMFS | 20 | 5 | 75% | All prod compute hosts | Dell PowerMax 2500 | FC | VMFS 6 | General production VMs |
| ds-prod-flasharray-fc-01 | VMFS | 10 | 6 | 40% | All prod compute hosts | Pure FlashArray //XL | FC | VMFS 6 | Latency-sensitive workloads |
| vsanDatastore | vSAN | 46 | 22 | 52% | cl-prod-compute-01 | vSAN (internal) | vSAN | — | Production vSAN cluster |
| ds-nfs-netapp-01 | NFS | 50 | 30 | 40% | All prod + mgmt hosts | NetApp AFF A400 | NFS v3 | — | ISOs, templates, backups |

## Fields Reference

| Field | Description |
|---|---|
| Datastore Name | Follows naming standard: `<site>-<storage>-<protocol>-<##>` |
| Type | VMFS, vSAN, NFS, vVols |
| Capacity (TB) | Total provisioned size |
| Free (TB) | Available space at last check |
| % Used | Utilisation percentage |
| Hosts Mounted | Which hosts or clusters have the datastore mounted |
| Backing Array | Storage array providing the LUN or NFS export |
| Protocol | FC, iSCSI, NFS v3, NFS v4.1, vSAN |
| VMFS Version | VMFS 5 or VMFS 6 (not applicable for NFS/vSAN) |
| Notes | Owner, usage, any capacity warnings or exceptions |

## Capacity Thresholds

| Threshold | Action |
|---|---|
| > 70% used | Monitor closely — plan expansion or VM migration |
| > 80% used | Alert raised — schedule expansion within 2 weeks |
| > 90% used | Critical — immediate action required to free space or expand |

## Datastore Checklist

When presenting a new datastore:

- [ ] Datastore name follows the naming standard
- [ ] LUN or NFS export is zoned/routed correctly and only to intended hosts
- [ ] VMFS 6 used for all new block datastores
- [ ] Datastore mounted to all required hosts (not just one)
- [ ] Storage policy or tag applied to identify backing tier
- [ ] Datastore added to monitoring capacity alerting
- [ ] Inventory updated
