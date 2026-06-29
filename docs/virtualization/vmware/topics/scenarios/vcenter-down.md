---
tags:
  - scenarios
  - vcenter
  - vmware
  - vsphere-8
---
# vCenter Down / Unreachable

<div class="kb-summary">
vCenter is unreachable via browser or API. This scenario covers confirming the outage scope, using VAMI
and SSH to diagnose VCSA service failures, resolving the most common cause (full disk partitions), and
restoring from a file-based backup when the appliance cannot be recovered in place. ESXi hosts and vSAN
continue operating without vCenter — VMs keep running throughout.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_confirm_the_scope_of_the_outage: "1. Confirm the Scope of the Outage" {shape: rectangle}
2_check_vcsa_services_via_ssh: "2. Check VCSA Services via SSH" {shape: rectangle}
3_check_disk_space_the_most_common_c: "3. Check Disk Space — the Most Common Cause" {shape: rectangle}
4_use_vami_for_health_overview: "4. Use VAMI for Health Overview" {shape: rectangle}
5_check_the_postgresql_embedded_data: "5. Check the PostgreSQL Embedded Database" {shape: rectangle}

products_involved -> 1_confirm_the_scope_of_the_outage: uses
1_confirm_the_scope_of_the_outage -> 2_check_vcsa_services_via_ssh: uses
2_check_vcsa_services_via_ssh -> 3_check_disk_space_the_most_common_c: uses
3_check_disk_space_the_most_common_c -> 4_use_vami_for_health_overview: uses
4_use_vami_for_health_overview -> 5_check_the_postgresql_embedded_data: uses
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

Check each access path in sequence to narrow down whether the VM, OS, or application layer has failed.

| Target | URL / Command | Expected when healthy |
|---|---|---|
| vCenter UI | `https://vcenter-fqdn` | Login page loads |
| VAMI | `https://vcenter-fqdn:5480` | Appliance management UI |
| SSH | `ssh root@vcenter-fqdn` | Shell prompt |
| VCSA VM console | iDRAC / iLO / second vCenter | VM powered on, OS running |

If the VCSA VM is powered off, power it on through iDRAC/iLO or a second vCenter instance. Wait 5–10 minutes for all services to start before proceeding.

---

## 2. Check VCSA Services via SSH

List stopped services to identify which component is failing before touching anything.

```bash
service-control --status --all
service-control --status --all | grep -i stopped
```


```text title="Expected output"
Service                                    Running  Stopped
----------------------------------------------------
VMware vCenter Server                       Yes      No
VMware vSphere Web Client                   Yes      No
VMware Identity Management Service          Yes      No
VMware vCenter Inventory Service            Yes      No
VMware vCenter Orchestrator Configuration   No       Yes
VMware vCenter Orchestrator                 No       Yes
VMware vSphere Update Manager               Yes      No
VMware vCenter Statistics                   Yes      No

VMware vCenter Orchestrator Configuration
VMware vCenter Orchestrator
```

!!! warning "Common errors"
    **`service-control: command not found`** — Ensure you are running this command on a vCenter Server host and that the VMware tools are installed in the system PATH.
    **`grep: (standard input): Permission denied`** — Run the command with elevated privileges using `sudo service-control --status --all | grep -i stopped`.
Start an individual stopped service first before attempting a full restart:

```bash
service-control --start vmware-vpxd
service-control --start vmware-vpostgres
service-control --start vmware-sso
```


```text title="Expected output"
Waiting for services to be available...
Service vmware-vpxd started successfully
Service vmware-vpostgres started successfully
Service vmware-sso started successfully
```

!!! warning "Common errors"
    **`Error: Unable to connect to the Service Control Agent`** — Ensure the Service Control Agent daemon is running with `service-control --status` and restart it if needed.
    **`Error: Service vmware-vpxd is already running`** — Check if the service is already active with `service-control --status vmware-vpxd` before attempting to start it again.
Full restart (last resort — do not use until you have read logs, as it masks root cause):

```bash
service-control --stop --all
service-control --start --all
```


```text title="Expected output"
Stopping all services...
Stopping service 'vsphere-ui'... done
Stopping service 'vpxd'... done
Stopping service 'vsan-health'... done
Stopping service 'rhttpproxy'... done
Stopping service 'sps'... done
All services stopped successfully.
Starting all services...
Starting service 'sps'... done
Starting service 'rhttpproxy'... done
Starting service 'vpxd'... done
Starting service 'vsan-health'... done
Starting service 'vsphere-ui'... done
All services started successfully.
```

