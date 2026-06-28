---
tags:
  - operations
  - san
---
# Brocade SANnav — Install and Upgrade
![Brocade SANnav — Install and Upgrade](../../../../assets/san-brocade-sannav-operations-install-upgrade.svg)

```bash
# After VM powers on, access the console or SSH with default credentials
# Default credentials: admin / passw0rd (change on first login)
ssh admin@<sannav-ip>

# Verify network connectivity
ping 8.8.8.8       # or internal NTP/DNS server
hostname           # should return configured FQDN

# Check service startup
sannav status
# Wait 5-10 minutes for all services to start on first boot

# Change default admin password
passwd admin
```

```bash
# On each switch (FOS CLI)
snmpconfig --set trapdest -index <n> -trapdest 0.0.0.0   # clear trap destination
userconfig --delete sannav_svc
```

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

- [Sannav — Procedures](../procedures/)
- [Sannav — Health Checks](../health-checks/)
- [Sannav — Deploy](../../deploy/)
