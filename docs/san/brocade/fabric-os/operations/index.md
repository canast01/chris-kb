# Operations

> Part of the [Brocade Fabric OS](../) reference.

---

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Run `switchshow` | `switchshow` | confirm all expected ports are online/active, flag any unexpected offline or faulty ports |
| [ ] Run `fabricshow` | `fabricshow` | verify fabric membership is stable and the correct switch holds the principal role |
| [ ] Run `islshow` | `islshow` | confirm all ISLs are up and running at expected speed (e.g. 32G) |
| [ ] Run `porterrshow` | `porterrshow` | review error counters; flag any increments in `enc_in`, `loss_sync`, or `link_fail` |
| [ ] Run `errshow` | `errshow` | scan recent error log entries for hardware or fabric events |
| [ ] Run `cfgshow | head -20` | `cfgshow | head -20` | confirm active zone config name matches expected, no unexpected changes |
| [ ] Verify firmware level is consistent across all switches in the fabric | `version` |  |
| [ ] Check management platform (DCNM or BNA) for any active alerts or f |  |  |

## Health Check

- [ ] All ports in expected state: `switchshow`
- [ ] Fabric principal switch correct, all members present: `fabricshow`
- [ ] All ISLs up and at correct speed: `islshow`
- [ ] No error counter increments on any port: `porterrshow`
- [ ] SFP/GBIC optical levels within range: `sfpshow`
- [ ] No critical entries in error log: `errshow`
- [ ] Active zone config matches expected: `cfgshow`
- [ ] No thermal or power alerts in switch environment: `sensorshow`

```bash
# Full fabric health sweep
switchshow
fabricshow
islshow
porterrshow
sfpshow
errshow
cfgshow | head -20
sensorshow
```

## Change Readiness

- [ ] Zone configuration backup taken: run `cfgsave` and export offline copy via `configupload`
- [ ] Both Fabric A and Fabric B are healthy before touching either
- [ ] ISL utilization has headroom — no ISL above 70% sustained load
- [ ] NPIV usage documented: note which ports have NPIV-enabled devices logged in
- [ ] `porterrshow` counters clear or baselined before change
- [ ] Maintenance window approved and communicated to affected teams
- [ ] Rollback plan documented: zone config restore procedure confirmed

| Item | Status | Notes |
|---|---|---|
| Zone config backup | | `configupload` to jump host |
| Both fabrics healthy | | `switchshow` on both |
| ISL headroom confirmed | | `islshow` bandwidth check |
| NPIV inventory current | | Port-to-host mapping |
| Change window approved | | Ticket reference |

## Incident Triage

- [ ] Run `switchshow` — identify any offline, faulty, or unexpected port states
- [ ] Run `porterrshow` — look for error counter spikes on specific ports; note `enc_in`, `loss_sync`, `link_fail`
- [ ] Run `fabricshow` — check for fabric segmentation, missing switches, or unexpected principal election
- [ ] Run `errshow` — review log for root cause events, timestamps, and switch identity
- [ ] Run `islshow` — confirm ISLs are up; a downed ISL can cause fabric segmentation
- [ ] Check SFP health on affected ports: `sfpshow <slot/port>`
- [ ] Verify zoning has not changed unexpectedly: `cfgshow` and compare to backup
- [ ] Escalate to Brocade TAC if hardware failure confirmed or log entries indicate switch fault

| Question | Answer |
|---|---|
| Which ports are offline or faulty? | `switchshow` output |
| Are there error counter spikes? | `porterrshow` — check `enc_in`, `loss_sync`, `link_fail` |
| Is the fabric segmented? | `fabricshow` — missing domain IDs indicate segmentation |
| What does the error log show? | `errshow` — timestamps and event codes |
| Are ISLs intact? | `islshow` — down ISL = likely root cause of isolation |

## Maintenance Window

1. Confirm both fabrics are healthy via `switchshow` and `fabricshow` on all switches
2. Take a configuration backup: `configupload` to a secure jump host
3. Notify storage and compute teams that Fabric A (or B) will be affected
4. Perform the change on one fabric only — leave the other fabric carrying full host I/O
5. After change, run `switchshow`, `fabricshow`, and `islshow` to confirm fabric is stable
6. Validate host multipath paths via host-side `esxcli storage nmp device list` or `multipath -ll`
7. Confirm zone configuration is correct: `cfgshow` and compare to pre-change backup
8. Repeat procedure on second fabric only after first fabric is fully validated

## Post-Change Validation

- [ ] `switchshow` — all ports back in expected state, no unexpected offline ports
- [ ] `fabricshow` — fabric membership intact, principal switch unchanged
- [ ] `islshow` — all ISLs up and at expected speed
- [ ] `porterrshow` — no new error counter increments since change completed
- [ ] `cfgshow` — active zone config name and contents match expected post-change state
- [ ] Host multipath paths are active and balanced (check host-side multipath tool)
- [ ] Management platform (DCNM/BNA) shows no new alarms for affected fabric
- [ ] Close change ticket with validation evidence attached
