# SRDF/A Troubleshooting

Common SRDF/A issues include link failures, increasing cycle times, suspended consistency groups, and volume capacity mismatches between source and target arrays. Always collect `symrdf query -g <group> -v` and `symcfg list -v` output before engaging Dell support. Correlate array event logs with network monitoring timestamps to distinguish storage-side from WAN-side causes.

| Symptom | Likely Cause | First Steps |
|---|---|---|
| SRDF/A link down | ISL failure or FCIP port error | Check switch ISL state, verify FCIP tunnel, review SRDF group state with `symrdf list` |
| Cycle time increasing | WAN bandwidth saturation | Check delta set size via `symcfg list -v`, review WAN utilisation graphs |
| Consistency group suspended | Host I/O spike exceeds delta set capacity | Review change rate, consider increasing cycle time temporarily |
| Target volume capacity mismatch | Thin pool exhaustion on target | Expand target thin pool or add devices to the pool |
| `Invalid` pair state | Prior failover not cleanly resolved | Run `symrdf restore` or `symrdf resync` after confirming data validity |
