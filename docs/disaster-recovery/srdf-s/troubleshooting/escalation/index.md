# SRDF/S — Escalation

> Part of the [SRDF/S Troubleshooting](../) reference.

Dell SRDF/S support cases are opened at support.dell.com under the relevant PowerMax array service tag. P1 cases (active production replication failure with data risk) trigger a 30-minute callback SLA under ProSupport Plus and Mission Critical contracts. Collect all required diagnostics before calling to avoid delays during triage.

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
