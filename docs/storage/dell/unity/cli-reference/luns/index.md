# LUNs

> Part of the Dell Unity CLI Reference (Unisphere CLI).

---

```bash
# List LUNs
uemcli -d <ip> /stor/config/lun show
uemcli -d <ip> /stor/config/lun show -detail

# Create LUN
uemcli -d <ip> /stor/config/lun create -name <lun_name> -pool <pool_id> -size 100G

# Modify LUN
uemcli -d <ip> /stor/config/lun -id <lun_id> set -size 200G
uemcli -d <ip> /stor/config/lun -id <lun_id> set -name <new_name>

# Delete LUN
uemcli -d <ip> /stor/config/lun -id <lun_id> delete

# LUN snapshots
uemcli -d <ip> /prot/snap show -res <lun_id>
uemcli -d <ip> /prot/snap create -name <snap_name> -res <lun_id>
uemcli -d <ip> /prot/snap -id <snap_id> delete
uemcli -d <ip> /prot/snap -id <snap_id> restore
```
