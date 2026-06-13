---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# SRDF/A — Escalation


<div class="kb-summary">
SRDF/A escalation procedures — case creation and Dell EMC support triage for async replication failures.

*Applies to: SRDF/A*
</div>

```text
┌───────────────────────────────────────── SRDF/A — Escalation ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    SRDF/A — Escalation Path                                   │   │
│   │              L1 Triage: review logs, match to known issues in runbook (0–30 min)              │   │
│   │         L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)         │   │
│   │             Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)             │   │
│   │            Sev1 (data loss / production impact): page on-call + open critical case            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Information to Collect Before Escalating                           │   │
│   │               Product version: SRDF/A version string from About / version command             │   │
│   │                                  Full log bundle: symrdf query                                │   │
│   │                     Symptom timeline: when first occurred; any changes made                   │   │
│   │                Scope: single job / all jobs / all components — narrows root cause             │   │
│   │                    Error codes: exact error messages and exit codes from logs                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports      │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology               │
│  R1            = source SRDF volume on production array; host writes flow here                        │
│  R2            = target SRDF volume on DR array; receives replicated data asynchronously              │
│  Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically          │
│  Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO                  │
│  symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore       │
│  SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth             │
│  Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle            │
│  Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts                   │
│  Restore       = after failover resolution, re-establishes replication with R1 as source              │
│  Establish     = initial sync or re-sync operation that copies R1 to R2 in full                       │
│  Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication                 │
│  FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link                      │
│  Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [SRDF/A](../index.md) reference.

Dell SRDF/A support cases are opened via the Dell Support Portal (support.dell.com) under the relevant PowerMax array service tag. When opening a case, classify the severity appropriately: P1 for active replication failure with no workaround, P2 for degraded replication with workaround in place. Collect the required diagnostics before calling to accelerate triage.

**Required information for SR:**

| Item | Command / Source |
|---|---|
| Pmax serial numbers (both sites) | `symcfg list` |
| SRDF group IDs | `symrdf list` |
| Replication lag stats | `symrdf query -g <group> -v` |
| Array event log | Unisphere for PowerMax → Events |
| Solutions Enabler version | `symcli -version` |
| syminq output | `syminq` |

**Support tiers:**
- **ProSupport**: Next business day parts/labour.
- **ProSupport Plus**: 24×7 proactive monitoring and predictive issue detection.
- **Mission Critical**: Dedicated TAM and 4-hour onsite SLA for P1 incidents.

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

---

## See also

- [Srdf A — Diagnostics](diagnostics/)
- [Srdf A — Common Issues](common-issues/)
