# PowerScale — Standards

## Sizing Guidelines

| Dimension | Guidance |
|---|---|
| Minimum cluster size | 3 nodes (OneFS requires minimum 3 for quorum and N+1 protection) |
| Target capacity utilisation | Stay below 80% of usable capacity; OneFS performance degrades above 90% |
| Node type selection | F-series (all-NVMe) for high-IOPS workloads; H-series for mixed; A-series for archive and cold data |
| Protection level | N+2 or N+3 recommended for production clusters; N+1 minimum |
| SmartConnect zones | One IP pool per access zone; at least 3 IPs per pool for effective round-robin balancing |
| SyncIQ bandwidth | Size WAN link to sustain peak change rate; enable SyncIQ throttle for business hours |
| Snapshot retention | Limit snapshot count per policy; large snapshot counts on heavily-changed directories consume metadata space |

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Cluster name | `<site>-ps-<number>` | `lon-ps-01` |
| Access zone | `<business-unit>-zone` | `media-zone`, `hdfs-zone` |
| IP pool | `<zone>-pool-<number>` | `media-zone-pool-01` |
| SmartConnect zone DNS name | `<zone>.<site>.storage.example.com` | `media.lon.storage.example.com` |
| NFS export path | `/ifs/<env>/<bu>/<project>` | `/ifs/prod/media/editorial` |
| SMB share name | `<bu>_<project>` | `media_editorial` |
| SyncIQ policy name | `<src-path-slug>-to-<dst-cluster>` | `editorial-to-ams-ps-01` |
| Snapshot policy name | `<path-slug>-snap-<frequency>` | `editorial-snap-daily` |
| Quota path | Matches NFS export path | `/ifs/prod/media/editorial` |

## Build Baseline

Every new PowerScale cluster or access zone deployment must meet the following before handover:

- **OneFS version**: deploy at N-1 or current GA; patch level at latest available fix.
- **Back-end network**: dedicated VLAN or physical switch for intra-cluster traffic; no client traffic allowed on back-end.
- **SmartConnect**: DNS delegation confirmed and tested; connection balancing policy set to `Round Robin` or `CPU Usage` per workload.
- **Authentication**: Active Directory provider joined for each access zone requiring Windows/SMB clients; NIS or LDAP configured for Unix/NFS clients.
- **Protection level**: set to N+2 minimum on all production directories.
- **SmartPools**: tiering policy reviewed; `Requested protection` default set per node pool.
- **SyncIQ**: replication policies created for all production paths with RPO defined; initial seed complete.
- **Quotas**: advisory, soft, and hard quota thresholds applied to all shared directories before production data lands.
- **Snapshots**: SnapshotIQ policy configured with at minimum 7-day daily retention for each production path.
- **CloudIQ / SNMP**: monitoring integration confirmed; node-down and capacity alerts enabled.
- **NTP**: cluster NTP configured and synchronised — required for Kerberos authentication and SyncIQ consistency.

## Configuration Checklist

- [ ] Cluster registered in CMDB with serial numbers, site, and owning team
- [ ] Back-end network connectivity verified between all nodes (`isi network interfaces list`)
- [ ] Access zones created per business unit; correct IP pools assigned
- [ ] SmartConnect DNS delegation verified with `nslookup <sc-zone-dns-name>`
- [ ] Active Directory or LDAP authentication joined and tested per zone
- [ ] NFS exports created with correct client permissions and root squash settings
- [ ] SMB shares created with correct ACL inheritance and ABE settings
- [ ] Quotas applied to all project directories; hard limits tested
- [ ] SyncIQ policies running; first replication completed without error
- [ ] Snapshot policies active; snapshot accessibility tested via `.snapshot` path
- [ ] SNMP or CloudIQ monitoring confirmed; test alert received
- [ ] Firewall rules confirmed: NFS 2049, SMB 445, HDFS 8020 open as required
