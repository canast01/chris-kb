# vSphere Replication — Procedures

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│              vSphere Replication — Operational Flow                                                   │
│                                                                                                       │
│  Configure Replication          Monitor + Manage                                                      │
│  ┌────────────────────────┐     ┌────────────────────────┐                                            │
│  │ vCenter → [VM] →       │     │ Pause / Resume         │                                            │
│  │  Configure Replication │     │ Sync Now (immediate)   │                                            │
│  │  RPO: 5min–24hrs       │     │ Change RPO             │                                            │
│  │  Target DS + VRS       │     │ Change target DS       │                                            │
│  │  Quiesce / encrypt     │     └────────────────────────┘                                            │
│  └────────────────────────┘                                                                           │
│                                                                                                       │
│  Recover VM (standalone)        Add to SRM Protection Group                                           │
│  ┌────────────────────────┐     ┌────────────────────────┐                                            │
│  │ Target Site vCenter    │     │ 1. Configure VR on VM  │                                            │
│  │ → Replications →       │     │ 2. Wait for initial    │                                            │
│  │   Recover              │     │    sync (status: OK)   │                                            │
│  │   (Test or actual)     │     │ 3. SRM → PG → Add VMs  │                                            │
│  └────────────────────────┘     └────────────────────────┘                                            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Configure vSphere Replication for a VM

Enables continuous asynchronous replication of a single VM to a recovery site. Use when onboarding a new workload into the DR plan or adding a VM that was missed during initial configuration.

**Prerequisites:** vSphere Replication Appliance (VRA) deployed and registered at both source and target sites. VMware Tools installed on the VM (required for quiescing). Network connectivity on port 31031 between source and target VRS appliances.

**Steps:**

1. In vCenter, right-click the VM and select **vSphere Replication → Configure Replication**.
2. On the **Target site** screen, select the recovery site (e.g., `amsterdam`). Click **Next**.
3. On the **Target location** screen:
   - Select the target vCenter server.
   - Select the target datastore. Ensure it has sufficient free space (at least the provisioned size of the VM plus headroom for replicated instances).
   - Optionally select a specific **Replication Server (VRS)**; leave as **Auto** to let VR balance load.
4. On the **Replication settings** screen:
   - **RPO:** Set based on the VM's recovery point objective. Common values: `5 minutes` (critical), `1 hour` (standard), `4 hours` (low-priority).
   - **Recovery point instances:** Number of snapshots retained at the target (1–24). More instances give more recovery flexibility but consume more storage.
   - **Quiesce guest file system:** Enable for application-consistent replicas. Requires VMware Tools. Disable if the OS lacks quiesce support.
   - **Network compression:** Enable when replicating over WAN links with limited bandwidth. Adds CPU overhead on the VRS.
   - **Encryption in transit:** Enable when replicating over untrusted networks.
5. On the **Seeds** screen: if the VM's VMDK files already exist at the target (e.g., from a previous backup or clone), point VR to them to skip the full initial sync and only replicate deltas.
6. Review the summary and click **Finish**.
7. Monitor the initial sync under **vCenter → Site Recovery → Replications**. Status moves: `Syncing (initial)` → `OK`.
---

## Configure vSphere Replication for Multiple VMs (Bulk)

Onboard a group of VMs at once when protecting an entire application tier or migrating a large workload set into DR coverage. Bulk configuration avoids navigating each VM individually.

**Steps:**

1. In vCenter, navigate to **Site Recovery → Replications**.
2. Click **New** (or the **+** icon) to open the **Configure Replication** wizard.
3. On the **Virtual machines** screen, use the search or folder tree to select multiple VMs. Hold **Ctrl** or **Shift** to multi-select.
4. Apply shared settings across all selected VMs:
   - Target site, target datastore, and VRS assignment.
   - RPO and recovery point instance count.
   - Quiesce, compression, and encryption toggles.
5. Click **Finish**. vSphere Replication queues an initial sync job for each VM.
6. Monitor progress in **Replications** — each VM shows its sync percentage and estimated time to first `OK` status.

