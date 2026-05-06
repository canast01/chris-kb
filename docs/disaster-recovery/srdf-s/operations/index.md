# SRDF/S Operations

Daily operations for SRDF/S focus on confirming all pairs remain in `Synchronized` state and that write response times have not degraded. Use `symrdf query` as the primary health command and set alerting thresholds on pair state transitions in Aria Operations or equivalent monitoring. Any pair entering a non-synchronized state during business hours should be treated as a P2 incident until root cause is confirmed.

**Daily checks:**

| Check | Command | Expected Result |
|---|---|---|
| Pair state | `symrdf query -g <group>` | All pairs `Synchronized` |
| Group list | `symrdf list -v` | No `Invalid` or `Split` entries |
| Link connectivity | `symcfg list -rdfg` | Port state `Online` |
| Write response time | Aria Operations / Unisphere | Within baseline ±10% |
| Site latency | Network monitoring | ≤5ms RTT |
