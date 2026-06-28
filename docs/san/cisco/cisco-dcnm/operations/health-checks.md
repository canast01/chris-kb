---
tags:
  - operations
  - san
---
# Cisco DCNM — Health Checks

```bash
ssh root@dcnm-dc1.corp.example.com

# DCNM service status
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server status
# All services should show as running

# Disk usage
df -h
# Alert if /var/lib/pgsql or /var/dcnm is > 80% used

# Database size
du -sh /var/lib/pgsql/data/

# Check DCNM server log for errors
grep -i "ERROR\|SEVERE\|Exception" /var/log/dcnm/server.log | tail -50

# NTP status
timedatectl status
# Expected: synchronized: yes
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **DCNM service status** — SSH to the DCNM server and run `/usr/local/cisco/dcm/dcnm/sbin/dcnm-server status`; all listed services must show `running`; alternatively confirm the DCNM web UI loads successfully and you can log in.
2. **Fabric discovery status** — In the DCNM web UI, navigate to **Fabric Builder → Fabrics → select fabric**; confirm every switch in the topology shows state `Managed` and is not `Unreachable` or `Unmanaged`.
3. **Pending deployments** — In the DCNM web UI, check **Fabric Builder → Deploy** or the configuration compliance view; any switch showing `Out-of-Sync` or `Pending` has uncommitted config changes — review and deploy or roll back.
4. **Switch connectivity** — Navigate to **DCNM → Topology**; verify all switches appear as reachable nodes with no greyed-out or disconnected links; an unreachable switch indicates an SNMP/SSH connectivity failure.
5. **Active alarms** — Navigate to **DCNM → Alarms → Alarm Policies / Event Analytics**; review all open Critical and Major alarms; acknowledge resolved alarms and open incidents for any that are active.
6. **Backup status** — Navigate to **DCNM → Administration → Backup and Restore**; confirm the last backup completed successfully and the timestamp is within the expected schedule; check `df -h /var/lib/dcnm` to confirm backup storage is below 80%.
7. **Database disk space** — On the DCNM server run `df -h /var/lib/pgsql` (or the configured data directory); alert if usage exceeds 80%; also run `du -sh /var/lib/pgsql/data/` to confirm the database size is within expected range.

```bash
# On MDS switch to verify zone set consistency
show zoneset active vsan <vsan-id>
# Compare against expected zone set exported from DCNM
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Cisco Dcnm — Procedures](../procedures/)
- [Cisco Dcnm — CLI Reference](../cli-reference/)
- [Cisco Dcnm — Common Issues](../troubleshooting/common-issues/)