**Note:** If VMs have significantly different storage sizes, consider staggering their initial syncs by configuring them in smaller groups to avoid saturating the replication network or target datastore throughput.
---

## Change RPO for an Existing Replication

Adjust the recovery point objective for a VM whose protection tier has changed — for example, a database that has been promoted from standard to critical, or a dev VM being wound down to a less frequent schedule.

**Steps:**

1. In vCenter, navigate to **Site Recovery → Replications**.
2. Locate the VM. Right-click it and select **Edit**.
3. On the **Replication settings** screen, change the **RPO** value.
   - Minimum: 5 minutes (requires sufficient bandwidth and VRS capacity).
   - Maximum: 24 hours.
4. Click **OK**. The new RPO takes effect immediately for the next scheduled sync cycle.
5. Verify the change: the **RPO** column in the Replications view updates within a few seconds.
**RPO violation:** If the replication cannot meet the configured RPO (due to network congestion, large change rate, or VRS overload), vCenter raises an alert. Address by reducing change rate, increasing bandwidth, or raising the RPO to a achievable value.

---

## Pause and Resume Replication

Temporarily suspends replication traffic for a VM without removing the replication configuration. Use during storage maintenance windows, network cut-overs, or when the target site is briefly unavailable.

**Pause:**

1. Navigate to **vCenter → Site Recovery → Replications**.
2. Right-click the target VM and select **Pause**.
3. Confirm the action. The replication status changes to `Paused`.

**Resume:**

1. Navigate to **vCenter → Site Recovery → Replications**.
2. Right-click the paused VM and select **Resume**.
3. vSphere Replication performs a delta sync from the last successful sync point — only changed blocks since the pause are transferred. Full resync is not required.
**RPO impact:** While paused, the VM accumulates RPO debt. If paused longer than the configured RPO window, an RPO violation alert fires. This is expected — clear the alert after resuming once the replication catches up.

---

## Recover or Remove a Stuck Replication

A replication task can become stuck in states like `Syncing` indefinitely, `Error`, or `Not Active`. This typically happens after a VRS restart, network interruption, or vCenter database inconsistency.

**Diagnose:**

1. Navigate to **Site Recovery → Replications**. Identify VMs with status `Error` or `Syncing` with no progress for more than 30 minutes.
2. Click the VM and check the **Recent Tasks** and **Events** tabs for error codes.
3. Common errors:
   - `VR_ERROR_NETWORK`: network connectivity issue between source and target VRS on port 31031.
   - `VR_ERROR_DATASTORE_FULL`: target datastore has insufficient free space.
   - `VR_ERROR_INVALID_VM_STATE`: VM snapshot conflict or inconsistent disk state.

**Recovery steps (try in order):**

1. **Sync Now:** Right-click → **Sync Now** to trigger an immediate delta sync and reset the sync cycle. This resolves transient errors.
2. **Pause then Resume:** Right-click → **Pause**, wait 30 seconds, then **Resume**. Forces the VRS to re-establish the replication stream.
3. **Edit and re-save:** Right-click → **Edit**, make no changes, click **OK**. Triggers re-registration of the replication task.
4. **Remove and reconfigure:** As a last resort, remove the replication (keeping replica files), then reconfigure using the existing replica as a seed. This avoids a full initial sync.

```bash
# Verify network connectivity from source VRS to target VRS on port 31031
nc -vz target-vrs.example.local 31031

# Check VRA logs via VAMI (port 5480) on the VRS appliance:
# Diagnostics → Log Bundle → Download
# Look for hbr_server.log entries matching the stuck VM's moref ID
```

---

## Move a Replication to a Different Target Datastore

Relocate a VM's replica files to a different datastore at the target site — for example, when decommissioning a datastore, rebalancing storage, or moving from HDD to SSD-backed storage.

**Steps:**

1. Navigate to **vCenter → Site Recovery → Replications**.
2. Right-click the VM and select **Edit**.
3. On the **Target location** screen, select the new target datastore.
4. Click **OK**. vSphere Replication migrates the replica VMDK files to the new datastore during the next sync cycle (non-disruptively — replication continues while the move occurs).
5. After the move completes, the **Target location** column in the Replications view reflects the new datastore.
**Note:** The datastore move is online. The VM at the source site continues running, and replication continues during the migration. No RPO impact beyond the normal sync cycle.

