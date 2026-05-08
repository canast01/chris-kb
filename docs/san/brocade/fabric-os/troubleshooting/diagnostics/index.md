# FabricOS — Diagnostics

> Part of the [Troubleshooting](../) reference.

---

## Diagnostic Commands

```bash
# Full diagnostic dump (used when opening support cases)
supportShow

# Save diagnostics bundle to FTP/SCP for TAC
supportSave

# Error log
errShow
errDump

# Port diagnostics (port must be offline first)
portTest <slot/port>
spinFab <slot/port>
portLogShow <slot/port>
```

---

## Log Locations

| Log | Command |
|---|---|
| RAS log (hardware/fabric events) | `errShow` / `errDump` |
| Audit log (login, config changes) | `auditlog --show` |
| Port event log | `portLogShow <slot/port>` |
| MAPS alerts | `mapsDb --show` |

---

## Data Collection for Support

Add diagnostic data collection procedures here.
