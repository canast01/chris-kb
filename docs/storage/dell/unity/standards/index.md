# Dell Unity Standards
## Naming Conventions

Consistent naming across Unity objects simplifies identification, scripting, and troubleshooting. Apply the following scheme across all Unity deployments.

| Object | Format | Example |
|---|---|---|
| LUN | `<env>-<app>-lun<nn>` | `prod-oracle-lun01`, `dev-mssql-lun02` |
| Storage Pool | `pool-<tier>` | `pool-performance`, `pool-capacity`, `pool-flash` |
| NAS Server | `nas-<env>-<nn>` | `nas-prod-01`, `nas-dev-01` |
| Filesystem | `fs-<app>-<env>` | `fs-oracle-prod`, `fs-home-dev` |
| Snapshot | `<resource>.<YYYYMMDD>` | `prod-oracle-lun01.20260506`, `fs-oracle-prod.20260506` |
| Snapshot Schedule | `sched-<resource>-<frequency>` | `sched-prod-lun01-daily`, `sched-fs-oracle-weekly` |
| Replication Session | `rep-<source-array>-<dest-array>-<resource>` | `rep-unity01-unity02-prod-oracle-lun01` |
| Host | `<hostname>` (match CMDB/DNS name exactly) | `db-prod-01`, `esxi-prod-04` |
| NFS Export | `<filesystem>-<access-type>` | `fs-oracle-prod-ro`, `fs-home-dev-rw` |
| SMB Share | `<app>-<env>` | `oracle-prod`, `home-dev` |

## Build Baseline

Every Unity deployment should be built to the following baseline before handover to operations:

**Pool Configuration**

- Production performance pools: RAID-10 using 10K SAS or NVMe drives.
- Production capacity pools: RAID-5 (4+1) using NL-SAS drives.
- All-flash pools: RAID-5 or RAID-6 with data reduction (compression + deduplication) enabled.
- FAST Cache enabled for pools with mixed or random I/O profiles; disabled for backup or sequential workloads.
- Pool capacity alerts set at 70% and 80% subscribed in Unisphere.

**System Configuration**

- NTP configured with at least two NTP sources — verify with `uemcli /net/ntp show`.
- DNS configured for management and NAS server interfaces.
- Syslog forwarding enabled to the central syslog server — `uemcli /sys/syslog create`.
- SNMP configured for monitoring integration if required by site standards.
- Email notifications enabled for all CRITICAL and ERROR alerts.
- LDAP or Active Directory authentication configured for Unisphere admin access.
- SupportAssist (SRS/ESRS) enabled and verified calling home to Dell.

**Security Baseline**

- Default admin password changed on first login.
- TLS 1.0 and 1.1 disabled; TLS 1.2 or higher enforced.
- Unused protocols (FTP, Telnet on management) disabled.
- D@RE (Data at Rest Encryption) enabled if the hardware supports it.

## Configuration Checklist

Complete this checklist before signing off a new Unity deployment or a post-upgrade validation:

- [ ] Both SP A and SP B online and healthy (`uemcli /env/sp show`)
- [ ] All drive enclosures discovered and drives in Normal state
- [ ] Storage pools created with correct RAID level and capacity alerts configured
- [ ] FAST Cache configured and enabled on applicable pools
- [ ] Data reduction enabled on flash pools
- [ ] NTP synced and confirmed on both SPs
- [ ] DNS resolves management IPs and NAS server IPs
- [ ] Syslog forwarding verified (test message received at syslog server)
- [ ] Email notification tested (test alert delivered to recipients)
- [ ] LDAP/AD authentication configured and a test admin login succeeds
- [ ] SupportAssist connectivity confirmed (Settings > Support > SupportAssist)
- [ ] FC zoning or iSCSI IQN registration completed for all production hosts
- [ ] Replication sessions created and in Active state for all protected resources
- [ ] Snapshot schedules created and first scheduled snapshot confirmed
- [ ] Unisphere health check passing (`uemcli /sys/general healthcheck`)