---

## Remove Replication from a VM

Permanently removes the replication configuration for a VM. Use when decommissioning a workload, removing a VM from the DR scope, or cleaning up after a migration.

**Steps:**

1. Navigate to **vCenter → Site Recovery → Replications**.
2. Right-click the VM and select **Remove Replication**.
3. On the confirmation dialog, choose what to do with replica files at the target:
   - **Remove replica files:** Deletes `.vrepl` and `.hbr` files from the target datastore. Use when you no longer need the replica.
   - **Keep replica files:** Retains the replica on the target datastore. Use if you plan to re-enable replication using these files as a seed, or if the files will serve as an ad-hoc backup copy.
4. Click **OK**.
5. Verify: the VM no longer appears in the **Replications** list.
**Caution:** Removing replication does not affect the source VM — it continues running normally. The replica at the target is a dependent copy; deleting it removes DR coverage immediately.

---

## Test a Replication (Non-Disruptive)

Validates that the replica is bootable and application-consistent without affecting the source VM or ongoing replication. Required for DR testing and compliance audits.

**How it works:** vSphere Replication creates a temporary isolated copy of the replica in a sandbox network at the target site. The source VM continues running and replication continues uninterrupted during the test.

**Steps:**

1. Navigate to **Target site vCenter → Site Recovery → Replications**.
2. Right-click the VM and select **Recover**.
3. On the **Recovery type** screen, select **Test** (non-destructive). Do not select "Recovery" — that is destructive and intended for actual DR events.
4. Select the **Recovery Point** to use (choose the most recent `OK` instance or a specific point-in-time instance).
5. Select the **Target host/cluster** and **Resource pool** where the test VM will power on.
6. Select the **Test network** — an isolated port group with no uplink to production. This prevents the test VM from causing IP conflicts.
7. Review the summary and click **Finish**.
8. Monitor the test VM powering on in the target site's **Recent Tasks**.
9. Validate the VM: log in, check application services, verify data integrity.
10. Record results for DR test documentation.
---

## Clean Up After a Replication Test

After a replication test is validated, the test VM must be removed. Leaving test VMs running causes resource contention and confuses monitoring.

**Steps:**

1. Navigate to **Target site vCenter → Site Recovery → Replications**.
2. Locate the VM. It shows a status of `Testing` or has a `(test)` indicator.
3. Right-click and select **Clean Up** (or **Remove Test Recovery**).
4. Confirm. vSphere Replication powers off and deletes the test VM and any associated test snapshots.
5. The original replication resumes its normal sync cycle — replication was never interrupted.
6. Verify: the replication status returns to `OK` and the test VM is gone from the target inventory.
**Note:** Always clean up test VMs promptly. Running test VMs consume datastore space (they are full snapshots of the replica), CPU, and memory at the recovery site.

---

## Register VR with SRM

Connects the vSphere Replication infrastructure to Site Recovery Manager so VR-replicated VMs can be added to SRM protection groups and recovery plans.

**Prerequisites:** SRM is installed and configured at both sites. VRA is deployed and operational.

**Steps:**

1. In vCenter, navigate to **Site Recovery → vSphere Replication**.
2. Select the **VR Appliance** at the source site.
3. Click **Register with SRM** (or navigate to the VRA VAMI at `https://<vra-ip>:5480`).
4. In the VAMI, go to **Configuration → Site Recovery Manager**.
5. Enter the SRM server address, port (443), and credentials.
6. Click **Register**. SRM and VR establish a trust relationship.
7. Repeat on the target site's VRA if bidirectional protection is needed.
8. Verify in **SRM → Summary**: the VR server should appear as a registered replication provider.

```bash
# Access VRA VAMI
https://vra-source.example.local:5480
  Configuration → Site Recovery Manager
    SRM Server: srm-source.example.local
    Port: 443
    Username: administrator@vsphere.local
    Password: ••••••••
    → Register

# Verify via SRM UI:
SRM → Summary → Replication → vSphere Replication Servers: [listed]
```

