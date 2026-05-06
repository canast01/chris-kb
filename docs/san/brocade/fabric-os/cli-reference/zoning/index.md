# Zoning

> Part of the [Brocade Fabric OS CLI Reference](../).

---

```bash
# View zones
zoneShow
cfgShow
aliShow

# Create alias
alicreate "<alias_name>","<wwn>"
aliadd "<alias_name>","<wwn>"

# Create zone
zonecreate "<zone_name>","<alias1>;<alias2>"
zoneadd "<zone_name>","<alias>"

# Zone config
cfgcreate "<cfg_name>","<zone1>;<zone2>"
cfgadd "<cfg_name>","<zone_name>"
cfgremove "<cfg_name>","<zone_name>"

# Activate / save
cfgenable "<cfg_name>"
cfgsave
cfgdisable

# Transactional save (abort if issues)
cfgtransabort

# Peer zones
zonecreate --peerzone "<zone_name>" -principal "<wwn>" -members "<wwn1>;<wwn2>"
```
