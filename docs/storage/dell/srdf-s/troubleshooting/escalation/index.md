---
tags:
  - dell
  - troubleshooting
---
# SRDF/S — Escalation


<div class="kb-summary">
Escalation reference covering Required Information for Support Request, Support Tiers, When to Escalate.
</div>

```text
┌───────────────────────────────────────── SRDF/S — Escalation ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    SRDF/S — Escalation Path                                   │   │
│   │              L1 Triage: review logs, match to known issues in runbook (0–30 min)              │   │
│   │         L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)         │   │
│   │             Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)             │   │
│   │            Sev1 (data loss / production impact): page on-call + open critical case            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Information to Collect Before Escalating                           │   │
│   │               Product version: SRDF/S version string from About / version command             │   │
│   │                                  Full log bundle: symrdf query                                │   │
│   │                     Symptom timeline: when first occurred; any changes made                   │   │
│   │                Scope: single job / all jobs / all components — narrows root cause             │   │
│   │                    Error codes: exact error messages and exit codes from logs                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment        │
│  R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency       │
│  R2            = target volume; must acknowledge each write; acts as synchronous mirror               │
│  RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency       │
│  RPO=0         = zero recovery point objective; no data loss possible under normal operation          │
│  RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min       │
│  symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver       │
│  Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split                          │
│  Consistent    = transient state where R1 write is in transit but not yet confirmed on R2             │
│  Failover      = makes R2 read-write; production continues from DR site after R1 failure              │
│  Restore       = re-synchronises after failover; direction is reversed until R1 catches up            │
│  RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters           │
│  FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)            │
│  RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [SRDF/S Troubleshooting](../index.md) reference.

Dell SRDF/S support cases are opened at support.dell.com under the relevant PowerMax array service tag. P1 cases (active production replication failure with data risk) trigger a 30-minute callback SLA under ProSupport Plus and Mission Critical contracts. Collect all required diagnostics before calling to avoid delays during triage.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Required Information for Support Request

| Item | Command / Source |
|---|---|
| Pmax serial numbers (both sites) | `symcfg list` |
| SRDF group ID and current state | `symrdf query -g <group> -v` |
| Pair state history | Array event log (Unisphere → Events) |
| Solutions Enabler version | `symcli -version` |
| Site RTT measurement | Network team latency report |
| Array event log export | Unisphere for PowerMax → Export Logs |

---

## Support Tiers

| Tier | Coverage | P1 SLA |
|---|---|---|
| **ProSupport** | 8×5 NBD for non-critical; 24×7 for P1 | 24×7 phone support |
| **ProSupport Plus** | 24×7 proactive health monitoring; predictive issue detection | 30-minute callback |
| **Mission Critical** | Dedicated TAM, 4-hour onsite SLA for P1 SRDF failures | 4-hour onsite |

---

## When to Escalate

- Pair state `Invalid` with data risk and no clear root cause
- Failover refused with errors not covered by known field notes
- R2 data consistency in question after unplanned failover
- SRDF group port offline with no clear physical cause
- Resync repeatedly failing or stalling beyond expected window
