# Disks & Snapshots

> Part of the Azure CLI Reference.

```text
┌──────────────────────────────────────────────────────────┐
│                    Disk CLI Flow                         │
│                                                          │
│  az disk create ──────────────► Managed Disk             │
│                                      │                   │
│  az vm disk attach ─────────────────►│                   │
│  az vm disk detach ◄─────────────────┘                   │
│                                      │                   │
│                                      ▼                   │
│                               ┌──────────────┐           │
│                               │  Azure VM    │           │
│                               └──────────────┘           │
│                                                          │
│  az snapshot create ◄──────── source disk/blob           │
│         │                                                │
│         ▼                                                │
│  ┌────────────────────┐                                  │
│  │   Snapshot         │── az disk create (from snap)     │
│  │  (point-in-time)   │                                  │
│  └────────────────────┘                                  │
└──────────────────────────────────────────────────────────┘
```

---

```bash
# Managed disks
az disk list --resource-group <rg> --output table
az disk show --resource-group <rg> --name <disk>
az disk create --resource-group <rg> --name <disk> --size-gb 128 --sku Premium_LRS
az disk delete --resource-group <rg> --name <disk> --yes

# Attach disk to VM
az vm disk attach --resource-group <rg> --vm-name <vm> --name <disk>
az vm disk detach --resource-group <rg> --vm-name <vm> --name <disk>

# Snapshots
az snapshot list --resource-group <rg> --output table
az snapshot create --resource-group <rg> --name <snap> --source <disk_id>
az snapshot delete --resource-group <rg> --name <snap>
```
