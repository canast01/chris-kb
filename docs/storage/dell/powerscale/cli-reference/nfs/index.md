# NFS Exports

> Part of the Dell PowerScale (Isilon) CLI Reference.

---

```bash
# List exports
isi nfs exports list
isi nfs exports view <export_id>

# Create export
isi nfs exports create /ifs/<path> --clients <ip_or_cidr> --read-write-clients <ip_or_cidr> --root-clients <ip_or_cidr>

# Modify export
isi nfs exports modify <export_id> --addroot-clients <ip>
isi nfs exports modify <export_id> --read-write-clients <ip>

# Delete export
isi nfs exports delete <export_id>

# Reload / check NFS
isi nfs exports check
isi nfs settings global view
isi nfs settings export view
```
