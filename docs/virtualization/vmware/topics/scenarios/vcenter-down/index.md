# vCenter Down / Unreachable

<div class="kb-summary">
vCenter is unreachable via browser or API. This scenario covers confirming the outage scope, using VAMI
and SSH to diagnose VCSA service failures, resolving the most common cause (full disk partitions), and
restoring from a file-based backup when the appliance cannot be recovered in place. ESXi hosts and vSAN
continue operating without vCenter — VMs keep running throughout.
</div>

```text
┌─────────────────────────────── vCenter Down — Investigation Flow ───────────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│   │  START: https://vcenter-fqdn unreachable / UI times out / monitoring alert fires                │ │
│   └──────────────────────────────────────────┬──────────────────────────────────────────────────────┘ │
│                                              │                                                        │
│              ┌───────────────────────────────┼───────────────────────────────┐                        │
│              ▼                               ▼                               ▼                        │
│   ┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐               │
│   │ VCSA VM powered on? │        │ VAMI reachable?     │        │ SSH accessible?     │               │
│   │ Check iDRAC / iLO   │        │ :5480 → Monitor     │        │ Check services      │               │
│   │ or second vCenter   │        │ tab → Health        │        │ via CLI             │               │
│   └────────┬────────────┘        └────────┬────────────┘        └─────────┬───────────┘               │
│            │                              │                               │                           │
│            ▼                              ▼                               ▼                           │
│   ┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐               │
│   │ Powered off → power │        │ Disk full? → clean  │        │ service-control     │               │
│   │ on; wait for boot   │        │ logs → restart svc  │        │ --status --all      │               │
│   └─────────────────────┘        └─────────────────────┘        └─────────┬───────────┘               │
│                                                                            │                          │
│                          ┌─────────────────────────────────────────────────┘                          │
│                          ▼                                                                            │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│   │  Services won't start → read vpxd.log → DB check → cert issue → restore from backup?           │  │
│   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter VCSA | Primary failing component; VAMI, service-control, and vpxd.log are the main diagnostic surfaces |
| ESXi hosts | Continue running independently; VMs keep running; no management actions available during outage |
| vSAN | Continues operating without vCenter; health monitoring is unavailable until vCenter recovers |
| Aria SuiteLC | Manages vCenter certificate renewals; relevant if outage is caused by an expired certificate |

---

## 1. Confirm the Scope of the Outage

Before starting recovery, determine what is and is not reachable:

| Target | URL / Command | Expected when healthy |
|---|---|---|
| vCenter UI | `https://vcenter-fqdn` | Login page loads |
| VAMI | `https://vcenter-fqdn:5480` | Appliance management UI |
| SSH | `ssh root@vcenter-fqdn` | Shell prompt |
| VCSA VM console | iDRAC / iLO / second vCenter | VM powered on, OS running |

If the VCSA VM is powered off, power it on through iDRAC/iLO or a second vCenter instance (if one exists
in the environment). Wait 5–10 minutes for all services to start before proceeding.

---

## 2. Check VCSA Services via SSH

If SSH is accessible, check which services are stopped:

```bash
service-control --status --all
```

Filter for stopped services:

```bash
service-control --status --all | grep -i stopped
```

Start an individual stopped service first before attempting a full restart:

```bash
service-control --start vmware-vpxd
service-control --start vmware-vpostgres
service-control --start vmware-sso
```

Full restart (last resort — do not use until you have read logs, as it masks root cause):

```bash
service-control --stop --all
service-control --start --all
```

---

## 3. Check Disk Space — the Most Common Cause

Full disk partitions are the single most common cause of vCenter service failures. Check before anything
else:

```bash
df -h
```

The partition most frequently responsible is `/storage/log`. Any partition at 100% will cause vCenter
services to crash or refuse to start.

Clean old logs using the VMware-provided cleanup script:

```bash
/usr/lib/vmware-vpx/scripts/cleanup_appliance_logs.py
```

After freeing space, start services and confirm:

```bash
service-control --start vmware-vpxd
service-control --status vmware-vpxd
```

If the partition fills again within hours, a service is logging at excessive verbosity. Check
`/var/log/vmware/vpxd/` for log files larger than expected and reduce log level via VAMI.

---

## 4. Use VAMI for Health Overview

If VAMI at `https://vcenter-fqdn:5480` is reachable even when the UI is not, use it for a quick health
overview before touching the CLI. Navigate to:

