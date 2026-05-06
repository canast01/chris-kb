# System & Status

> Part of the Dell Unity CLI Reference (Unisphere CLI).

---

```bash
# System info
uemcli -d <ip> /sys/general show -detail
uemcli -d <ip> /sys/time show
uemcli -d <ip> /sys/sw/version show

# Alerts and events
uemcli -d <ip> /prac/alert show
uemcli -d <ip> /event/syslog show

# Licenses
uemcli -d <ip> /sys/lic show

# Support / ESRS
uemcli -d <ip> /sys/esrs show
```
