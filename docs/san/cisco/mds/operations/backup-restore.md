---
tags:
  - operations
  - san
---
# Cisco MDS 9000 — Backup and Restore

*Applies to: Cisco MDS / NX-OS*
![Cisco MDS 9000 — Backup and Restore](../../../../assets/san-cisco-mds-operations-backup-restore.svg)

```bash
# Save running to startup config
copy running-config startup-config

# Copy running config off-switch via SCP
copy running-config scp://<user>@<server>/<path>/<filename>

# Copy running config off-switch via TFTP
copy running-config tftp://<server>/<filename>

# Display full running config (for manual capture)
show running-config
```


```text title="Expected output"
Source filename [running-config]? 
Destination filename [startup-config]? 
[######################] 100%
Copy complete.

Source filename [running-config]? 
Address or name of remote host [<server>]? 192.168.1.50
Destination filename [/backups/mds9148_config.txt]? 
Password: 
[######################] 100%
1547 bytes copied in 2.341 secs (661 bytes/sec)

Source filename [running-config]? 
Address or name of remote host [192.168.1.45]? 
Destination filename [mds_tftp_backup.cfg]? 
[######################] 100%
1547 bytes copied in 1.892 secs (818 bytes/sec)

version 9.1(1)
feature telnet
feature ssh
interface fc1/1
  description "Uplink to SAN Core"
  speed 16000
  no shutdown
interface fc1/2
  description "Storage Array Connection"
  speed 16000
  no shutdown
...
(output truncated — use `show running-config | no-more` for full display)
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the MDS switch is in the correct mode (use `config t` for configuration mode) and that the copy command syntax matches your firmware version.
    **`% Error opening tftp://192.168.1.45/mds_tftp_backup.cfg (Connection timed out)`** — Confirm the TFTP server is reachable and running on the specified IP, and that network connectivity exists from the switch management interface.
    **`% Authentication failed for scp://<user>@192.168.1.50`** — Verify the username and password are correct, the remote server has SCP enabled, and the user has write permissions to the destination directory.
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Mds — Procedures](../procedures/)
- [Mds — Health Checks](../health-checks/)
- [Mds — Common Issues](../../troubleshooting/common-issues/)
