---
tags:
  - dell
  - operations
---
# RecoverPoint — Health Checks

```bash
# SSH to RPA cluster management IP
ssh admin@<rpa-cluster-ip>

# RPA cluster and node health
system status

# All CGs — expect ACTIVE for all production CGs
groups status

# Detailed CG view including lag, RPO, and journal fill
groups status detail

# Journal utilization for all CGs
journals list

# Active alarms (hardware and software)
alarms list

# Inter-site link statistics (latency, bandwidth)
links statistics

# Cluster quorum state
cluster quorum check
```

```d2
direction: right

run_this_routine: "Run This Routine" {shape: rectangle}
verify: "Verify" {shape: rectangle}

run_this_routine -> verify
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

Run these commands via SSH to the RPA cluster management IP each day for a complete RecoverPoint health snapshot.

1. **RPA cluster health** — confirm all RPA nodes are Online and cluster is healthy:
   ```bash
   get_system_settings
   ```
   Or review the health dashboard in Unisphere for RecoverPoint.
2. **Replication link status** — all links must show Status: Active:
   ```bash
   get_links
   ```
3. **Consistency group health** — all CGs must show Protection Status: Active:
   ```bash
   get_groups
   ```
4. **RPO compliance** — review each CG's displayed RPO lag; flag any CG reporting "RPO Violated" and escalate immediately.
5. **Journal space** — verify journal free space is above 20 % per CG:
   ```bash
   get_journal_capacity
   ```
6. **Splitter connectivity** — all splitters must show Status: Connected:
   ```bash
   get_splitters
   ```
7. **WAN link bandwidth** — check replication throughput against link capacity; sustained >80 % utilisation requires investigation:
   ```bash
   get_statistics
   ```
8. **RPA firmware consistency** — confirm all RPAs in the cluster run the same firmware version:
   ```bash
   get_rpa_settings
   ```
9. **RecoverPoint alerts** — review open alerts; acknowledge known ones and investigate any new alerts:
   ```bash
   get_alerts
   ```
10. **Fan-out replication** (if configured) — verify all target copies are current within their configured RPO; flag any copy lagging beyond target.

```bash
# List journal volumes with utilization
journals list

# Expected output columns:
#   Journal Name   CG Name         Used%   Free%   Status
#   JRN-CG-ORA-DR  CG-ORACLE-PROD  34%     66%     OK
```

```text title="Expected output"
Journal Name      CG Name           Used%   Free%   Status
JRN-CG-ORA-DR     CG-ORACLE-PROD    34%     66%     OK
JRN-CG-SQL-DR     CG-SQLSERVER-01   78%     22%     OK
JRN-CG-VMW-DR     CG-VMWARE-PROD    45%     55%     OK
JRN-CG-SAP-DR     CG-SAP-HANA       91%     9%      WARNING
JRN-CG-EXC-DR     CG-EXCHANGE-02    12%     88%     OK
JRN-CG-NAS-DR     CG-NETAPP-BACKUP  67%     33%     OK
```

!!! warning "Common errors"
    **`journals: command not found`** — Verify the RecoverPoint CLI is installed and the PATH includes the RecoverPoint bin directory, or source the environment setup script.
    **`Error: Unable to connect to RecoverPoint cluster at 192.168.1.50`** — Confirm network connectivity to the RecoverPoint appliance and that credentials are configured via `rp_login` or environment variables.
    **`Journal JRN-CG-ORA-DR status: CRITICAL (Used% exceeds 95%)`** — Increase journal volume capacity or reduce the consistency group replication window to prevent write failures.
```bash
# Confirm splitter health (for RP4VM software splitters on ESXi)
esxcli software vib list | grep -i rp

# Confirm RPA software versions are consistent across cluster
boxmgmt verify_rpa_version

# Review audit log for unexpected operations (logins, image access events)
get_audit_log -last 500

# Confirm DR site RPA cluster is also healthy
ssh admin@<dr-rpa-cluster-ip> "system status"
ssh admin@<dr-rpa-cluster-ip> "groups status"
```


```text title="Expected output"
Name                                    Version                            Vendor Code
RecoverPoint-splitter                   5.4.2.1-18294756                   Dell
RecoverPoint-splitter-hotfix            5.4.2.1-18294756                   Dell

RPA Version Verification Report
================================
rpa-prod-01.corp.local: 5.4.2.1
rpa-prod-02.corp.local: 5.4.2.1
rpa-prod-03.corp.local: 5.4.2.1
Status: CONSISTENT

Audit Log (Last 500 Events)
================================
2024-01-15 14:32:18 | admin | LOGIN | 192.168.1.45 | SUCCESS
2024-01-15 14:33:02 | svc_backup | IMAGE_ACCESS | /mnt/rp_images/prod_vm_001 | READ
2024-01-15 14:35:41 | admin | CONFIG_CHANGE | replication_policy_update | SUCCESS
2024-01-15 14:38:15 | svc_backup | IMAGE_ACCESS | /mnt/rp_images/prod_vm_002 | READ
2024-01-15 14:40:22 | admin | LOGOUT | 192.168.1.45 | SUCCESS
...

System Status (DR Site)
================================
System Health: HEALTHY
Uptime: 42 days 18 hours
CPU Usage: 34%
Memory Usage: 58%

Replication Groups Status (DR Site)
================================
Group: prod-to-dr-01 | Status: CONSISTENT | RPO: 0s | Lag: 0ms
Group: prod-to-dr-02 | Status: CONSISTENT | RPO: 0s | Lag: 2ms
Group: prod-to-dr-03 | Status: CONSISTENT | RPO: 0s | Lag: 1ms
```

!!! warning "Common errors"
    **`ssh: Could not resolve hostname <dr-rpa-cluster-ip>: Name or service not known`** — Replace `<dr-rpa-cluster-ip>` with the actual DR RPA cluster IP address or hostname.
    **`Permission denied (publickey,password)`** — Ensure the admin account credentials are correct and SSH key-based authentication is configured, or use `ssh -u admin@<dr-rpa-cluster-ip>` with password prompt.
    **`boxmgmt: command not found`** — Source the RecoverPoint environment setup script (typically `. /opt/rp/bin/rp_env.sh`) or ensure the RPA management tools are in your PATH.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Recoverpoint — Procedures](../procedures/)
- [Recoverpoint — CLI Reference](../cli-reference/)
- [Recoverpoint — Common Issues](../../troubleshooting/common-issues/)