- **Monitor → Health** — CPU, memory, disk, and network at a glance.
- **Services** tab — lists all VCSA services with start/stop controls.
- **Disk** — shows partition utilisation per mount point.

VAMI is a separate lightweight process from the vCenter services. It often remains available when
vpxd has crashed, making it the fastest first check.

---

## 5. Check the PostgreSQL Embedded Database

vCenter stores all inventory, configuration, and task history in an embedded PostgreSQL database. If
the database is down, vpxd cannot start:

```bash
/usr/lib/vmware-vpostgres/current/bin/pg_isready -h localhost
```

Expected output when healthy:

```text
localhost:5432 - accepting connections
```

If the database is not accepting connections, check its log:

```bash
tail -50 /var/log/vmware/vpostgres/postgresql*.log
```

Common database failures: disk full (database cannot write WAL), corrupt data files after ungraceful
shutdown, connection limit exhausted. A full disk is by far the most frequent cause.

---

## 6. Read vpxd.log for Startup Errors

If services fail to start, vpxd.log contains the startup sequence and the exact failure:

```bash
tail -100 /var/log/vmware/vpxd/vpxd.log | grep -iE "error|fatal|failed|exception"
```

Common fatal startup errors:

```text
Failed to connect to database          → PostgreSQL down or credentials mismatch
SSL handshake failed                   → certificate expired or NTP drift
Address already in use: port 443       → previous vpxd process still running (kill it)
VMOMI::Exception: timeout             → SSO service not yet ready; wait and retry
```

For the "address in use" error, find and kill the stale process:

```bash
ps aux | grep vpxd
kill -9 <pid>
service-control --start vmware-vpxd
```

---

## 7. Certificate Failures — Aria SuiteLC or certificate-manager

If vCenter fails due to an expired SSL certificate, the symptom in vpxd.log is:

```text
SSL Exception: certificate has expired
```

Use the VMware certificate-manager CLI to renew or replace the certificate:

```bash
/usr/lib/vmware-vmca/bin/certificate-manager
```

If Aria SuiteLC is deployed and managing certificates, initiate the renewal from Aria SuiteLC →
**Certificate Management → vCenter → Renew**. Do not run certificate-manager and Aria SuiteLC on the
same VCSA at the same time — they will conflict.

---

## 8. Restore from File-Based Backup

If the VCSA cannot be recovered in place (filesystem corruption, failed upgrade, unrecoverable service
crash), restore from a VAMI file-based backup.

Prerequisite: VAMI file-based backup must have been configured before the incident. If no backup exists,
you must rebuild vCenter from scratch and manually reconnect hosts.

Restore procedure:

1. Deploy a fresh VCSA of the same version as the backup using the VCSA installer ISO.
2. During deployment, select **Restore from backup** instead of fresh install.
3. Provide the backup file location (FTP/FTPS/HTTP/HTTPS/SCP/NFS).
4. Complete the restore — all inventory, permissions, and configuration are recovered.
5. ESXi hosts reconnect automatically after restore (they retain vCenter connection details).

After restore, verify all hosts show "Connected" in vCenter within 10 minutes.

---

## Common Mistakes

- **Restarting all services without reading logs first.** A full `service-control --stop --all` hides
  the root cause in log output and may interrupt a service that was in the process of recovering itself.
- **Not checking disk space before anything else.** Disk full is the most common cause. Checking it
  takes 10 seconds and eliminates the most likely failure mode immediately.
- **Not having a VAMI backup configured before the incident.** Without a file-based backup, vCenter
  cannot be restored — only rebuilt. Configure VAMI backup to a network location with daily schedule
  before you need it.
- **Running both certificate-manager and Aria SuiteLC on the same VCSA.** These tools conflict and can
  leave the certificate chain in a broken state requiring a full regeneration.

---

## Related Scenarios

- [ESXi Host Disconnected from vCenter](../esxi-host-disconnected/index.md) — when vCenter recovers but
  individual hosts remain disconnected, use the host disconnect procedure.
- [NTP Drift Causing SSO or Certificate Errors](../ntp-drift-sso-certificate/index.md) — if vpxd.log
  shows SSL or SSO failures during startup, NTP drift is a common root cause.
- [VxRail LCM Upgrade Failure](../vxrail-lcm-upgrade-failure/index.md) — a failed VxRail upgrade can
  leave vCenter in a partially upgraded and unbootable state.
