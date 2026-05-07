# Switch Status & Identity

> Part of the Cisco MDS NX-OS CLI Reference.

## Switch Identity

```bash
show version           # NX-OS version, uptime, hardware
show inventory         # chassis, modules, transceivers
show system uptime
show license usage
show feature           # enabled features
```

## Environment Health

```bash
show environment       # fans, power, temperature
show environment fan
show environment power
show environment temperature
```

## Module / Slot Status

```bash
show module            # all line cards and supervisor modules
show module <slot>
```

All modules should show status `ok`. A `failed` or `powered-dn` module requires immediate investigation.

## CPU & Memory

```bash
show system resources   # CPU and memory utilization
show processes cpu      # per-process CPU breakdown
show processes memory   # per-process memory
```

## Running Configuration

```bash
show running-config
show startup-config
```

## Logging

```bash
show logging            # recent syslog events
show logging last 50    # last 50 log entries
```

## Quick Health Summary

| Check | Command | Expected |
|---|---|---|
| Version | `show version` | Expected NX-OS release |
| Modules | `show module` | All `ok` |
| Environment | `show environment` | No alerts |
| CPU | `show system resources` | < 70% |
| Recent logs | `show logging last 50` | No error storms |

## Pre-Change Baseline

```bash
show version > /tmp/pre-change-version.txt
show running-config > /tmp/pre-change-config.txt
show interface brief
show flogi database
```
