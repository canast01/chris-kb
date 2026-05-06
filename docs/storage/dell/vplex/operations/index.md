# Operations

> Part of the [Dell VPLEX](../) reference.

---

## Daily Checks

Run these vplexcli checks each morning to confirm cluster health, director status, distributed device sync, and Witness connectivity.

- [ ] Check cluster health indications: `ll /clusters/*/health-indications/` — all health-indications should show `health-state: ok`; investigate any cluster showing a non-ok state
- [ ] Check distributed device health: `ll /distributed-storage/distributed-devices/*/health-indications/` — all distributed devices should show `health-state: ok` and `rebuild-allowed: true`; an `out-of-sync` device requires immediate attention
- [ ] Check director hardware health: `ll /engines/*/directors/*/hardware/` — all directors should show healthy component states; a faulted director reduces redundancy and must be escalated
- [ ] Verify Witness connectivity for Metro deployments: `ll /metro-node/*/witness/` — Witness should show `connected: true` and `reachable: true`; loss of Witness connectivity risks I/O suspension on a subsequent site failure
- [ ] Check consistency group state: `ll /distributed-storage/consistency-groups/` — all groups should show `operational-status: ok`
- [ ] Verify storage views are intact for all hosts: `ll /clusters/*/exports/storage-views/` — confirm the expected number of storage views and initiator-to-port mappings
- [ ] Review any active alerts in Unisphere for VPLEX or from email/SNMP notifications for alerts generated overnight

## Health Check

Run these checks before any VPLEX maintenance or as first-response steps when a host reports I/O issues.

- [ ] `ll /clusters/*/health-indications/` — all clusters show `health-state: ok`
- [ ] `ll /distributed-storage/distributed-devices/*/health-indications/` — all distributed devices show `health-state: ok`; no devices in `out-of-sync` or `rebuilding` state
- [ ] `ll /engines/*/directors/*/hardware/` — all directors across all engines are healthy; no director components in a faulted state
- [ ] `ll /metro-node/*/witness/` — Witness is `connected` and `reachable` from both clusters (Metro deployments)
- [ ] `ll /distributed-storage/consistency-groups/` — all consistency groups show `operational-status: ok`
- [ ] `ll /clusters/*/exports/storage-views/` — storage views are present with the expected initiator and port bindings
- [ ] `health-check --full` — system-level health check returns no warnings or errors
- [ ] ICL (inter-cluster link) latency between Metro sites is within the expected sub-10ms threshold

~~~bash
# Check cluster-level health indications
ll /clusters/*/health-indications/

# Check all distributed device health states
ll /distributed-storage/distributed-devices/*/health-indications/

# Check director hardware health across all engines
ll /engines/*/directors/*/hardware/

# Check Witness connectivity (Metro deployments)
ll /metro-node/*/witness/

# Check consistency group operational status
ll /distributed-storage/consistency-groups/

# List all storage views and their initiator-to-port bindings
ll /clusters/*/exports/storage-views/

# Run a full system health check
health-check --full

