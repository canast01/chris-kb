---
tags:
  - azure
---
# Disks & Snapshots

<div class="kb-summary">
Azure disks CLI: `az disk create/resize`, `az snapshot create`, `az disk grant-access`, `az disk revoke-access`, and managed disk SKU conversion commands.

*Applies to: Azure*
</div>

> Part of the Azure CLI Reference.

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

## See also

- [Azure CLI Reference](../index.md)
- [Azure Storage](../../storage/index.md)
- [Azure Compute](../../compute/index.md)
