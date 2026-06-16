---
tags:
  - operations
---
# Virtualization Health Checks


<div class="kb-summary">
Virtualization health checks: ESXi host connectivity, cluster HA/DRS status, datastore space, vSAN health, and vCenter service status — reusable across VMware products.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌──────────────────────────────────── Virtualization Health Checks ─────────────────────────────────────┐
│                                                                                                       │
│    Structured checks across daily operations, capacity planning, and change management                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Daily (~15 min)       │  │      Capacity (weekly)      │  │      Pre / Post Change      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        vCenter alarms       │  │       CPU < 70% target      │  │        Alarms cleared       │   │
│   │      Host connectivity      │  │       RAM balloon = 0       │  │         vSAN healthy        │   │
│   │         vSAN health         │  │        Storage < 80%        │  │       Snapshots clear       │   │
│   │       Datastore space       │  │       Growth trend OK       │  │      Backups confirmed      │   │
│   │        VM state check       │  │       Forecast 90 days      │  │        HA/DRS active        │   │
│   │        Backup status        │  │       Licence headroom      │  │      App owner sign-off     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    HA         = High Availability; restarts VMs on surviving hosts when a host fails                  │
│    DRS        = Distributed Resource Scheduler; balances VM load across cluster hosts                 │
│    vSAN       = VMware hyper-converged storage; health = no resync, no degraded objects               │
│    Balloon    = VMware memory reclaim driver; non-zero = host under memory pressure                   │
│    Swap       = VM disk-based memory swap; non-zero = critical memory shortage on host                │
│    Datastore  = Storage volume presented to ESXi; monitor used % and provisioning ratio               │
│    VAMI       = vCenter Appliance Management Interface; port 5480; cert and patch mgmt                │
│    Alarm      = vCenter triggered alert; P1=red critical, P2=yellow warning, P3=info                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Run This Routine

Run these steps at the start of any virtualization operations shift or before a planned change window. These are cross-product checks — for product-specific detail, see each product's own health-checks page.

1. **vCenter connectivity** — confirm the UI is reachable and returning HTTP 200:
   ```bash
   curl -sk -o /dev/null -w "%{http_code}" https://<vcenter>/ui
   ```
   **Expected output:** `200` — any other code (401, 5xx, or no response) indicates a vCenter problem.
2. **ESXi host count** — vCenter → **Hosts and Clusters** → verify expected host count; investigate any hosts showing as disconnected or not responding.
3. **vSAN health** — vCenter → **Cluster → Monitor → vSAN Health** → all checks should show green; flag any WARN or ERROR status and check the detail pane for the affected component.
4. **NSX Manager cluster** — confirm all NSX Manager nodes report as Up:
   ```bash
   curl -sk -u 'admin:pw' https://<nsx>/api/v1/cluster/status
   ```
   **Expected output:** JSON with `"mgmt_cluster_status": {"status": "STABLE"}` and all member nodes showing `"status": "UP"`.
5. **VM alarm count** — vCenter → **Alarms → Active Alarms** → review count by severity; investigate any P1 (red) or P2 (yellow) alarms before proceeding with any change work.
6. **DRS/HA status** — vCenter → **Cluster → Summary** → verify HA is Enabled with no admission control failures, and DRS is Enabled and not in manual-override mode.
7. **vMotion queue** — vCenter → **Recent Tasks** → filter for vMotion tasks; any task running longer than 30 minutes indicates a stalled migration that needs investigation.
8. **Storage alarm** — vCenter → **Datastores** → check that no datastore exceeds 85% used capacity; flag any datastore in maintenance mode that is not expected to be there.
9. **Backup job status** — cross-check with Veeam or Commvault: all jobs from the last 24 hours should show **Completed** or **Completed with Warnings** (investigate warnings); any **Failed** job requires immediate follow-up before changes proceed.
10. **Certificate expiry** — check the vCenter certificate expiry and flag if fewer than 60 days remain:
    ```bash
    openssl s_client -connect <vcenter>:443 </dev/null 2>/dev/null | openssl x509 -noout -dates
    ```
    **Expected output:** `notAfter` date ≥ 60 days from today. If fewer than 60 days remain, raise a certificate renewal ticket immediately.

## Verify

After completing the full routine:

- All 10 steps completed with no escalation triggers — sign off in the shift log.
- If any step triggered an escalation condition, confirm the incident ticket is open before signing off.
- Re-run the affected check after any remediation to confirm resolution.

---

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="daily-health-check/">
  <strong>Daily Health Check</strong>
  <span>Daily checks across vCenter, ESXi, vSAN, NSX, VxRail, and Aria.</span>
</a>

<a class="kb-card" href="pre-change-check/">
  <strong>Pre-Change Check</strong>
  <span>Checks before maintenance, patching, upgrades, migrations, or config changes.</span>
</a>

<a class="kb-card" href="post-change-validation/">
  <strong>Post-Change Validation</strong>
  <span>Validation after maintenance, upgrades, patching, or configuration changes.</span>
</a>

<a class="kb-card" href="capacity-review/">
  <strong>Capacity Review</strong>
  <span>Cluster, datastore, vSAN, CPU, memory, and growth review.</span>
</a>

<a class="kb-card" href="alert-review/">
  <strong>Alert Review</strong>
  <span>Review active alerts, stale alerts, ownership, and escalation needs.</span>
</a>

<a class="kb-card" href="management-access-check/">
  <strong>Management Access Check</strong>
  <span>vCenter, ESXi, VxRail Manager, NSX, and Aria access validation.</span>
</a>

</div>
