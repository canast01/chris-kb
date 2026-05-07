# Diagnostics & Health

> Part of the Brocade Fabric OS CLI Reference.
## Switch Health Summary

```bash
switchStatusShow       # overall health: HEALTHY / MARGINAL / DOWN
supportShow            # full diagnostic dump (used when opening support cases)
supportSave            # save diagnostics bundle to FTP/SCP for TAC
```

## Event Log

```bash
errShow                # show all error log entries
errDump                # dump full error log
errClear               # clear error log (use with caution)
```

## Port Diagnostics

```bash
# Run a port loopback test (port must be offline)
portTest <slot/port>

# Spin fabric test (inter-switch frame forwarding)
spinFab <slot/port>

# View port event history
portLogShow <slot/port>
portLogClear <slot/port>    # clear port log
```

## MAPS (Monitoring and Alerting Policy Suite)

MAPS provides threshold-based alerting for fabric health:

```bash
# Show MAPS policy status
mapsPolicy --show

# Show MAPS alerts
mapsDb --show

# Show current dashboard (health summary)
mapsDashboard --show
```

## Fabric Diagnostics

```bash
fabricShow             # all switches in fabric, domain IDs, state
nsShow                 # name server — all logged-in devices
nsAllShow              # name server across entire fabric
topologyShow           # ISL topology and domain connections
```

## Temperature / Environment

```bash
sensorShow             # all environmental sensors
tempShow
fanShow
psShow
```

## Buffer Credit Diagnostics

```bash
portBufShow <slot/port>     # buffer-to-buffer credits
```

Low BB credits cause I/O delays. Check during performance issues.

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Switch status MARGINAL | `errShow` | Investigate hardware errors |
| Port diagnostics fail | Port offline | Disable port before running `portTest` |
| MAPS alert firing | `mapsDb --show` | Investigate threshold breach |
| High error rate | `errShow` | Correlate with port errors |
