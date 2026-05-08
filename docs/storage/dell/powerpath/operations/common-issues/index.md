# PowerPath — Common Issues

## Incident Triage

When a host reports I/O errors, elevated latency, or a block device is inaccessible, work through this sequence first.

- [ ] Run `powermt display dev=all` on the affected host immediately — identify which pseudo devices have dead paths and how many paths remain alive for each
- [ ] Check the PowerPath policy: `powermt display options` — if policy shows `BasicFailover` instead of `CLAROpt`, load balancing is degraded; investigate license and run `powermt config`
- [ ] Run `powermt restore` to instruct PowerPath to retry all paths currently marked dead — this alone resolves transient path losses caused by brief fabric events
- [ ] Check HBA port states: `powermt display ports class=all` — a port in `dead` state indicates the HBA itself has lost fabric connectivity, not just individual paths
- [ ] Review host OS logs for the path failure timestamp: `grep -i "powermt\|path\|dead" /var/log/messages` — correlate with fabric switch events
- [ ] Check the SAN fabric switch: confirm the affected HBA WWN and storage array port are still zoned and active; look for CRC errors or port login/logout events on the switch
- [ ] If paths are dead and `powermt restore` does not recover them, confirm the array-side LUN masking is intact — check the masking view or storage view on the array
- [ ] Run `powermt check_registration` if paths show `unlic` state — a license issue will cause PowerPath to drop management of devices after a license check failure

| Question | Answer |
|---|---|
| Which pseudo devices have dead paths? | |
| How many paths remain alive per device? | |
| What is the current load balancing policy? | |
| Are any HBA ports in dead state? | |
| Did powermt restore recover any dead paths? | |

## Common Issue Reference

| Symptom | Likely Cause | Action |
|---|---|---|
| Dead paths after reboot | HBA driver load order | Run `powermt restore` after boot |
| Device missing | LUN not presented or rescan needed | `powermt config` |
| Performance issues | Suboptimal path policy | `powermt set policy=co dev=all` |
| Path flapping | SAN fabric instability | Check switch and cable |
| multipathd conflict | Both multipath stacks active | Disable `multipathd` |
| Dead paths on all HBAs | SAN switch or array port issue | Check zoning and array port health |
| Dead paths on one HBA | HBA failure or cable/SFP | Replace HBA or cable |
| Paths not auto-recovering | `powermt restore` needed | Run `powermt restore` after SAN fix |
| New LUNs not visible | No rescan | Run `powermt config` |
| Unbalanced path I/O | Wrong policy | `powermt set policy=co dev=all` |
| `unlic` paths | License expired or not applied | Run `powermt check_registration` |
