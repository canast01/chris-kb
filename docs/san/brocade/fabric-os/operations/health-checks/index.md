# FabricOS — Health Checks

> Part of the [Operations](../) reference.

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Run `switchshow` | `switchshow` | Confirm all expected ports are online/active, flag any unexpected offline or faulty ports |
| [ ] Run `fabricshow` | `fabricshow` | Verify fabric membership is stable and the correct switch holds the principal role |
| [ ] Run `islshow` | `islshow` | Confirm all ISLs are up and running at expected speed (e.g. 32G) |
| [ ] Run `porterrshow` | `porterrshow` | Review error counters; flag any increments in `enc_in`, `loss_sync`, or `link_fail` |
| [ ] Run `errshow` | `errshow` | Scan recent error log entries for hardware or fabric events |
| [ ] Run `cfgshow \| head -20` | `cfgshow \| head -20` | Confirm active zone config name matches expected, no unexpected changes |
| [ ] Verify firmware level is consistent across all switches in the fabric | `version` | |
| [ ] Check management platform (SANnav) for any active alerts | | |

---

## Health Check Checklist

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

---

## Post-Change Validation

- [ ] `switchshow` — all ports back in expected state, no unexpected offline ports
- [ ] `fabricshow` — fabric membership intact, principal switch unchanged
- [ ] `islshow` — all ISLs up and at expected speed
- [ ] `porterrshow` — no new error counter increments since change completed
- [ ] `cfgshow` — active zone config name and contents match expected post-change state
- [ ] Host multipath paths are active and balanced (check host-side multipath tool)
- [ ] Management platform (SANnav) shows no new alarms for affected fabric
- [ ] Close change ticket with validation evidence attached
