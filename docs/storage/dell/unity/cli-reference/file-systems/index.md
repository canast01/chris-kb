# File Systems (NAS)

> Part of the Dell Unity CLI Reference (Unisphere CLI).

---

```bash
# NAS servers
uemcli -d <ip> /net/nas/server show
uemcli -d <ip> /net/nas/server show -detail
uemcli -d <ip> /net/nas/server create -name <nas_name> -sp <sp_id> -pool <pool_id>

# File systems
uemcli -d <ip> /stor/config/fs show
uemcli -d <ip> /stor/config/fs show -detail
uemcli -d <ip> /stor/config/fs create -name <fs_name> -nasServer <nas_id> -pool <pool_id> -size 1T
uemcli -d <ip> /stor/config/fs -id <fs_id> set -size 2T
uemcli -d <ip> /stor/config/fs -id <fs_id> delete

# NFS shares
uemcli -d <ip> /stor/config/nfs show
uemcli -d <ip> /stor/config/nfs create -fs <fs_id> -path / -nfsVersion NFSv3
uemcli -d <ip> /stor/config/nfs -id <nfs_id> set -hostAccess "<ip>(rw)"
uemcli -d <ip> /stor/config/nfs -id <nfs_id> delete

# CIFS shares
uemcli -d <ip> /stor/config/cifs show
uemcli -d <ip> /stor/config/cifs create -name <share_name> -fs <fs_id> -path /
uemcli -d <ip> /stor/config/cifs -id <cifs_id> delete
```
