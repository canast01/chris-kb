# NetApp ONTAP

<div class="kb-grid kb-grid-11">
  <div class="kb-card">
    <h3><a href="cli-reference/">CLI Reference</a></h3>
    <p>Cluster, volume, SVM, NFS, CIFS, iSCSI, FC, SnapMirror, and QoS commands.</p>
  
<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Architecture overview, components, and design patterns.</span>
</a>

<a class="kb-card" href="cluster-health/">
  <strong>Cluster Health</strong>
  <span>Cluster Health notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="integration/">
  <strong>Integration</strong>
  <span>Integration with other systems and platforms.</span>
</a>

<a class="kb-card" href="lifecycle/">
  <strong>Lifecycle</strong>
  <span>Installation, upgrades, patching, and decommission.</span>
</a>

<a class="kb-card" href="protocols/">
  <strong>Protocols</strong>
  <span>Protocols notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Security configuration, hardening, and access control.</span>
</a>

<a class="kb-card" href="standards/">
  <strong>Standards</strong>
  <span>Configuration standards, naming conventions, and baselines.</span>
</a>

<a class="kb-card" href="svms/">
  <strong>Svms</strong>
  <span>Svms notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostic steps, and resolution guides.</span>
</a>

<a class="kb-card" href="vendor-support/">
  <strong>Vendor Support</strong>
  <span>Support bundles, case management, and escalation paths.</span>
</a>
</div>
  <a class="kb-card" href="scripts/">
    <strong>Scripts</strong>
    <span>Perl cluster health check, SnapMirror lag monitor, Python volume reporter, and Ansible playbook.</span>
  </a>
  <div class="kb-card">
    <h3><a href="operations/">Operations</a></h3>
    <p>Daily checks, health check, change readiness, incident triage, maintenance window, and post-change validation.</p>
  </div>
</div>

## Overview

NetApp ONTAP is the enterprise storage operating system running on AFF (all-flash), FAS (hybrid flash/disk), and ONTAP Select (software-defined) platforms. It organizes storage in a hierarchy of cluster → nodes → aggregates → SVMs (Storage VMs) → volumes → LUNs or shares, and serves data over NFS, SMB/CIFS, iSCSI, FC, FCoE, NVMe/FC, and S3. Built-in data protection features include SnapMirror for replication, SnapVault for backup retention, and SyncMirror for RAID-level mirroring across disk shelves or HA pairs.

## Where It Fits

- Primary NAS and SAN storage for enterprise applications, databases, and VMware/Hyper-V environments
- Multi-protocol file sharing (NFS for Linux/VMware, SMB for Windows) from a single SVM
- Block storage for Oracle, SQL Server, and other applications via iSCSI, FC, or NVMe/FC
- Disaster recovery and data vaulting using SnapMirror and SnapVault relationships to a secondary cluster or cloud
- High-availability production storage with non-disruptive takeover/giveback via HA pairs and storage failover
- Test/dev environments leveraging writable FlexClone volumes from production snapshots at near-zero space cost

## Daily Checks

- Check overall cluster health: `cluster show`
- Review broken or failed disks: `storage disk show -broken`
- Verify storage failover state: `storage failover show`
- Check volumes approaching capacity: `volume show -fields used-percent`
- Review active health alerts: `system health alert show`
- Confirm SnapMirror relationships are healthy: `snapmirror show`
- Check recent EMS events or AutoSupport callhome messages: `event log show -messagename callhome.*`
- Verify all SVMs and network interfaces are online: `svm show` and `network interface show`

## Health Commands

~~~bash
# Cluster node and HA status
cluster show
storage failover show

# Aggregate capacity and status
storage aggregate show

# Volume space usage across all SVMs
volume show -fields used-percent

# SnapMirror relationship health and lag time
snapmirror show
snapmirror show -fields lag-time

# Broken or failed disks
storage disk show -broken

# Active health alerts
system health alert show

# Recent callhome EMS events
event log show -messagename callhome.*

