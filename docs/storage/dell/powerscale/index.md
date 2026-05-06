# Dell PowerScale

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>isi commands for cluster status, NFS, SMB, snapshots, SyncIQ, quotas, auth, and statistics.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Perl cluster health check, SyncIQ monitor, quota report, and Ansible playbook.</span>
</a>

</div>

## Overview

Dell PowerScale (formerly Isilon) is a scale-out NAS platform running the OneFS distributed operating system, where all nodes form a single shared namespace under `/ifs`. Clusters scale from 3 to 252 nodes, with each node added linearly increasing both capacity and throughput. PowerScale supports multi-protocol access including NFS, SMB/CIFS, HDFS, S3, and FTP from the same file system.

## Where It Fits

- Unstructured data at scale: media and entertainment workflows, genomics, EDA, home directories
- Multi-protocol environments where the same data must be accessible via NFS and SMB simultaneously
- Hadoop and analytics workloads using HDFS access directly against `/ifs`
- Disaster recovery and data replication targets via SyncIQ asynchronous replication
- Tiered storage environments using SmartPools to automatically migrate data across SSD, SAS, and SATA node pools
- Object storage workloads via the S3-compatible access zone interface

## Daily Checks

- Run `isi status` to confirm all nodes are online and no node is in a SMARTFAIL or DOWN state
- Run `isi event list` and filter for CRITICAL or ERROR severity events that require action
- Check cluster capacity with `isi storagepool list` — alert if any tier exceeds 80% used
- Verify SyncIQ policy health with `isi sync policies list` and review recent job outcomes with `isi sync reports list`
- Check for quota violations with `isi quota list` — look for directories that have exceeded soft or hard thresholds
- Confirm active cluster jobs with `isi job list` — note any jobs in a PAUSED or FAILED state
- Review CPU and throughput statistics with `isi statistics query current --keys CPU` for any nodes showing sustained high utilisation

## Health Commands

~~~bash
# Overall cluster node and drive health summary
isi status

# List all active and recent cluster background jobs
isi job list

# List all storage pool tiers and their capacity usage
isi storagepool list

# List all SmartQuota entries
isi quota list

# List SyncIQ replication policies and their last run status
isi sync policies list

# Show the last replication reports for all SyncIQ policies
isi sync reports list

# Show all cluster events (filter for CRITICAL to triage)
isi event list

# Query current per-node CPU statistics
isi statistics query current --keys CPU

# List all configured network subnets and SmartConnect zones
isi network subnets list

# Show installed OneFS version and license status
isi license list
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| SyncIQ policy stuck or failing | Network interruption, target cluster unreachable, or snapshot conflict | Run `isi sync reports list` for the policy; check network reachability to target; resolve snapshot conflicts and re-run |
| Write failures on a quota-managed directory | Hard quota threshold exceeded | Run `isi quota list` to identify the directory; raise or remove the hard limit, or delete data to free space |
| SmartConnect DNS name not resolving for a zone | Zone delegation missing or DNS zone misconfigured | Check that the parent DNS zone has an NS record delegating the SmartConnect zone to the cluster; verify with `isi network subnets list` |
| Node showing SMARTFAIL in `isi status` | Drive failures or node hardware fault caused OneFS to begin removing the node from the cluster | Do not remove the node manually; monitor `isi job list` for the Restripe job completing; open a Dell support case |
| Drive failure with no automatic rebuild | Drive in REPLACE state but no spare capacity | Check `isi status` for drive details; confirm the storage pool has available capacity for restripe; replace physical drive |
| Cluster capacity unexpectedly full | Snapshot accumulation or runaway data ingest | Review snapshot usage with `isi snapshot list`; delete expired or unneeded snapshots; identify large directories with `isi quota list` |

## Operational Tasks

- Add a new access zone for a client group with `isi zone zones create` and assign a dedicated SmartConnect zone and IP pool
- Create a SmartQuota with advisory, soft, and hard thresholds: `isi quota quotas create --path /ifs/data/project --type directory --hard-threshold 10T --soft-threshold 9T --advisory-threshold 8T`
- Create and run a SyncIQ replication policy: `isi sync policies create` and trigger with `isi sync policies run <name>`
- Create a point-in-time snapshot: `isi snapshot snapshots create --path /ifs/data/project --name daily-$(date +%Y%m%d)`
- Review and modify SmartPool tiering policies to ensure hot data resides on SSD nodes
- Expand the cluster by adding a new node and running `isi devices drive format` once hardware is cabled
- Monitor SmartConnect load balancing across IP pools with `isi network pools list`
- Confirm OneFS patch level and schedule upgrades using `isi upgrade cluster upgrade` in parallel upgrade mode

## Upgrade Notes

1. Run `isi status` and resolve all node and drive errors before beginning; do not upgrade with a node in SMARTFAIL or DOWN state
2. Verify the target OneFS version is within the supported upgrade path from the current version using the Dell upgrade compatibility matrix
3. Confirm all SyncIQ policies are in a healthy completed state; pause scheduled policies during the upgrade window
4. Download the upgrade image to `/ifs/data/` and verify the checksum against the Dell-published hash
5. Initiate a parallel upgrade (recommended for OneFS 8.2.2 and later): `isi upgrade cluster upgrade --parallel` — this upgrades all nodes simultaneously with a smaller maintenance window than rolling upgrades
6. Monitor progress with `isi upgrade view` until all nodes report the new version
7. After upgrade, run `isi status`, `isi license list`, and re-enable any SyncIQ policies that were paused; verify client NFS and SMB access

## Best Practices

- Design access zones per client group or business unit rather than per individual volume — this simplifies protocol and authentication policy management
- Always configure three quota threshold levels (advisory, soft with grace period, hard) on user-facing directories to prevent sudden write failures
- Validate SyncIQ RPO and RTO regularly by checking the last successful replication timestamp in `isi sync reports list` against your recovery objectives
- Use SmartConnect zones with round-robin or CPU-based connection balancing to distribute NFS and SMB client connections evenly across nodes
- Keep OneFS within N-2 versions of the current release to remain within Dell's supported upgrade paths and receive security patches
- Do not store data outside of `/ifs` — all persistent data must reside within the cluster file system to benefit from protection and replication
- Monitor per-node performance with `isi statistics` regularly to identify hot nodes; rebalance workloads across access zones if persistent imbalance is observed
