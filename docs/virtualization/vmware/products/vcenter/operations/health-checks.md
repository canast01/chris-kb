---
tags:
  - operations
  - vcenter
  - vmware
  - vsphere-8
description: "Health Checks reference covering Disk Partition Usage, SSO and Lookup Service Health, DNS and NTP Validation, PowerCLI Health Checks, Daily Checks and 2..."
---
# vCenter — Health Checks

<div class="kb-summary">
Health Checks reference covering Disk Partition Usage, SSO and Lookup Service Health, DNS and NTP Validation, PowerCLI Health Checks, Daily Checks and 2 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

Run these commands in sequence for a complete vCenter health snapshot. Each block can be pasted directly into an SSH session on the VCSA appliance shell.

```bash
# 1. VCSA service health — list all services, filter out stopped ones
service-control --status --all | grep -v STOPPED

# 2. vCenter version and build number
vpxd --version

# 3. SSO / Lookup Service health
service-control --status vmware-sts
service-control --status vmware-lookupsvc

# 4. Certificate store list — inspect VECS stores for expiring certs
/usr/lib/vmware-vmafd/bin/vecs-cli store list

# 5. Disk usage — key VCSA partitions: DB, logs, seat data
df -h /storage/db /storage/log /storage/seat

# 6. vCenter HA state (run only if VCHA is deployed)
python3 /usr/lib/vmware-vcha/VcHaMgr.py state

# 7. NTP sync status — confirm clock is synchronised
timedatectl status

# 8. Connected host count via REST API
# Replace credentials before running
curl -sk -u 'administrator@vsphere.local:password' \
  https://localhost/api/vcenter/host | python3 -m json.tool | grep -c connection_state

# 9. Recent vpxd errors — last 100 lines of the main vCenter log
tail -100 /var/log/vmware/vpxd/vpxd.log | grep -i error

# 10. Backup job status — check VAMI file-based backup schedule
# Verify via VAMI at https://<vcenter>:5480 → Backup, or inspect cron
crontab -l 2>/dev/null | grep -i backup
```


```text title="Expected output"
SERVICE vmware-vpxd RUNNING
SERVICE vmware-vsan-health RUNNING
SERVICE vmware-eam RUNNING
SERVICE vmware-mbcs RUNNING
SERVICE vmware-sts RUNNING
SERVICE vmware-lookupsvc RUNNING
SERVICE vmware-rhttpproxy RUNNING
SERVICE vmware-netdumper RUNNING
SERVICE vmware-content-library RUNNING
...

VMware vCenter Server 8.0.1 build-21495797

SERVICE vmware-sts RUNNING
SERVICE vmware-lookupsvc RUNNING

VECS store list:
	APPLIANCE_SSL_CERT
	MACHINE_SSL_CERT
	TRUSTED_ROOTS
	TRUSTED_ROOT_CRLS

Filesystem     Size  Used Avail Use% Mounted on
/storage/db    500G  387G  113G  78% /storage/db
/storage/log   100G   34G   66G  34% /storage/log
/storage/seat   50G   12G   38G  24% /storage/seat

HA Enabled: true
HA State: HEALTHY
Node Role: ACTIVE
Cluster Mode: ENABLED

               Local time: Wed 2024-01-17 14:32:18 UTC
           Universal time: Wed 2024-01-17 14:32:18 UTC
                 RTC time: Wed 2024-01-17 14:32:18 UTC
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active

5

2024-01-17T14:28:43.421Z [vpxd 7654] [Originator@6876 sub=Default] [error] Connection timeout to host 192.168.1.45
2024-01-17T14:15:12.089Z [vpxd 7654] [Originator@6876 sub=Default] [error] Failed to retrieve datastore inventory

0 2 * * * /usr/lib/vmware-vami/scripts/backup.sh >> /var/log/vmware-vami/backup.log 2>&1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification (already present in example; if still failing, verify curl is installed with `which curl`). |
    | `python3: command not found` | Install Python 3 with `apt-get install python3` on Debian-based VCSA or use the full path `/usr/bin/python3`. |
    | `/var/log/vmware/vpxd/vpxd.log: No such file or directory` | Verify vpxd service is running with `service-control --status vmware-vpxd` and check log location with `find /var/log -name vpxd.log`. |
Key partitions to monitor:
- `/storage/log` — fills quickly during issues
- `/storage/db` — vCenter database
- `/storage/core` — core appliance data

## SSO and Lookup Service Health

![SSO and Lookup Service Health](../../../../../assets/virtualization-vmware-vcenter-hc-sso-and-lookup-service-health.svg)

```bash
service-control --status vmware-sts
service-control --status vmware-lookupsvc
service-control --status vmware-eam
```


```text title="Expected output"
vmware-sts is running
vmware-lookupsvc is running
vmware-eam is running
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `service-control: command not found` | Ensure you are running this command on the vCenter Server appliance (VCSA) with root privileges, as `service-control` is only available in the vCenter environment. |
    | `vmware-sts is stopped` | Restart the STS service with `service-control --start vmware-sts` and wait 30-60 seconds for dependent services to recover. |
