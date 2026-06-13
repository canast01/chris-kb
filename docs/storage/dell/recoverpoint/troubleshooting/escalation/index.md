---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# RecoverPoint — Escalation


<div class="kb-summary">
RecoverPoint case creation, log collection, and Dell EMC support escalation procedures for unresolved replication failures.
</div>

```text
┌────────────────────────────────────── RecoverPoint — Escalation ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 RecoverPoint — Escalation Path                                │   │
│   │              L1 Triage: review logs, match to known issues in runbook (0–30 min)              │   │
│   │         L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)         │   │
│   │             Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)             │   │
│   │            Sev1 (data loss / production impact): page on-call + open critical case            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Information to Collect Before Escalating                           │   │
│   │            Product version: RecoverPoint version string from About / version command          │   │
│   │                           Full log bundle: image access enable/disable                        │   │
│   │                     Symptom timeline: when first occurred; any changes made                   │   │
│   │                Scope: single job / all jobs / all components — narrows root cause             │   │
│   │                    Error codes: exact error messages and exit codes from logs                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites           │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication          │
│  Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA                  │
│  Journal       = write-order-consistent storage capturing all writes for point-in-time access         │
│  Consistency Group= set of volumes protected together; writes are applied in order across all         │
│  Bookmark      = named marker in journal; enables deterministic recovery to a known state             │
│  Image Access  = mounting a journal point-in-time image to a host for testing or recovery             │
│  Failover      = activating the replica at the recovery site; breaks replication relationship         │
│  Test Copy     = non-disruptive image access for validation without breaking replication              │
│  RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero          │
│  RTO           = Recovery Time Objective; time from failover to service restored                      │
│  Reverse       = after failover, replicates from recovery site back to re-sync production             │
│  Splitter Lag  = delay between host write and journal commit; monitor for replication health          │
│  CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps          │
│  Distributed CG= consistency group spanning volumes on multiple storage arrays                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [RecoverPoint](../../index.md) > [Troubleshooting](../index.md) reference.

---

Dell support for RecoverPoint is accessed via support.dell.com, with service requests opened against the RPA cluster serial number or site license. Before opening an SR, collect the RecoverPoint support bundle from the CLI using `get support_bundle` on each RPA, as well as the full cluster state from the management console. Provide RPA software versions for both Site A and Site B, the total consistency group count, per-CG journal sizes, and the replication link state at the time of the issue.

- **Support portal:** [support.dell.com](https://support.dell.com) — select RecoverPoint product line
- **SR creation:** Use RPA cluster serial number; specify site A and site B versions
- **Log collection:**
  ```text
  get support_bundle
  ```
  Run on each RPA; bundle includes system logs, CG state, journal metadata, and link statistics
- **Required information for SR:**
  - RPA software version (Site A and Site B)
  - Number of consistency groups and volumes
  - Journal volume sizes and current utilization
  - Replication link state and lag at time of incident
  - Management console screenshot of affected CGs
- **Compatibility matrix:** RecoverPoint compatibility matrix available on Dell's support site under RecoverPoint documentation
- **Escalation:** Request Engineering Escalation in the SR for production-down or data-loss risk scenarios

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
