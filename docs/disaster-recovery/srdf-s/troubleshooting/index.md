# SRDF/S Troubleshooting

SRDF/S issues typically manifest as pair state transitions away from `Synchronized`, elevated host write latency, or unexpected failover splits. Because SRDF/S is synchronous, any WAN degradation directly impacts production host I/O — treat latency increases above 5ms RTT as a storage incident, not purely a network one. Always collect `symrdf query -g <group> -v` and array event logs before engaging Dell support.

| Symptom | Likely Cause | Diagnostic Steps |
|---|---|---|
| Pair enters `Write Disabled` | WAN latency exceeded threshold; write queue backed up | Check site RTT, review array write pending counts via `symcfg list -v` |
| Pair in `Invalid` state | Unresolved split from prior failover | Review last failover event log; run `symrdf resync` after confirming R1 data validity |
| Pair in `Split` state | Manual split or link failure | Check FCIP/ISL link state; determine which side has latest data before re-establishing |
| ISL/FCIP link failure | Physical or FCIP tunnel loss | Verify switch ISL counters, FCIP session state; escalate to network team |
| Unintended failover during maintenance | Maintenance window not declared; monitors fired | Always suspend SRDF monitoring and set pair to `Suspended` before array maintenance |
