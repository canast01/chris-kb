# Hosts & Access

> Part of the Dell Unity CLI Reference (Unisphere CLI).

---

```bash
# Hosts
uemcli -d <ip> /remote/host show
uemcli -d <ip> /remote/host show -detail
uemcli -d <ip> /remote/host create -name <host_name> -type Initiator

# Initiators
uemcli -d <ip> /remote/initiator show
uemcli -d <ip> /remote/initiator create -host <host_id> -uid <wwn_or_iqn> -type FC

# LUN access (host-to-LUN mapping)
uemcli -d <ip> /stor/config/lunacl show
uemcli -d <ip> /stor/config/lunacl create -lun <lun_id> -host <host_id>
uemcli -d <ip> /stor/config/lunacl -id <acl_id> delete
```