---

## Verify VR Appliance Registration

Confirms that the VRA is correctly registered with vCenter and SRM. Run this check after deploying a new VRA, after a site recovery, or during routine DR health checks.

**Steps:**

1. Navigate to **vCenter → Site Recovery → vSphere Replication → Replication Servers**.
2. Confirm the VRA appliance is listed with a **Connected** status.
3. Check the VRA version matches the expected version for your environment.
4. In the VRA VAMI (`https://<vra-ip>:5480`), go to **Configuration → vCenter Server** and confirm the registered vCenter matches the expected FQDN.
5. Check **Configuration → Site Recovery Manager** and confirm the SRM server is registered.
6. Run a test replication configuration on a non-critical VM to confirm end-to-end connectivity.
---

## Check SRM Protection Group Sync Status

Verifies that VR-backed SRM protection groups reflect the current replication state of all member VMs. Run before DR tests or during monthly DR health reviews.

**Steps:**

1. In SRM, navigate to **Protection → Protection Groups**.
2. Select the VR-based protection group (type: **vSphere Replication**).
3. Review the **Status** column for each VM:
   - `Protected`: VM is replicating successfully and is ready for recovery.
   - `Not Protected`: VM has a replication error or has been removed from VR.
   - `Needs Attention`: RPO violation or sync issue — investigate before the next test.
4. Click into any VM showing `Not Protected` and review the error in the **Details** pane.
5. For out-of-sync VMs: resolve the underlying VR issue (see "Recover or Remove a Stuck Replication"), then trigger a **Sync** on the protection group to refresh status.
6. Review the **Recovery Plans** that reference this protection group and confirm they show `Ready`.
---

## Check Overall Replication Health

Gets a top-level view of all replications in the environment. Use during daily operational checks or before a DR exercise.

**Steps:**

1. Navigate to **vCenter → Site Recovery → Replications**.
2. Review the status summary at the top: total replications, number in `OK`, `Syncing`, `Error`, or `RPO Violation` states.
3. Filter by status to isolate problem VMs:
   - **Error:** Requires immediate attention — replication is broken.
   - **RPO Violation:** Replication is running but cannot meet the configured RPO. Investigate bandwidth, change rate, or VRS load.
   - **Syncing:** Normal during initial sync or after a resume. Flag if stuck for more than 2× the expected sync window.
4. Check the **VRS health** under **vSphere Replication → Replication Servers**: all appliances should show `Connected`.
5. Export or screenshot the summary for DR health documentation.

```bash
# Via vSphere API / PowerCLI — list replication status for all VMs
Connect-VIServer vcenter-source.example.local
$vrService = Get-View -ViewType ServiceInstance
# Use Hbr API or SRM API for programmatic status — requires SRM PowerCLI module:
Get-SRMProtectionGroup | Get-SRMVM | Select Name, State, LastError
```

---

## Check Individual VM Replication Status

Drill into a specific VM's replication details to assess sync health, last sync time, and current RPO compliance.

**Steps:**

1. Navigate to **vCenter → Site Recovery → Replications**.
2. Locate the VM (use the search bar if the list is long).
3. Click the VM to open the **Details** pane. Review:
   - **Status:** `OK`, `Syncing`, `Paused`, `Error`, or `RPO Violation`.
   - **Last sync:** Timestamp of the last successful replication sync.
   - **Current RPO:** Time since last sync — compare to the configured RPO value.
   - **Replication server:** Which VRS is handling this VM's replication traffic.
   - **Target location:** Datastore and vCenter at the recovery site.
4. Click the **Recovery points** tab to review available restore points and their timestamps.
5. For detailed error information, click **Events** or check the VRS VAMI log bundle.
---

## Interpret RPO Violation Alerts

An RPO violation means the replication is running but cannot complete a sync cycle within the configured RPO window. The alert does not mean replication has stopped — it means the protection SLA is being missed.

**Common causes and remediation:**

