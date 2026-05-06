# SRM Operations

Weekly SRM operations focus on validating protection group health, confirming SRA connectivity, and ensuring recovery plans remain executable. All protection groups must show `OK` status; any group in `Not Ready` or `Error` state must be investigated and resolved before the end of the business day. Quarterly test failovers validate the full recovery plan workflow and must be completed in isolated network segments to avoid impacting production.

**Weekly checks:**

| Check | Location / Command | Expected State |
|---|---|---|
| Protection group status | SRM UI → Protection Groups | All groups `OK` |
| SRA connectivity | SRM UI → Array Managers | Connection `Connected` |
| vSphere Replication health | vSphere Replication UI → Monitor | No replication errors |
| Recovery plan status | SRM UI → Recovery Plans | All plans `Ready` |
| Failed protection jobs | SRM UI → Tasks & Events | No failed jobs in last 7 days |

**Quarterly:**
- Execute test failover on at least one non-critical recovery plan.
- Document results and resolve any script or network mapping failures.
- Confirm SRA version compatibility with current array firmware.
