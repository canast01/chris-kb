# Ports

> Part of the [Brocade Fabric OS CLI Reference](../).

---

```bash
# Port status
portShow <slot/port>
portStatsShow <slot/port>
portErrShow
portLogShow <slot/port>
portLogDump
portCfgShow <slot/port>

# Port admin
portDisable <slot/port>
portEnable <slot/port>
portCfgSpeed <slot/port> <speed>    # 0=auto, 4, 8, 16, 32
portCfgLongDistance <slot/port> <mode>

# Port stats reset
portStatsReset <slot/port>
```
