# Diagnostics & Health

> Part of the [Brocade Fabric OS CLI Reference](../).

---

```bash
# Switch health check
switchStatusShow
supportShow        # Full diagnostic dump
supportSave        # Save diagnostics to file

# Port diagnostics
portTest <slot/port>
spinFab --help

# Error isolation
errShow
errClear
errDump

# Link reset
portLogClear <slot/port>
```
