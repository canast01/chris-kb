# Dell Data Domain

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>HA topology, components, connectivity, and sizing.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Naming conventions, build baseline, and configuration checklist.</span></a>
<a class="kb-card" href="lifecycle/"><strong>Lifecycle</strong><span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Command reference by category with syntax and examples.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for daily checks, health, incident triage, and validation.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic commands, log locations, and error codes.</span></a>
<a class="kb-card" href="integration/"><strong>Integration</strong><span>VMware, backup tools, monitoring, authentication, and API integration.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span></a>
<a class="kb-card" href="vendor-support/"><strong>Vendor Support</strong><span>Opening a case, information to collect, support portal, and SLA tiers.</span></a>
</div>

## Overview

Dell PowerProtect DD (Data Domain) is a purpose-built backup appliance that performs inline global deduplication as data is written, achieving typical reduction ratios of 20:1 or higher. It serves as a backup target for leading data protection software via DDBoost, NFS, CIFS, and VTL interfaces. MTrees provide logical partitioning of the DD filesystem, enabling multi-tenant or per-application isolation of backup streams.

## Where It Fits

- Backup target for Avamar, NetWorker, Veeam, Commvault, and other backup software via DDBoost protocol
- Deduplication landing zone for long-term backup retention and tape replacement
- Replication target for disaster recovery — MTree or collection replication to a remote DD
- Cloud tier gateway for offloading aged backup data to AWS S3, Azure Blob, or Elastic Cloud Storage
- Multi-tenant backup storage — separate MTrees per business unit or application owner
- Integration with copy data management workflows where a deduplicated source is required

## Daily Checks

- Run `alerts show current` to review any active hardware or software alerts
- Run `filesys show space` to confirm pre- and post-compression capacity usage and headroom
- Run `filesys show compression` to verify the global dedup ratio (healthy is 20:1+; investigate if it drops significantly)
- Run `replication show` to confirm all replication contexts are in `Normal` or `Replicating` state
- Run `ddboost show clients` to verify DDBoost-connected backup servers are active and authenticated
- Check `filesys status` to confirm the filesystem is enabled and running
- Review `system show` for hardware health (fans, PSUs, disk status)

## Health Commands

~~~bash
# Check filesystem status and whether it is enabled
filesys status

# Show pre- and post-compression space usage
filesys show space

# Show global deduplication and compression ratio
filesys show compression

# List all replication contexts and their current state
replication show

# Show detailed replication lag and throughput per context
replication status

# List all MTrees and their individual space usage
mtree list

# Show per-MTree dedup ratio
mtree show compression mtree /data/col1/<mtree-name>

# List DDBoost-connected clients and storage units
ddboost show clients
ddboost status

# Show currently active alerts
alerts show current

# Show system hardware and software version info
system show
net show all

# Show admin access and user configuration
adminaccess show
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Replication context stuck in `Replicating` or falling behind | Network bandwidth saturation, high ingest rate on source, or target filesystem full | Run `replication show` to check lag; run `filesys show space` on target; throttle if needed with `replication throttle` |
| Capacity usage not reclaiming after deletions | Filesystem cleaning not run after deletes | Run `filesys clean start`; clean physically removes unreferenced chunks from disk |
| DDBoost client authentication error | Expired or mismatched DDBoost user certificate or password | Re-register storage unit in backup software; verify DDBoost user with `ddboost show clients` |
| Low dedup ratio (below 10:1) | Encrypted or already-compressed data streams, unique data (databases, VMs with change), or first-pass backup | Run `filesys show compression`; confirm data type; check if DDBoost source-side dedup is enabled in backup software |
| Filesystem not enabled after reboot | Filesys did not auto-start or hardware fault prevented mount | Run `filesys status`; if disabled, run `filesys enable` and review alerts |
| Alert: disk in `Absent` or `Failed` state | Physical disk failure or loose connection | Run `disk show state`; open a Dell support case for disk replacement under maintenance |

## Operational Tasks

- Create a new MTree with `mtree create /data/col1/<name>` and set soft/hard quotas
- Register a DDBoost storage unit in the backup application and map it to the new MTree
- Configure MTree replication: `replication add source mtree://<src-dd>/data/col1/<name> destination mtree://<dst-dd>/data/col1/<name>`
- Schedule filesystem cleaning: `filesys clean set-frequency weeks 1` (default is weekly on Tuesday at 06:00)
- Monitor and adjust replication throttle schedules with `replication throttle`
- Expand shelf capacity: run `disk show state` to confirm new shelf is recognised, then `filesys expand`
- Rotate DDBoost user credentials and update all backup server registrations
- Review and age out expired MTrees or storage units no longer used by backup jobs

## Upgrade Notes

1. Run `system show` and `adminaccess show` to record current DDOS version and admin configuration before starting
2. Download the target DDOS upgrade package from Dell Support and verify the MD5 checksum
3. Confirm all replication contexts are in `Normal` state with `replication show`; suspend replication with `replication sync` if needed to avoid mid-upgrade inconsistencies
4. Run `filesys clean start` and wait for it to complete before upgrade to reduce post-upgrade clean time
5. Upload the upgrade package via `system upgrade` or the System Manager GUI; DDOS upgrades are non-disruptive for most minor versions but verify the release notes
6. After upgrade, run `filesys status`, `replication show`, and `alerts show current` to confirm all services are healthy
7. Re-validate DDBoost connectivity from each backup server and run a test backup and restore

## Best Practices

- Schedule `filesys clean` no more than once per week; running it more frequently can cause disk fragmentation and degrade restore and replication performance
- Target a global dedup ratio of 20:1 or better; investigate drops with `filesys show compression` before they become capacity issues
- Use MTree replication (not collection replication) for granular per-application or per-tenant replication control
- Set MTree soft and hard quotas to prevent a single backup stream from consuming all available capacity
- Enable DD Encryption at Rest (D@RE) during initial setup; retroactively enabling it requires a filesys rebuild
- Keep at least 10–15% of raw capacity free to allow the filesystem cleaner to operate efficiently
- Monitor DDBoost client connections regularly; stale or orphaned clients can hold locks that impact performance
- Test end-to-end recovery from the DD target at least quarterly to validate both dedup integrity and restore throughput
