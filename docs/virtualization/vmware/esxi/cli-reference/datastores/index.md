# Datastores & VMDK

> Part of the [VMware ESXi CLI Reference](../).

---

## Datastores & VMDK

```bash
# Browse datastores
ls /vmfs/volumes/
ls /vmfs/volumes/<datastore>/
du -sh /vmfs/volumes/<datastore>/*

# vmkfstools — disk operations
vmkfstools -l /vmfs/volumes/<ds>/<vm>/<vm>.vmdk
vmkfstools -c 100G -d thin /vmfs/volumes/<ds>/<vm>/<vm>.vmdk
vmkfstools -i source.vmdk dest.vmdk
vmkfstools -X 200G /vmfs/volumes/<ds>/<vm>/<vm>.vmdk
vmkfstools -e /vmfs/volumes/<ds>/<vm>/<vm>.vmdk

# Datastore info via vim-cmd
vim-cmd hostsvc/datastore/listsummary
vim-cmd hostsvc/datastore/info <datastore_name>
```
