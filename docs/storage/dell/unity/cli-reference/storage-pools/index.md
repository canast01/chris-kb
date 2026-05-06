# Storage Pools

> Part of the Dell Unity CLI Reference (Unisphere CLI).

---

```bash
# List pools
uemcli -d <ip> /stor/config/pool show
uemcli -d <ip> /stor/config/pool show -detail

# Create pool (RAID5 example)
uemcli -d <ip> /stor/config/pool create -name <pool_name> -diskGroup <dg_id> -raidType RAID5

# Modify pool
uemcli -d <ip> /stor/config/pool -id <pool_id> set -name <new_name>

# Delete pool
uemcli -d <ip> /stor/config/pool -id <pool_id> delete
```
