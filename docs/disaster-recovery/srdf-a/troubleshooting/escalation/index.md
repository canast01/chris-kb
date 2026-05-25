# SRDF/A — Escalation

> Part of the [SRDF/A](../../index.md) reference.

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