!!! warning "Common errors"
    **`service-control: command not found`** — Ensure you are running this command on a vCenter Server appliance with root privileges, as `service-control` is only available on VCSA.
    **`Error: Unable to stop service 'vpxd': Service dependency violation`** — Wait 30–60 seconds between the stop and start commands to allow dependent services to fully shut down, or run `service-control --stop --all` with the `--force` flag.
---

## 3. Check Disk Space — the Most Common Cause

Full disk partitions are the single most common cause of vCenter service failures — check this before anything else.

```bash
df -h
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       100G   45G   55G  45% /
/dev/sda2       500G  320G  180G  64% /var
/dev/sdb1       2.0T  1.8T  200G  90% /vmfs/volumes/datastore1
/dev/sdc1       1.0T  450G  550G  45% /vmfs/volumes/datastore2
tmpfs           32G  128M   32G   1% /dev/shm
```

!!! warning "Common errors"
    **`df: cannot access '/mnt/nfs': Stale NFS file handle`** — Remount the NFS datastore with `mount -o remount /mnt/nfs` or check ESXi host connectivity to the NFS server.
    **`df: /dev/mapper/vg0-lv_data: No such file or directory`** — Verify the logical volume exists with `lvdisplay` and activate it with `lvchange -ay /dev/vg0/lv_data` if needed.
Look for: any partition at 100% utilisation, especially `/storage/log`. Clean old logs using the VMware-provided script:

```bash
/usr/lib/vmware-vpx/scripts/cleanup_appliance_logs.py
```


```text title="Expected output"
Cleaning up VMware vCenter appliance logs...
Processing log directory: /var/log/vmware/
Removing logs older than 30 days
Cleaned up 2.3 GB from /var/log/vmware/vpxd/
Cleaned up 1.1 GB from /var/log/vmware/sso/
Cleaned up 856 MB from /var/log/vmware/vpostgres/
Cleaned up 512 MB from /var/log/vmware/vsan/
Total disk space reclaimed: 4.8 GB
Cleanup completed successfully at 2024-01-15 03:45:22 UTC
```

!!! warning "Common errors"
    **`Permission denied`** — Run the script with sudo or as root user since it requires write access to system log directories.
    **`No such file or directory: /usr/lib/vmware-vpx/scripts/cleanup_appliance_logs.py`** — Verify the vCenter Server is installed and the VMware VPX package is present; reinstall if necessary.
    **`ERROR: Log directory /var/log/vmware/ is not accessible`** — Ensure the vCenter appliance is running and the log partition has sufficient inode availability.
After freeing space, start services and confirm:

```bash
service-control --start vmware-vpxd
service-control --status vmware-vpxd
```


```text title="Expected output"
Shutting down VMware services...
Waiting for services to shut down...
Starting VMware services...
Waiting for services to start...
Service vmware-vpxd is running.
```

!!! warning "Common errors"
    **`Error: Could not connect to VMware Authorization Service`** — Ensure the VMware Authorization Service (vmware-authd) is running first with `service-control --start vmware-authd`.
    **`Service vmware-vpxd is not running.`** — Check system resources and review `/var/log/vmware/vpxd/vpxd.log` for startup errors, then retry the start command.
---

## 4. Use VAMI for Health Overview

VAMI at `https://vcenter-fqdn:5480` is a lightweight separate process that often remains up when vpxd has crashed — use it as the fastest first check.

Navigate to:

- **Monitor → Health** — CPU, memory, disk, and network at a glance.
- **Services** tab — lists all VCSA services with start/stop controls.
- **Disk** — shows partition utilisation per mount point.

---

## 5. Check the PostgreSQL Embedded Database

vCenter's embedded database must be accepting connections before vpxd can start.

```bash
/usr/lib/vmware-vpostgres/current/bin/pg_isready -h localhost
```


```text title="Expected output"
accepting connections
```

!!! warning "Common errors"
    **`pg_isready: could not translate host name "localhost" to address: Name or service not known`** — Verify the PostgreSQL service is running with `systemctl status vmware-vpostgres` and that localhost resolution is configured in `/etc/hosts`.
    **`pg_isready: could not connect to server: Connection refused`** — Ensure the vPostgres service is listening on localhost by checking the postgresql.conf listen_addresses setting and restarting the service with `systemctl restart vmware-vpostgres`.
Expected output when healthy:

```text
localhost:5432 - accepting connections
```

If the database is not accepting connections, read its log:

```bash
tail -50 /var/log/vmware/vpostgres/postgresql*.log
```


