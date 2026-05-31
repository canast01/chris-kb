# FabricOS — Health Checks

```text
┌────────────────────────────────── Brocade Fabric OS — Health Checks ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Daily FOS health checks: switch state, port errors, SFP optics, MAPS alerts          │   │
│   │            switchshow: verify all ports Online; check switch health state (Healthy)           │   │
│   │      porterrshow: review CRC, LOS, LOSync counters; nonzero values require investigation      │   │
│   │             sfpshow: review Tx/Rx power dBm; compare against SFP vendor thresholds            │   │
│   │          MAPS dashboard: check active alert policy; review mapsDb for rule violations         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Switch state -> port errors -> SFP optics -> MAPS alerts -> fabric topology review                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Switch Health        │  │         Port Health         │  │         SFP / Optics        │   │
│   │          switchshow         │  │         porterrshow         │  │           sfpshow           │   │
│   │       switchstatusshow      │  │        portstatsclear       │  │         Tx power dBm        │   │
│   │        MAPS dashboard       │  │         CRC counter         │  │         Rx power dBm        │   │
│   │        Fan/PSU status       │  │        Loss of Signal       │  │         Temperature         │   │
│   │          fabricshow         │  │         Loss of Sync        │  │        Vendor limits        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Clear error counters only after investigating and resolving the underlying cause                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Check       │     Command      │     Frequency     │    Threshold     │      Action      │   │
│   │   Switch state   │    switchshow    │       Daily       │    All Online    │Investigate faults│   │
│   │   Port errors    │   porterrshow    │       Daily       │     Zero CRC     │Replace cable/SFP │   │
│   │    SFP power     │     sfpshow      │       Weekly      │   Vendor range   │   Replace SFP    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FC switches · SFP transceivers · ISL cables · console/mgmt access                        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    switchshow     = Lists all ports with state (Online/Offline/Faulty) and connected device WWN       │
│    porterrshow    = Displays error counters per port: CRC, LOS, LOSync, ITW, Enc_in                   │
│    portstatsclear = Resets error counters to zero; use only after resolving the issue                 │
│    sfpshow        = Displays SFP diagnostics: Tx/Rx power, temperature, voltage                       │
│    switchstatusshow = Summary health status of switch: Healthy, Marginal, or Down                     │
│    fabricshow     = Lists all switches in fabric with domain IDs and WWNs                             │
│    MAPS dashboard = SANnav MAPS view showing active policy and current rule violations                │
│    CRC error      = Cyclic Redundancy Check error; indicates corrupt FC frame; cable/SFP issue        │
│    Loss of Signal = LOS: no optical signal detected; SFP or cable failure                             │
│    Loss of Sync   = LOSync: signal present but frame sync lost; speed mismatch or noise               │
│    Tx/Rx power    = SFP optical power in dBm; each SFP type has defined acceptable range              │
│    MAPS alert     = Automated rule-based alert when metric breaches configured threshold              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Operations](../index.md) reference.

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
