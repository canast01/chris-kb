---
tags:
  - netapp
  - operations
---
# NetApp Keystone — Operations: Backup & Restore
![NetApp Keystone — Operations: Backup & Restore](../../../../assets/storage-netapp-keystone-operations-backup-restore.svg)

```bash
# SSH into Keystone Collector VM
ssh admin@<keystone-collector-ip>

# Export current configuration
keystone-config export --output /tmp/ks-config-$(date +%Y%m%d).tar.gz
scp admin@<keystone-collector-ip>:/tmp/ks-config-$(date +%Y%m%d).tar.gz ./

# Verify configuration is parseable
tar -tzf ks-config-<date>.tar.gz
```


```text title="Expected output"
admin@192.168.1.45's password: 
Welcome to NetApp Keystone Collector v4.2.1
Last login: Wed Jan 15 10:23:47 2025 from 10.0.0.88

admin@keystone-collector-01:~$ keystone-config export --output /tmp/ks-config-20250115.tar.gz
[INFO] Exporting Keystone configuration...
[INFO] Collecting system metrics
[INFO] Collecting subscription data
[INFO] Archiving configuration files
[INFO] Configuration export completed successfully
[INFO] Archive saved to /tmp/ks-config-20250115.tar.gz (2.3 MB)

ks-config-20250115.tar.gz                                    100% 2412KB   8.2MB/s   00:00

admin@keystone-collector-01:~$ tar -tzf ks-config-20250115.tar.gz
config/keystone.conf
config/collectors.json
config/subscriptions.json
metrics/system-metrics-20250115.json
metrics/capacity-report-20250115.json
logs/keystone-collector.log
certs/keystone-collector.crt
...
```

!!! warning "Common errors"
    **`Permission denied (publickey,password).`** — Verify the Keystone Collector IP address is correct and your SSH key or password is valid for the admin user.
    **`tar: ks-config-20250115.tar.gz: Cannot open: No such file or directory`** — Ensure the SCP command completed successfully and the file exists in the current directory with the correct date format matching the export command.
```bash
# On new or rebuilt Collector VM:
scp ks-config-<date>.tar.gz admin@<new-collector-ip>:/tmp/

ssh admin@<new-collector-ip>
keystone-config import --input /tmp/ks-config-<date>.tar.gz

# Verify after import
keystone-config validate
keystone-collector status
```


```text title="Expected output"
admin@<new-collector-ip>'s password: 
ks-config-20240115.tar.gz                                    100%  2.4MB   1.2MB/s   00:02
admin@collector-vm-02:~$ keystone-config import --input /tmp/ks-config-20240115.tar.gz
Importing configuration from /tmp/ks-config-20240115.tar.gz...
Configuration imported successfully.
  - Subscriptions: 3
  - Collectors: 1
  - Storage systems: 5
  - Capacity pools: 12
admin@collector-vm-02:~$ keystone-config validate
Validation Status: PASSED
  ✓ Configuration syntax valid
  ✓ All storage systems reachable
  ✓ Collector credentials verified
  ✓ Capacity thresholds configured
admin@collector-vm-02:~$ keystone-collector status
Keystone Collector Status: RUNNING
  Version: 5.2.1
  Uptime: 0h 2m 15s
  Last collection: 2024-01-15 14:32:18 UTC
  Data points collected: 1,247
```

!!! warning "Common errors"
    **`keystone-config import: error: input file not found: /tmp/ks-config-<date>.tar.gz`** — Verify the SCP command completed successfully and the filename matches exactly, including the date format.
    **`keystone-config validate: error: Storage system <ip> unreachable (connection timeout)`** — Confirm network connectivity and firewall rules allow the Collector VM to reach the storage system management IP on port 443.
    **`keystone-collector status: error: service not running`** — Start the collector service with `sudo systemctl start keystone-collector` and check logs via `sudo journalctl -u keystone-collector -n 50`.
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

- [Keystone — Procedures](../procedures/)
- [Keystone — Health Checks](../health-checks/)
