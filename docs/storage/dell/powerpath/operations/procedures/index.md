# PowerPath — Procedures

## Change Readiness

Verify these items before performing any SAN fabric maintenance, array-side masking change, or PowerPath upgrade on a host.

- [ ] `powermt display dev=all` confirms all paths are alive and path count matches the site baseline — do not start a SAN change with dead paths already present
- [ ] Save current PowerPath configuration before any change: `powermt save` — this persists the policy and path state so it can be reviewed or restored if the change causes issues
- [ ] `powermt check_registration` confirms the license is valid — an expired license will degrade paths to `unlic` state after a reboot
- [ ] Confirm the expected post-change path count per device — for a single SAN port maintenance event, each device should retain at least half its paths
- [ ] If this is a PowerPath version upgrade: confirm OS and kernel version compatibility against the Dell PowerPath support matrix before installing
- [ ] Quiesce or verify host I/O is healthy before the change — confirm the application is not in a high-latency state that would be worsened by temporarily reduced path count
- [ ] Notify the application team that SAN maintenance will temporarily reduce available paths; confirm their application can tolerate this
- [ ] Document the current `powermt display dev=all` output as the pre-change baseline for post-change comparison

| Item | Status | Notes |
|---|---|---|
| All paths alive, count matches baseline | | |
| powermt save completed | | |
| License valid (check_registration) | | |
| Post-change minimum path count acceptable | | |
| OS/kernel compatibility verified (if upgrade) | | |

## Maintenance Window

Steps for SAN port or fabric maintenance that will temporarily reduce the active path count on PowerPath hosts.

1. Identify all hosts with paths through the port or fabric component being maintained — run `powermt display dev=all` on each host and record the pre-change path count per device
2. Run `powermt save` on each affected host to persist the current policy and path configuration
3. Confirm each device will retain at least half its active paths during the maintenance — do not proceed if a device would drop to a single path or zero paths
4. Notify application owners that path count will be temporarily reduced; confirm applications can tolerate the reduced redundancy
5. Remove or disable the target SAN port or fabric component per the approved runbook
6. On affected hosts, run `powermt display dev=all` to confirm remaining paths are alive and I/O is continuing via the surviving paths
7. Complete the maintenance on the SAN port or fabric component; restore the port to service
8. Run `powermt restore` on each affected host to bring the returned paths back online, then run `powermt display dev=all` to confirm the original path count has been restored

## Post-Change Validation

Run these checks after any SAN, fabric, or PowerPath change to confirm multipath health is fully restored.

- [ ] `powermt display dev=all` — all paths are alive and path count per device matches the pre-change baseline; no dead paths remain
- [ ] `powermt display ports class=all` — all HBA ports show `alive`; no ports stuck in `dead` state
- [ ] `powermt display options` — Policy is `CLAROpt` for all device classes; no policy drift occurred during the change
- [ ] `powermt check_registration` — license remains valid post-change
- [ ] No path flap entries in host OS logs in the 30 minutes following the maintenance window
- [ ] Application owners confirm I/O has resumed normally and no elevated latency is observed
- [ ] `powermt save` run after the change to persist the restored configuration state
