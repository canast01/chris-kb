# Dell Unity

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

Dell Unity is a mid-range unified storage platform supporting block (Fibre Channel and iSCSI), file (NFS and SMB), and VMware (NFS datastores and VMFS over iSCSI/FC) workloads from a single system. It uses a dual storage processor (SP A / SP B) active-active architecture and is available as Unity XT (physical hardware) and UnityVSA (software-defined virtual appliance). Administration is via the Unisphere for Unity GUI or the `uemcli` command-line interface.

## Where It Fits

- Consolidated block and file storage for mid-size environments that want a single management interface
- VMware environments requiring NFS datastores or VMFS LUNs with VAAI integration
- Workloads requiring inline data reduction (compression and deduplication) on a hybrid or all-flash pool
- Disaster recovery configurations using native Unity replication sessions to a secondary array
- Environments tiering hot I/O to FAST Cache (SSD read/write cache) without full all-flash investment
- Dev/test environments that benefit from thin-cloned snapshots for rapid provisioning

## Daily Checks

- Check system health: `uemcli /env/health show -filter "health.value ne OK"` — any non-OK component requires investigation
- Review active alerts: `uemcli /sys/alert show` — triage by severity and acknowledge resolved alerts
- Check pool capacity: `uemcli /stor/pool show -detail` — alert if any pool approaches 80% subscribed or consumed
- Verify both storage processors are online and in a normal state in Unisphere or via `uemcli /env/sp show`
- Check replication session status: `uemcli /rep/session show` — confirm all sessions are in Active state with no errors
- Review current software version and pending updates: `uemcli /sys/sw show`
- Confirm snapshot schedules are running and snapshots are not consuming unexpected capacity: `uemcli /stor/snap show`

## Health Commands

~~~bash
# Show all components that are not in an OK health state
uemcli /env/health show -filter "health.value ne OK"

# Show detailed pool capacity, health, and FAST Cache status
uemcli /stor/pool show -detail

# Show all LUNs with their pool assignment and capacity
uemcli /store/lun show

# Show all network interfaces and their SP assignment
uemcli /net/if show

# Show all active system alerts
uemcli /sys/alert show

# Show installed software version and pending OE upgrades
uemcli /sys/sw show

# Show all snapshots and their parent resource
uemcli /stor/snap show

# Show all replication sessions and their current state
uemcli /rep/session show
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Pool capacity threshold alert | Thin-provisioned LUNs consuming more space than expected, or snapshot accumulation | Review pool detail with `uemcli /stor/pool show -detail`; delete unneeded snapshots; expand pool or add drives |
| SP failover (SP A or SP B offline) | SP hardware fault, OE software panic, or planned maintenance | Check Unisphere alerts and SP fault LED; SP B automatically takes over LUN ownership from SP A; open Dell support case for unplanned failover |
| NFS stale file handle after SP failover | NFS client cached the original SP's IP and the interface moved to the peer SP | Remount the NFS export on affected clients; ensure NFS clients use the management DNS name rather than a hard-coded SP IP |
| Replication session broken or paused | Network interruption between source and destination arrays, or destination pool full | Check `uemcli /rep/session show`; resolve network or capacity issue; resume session with `uemcli /rep/session -id <id> resume` |
| Disk fault in pool | Physical drive failure; Unity automatically begins rebuilding if a hot spare is available | Check `uemcli /env/health show -filter "health.value ne OK"` for the faulted disk; replace physical drive; verify rebuild progress in Unisphere |
| Pool over-subscribed warning | Sum of thin LUN allocated sizes exceeds physical pool capacity | Review thin LUN consumption vs. allocated size; reclaim space or expand the pool |

## Operational Tasks

- Create a new storage pool with drive selection and RAID type via `uemcli /stor/config/pool create`
- Provision a block LUN and map it to a host: `uemcli /store/lun create` then `uemcli /map/lunhostmap create`
- Create an NFS export for a NAS server: `uemcli /net/nas/nfs create`
- Expand an existing pool by adding drives: `uemcli /stor/config/pool -id <pool_id> expand`
- Create a snapshot of a LUN or file system on demand: `uemcli /stor/snap create -storRes <resource_id> -name <snap_name>`
- Configure or expand FAST Cache: `uemcli /stor/config/fastcache create` (requires SAS Flash 2 drives in RAID 1 pairs)
- Enable data reduction on a pool: ensure flash tier is at least 10% of total pool capacity, then enable via Unisphere or `uemcli /stor/config/pool`
- Test SP failover by triggering a manual SP restart in Unisphere during a maintenance window and confirming LUN access is maintained

## Upgrade Notes

1. Run `uemcli /env/health show -filter "health.value ne OK"` and resolve all faults before beginning; do not upgrade with a degraded pool or faulted SP
2. Confirm both SP A and SP B are online and in normal state — the upgrade process restarts each SP sequentially and requires both to be healthy
3. Download the OE upgrade package from Dell support and upload it to the array via Unisphere or `uemcli /sys/sw upload`
4. Verify the upgrade package checksum against the Dell-published hash before proceeding
5. Initiate the upgrade from Unisphere (Maintenance > Software Upgrades) or `uemcli /sys/sw upgrade` — the system upgrades SP B first, then SP A, with I/O continuing via the active SP throughout
6. Monitor upgrade progress in Unisphere; each SP restart takes several minutes — do not interrupt the process
7. After upgrade, verify both SPs return to normal health, confirm `uemcli /sys/sw show` shows the new version, and re-check all replication sessions and pool health

## Best Practices

- Set pool capacity alerts at 70% and 80% consumed — Unity will automatically invalidate snapshots and replication sessions when a pool falls below 5% free, which can cause data loss
- Use FAST Cache (SSD tier) for random I/O workloads such as databases and VMs; do not enable FAST Cache for sequential or large-block workloads such as database logs or backup streams
- Enable inline data reduction (compression and deduplication) on all-flash pools — ensure the flash tier is at least 10% of total pool capacity before enabling
- Create separate pools per service tier (production, dev/test, archive) rather than combining workloads in a single pool to contain the blast radius of capacity events
- Test SP failover during a scheduled maintenance window at least once per year to confirm that NFS and iSCSI hosts recover correctly
- Use the Unisphere Health Check (`uemcli /sys/general healthcheck`) regularly and before any maintenance to surface latent faults
- Do not hard-code SP A or SP B IP addresses in NFS mounts or iSCSI initiator configurations; always use the management virtual IP or DNS name that follows the active SP