## DNS and NTP Validation

![DNS and NTP Validation](../../../../../assets/virtualization-vmware-vcenter-hc-dns-and-ntp-validation.svg)

```bash
# Check DNS from vCenter appliance shell
nslookup <vcenter-fqdn>
dig <vcenter-fqdn>

# Check NTP status
timedatectl
```


```text title="Expected output"
Server:		10.0.0.1
Address:	10.0.0.1#53

Name:	vcenter.example.com
Address: 192.168.1.50

; <<>> DiG 9.11.4-P8-RedHat-9.11.4-26.P2-el7 <<>> vcenter.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 54321
;; QUESTION SECTION:
;vcenter.example.com.		IN	A

;; ANSWER SECTION:
vcenter.example.com.	300	IN	A	192.168.1.50

;; Query time: 2 msec
;; SERVER: 10.0.0.1#53(10.0.0.1)

               Local time: Wed 2024-01-10 14:32:45 UTC
           Universal time: Wed 2024-01-10 14:32:45 UTC
                 RTC time: Wed 2024-01-10 14:32:44
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
       RTC in local TZ: no
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nslookup: command not found` | Install bind-utils package with `yum install bind-utils` or use `dig` instead. |
    | `connection timed out; no servers could be reached` | Verify DNS server IP is correct in `/etc/resolv.conf` and network connectivity to the DNS server exists. |
    | `System clock synchronized: no` | Restart the NTP service with `systemctl restart ntp` or `systemctl restart chrony` depending on your time daemon. |
## PowerCLI Health Checks

![PowerCLI Health Checks](../../../../../assets/virtualization-vmware-vcenter-hc-powercli-health-checks.svg)

```powershell
# Host connectivity
Get-VMHost | Select-Object Name, ConnectionState, PowerState

# Cluster DRS/HA state
Get-Cluster | Select-Object Name, DrsEnabled, HAEnabled

# Recent error events
Get-VIEvent -MaxSamples 100 -Type Error | Select-Object CreatedTime, FullFormattedMessage

# Stale snapshots
Get-VM | Get-Snapshot | Where-Object {$_.Created -lt (Get-Date).AddDays(-3)} | Select-Object VM, Name, Created

# vCenter REST API health
curl -sk -u 'administrator@vsphere.local' https://<vcenter>/api/vcenter/health/system
```

## Daily Checks

![Daily Checks](../../../../../assets/virtualization-vmware-vcenter-hc-daily-checks.svg)

| Check | Command | Notes |
|---|---|---|
| vCenter GUI accessible | Browser to `https://<vcenter>/ui` | All VCSA services should be healthy |
| DRS and HA enabled | `Get-Cluster \| Select Name,DrsEnabled,HAEnabled` | Should be enabled on all production clusters |
| Hosts connected | `Get-VMHost \| Where-Object {$_.ConnectionState -ne "Connected"}` | Result should be empty |
| Unexpected powered-off VMs | `Get-VM \| Where-Object {$_.PowerState -eq "PoweredOff"}` | Flag unexpected powered-off VMs |
| Snapshots older than 3 days | `Get-VM \| Get-Snapshot \| Where-Object {$_.Created -lt (Get-Date).AddDays(-3)}` | Flag old snapshots |
| Certificate expiry | VAMI → Certificate Management | Flag any expiring within 60 days |
| Recent task failures | vCenter Monitor → Tasks | Review error-level tasks |

## Change Readiness Checklist

- [ ] vCenter backup is current — file-based backup or VAMI snapshot completed and verified
- [ ] No active DRS migrations in progress — confirm vCenter Tasks pane is idle
- [ ] HA admission control capacity checked
- [ ] Certificates valid for more than 30 days
- [ ] SSO and PSC health confirmed before any appliance-level change
- [ ] Rollback plan documented: VCSA restore procedure confirmed and tested
- [ ] Change window approved and communicated to all dependent teams

## When to Restore from Backup

Troubleshoot first if:
- Services can be restarted and recovered
- Disk space can be freed to restore normal function
- A single certificate or SSO issue can be repaired in place

Restore from backup if:
- Database is corrupt
- STS certificate cannot be repaired
- Services fail to start after all troubleshooting steps
- The appliance is unrecoverable after a hardware or VM failure

---

## See also

- [vCenter Troubleshooting — Common Issues](../../troubleshooting/common-issues/)
- [vCenter — Procedures](../procedures/)
- [vCenter — CLI Reference (PowerCLI & DCLI)](../cli-reference/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
