---
tags:
  - operations
  - san
---
# FabricOS — Health Checks


<div class="kb-summary">
Health Checks reference covering Daily Checks, Health Check Checklist, Post-Change Validation.
</div>

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

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. `switchshow` — verify all ports show **Online**; check switch state field shows **Healthy**
2. `fabricshow` — list all switches in fabric; flag any missing domain IDs or disconnected members
3. `porterrshow` — scan every port for non-zero CRC, LR_IN, or LR_OUT; non-zero requires immediate investigation
4. `cfgshow` — confirm active cfg name matches expected zoning configuration for this fabric
5. `islshow` — all ISLs should show **Up** at expected speed and link distance; investigate any Down ISLs
6. `sfpshow` — review Tx/Rx power dBm for every port against SFP vendor thresholds; replace out-of-range SFPs
7. `portshow <port>` on all F-ports (NPIV environments) — verify expected initiator WWNs are logged in
8. `configshow -all | wc -l` — confirm non-zero output; then `configupload` to save current config to backup server

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
