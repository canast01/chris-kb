# Ports

> Part of the Brocade Fabric OS CLI Reference.
## Port Status

```bash
portShow <slot/port>           # detailed port info (state, speed, WWN)
portStatsShow <slot/port>      # TX/RX frames, errors
portErrShow                    # error summary across all ports
portLogShow <slot/port>        # port event log
portLogDump                    # dump full port log to console
portCfgShow <slot/port>        # port configuration
```

## Port States

| State | Meaning |
|---|---|
| Online | Healthy, device logged in |
| No_Light | No SFP or no signal |
| No_Module | No SFP installed |
| Offline (Admin) | Administratively disabled |
| In_Sync | Link up but no device logged in |
| Faulty | Hardware fault |

## Enable / Disable a Port

```bash
portDisable <slot/port>
portEnable <slot/port>
```

## Port Speed

```bash
portCfgSpeed <slot/port> <speed>
# speed: 0=auto, 4, 8, 16, 32 (Gbps)
```

## Long Distance Mode

```bash
portCfgLongDistance <slot/port> <mode>
# modes: L0 (normal), L1, L2, LE, LD, LS
```

## Port Error Counters

```bash
portStatsShow <slot/port>
portErrShow
```

Key error fields:
| Field | Cause | Action |
|---|---|---|
| LossSignal | SFP or cable issue | Replace SFP; check cable |
| LossSync | Signal quality | Check SFP power level |
| EncInFrm | Encoding errors | Replace SFP |
| TooLong | Jumbo frame or fabric issue | Investigate MTU |

## Reset Port Stats

```bash
portStatsReset <slot/port>
```

## Persistent Disable / Enable

```bash
portPersistentDisable <slot/port>    # survives reboot
portPersistentEnable <slot/port>
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Port shows No_Light | SFP installed? | Seat SFP; check cable |
| Port flapping | Signal quality | Replace SFP; check cable |
| High error count | Encoding or signal | `portErrShow`; replace SFP |
| Device not logging in | Port state = Offline | `portEnable`; check zoning |