# Full node hardware configuration
system node run -node local sysconfig -a
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Volume full / write errors to hosts | Volume space exhausted; autogrow not configured or hit its max | Run `volume show -fields used-percent,autosize-mode`; increase max-autosize or delete snapshots with `snapshot delete` |
| Aggregate nearly full (>90%) | Thin-provisioned volumes grew beyond aggregate free space | Run `storage aggregate show`; move volumes to less-full aggregates with `volume move start` or add shelves |
| SnapMirror lag exceeding RPO | Network bandwidth contention, dedupe/SnapMirror scheduling conflict, or throttle set | Check `snapmirror show -fields lag-time`; review schedule; confirm no global throttle with `snapmirror config-replication show` |
| NFS mount hangs after SP takeover | Client holding stale NFS lock; automount not recovering after LIF migration | Verify LIF is on correct port with `network interface show`; unmount and remount on client; check NFS grace period |
| iSCSI session dropped | LIF failover changed IP; host iSCSI initiator did not reconnect | Run `iscsi session show`; confirm LIF IP stability; rescan iSCSI on host; verify multipath |
| Node takeover not auto-triggering | Storage failover disabled or partner unreachable | Run `storage failover show`; check `options cf.mode`; verify cluster interconnect links |

## Operational Tasks

- Create and mount a new FlexVol: `volume create` with junction-path, then verify with `volume show`
- Provision an iSCSI or FC LUN: `lun create` under a volume, then map with `lun mapping create` to an igroup
- Configure SnapMirror replication: peer clusters and SVMs, then create relationship with `snapmirror create` and initialize with `snapmirror initialize`
- Expand a volume or enable autogrow: `volume modify -volume <name> -size <new> -autosize-mode grow_shrink`
- Move a volume between aggregates non-disruptively: `volume move start -volume <name> -destination-aggregate <agg>`
- Create a FlexClone for test/dev: `volume clone create -parent-volume <vol> -junction-path <path>`
- Run storage efficiency (dedup/compression): `storage aggregate efficiency show`; schedule with `volume efficiency on`
- Perform a planned storage failover and giveback: `storage failover takeover` then `storage failover giveback`

## Upgrade Notes

1. Check the NetApp Interoperability Matrix Tool (IMT) and ONTAP upgrade advisor in Active IQ / BlueXP to identify the recommended target release and any required intermediate versions
2. Review the target release notes for known issues, deprecated features, and any manual steps required before or after the upgrade
3. Confirm all SnapMirror relationships are healthy and aggregates are below 90% capacity before beginning
4. Take an AutoSupport message to mark the start of the maintenance window: `autosupport invoke -node * -type all -message "Starting ONTAP upgrade"`
5. Use the automated non-disruptive upgrade (ANDU) path in System Manager or CLI (`system image update-package`) to upgrade one HA pair at a time; verify takeover/giveback completes cleanly after each node
6. After each node upgrade, validate cluster health with `cluster show`, check for any new health alerts, and confirm SnapMirror resumes
7. Post-upgrade, send a closing AutoSupport and review EMS logs for unexpected events

## Best Practices

- Enable volume autogrow with an explicit maximum (`volume modify -autosize-mode grow -max-autosize`) to prevent unexpected out-of-space conditions without allowing unbounded growth
- Set volume space guarantee to `none` for thin provisioning; ensure aggregate free space is monitored continuously to back thin-provisioned volumes
- Keep aggregates below 90% used capacity — above this threshold WAFL metadata operations slow and Snapshot spill-over risk increases
- Configure QoS policies (throughput floors and ceilings) on critical workloads to protect latency-sensitive applications from noisy neighbors
- Enable AutoSupport to allow NetApp proactive support to detect potential hardware failures and send callhome alerts before they become outages
- Schedule SnapMirror and storage efficiency jobs (deduplication, compression) in non-overlapping maintenance windows to avoid resource contention
- Use SVM DR in addition to volume-level SnapMirror for full namespace, NFS export, and CIFS share recovery at the DR site
- Review the Active IQ / BlueXP dashboard weekly for capacity forecasts, performance advisories, and firmware update recommendations
