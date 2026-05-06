# NFS & CIFS/SMB

> Part of the Dell Data Domain CLI Reference.

---

## NFS

```bash
nfs show exports
nfs add export /data/col1/<mtree> clients <ip_or_cidr>
nfs del export /data/col1/<mtree> clients <ip_or_cidr>
nfs show clients
nfs status
```

## CIFS / SMB

```bash
cifs show
cifs show clients
cifs share show
cifs share add /data/col1/<mtree>
cifs share del /data/col1/<mtree>
```