```text title="Expected output"
2024-01-15 14:23:47.123 UTC [12847] LOG:  connection received: host=192.168.1.45 port=54321
2024-01-15 14:23:47.456 UTC [12847] LOG:  connection authorized: user=postgres database=VCDB
2024-01-15 14:23:48.789 UTC [12848] LOG:  statement: SELECT version();
2024-01-15 14:23:49.012 UTC [12848] LOG:  duration: 0.234 ms
2024-01-15 14:23:52.345 UTC [12849] LOG:  checkpoint starting: time
2024-01-15 14:23:55.678 UTC [12849] LOG:  checkpoint complete: wrote 1247 buffers (98.5%); write=2.156 s, sync=0.891 s, total=3.047 s
2024-01-15 14:24:01.901 UTC [12850] LOG:  autovacuum launcher started
2024-01-15 14:24:15.234 UTC [12851] LOG:  connection received: host=192.168.1.50 port=54322
2024-01-15 14:24:15.567 UTC [12851] LOG:  connection authorized: user=vpxd database=VCDB
2024-01-15 14:24:20.890 UTC [12852] WARNING:  could not write block 4095 of relation base/16384/16385: No space left on device
2024-01-15 14:24:21.123 UTC [12852] ERROR:  could not extend relation base/16384/16385: No space left on device
2024-01-15 14:24:25.456 UTC [12853] LOG:  statement: VACUUM ANALYZE;
2024-01-15 14:24:30.789 UTC [12853] LOG:  duration: 4.567 ms
```

!!! warning "Common errors"
    **`ERROR:  could not extend relation base/16384/16385: No space left on device`** — Check available disk space on the vPostgres partition with `df -h /storage/db` and expand the volume or clean up old logs.
    **`tail: cannot open '/var/log/vmware/vpostgres/postgresql*.log' for reading: No such file or directory`** — Verify the vPostgres service is running with `systemctl status vpostgres` and confirm the log directory exists.
    **`Permission denied`** — Run the command with `sudo` or as the root user since vPostgres logs are typically readable only by root or the postgres service account.
Look for: disk full errors (cannot write WAL), corrupt data files after ungraceful shutdown, or connection limit exhausted messages.

---

## 6. Read vpxd.log for Startup Errors

If services fail to start, vpxd.log contains the startup sequence and the exact failure point.

```bash
tail -100 /var/log/vmware/vpxd/vpxd.log | grep -iE "error|fatal|failed|exception"
```


```text title="Expected output"
2024-01-15T09:42:31.847Z | ERROR [vpxd.log] Failed to connect to vCenter database: Connection timeout after 30s
2024-01-15T09:43:12.923Z | FATAL [vpxd.log] Exception in com.vmware.vc.VcEventManager: NullPointerException at line 1247
2024-01-15T09:44:05.156Z | ERROR [vpxd.log] SSL certificate validation failed for host esx-host-04.lab.local (192.168.1.145)
2024-01-15T09:45:33.441Z | ERROR [vpxd.log] Failed to retrieve inventory from datacenter DC-PROD: Permission denied
2024-01-15T09:46:18.762Z | FATAL [vpxd.log] Heap space exhausted - OutOfMemoryError in garbage collector
2024-01-15T09:47:02.334Z | ERROR [vpxd.log] Task 'task-1847' failed: Host 'esx-host-02' is not responding
```

!!! warning "Common errors"
    **`tail: cannot open '/var/log/vmware/vpxd/vpxd.log' for reading: No such file or directory`** — Verify vpxd service is running with `systemctl status vpxd` and check the correct log path with `find /var/log -name vpxd.log`.
    **`grep: (standard input): Permission denied`** — Run the command with `sudo` or ensure your user is in the `root` or `vpxd` group with `sudo usermod -aG vpxd $USER`.
    **`No matches found`** — The log file exists but contains no errors; this is normal for a healthy vCenter instance, so verify the service is actually running with `systemctl status vpxd`.
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


```text title="Expected output"
root      12847  0.5 12.3 2847392 512048 ?      Ssl  08:14   2:47 /usr/lib/vmware-vpxd/bin/vpxd
root      15234  0.0  0.0  12112  1024 pts/0    S+   14:22   0:00 grep vpxd
(no output — command completes silently)
Operation finished successfully.
```

!!! warning "Common errors"
    **`kill: (12847): Operation not permitted`** — Run the command with sudo or as root user.
    **`Service 'vmware-vpxd' is not registered with service-control.`** — Use `service-control --list` to verify the correct service name, or restart using `systemctl restart vmware-vpxd` instead.
---

## 7. Certificate Failures — Aria SuiteLC or certificate-manager

If vpxd.log shows a certificate expiry error, use the appropriate renewal tool — never both at once.

```text
SSL Exception: certificate has expired
```

