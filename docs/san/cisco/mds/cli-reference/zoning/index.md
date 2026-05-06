# Zoning

> Part of the [Cisco MDS NX-OS CLI Reference](../).

---

```bash
# View zoning
show zone
show zone vsan <id>
show zone active vsan <id>
show zoneset
show zoneset active vsan <id>
show zoneset active vsan <id> | grep <wwn>
show zone member vsan <id>

# Create zone / alias
zone name <zone_name> vsan <id>
  member pwwn <wwn>
  member device-alias <alias>

# Device aliases
show device-alias database
device-alias database
  device-alias name <alias> pwwn <wwn>
device-alias commit

# Zoneset
zoneset name <zoneset_name> vsan <id>
  member <zone_name>

# Activate
zoneset activate name <zoneset_name> vsan <id>

# Save
copy running-config startup-config
```
