# Diagnostics, Counters & SPAN

> Part of the [Cisco MDS NX-OS CLI Reference](../).
---

## Diagnostics & Counters

```bash
# Port errors
show interface fc<slot/port> counters
show interface fc<slot/port> counters errors
clear counters interface fc<slot/port>

# CRC / link reset errors
show interface fc<slot/port> | include CRC
show hardware internal errors

# Diagnostics
show diagnostics result module <slot>

# Port analysis
analyze port-channel

# Event log
show logging onboard
show logging last <n>

# Core health
show system internal sysmgr status
```

## SPAN & Monitoring

```bash
show monitor session all
monitor session <n> source interface fc<slot/port>
monitor session <n> destination interface fc<slot/port>
no monitor session <n>
```