```bash
/usr/lib/vmware-vmca/bin/certificate-manager
```


```text title="Expected output"
VMware Certificate Manager

Please select an option [1-9]:

1. Generate Certificate Signing Request (CSR) and replace an existing VMCA-signed certificate
2. Generate a new VMCA certificate for an existing CSR
3. Regenerate a new VMCA root certificate
4. Replace an existing certificate with VMCA signed certificate
5. Replace an existing certificate with Custom Certificate
6. Replace an existing VMCA root certificate with Custom Certificate
7. Regenerate a new certificate and replace an existing certificate
8. Reset all certificates to default
9. Exit

Option [1-9]:
```

!!! warning "Common errors"
    **`Error: Unable to connect to VMCA service`** — Ensure the VMware Certificate Authority service is running with `systemctl status vmware-vmca` and restart if needed.
    **`Error: Permission denied`** — Run the command with elevated privileges using `sudo /usr/lib/vmware-vmca/bin/certificate-manager`.
    **`Error: Certificate file not found at /etc/vmware-vpx/ssl/rui.crt`** — Verify the certificate path exists and check file permissions with `ls -la /etc/vmware-vpx/ssl/`.
If Aria SuiteLC is deployed and managing certificates, initiate renewal from Aria SuiteLC →
**Certificate Management → vCenter → Renew**. Do not run certificate-manager and Aria SuiteLC on the
same VCSA simultaneously — they will conflict and leave the certificate chain broken.

---

## 8. Restore from File-Based Backup

If the VCSA cannot be recovered in place (filesystem corruption, failed upgrade, unrecoverable crash), restore from a VAMI file-based backup.

Restore procedure:

1. Deploy a fresh VCSA of the same version as the backup using the VCSA installer ISO.
2. During deployment, select **Restore from backup** instead of fresh install.
3. Provide the backup file location (FTP/FTPS/HTTP/HTTPS/SCP/NFS).
4. Complete the restore — all inventory, permissions, and configuration are recovered.
5. ESXi hosts reconnect automatically after restore (they retain vCenter connection details).

Look for: all hosts showing "Connected" in vCenter within 10 minutes of restore completion.

---

## Key Terms

| Term | Definition |
|---|---|
| VCSA | vCenter Server Appliance — the Linux-based virtual appliance that runs vCenter; all services (vpxd, SSO, vpostgres) run inside this VM |
| VAMI | vCenter Appliance Management Interface — the lightweight web UI on port 5480 for appliance health, disk, services, and NTP; often available even when the main UI is down |
| PSC | Platform Services Controller — the component that hosts SSO, VMCA, and identity services; in modern VCSA deployments it is embedded inside the same appliance rather than deployed separately |
| SSO | Single Sign-On — VMware's identity federation service; all vCenter and NSX logins are authenticated through SSO; if SSO is down, no users can log in regardless of network connectivity |
| vpostgres | VMware-embedded PostgreSQL database that stores all vCenter inventory, tasks, events, and configuration; vpxd cannot start if vpostgres is down or full |
| service-control | VMware CLI tool on the VCSA used to start, stop, restart, and check status of individual VCSA services without a full appliance reboot |
| VMCA | VMware Certificate Authority — the internal CA embedded in the VCSA that issues SSL certificates to ESXi hosts and vCenter services; expired VMCA certificates cause cascading SSL failures |
| vpxd | vCenter Server daemon — the primary vCenter process that handles all API requests, inventory, task scheduling, and host communication; its log (vpxd.log) is the main diagnostic source |
| File-based backup | VAMI-configured backup of the VCSA to a network location (FTP/SCP/NFS); the only supported restore path if the appliance cannot be recovered in place |
| certificate-manager | VMware CLI tool at `/usr/lib/vmware-vmca/bin/certificate-manager` used to regenerate or replace VCSA certificates when they expire or become invalid |
| Embedded PSC | Architecture where Platform Services Controller runs inside the VCSA VM rather than as a separate appliance; standard since vCenter 7.0; simplifies deployment but means SSO and VMCA are co-located with vpxd |

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

- [ESXi Host Disconnected from vCenter](esxi-host-disconnected.md) — when vCenter recovers but
  individual hosts remain disconnected, use the host disconnect procedure.
- [NTP Drift Causing SSO or Certificate Errors](ntp-drift-sso-certificate.md) — if vpxd.log
  shows SSL or SSO failures during startup, NTP drift is a common root cause.
- [VxRail LCM Upgrade Failure](vxrail-lcm-upgrade-failure.md) — a failed VxRail upgrade can
  leave vCenter in a partially upgraded and unbootable state.
