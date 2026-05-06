# SRDF/S Vendor Support

Dell SRDF/S support cases are opened at support.dell.com under the relevant PowerMax array service tag. P1 cases (active production replication failure with data risk) trigger a 30-minute callback SLA under ProSupport Plus and Mission Critical contracts. Collect all required diagnostics before calling to avoid delays during triage.

**Required information for SR:**

| Item | Command / Source |
|---|---|
| Pmax serial numbers (both sites) | `symcfg list` |
| SRDF group ID and current state | `symrdf query -g <group> -v` |
| Pair state history | Array event log (Unisphere → Events) |
| Solutions Enabler version | `symcli -version` |
| Site RTT measurement | Network team latency report |
| Array event log export | Unisphere for PowerMax → Export Logs |

**Support tiers:**
- **ProSupport**: 8×5 NBD for non-critical; 24×7 for P1.
- **ProSupport Plus**: 24×7 proactive health monitoring; predictive issue detection.
- **Mission Critical**: Dedicated TAM, 4-hour onsite SLA for P1 SRDF failures.
