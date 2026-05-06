# Firmware & Configuration

> Part of the [Cisco MDS NX-OS CLI Reference](../).

---

```bash
# Firmware
show version
show install all status
install all kickstart <url> system <url>

# Config backup
copy running-config startup-config
copy running-config tftp://<server>/<filename>
copy tftp://<server>/<filename> running-config

# Show full config
show running-config
show startup-config
```
