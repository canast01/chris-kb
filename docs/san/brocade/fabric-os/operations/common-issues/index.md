# FabricOS — Known Issues

```text
┌────────────────────────────────────── FabricOS — Common Issues ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Most common FabricOS issues with root causes and resolution steps               │   │
│   │     Port issues: flapping (bad SFP/cable), offline (config/speed mismatch), BB credit zero    │   │
│   │ Zone issues: zone conflict (cfgmerge fail), alias not found, zoning mismatch between switches │   │
│   │     Fabric issues: segmented fabric (principal switch conflict), ISL degraded, E_Port down    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Port-level issues → zone issues → fabric-wide issues → login storms → escalation                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Port Issues         │  │         Zone Issues         │  │        Fabric Issues        │   │
│   │        Port flapping        │  │        Zone conflict        │  │       Segmented fabric      │   │
│   │         Port offline        │  │       Alias not found       │  │         ISL degraded        │   │
│   │        BB credit = 0        │  │       Zoning mismatch       │  │         E_Port down         │   │
│   │          CRC errors         │  │        cfgmerge fail        │  │         FLOGI storm         │   │
│   │        Bad SFP/cable        │  │       Zone not active       │  │          RSCN loop          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    supportshow output is the primary diagnostic artifact for TAC escalation                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issue       │      Check       │      Command      │       Fix        │    Escalation    │   │
│   │    Port flap     │  SFP Tx/Rx dBm   │      sfpshow      │   Replace SFP    │  TAC if persist  │   │
│   │    Segmented     │ Domain IDs same  │     fabricshow    │ Reset domain ID  │    TAC merge     │   │
│   │   FLOGI storm    │  HBA log events  │    portlogdump    │ portdisable HBA  │  TAC + OS team   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SFP optics · OM4 LC fibre cables · ISL trunk cables · HBA drivers                        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Port flapping = Port cycling online/offline rapidly; bad SFP, cable, or HBA driver                 │
│    BB credit     = Buffer-to-buffer credit; zero means port stalled waiting to send frames            │
│    CRC error     = Cyclic Redundancy Check failure; bad cable, SFP, or dirty connector                │
│    Zone conflict = cfgmerge failure when two fabrics with incompatible zones are merged               │
│    cfgmerge      = Automatic zone config merge when ISL established; fails on name conflict           │
│    Zoning mismatch = Zone config differs between switches; clear and reactivate                       │
│    Segmented fabric = ISL in E_Port Isolated state; domain ID or principal switch conflict            │
│    E_Port        = Expansion Port; ISL port type; isolated state = fabric segment                     │
│    FLOGI storm   = HBA flooding fabric with Fabric Login requests; disable port to stop               │
│    RSCN          = Registered State Change Notification; excessive RSCNs disrupt I/O                  │
│    ISL degraded  = ISL link showing errors or reduced bandwidth; check SFPs and cables                │
│    portlogdump   = Per-port event log dump; captures FLOGI, PLOGI, and error events                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [Operations](../index.md) reference.

---

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

---

## Port Issues

| Issue | Check | Action |
|---|---|---|
| Port shows No_Light | SFP installed? | Seat SFP; check cable |
| Port flapping | Signal quality | Replace SFP; check cable |
| High error count | Encoding or signal | `portErrShow`; replace SFP |
| Device not logging in | Port state = Offline | `portEnable`; check zoning |

---

## Zoning Issues

| Symptom | Command | Action |
|---|---|---|
| Host HBA not visible in name server | `nsshow` | Check cable, HBA driver, FLOGI; confirm VSAN membership |
| Host can't see LUNs | `zoneshow "<alias>"` | Confirm zone is in active zone set; check alias WWN |
| Zone set not active | `cfgshow` — no asterisk | Run `cfgenable "<zset>"` then `cfgsave` |
| Two hosts in same zone | `zoneshow` | Split into single-initiator zones immediately |
| Alias WWN is wrong | `alishow` | Delete and recreate alias with correct WWN |
| Change not persisted after reboot | | Run `cfgsave` after every change |

---

## Switch / Fabric Issues

| Issue | Check | Action |
|---|---|---|
| Switch status not HEALTHY | Environmental or hardware | Check `psShow`, `fanShow`, `tempShow` |
| Firmware version mismatch | `version` | Schedule Fabric OS upgrade |
| License missing | `licenseShow` | Add license key via `licenseAdd` |
| Fabric segmented | `fabricshow` | Investigate ISL state, domain ID conflicts |
| Principal switch changed | `fabricshow` | Review recent switch events; verify domain ID settings |

---

## MAPS and Alerting

| Issue | Check | Action |
|---|---|---|
| Switch status MARGINAL | `errShow` | Investigate hardware errors |
| Port diagnostics fail | Port offline | Disable port before running `portTest` |
| MAPS alert firing | `mapsDb --show` | Investigate threshold breach |
| High error rate | `errShow` | Correlate with port errors |

---

## Virtual Fabrics (VF) Issues

| Issue | Check | Action |
|---|---|---|
| Device not visible | Wrong FID context | `setContext <fid>` then `switchshow` |
| Port in wrong FID | `lscfg --show` | Reassign port to correct FID |
| VF not enabled | License | Verify VF license with `licenseShow` |
