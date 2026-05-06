# FlashBlade Standards

## Naming Conventions

| Object | Pattern | Example |
|---|---|---|
| Filesystem | `<env>-<team>-<purpose>` | `prod-ml-training-data` |
| Filesystem (backup) | `<env>-<source_system>-<tier>` | `prod-veeam-daily` |
| S3 bucket | `<env>-<team>-<purpose>` (lowercase, no underscores) | `prod-analytics-raw` |
| Object store account | `<team>` or `<application>` | `ml-platform` |
| Object store user | `<service_account_name>` | `svc-veeam-backup` |
| NFS export path | `/<env>/<team>/<purpose>` | `/prod/ml/training-data` |
| SMB share | `<ENV>-<TEAM>-<PURPOSE>` | `PROD-ANALYTICS-SHARE` |
| Snapshot (filesystem) | `<fsname>.<purpose>.<date>` | `prod-ml-training-data.weekly.20260501` |
| Replica link | `<source_fs>-to-<remote>` | `prod-ml-training-data-to-dr` |
| Array name | `<site>-fb-<seq>` | `lon-fb-01` |

## Build Baseline

Required settings to configure on every new FlashBlade before it enters production:

- [ ] Set array name to match naming convention
- [ ] Configure DNS servers and domain
- [ ] Configure NTP servers and validate time sync
- [ ] Set timezone
- [ ] Configure syslog forwarding to central log aggregator
- [ ] Configure SMTP alert relay and admin email alert recipients
- [ ] Join Active Directory (for SMB authentication and admin LDAP)
- [ ] Configure LDAP for NFS user/group ID mapping if required
- [ ] Create local break-glass admin account; store credentials in PAM vault
- [ ] Disable default admin account after AD/LDAP is validated
- [ ] Enable Pure1 phone-home and verify connectivity
- [ ] Configure management interface on dedicated management VLAN
- [ ] Configure data interfaces on dedicated data VLANs (separate NFS, SMB, S3 as needed)
- [ ] Configure replication interface on a dedicated replication VLAN
- [ ] Configure NFS export policies to restrict client IP access to authorised subnets (no `*` in production)
- [ ] Configure SMB share-level permissions and integrate with AD security groups
- [ ] Enable Safe Mode (immutable snapshots) — engage Pure Support to enable
- [ ] Apply SSL certificate from internal CA on management interface
- [ ] Document blade count, chassis serial, management IP, Purity//FB version, and network VIPs in CMDB

## Configuration Checklist

Ordered steps for initial FlashBlade setup:

1. **Rack and cable** — install chassis, connect dual power supplies to separate PDUs, connect management Ethernet, connect data Ethernet (10/25/100 GbE), connect replication Ethernet
2. **Initial access** — connect to management IP via browser or SSH; complete initial setup wizard (set management IP, gateway, DNS)
3. **Set array name and timezone** — configure array name to match naming convention; set timezone and NTP
4. **Register in Pure1** — register the FlashBlade serial number in Pure1 to activate licensing and monitoring
5. **Configure data interfaces** — assign IP addresses to data VIPs for NFS, SMB, and S3 protocol services; bind to correct VLANs
6. **Configure replication interface** — assign IP to the replication VLAN; verify reachability to DR site
7. **Configure alert notifications** — SMTP relay and admin email addresses
8. **Configure syslog forwarding** — forward to SIEM or log aggregator
9. **Configure authentication** — join AD for SMB and admin auth; configure LDAP for NFS UID/GID mapping if required; create role-mapped admin groups
10. **Apply security hardening** — see security/index.md
11. **Create filesystems** — provision filesystems using naming convention; set capacity limits appropriate for each team or workload
12. **Configure NFS exports** — set export policies with source IP restrictions; configure NFSv4.1 pNFS if required for high-throughput HPC or AI/ML workloads
13. **Configure SMB shares** — set share-level permissions mapped to AD groups; enable SMB encryption if required
14. **Create object store accounts and buckets** — create per-team or per-application S3 accounts; create buckets with lifecycle policies
15. **Configure snapshot schedules** — create per-filesystem snapshot policies with appropriate retention (daily/weekly/monthly) aligned with application RPO
16. **Configure replication** (if required) — set up replica links to the remote FlashBlade for ActiveDR; verify lag is within RPO
17. **Validate and document** — confirm all filesystems, exports, and buckets are accessible; run `purefb alert list` and `purefb blade list`; record build in CMDB