| Cause | Symptom | Fix |
|---|---|---|
| High VM change rate | Transfer size exceeds bandwidth | Increase RPO, add VRS, throttle guest I/O |
| Insufficient network bandwidth | Transfer queue backed up | Prioritise replication traffic (QoS), compress traffic |
| VRS overloaded | Multiple VMs violating RPO simultaneously | Deploy additional VRS, rebalance VM assignments |
| Target datastore I/O bottleneck | Slow write performance at target | Move replica to faster datastore |
| Snapshot quiesce timeout | Quiesce fails, sync skipped | Disable quiesce or fix VMware Tools on guest |

**Investigation steps:**

1. Navigate to **Site Recovery → Replications** and filter by **RPO Violation**.
2. Note which VMs are violating and which VRS they use — cluster of VMs on the same VRS suggests a VRS resource issue.
3. Click the violating VM → **Details** → note transfer size and transfer duration for recent sync cycles.
4. Compare transfer size against available bandwidth:
   - If transfer size > bandwidth × RPO window → reduce change rate or increase bandwidth.
5. Check VRS resource usage in the VAMI (`https://<vra-ip>:5480 → Monitoring`).
6. After remediation, monitor the replication through 2–3 consecutive sync cycles to confirm the violation clears.

```bash
# Estimate required bandwidth for a given VM and RPO
# Formula: (Daily change rate GB × 8 bits) / (RPO seconds) = required Mbps
# Example: 50 GB/day change rate, 1-hour RPO
echo "scale=2; (50 * 8 * 1024) / (3600)" | bc
# Result: ~113 Mbps minimum sustained bandwidth required
```

---

## Failback a Replicated VM (after SRM recovery)

After an SRM-initiated failover, the VM is running at the recovery site. Failback returns the VM to the original source site once the source site is restored.

**Prerequisites:** Source site is recovered and vCenter/ESXi hosts are operational. Replication was removed during the failover (SRM removes VR configuration as part of the recovery plan).

**Steps:**

1. At the **recovery site vCenter**, confirm the recovered VM is running and healthy.
2. Configure reverse replication: right-click the VM → **vSphere Replication → Configure Replication**, but this time select the **original source site** as the target.
   - Set the same RPO and settings as the original replication.
   - Use the original source datastore as the target.
3. Allow the initial sync to complete (status: `OK`).
4. Schedule a maintenance window for the failback.
5. At the scheduled time, power off the VM at the recovery site (or use SRM's planned failover).
6. Trigger a final **Sync Now** to capture last-minute changes.
7. At the **source site**, recover the VM: **Site Recovery → Replications → [VM] → Recover** (select **Recovery** type, not Test).
8. Power on the VM at the source site and validate application health.
9. Remove the reverse replication configuration now that the VM is back at the source.
10. Reconfigure forward replication (source → recovery) to restore DR coverage.
---

## Re-protect a VM (reverse replication direction)

After a failover (planned or unplanned), re-protection reconfigures replication in the reverse direction so the recovery site becomes the new source and the original site becomes the new target. This restores DR coverage for the failed-over VM without a full failback.

**When to use:** After a successful failover when you want to maintain DR protection for the VM from its new home at the recovery site, before deciding whether to fail back.

**Steps:**

1. At the **recovery site vCenter**, confirm the VM is running post-failover.
2. Right-click the VM → **vSphere Replication → Configure Replication**.
3. Set the **target site** to the **original source site** (now acting as the new DR target).
4. Select the target datastore at the original site.
5. Set RPO, instances, and other settings to match the original policy.
6. On the **Seeds** screen: if the original VMDK files still exist at the source site (they may, if the source failure was a vCenter/management-plane failure rather than a storage failure), use them as seeds to avoid a full resync.
7. Click **Finish** and monitor the initial sync.
8. Once status is `OK`, update SRM protection groups at the recovery site to include this VM in a protection group targeting the original site.
9. Validate by running a replication test (see "Test a Replication").
**Note:** Re-protection does not move the VM back to the source — it keeps the VM at the recovery site and builds a new replication stream in the reverse direction. This is the correct approach when the source site is operational but you have not yet decided to fail back.
