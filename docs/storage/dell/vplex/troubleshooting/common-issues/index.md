# Dell VPLEX — Common Issues

## Incident Triage

When hosts report I/O suspension, a distributed device is out-of-sync, or a director is unreachable, work through this sequence first.

- [ ] Run `ll /clusters/*/health-indications/` immediately — identify which cluster has entered a non-ok health state and note when the state change occurred
- [ ] Check distributed device sync state: `ll /distributed-storage/distributed-devices/*/health-indications/` — an `out-of-sync` device means one leg of the distributed device is not being written to; identify which cluster leg is affected
- [ ] Check Witness status for Metro deployments: `ll /metro-node/*/witness/` — if Witness is unreachable from one cluster and the ICL is also interrupted, VPLEX will suspend I/O on consistency groups to preserve write-order consistency
- [ ] Check director health: `ll /engines/*/directors/*/hardware/` — a director in a faulted state on one engine reduces redundancy and may cause host path failures
- [ ] Verify ICL connectivity between Metro clusters — an ICL interruption is the most common cause of distributed device out-of-sync events; check the WAN or dark fibre connection between sites
- [ ] Check consistency group state: `ll /distributed-storage/consistency-groups/` — identify any groups that have suspended I/O and determine the cause before resuming
- [ ] Verify storage views are intact: `ll /clusters/*/exports/storage-views/` — a missing or corrupted storage view can cause a specific host to lose access to its volumes
- [ ] Run `health-check --full` to get a system-wide view of all faults in a single output; use this output when opening a Dell support case

| Question | Answer |
|---|---|
| Which cluster shows non-ok health-state? | |
| Which distributed devices are out-of-sync? | |
| Is the Witness connected and reachable? | |
| Is the ICL between Metro clusters up? | |
| Which directors or director components are faulted? | |

## Common Symptoms and Resolutions

| Symptom | Likely Cause | Action |
|---|---|---|
| Host loses access to all VPLEX volumes | Director pair failure or storage view corruption | Check `ll /engines/*/directors/*/hardware/`; verify storage views are intact |
| Distributed device shows `out-of-sync` | ICL interruption between Metro clusters | Verify ICL connectivity; check WAN link; allow auto-resync once link is restored |
| I/O suspended on consistency group volumes | ICL down with Witness unreachable (split-brain protection) | Restore ICL or Witness connectivity; manually grant quorum if required |
| Single host loses access to volumes | Storage view issue or HBA path failure | Check storage view initiator membership; verify HBA paths with `powermt display dev=all` |
| Director shows `major-failure` in health-indications | Director hardware fault | Replace the faulted director; engage Dell support for hardware replacement |
| `health-check --full` reports warnings | Various | Review the specific component warnings in the output; investigate the flagged path |
| Witness not reachable from one cluster | Network issue or Witness VM down | Check network connectivity to Witness VM; verify Witness VM is running |
