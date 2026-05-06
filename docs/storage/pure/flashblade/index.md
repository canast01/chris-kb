# Pure FlashBlade

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>purefb commands for file systems, object store, snapshots, replication, network, and hardware.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Python REST API health check, filesystem capacity report, ActiveDR monitor, and Bash scripts.</span>
</a>

</div>

## Overview

Pure Storage FlashBlade is an all-flash scale-out storage platform running Purity//FB OS, designed for unstructured data workloads including AI/ML, analytics, backup, and high-performance computing. Each chassis holds multiple blades that combine compute and NVMe flash storage, allowing capacity and performance to scale together by adding blades. It natively serves NFS v3/v4.1, SMB 2/3, S3 object, and HDFS protocols from a single platform, and supports asynchronous replication (ActiveDR) and synchronous replication (ActiveCluster for file systems) for data protection.

## Where It Fits

- AI/ML training data repositories requiring high-throughput parallel access from GPU clusters via NFS or S3
- High-performance backup target for Veeam, Commvault, and Veritas using the Rapid Restore integration
- Object storage for analytics pipelines consuming S3-compatible data with high concurrency
- Unstructured data consolidation replacing legacy NAS filers with a single scale-out platform
- HDFS-compatible storage for Hadoop-based analytics workloads without requiring a full Hadoop cluster
- Disaster recovery target using ActiveDR asynchronous replication from a primary FlashBlade or FlashArray

## Daily Checks

- Check active alerts: `purefb alert list` — review any hardware, capacity, or replication warnings
- Check blade health: `purefb blade list` — confirm all blades are in `healthy` state with no `failed` or `missing` entries
- Review hardware component status: `purefb hardware list` — confirm no failed power supplies, fans, or FMs (fabric modules)
- Check filesystem capacity and utilization: `purefb filesystem list` — confirm no filesystems are approaching their limit
- Check S3 bucket usage and object counts: `purefb bucket list`
- Review replication status: `purefb replication list` — confirm ActiveDR links are healthy and lag is within RPO
- Review recent snapshots and confirm expiry policy is functioning: `purefb snap list`
- Check network interface status: `purefb network interface list` — confirm all data and replication interfaces are `up`

## Health Commands

~~~bash
# Show array name, Purity version, and overall status
purefb array list

# List all blades with health state and capacity contribution
purefb blade list

# List all hardware components (FMs, PSUs, fans) and their status
purefb hardware list

# List all filesystems with provisioned and used capacity
purefb filesystem list

# List all S3 buckets
purefb bucket list

# List all active alerts
purefb alert list

# List snapshots for filesystems and object store
purefb snap list

# Show replication links and lag for ActiveDR relationships
purefb replication list

# List all network interfaces and their status
purefb network interface list
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Blade in `failed` or `missing` state | Physical blade failure or seating issue | Run `purefb blade list` to confirm; open a Pure support case immediately — capacity and performance will be degraded until replaced |
| NFS mounts showing stale file handle errors after FlashBlade maintenance | Client-side NFS state was not cleaned up after a FlashBlade controller event | Unmount and remount the NFS filesystem on affected clients; for persistent mounts check `/etc/fstab` uses `soft` or `intr` options |
| S3 access key returning 403 Forbidden | S3 access key expired, suspended, or IAM policy does not grant the required permissions | Run `purefb objectstoreaccount list` and verify key status; regenerate key or review bucket policy and user permissions |
| ActiveDR replication lag exceeding RPO | Network bandwidth insufficient for change rate, or replication link is down | Run `purefb replication list` to check lag and link status; verify network path between sites; check for bandwidth saturation on replication interfaces |
| Filesystem approaching provisioned limit | Organic data growth or backup tool writing more data than expected | Expand the filesystem limit: `purefb filesystem setattr --size <new_size> <fsname>`; review backup retention policy to expire older data |
| SMB client unable to access share after AD password change | FlashBlade machine account password or AD bind credentials have expired | Rejoin the FlashBlade to Active Directory or update the AD bind credentials in the FlashBlade AD configuration |

## Operational Tasks

- Create a new NFS filesystem: `purefb filesystem create --size <size> --nfs --nfs-rules '<export_policy>' <fsname>`
- Create a new S3 bucket: `purefb bucket create --account <account_name> <bucketname>`
- Create an S3 object store account and access key: `purefb objectstoreaccount create <account>` then `purefb objectstoreuser create --account <account> <username>`
- Set up an ActiveDR replication link to a remote FlashBlade: configure a connection on both arrays, then create a filesystem replica link with `purefb replication fslink create`
- Take a filesystem snapshot on demand: `purefb snap create --filesystem <fsname> <snapname>`
- Restore a filesystem from snapshot: create a new filesystem from the snapshot or overwrite using `purefb filesystem copy`
- Expand an existing filesystem: `purefb filesystem setattr --size <new_size> <fsname>` — expansion is non-disruptive to connected clients
- Add a new blade to scale capacity: insert blade physically, then use `purefb blade add` — the system automatically rebalances data across blades

## Upgrade Notes

1. Log into Pure1 to review the FlashBlade upgrade readiness report — Pure1 pre-checks the target Purity//FB version against your configuration and flags any blockers
2. Confirm all blades are in `healthy` state (`purefb blade list`) and no hardware alerts are open before beginning the upgrade
3. Notify NFS, SMB, and S3 clients of a potential brief reconnection event during the upgrade; FlashBlade upgrades are non-disruptive but protocol sessions may briefly re-establish
4. Download the Purity//FB upgrade image from the Pure Support portal and stage it on the array
5. Run the pre-upgrade validation to confirm the system is ready to upgrade without warnings
6. Execute the upgrade during a maintenance window and monitor progress from the Purity GUI or CLI
7. After upgrade, verify all filesystems, buckets, and replication links are healthy: `purefb filesystem list`, `purefb replication list`, and `purefb alert list`

## Best Practices

- Separate filesystems per application or team rather than sharing a single large filesystem — this enables independent capacity limits, snapshot schedules, and replication policies per workload
- Use S3 lifecycle policies (object expiry rules on buckets) to automatically expire old objects and prevent uncontrolled storage growth for analytics or backup workloads
- Configure Pure1 monitoring with capacity threshold alerts (e.g., at 70% and 85% used) and hardware fault notifications so issues are caught before they impact operations
- Test ActiveDR failover and failback procedures at least annually — include NFS and S3 client remounting steps in the DR runbook, not just the FlashBlade-side commands
- Use SAML/SSO integration for admin access rather than local accounts — this enforces MFA, enables central access revocation, and provides audit trail through your identity provider
- For backup workloads (Veeam, Commvault), use a dedicated filesystem per backup tier (daily, weekly, monthly) with matching snapshot retention so recovery points are easy to identify and manage
- Set NFS export policies to restrict client IP ranges to authorized subnets only — avoid exporting with `*` (all hosts) in production environments
- Monitor replication lag daily and define a documented RPO threshold; set alerts when lag exceeds the acceptable window rather than discovering breaches during an incident
