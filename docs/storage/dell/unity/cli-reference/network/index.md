# Network Interfaces

> Part of the Dell Unity CLI Reference (Unisphere CLI).

---

```bash
# Interfaces
uemcli -d <ip> /net/if show
uemcli -d <ip> /net/if show -detail

# Create iSCSI interface
uemcli -d <ip> /net/if create -type iSCSI -ipv4 <ip> -netmask <mask> -gateway <gw> -sp <sp_id> -port <port_id>

# iSCSI portals
uemcli -d <ip> /net/iscsi/node show
```
