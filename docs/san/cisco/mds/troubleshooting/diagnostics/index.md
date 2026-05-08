# MDS — Diagnostics

> Part of the [Cisco MDS](../../) reference.

---

## Diagnostic Commands

```bash
# Port errors and counters
show interface fc<slot/port> counters
show interface fc<slot/port> counters errors
clear counters interface fc<slot/port>

# CRC / link reset errors
show interface fc<slot/port> | include CRC
show hardware internal errors

# Hardware diagnostics
show diagnostics result module <slot>

# Event log
show logging onboard
show logging last <n>

# Core health
show system internal sysmgr status
```

## SPAN (Traffic Capture)

```bash
show monitor session all
monitor session <n> source interface fc<slot/port>
monitor session <n> destination interface fc<slot/port>
no monitor session <n>
```

## FC Frame Capture

```bash
# Data-plane FC frame capture via SPAN
monitor session 1 source interface fc1/1 rx
monitor session 1 destination interface fc2/1   # Dedicated capture port
no monitor suspend 1

# Management-plane packet capture
ethanalyzer local interface mgmt capture-filter "host <mgmt-ip>" write bootflash:capture.pcap
```

## Change notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change