# Show cluster hardware inventory
ll /clusters/*/hardware/
~~~

## Change Readiness

Verify these items before performing any VPLEX change — GeoSynchrony upgrades, director replacements, back-end storage changes, or storage view modifications.

- [ ] `ll /distributed-storage/distributed-devices/*/health-indications/` — all distributed devices show `health-state: ok`; do not start a change with any device out-of-sync
- [ ] Witness is reachable from both Metro clusters: `ll /metro-node/*/witness/` — loss of Witness during a change that takes a cluster offline will suspend I/O on consistency group volumes
- [ ] All consistency groups show `operational-status: ok`: `ll /distributed-storage/consistency-groups/`
- [ ] Host I/O validated: confirm path counts and multipath state on all hosts using VPLEX storage views (`powermt display dev=all` or `multipath -ll` on connected hosts)
- [ ] Back-end array health confirmed — run health checks on the back-end PowerMax, Unity, or other array before any VPLEX change that touches back-end storage volumes
- [ ] For GeoSynchrony upgrades: confirm target version compatibility with back-end array firmware, hypervisor versions, and host OS multipath drivers from the Dell VPLEX compatibility matrix
- [ ] Confirm VMS (VPLEX Management Server) VM is running and backed up — losing VMS during a change does not impact I/O but makes configuration recovery impossible without a backup
- [ ] Notify application and host owners of the maintenance window; confirm consistency groups can be suspended briefly if needed for the specific change type

| Item | Status | Notes |
|---|---|---|
| All distributed devices health-state: ok | | |
| Witness connected and reachable | | |
| All consistency groups ok | | |
| Host path counts match baseline | | |
| Back-end array health confirmed | | |
| VMS VM backed up | | |

## Incident Triage

When hosts report I/O suspension, a distributed device is out-of-sync, or a director is unreachable, work through this sequence first.

- [ ] Run `ll /clusters/*/health-indications/` immediately — identify which cluster has entered a non-ok health state and note when the state change occurred
- [ ] Check distributed device sync state: `ll /distributed-storage/distributed-devices/*/health-indications/` — an `out-of-sync` device means one leg of the distributed device is not being written to; identify which cluster leg is affected
- [ ] Check Witness status for Metro deployments: `ll /metro-node/*/witness/` — if Witness is unreachable from one cluster and the ICL is also interrupted, VPLEX will suspend I/O on consistency groups to preserve write-order consistency
- [ ] Check director health: `ll /engines/*/directors/*/hardware/` — a director in a faulted state on one engine reduces redundancy and may cause host path failures
- [ ] Verify ICL connectivity between Metro clusters — an ICL interruption is the most common cause of distributed device out-of-sync events; check the WAN or dark fibre connection between sites
- [ ] Check consistency group state: `ll /distributed-storage/consistency-groups/` — identify any groups that have suspended I/O and determine the cause before resuming
- [ ] Verify storage views are intact: `ll /clusters/*/exports/storage-views/` — a missing or corrupted storage view can cause a specific host to lose access to its volumes
- [ ] Run `health-check --full` to get a system-wide view of all faults in a single output; use this output when opening a Dell support case

| Question | Answer |
|---|---|
| Which cluster shows non-ok health-state? | |
| Which distributed devices are out-of-sync? | |
| Is the Witness connected and reachable? | |
| Is the ICL between Metro clusters up? | |
| Which directors or director components are faulted? | |

## Maintenance Window

Steps for planned VPLEX maintenance — director replacement, GeoSynchrony NDU, or site-level switch for Metro workloads.

1. Notify host and application owners of the maintenance window; confirm consistency group volumes can tolerate temporary director redundancy reduction during director-level NDU
2. Confirm `ll /distributed-storage/distributed-devices/*/health-indications/` shows all devices `health-state: ok` before starting; do not start a director upgrade with any device out-of-sync
3. Confirm Witness is reachable from both clusters: `ll /metro-node/*/witness/`; for planned site switch tests, confirm the Witness is in the third failure domain
4. For GeoSynchrony NDU: upgrade one director at a time per engine; after each director upgrade, wait for `ll /engines/*/directors/*/hardware/` to confirm the director returned to healthy state before proceeding to the next
5. After all directors on an engine are upgraded, confirm distributed device health with `ll /distributed-storage/distributed-devices/*/health-indications/` before moving to the next engine
6. For a planned Metro site switch: suspend consistency group I/O cleanly, perform the site switch, verify host I/O resumes on the surviving cluster, then restore Witness and ICL before resuming the original cluster
7. Upgrade the VMS after all directors are at the new GeoSynchrony code level
8. Run `health-check --full` and confirm all clusters, directors, distributed devices, and consistency groups are healthy before closing the maintenance window

## Post-Change Validation

Run these checks after any VPLEX change to confirm the system is healthy and hosts have full path redundancy restored.

- [ ] `ll /clusters/*/health-indications/` — all clusters show `health-state: ok`
- [ ] `ll /distributed-storage/distributed-devices/*/health-indications/` — all distributed devices show `health-state: ok`; no devices in out-of-sync or rebuilding state
- [ ] `ll /engines/*/directors/*/hardware/` — all directors are healthy; no components in a faulted state post-change
- [ ] `ll /metro-node/*/witness/` — Witness is `connected: true` and `reachable: true` from both clusters
- [ ] `ll /distributed-storage/consistency-groups/` — all consistency groups show `operational-status: ok`
- [ ] Host path validation: `powermt display dev=all` or `multipath -ll` on representative hosts shows all paths alive and path count matches the pre-change baseline
- [ ] `health-check --full` returns no warnings or errors
- [ ] Application owners confirm I/O has resumed normally and no elevated latency is observed post-change
