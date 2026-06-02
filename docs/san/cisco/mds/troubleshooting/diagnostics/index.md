# MDS — Diagnostics


<div class="kb-summary">
> Part of the [Cisco MDS](../../index.md) reference.
</div>

---

## Overview

MDS NX-OS provides a layered set of diagnostic tools: real-time counters, hardware test results, system logs, SPAN-based FC frame capture, and management-plane packet capture. Use these tools in sequence — start with high-level state commands, then drill into specific counters or captures when the root cause is not yet clear.

---

## Layer 1: Interface and Counter Diagnostics

### Port Status and Error Counters

```bash
# Detailed single port status
show interface fc1/1

# All port error counters
show interface fc1/1 counters errors

# All port transmit/receive counters
show interface fc1/1 counters

# Clear counters to establish a fresh baseline
clear counters interface fc1/1

# Check immediately after clearing to confirm problem is active
show interface fc1/1 counters errors
```
┌─────────────────────────────── Cisco MDS — Troubleshooting Diagnostics ───────────────────────────────┐
│                                                                                                       │
│  Diagnostic toolset: show commands, SPAN, FC Ping/Traceroute, and tech-support bundles.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Show Command Toolkit             │  │            FC Ping and Traceroute           │   │
│   │         show flogi database: logins          │  │         fcping: N_Port reachability         │   │
│   │         show zone active: zone state         │  │           fctrace: path hop-by-hop          │   │
│   │         show interface fc: counters          │  │         FC loopback: port self-test         │   │
│   │          show topology: fabric map           │  │             DCNM: topology view             │   │
│   │         show hardware: module status         │  │          Ethanalyzer: mgmt capture          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Show commands give state snapshots; FC ping/trace verify end-to-end path connectivity                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               SPAN and Capture               │  │                Log Collection               │   │
│   │          FC SPAN: mirror FC traffic          │  │          Tech-support: full bundle          │   │
│   │           SPAN dest: analyzer port           │  │         show logging: syslog buffer         │   │
│   │          RSPAN: remote SPAN over IP          │  │          Event history: per-module          │   │
│   │        Capture with Wireshark via tap        │  │         Core dump: supervisor crash         │   │
│   │           SPAN ACL: filter traffic           │  │         TAC upload: encrypted bundle        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS supervisor · FC analyzer port · management Ethernet · syslog/DCNM server                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FC SPAN        = Fibre Channel Switched Port Analyzer; mirrors selected FC traffic                   │
│  RSPAN          = Remote SPAN; forwards mirrored frames to remote analyzer over IP                    │
│  fcping         = FC-layer reachability test using ECHO Extended Link Service                         │
│  fctrace        = FC-layer traceroute; maps path from source to destination N_Port                    │
│  Ethanalyzer    = Cisco tool capturing management-plane Ethernet packets on supervisor                │
│  tech-support   = Comprehensive diagnostic bundle; includes logs, configs, counters                   │
│  Event history  = Per-process ring buffer of internal events; survives minor faults                   │
│  Core dump      = Memory snapshot taken when a process crashes; aids TAC analysis                     │
│  TAC            = Technical Assistance Center; Cisco support team                                     │
│  SPAN ACL       = Filter applied to SPAN session to capture only matching traffic                     │
│  show topology  = CLI command displaying fabric-wide switch and ISL map                               │
│  FC loopback    = Hardware self-test looping frames back at the port for validation                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

CPU sustained above 80% or memory usage above 90% warrants investigation. High CPU from the `fc_platform` or zone processes may indicate FLOGI storms or a large zone database activation in progress.

### Module and Hardware Health

```bash
# All line cards and supervisor modules — confirm all status is 'ok'
show module

# Detailed status for a specific module slot
show module 1

# Hardware diagnostic test results
show diagnostics result module 1

# Run hardware diagnostics (online, non-disruptive)
diagnostic start module 1 test all
show diagnostics result module 1
```

Hardware diagnostics cover ASIC registers, memory, and crossbar interconnects. Any `FAILED` result requires module replacement.

### On-board Logging (OBFL)

NX-OS maintains an on-board log that persists across reloads. Useful for identifying intermittent faults that occurred before a reload.

```bash
# View on-board flash log (persistent across reloads)
show logging onboard

# Filter to specific event type
show logging onboard stack-trace
show logging onboard error-stats
show logging onboard temperature-history
```

### Environment and Power

```bash
# Full environment summary (fans, power, temperature)
show environment

# Individual component checks
show environment fan
show environment power
show environment temperature

# Power budget
show environment power detail
```

---

## Layer 3: Fabric and FC Protocol Diagnostics

### FCNS (Name Server) Database

The FCNS database lists all devices registered with the fabric per VSAN. It is a superset of FLOGI — devices must FLOGI first, then register with the Name Server.

```bash
# All registered devices per VSAN
show fcns database vsan 10

# Detailed (includes port type, device symbolic name)
show fcns database detail vsan 10

# Find a specific device by WWPN
show fcns database | grep <wwpn>

# Name server statistics
show fcns statistics vsan 10
```

### FSPF (Fabric Routing)

FSPF (Fabric Shortest Path First) is the routing protocol that distributes topology information between switches. If ISLs exist but traffic is not routing correctly, check FSPF.

```bash
# FSPF link state database
show fspf database vsan 10

# FSPF interface cost and state
show fspf interface fc2/1 vsan 10

# FSPF neighbors
show fspf neighbors vsan 10
```

### FC Domain Diagnostics

```bash
# Domain information for all VSANs
show fcdomain

# Domain list for a specific VSAN
show fcdomain domain-list vsan 10

# Principal switch status (fabric arbitration)
show fcdomain vsan 10 | include principal

# Disruptive: reconfigure fabric (only if domain conflict confirmed)
fcdomain restart disruptive vsan 10
```

### Zone Database Diagnostics

```bash
# Full zone database for a VSAN (pending + committed)
show zone vsan 10

# Active (enforced) zone configuration only
show zoneset active vsan 10

# Zone mode and status
show zone status vsan 10

# Check a specific device's zone memberships
show zone member pwwn <wwpn> vsan 10
show zone member device-alias <alias> vsan 10

# Check for pending uncommitted zone changes (enhanced mode)
show zone pending vsan 10
show zone pending-diff vsan 10
```

### IVR (Inter-VSAN Routing) Diagnostics

```bash
# IVR overall status
show ivr

# IVR VSAN topology
show ivr vsan-topology

# IVR zone database
show ivr zone
show ivr zoneset active

# IVR service group
show ivr service-group
```

---

## Layer 4: Traffic Capture (SPAN)

SPAN (Switched Port Analyzer) mirrors FC frames from a source port to a dedicated capture port, where a protocol analyzer (Wireshark, Finisar Xgig) can decode FC frames.

### Configure a SPAN Session

```bash
# Create SPAN session
monitor session 1 source interface fc1/1 rx
monitor session 1 destination interface fc2/48   # dedicated SD port

# Remove suspension flag if present
no monitor suspend 1

# Check session status
show monitor session 1
show monitor session all
```

The destination port must be in SD (SPAN Destination) mode:

```bash
interface fc2/48
  switchport mode SD
  no shutdown
```

### Remove a SPAN Session

```bash
no monitor session 1

# Verify cleared
show monitor session all
```

### Management-plane Packet Capture

For capturing management-plane traffic (SSH, SNMP, syslog) on the mgmt0 interface:

```bash
# Capture 200 packets matching a specific host
ethanalyzer local interface mgmt capture-filter "host 192.168.1.50" limit-captured-frames 200

# Write capture to file on bootflash
ethanalyzer local interface mgmt capture-filter "host 192.168.1.50" write bootflash:mgmt-capture.pcap limit-captured-frames 500

# Copy pcap off-switch for Wireshark analysis
copy bootflash:mgmt-capture.pcap scp://<user>@<server>/<path>/
```

---

## Layer 5: Syslog Analysis

### Reading the Syslog

```bash
# Most recent entries
show logging last 50

# Full buffer
show logging

# Filter to specific severity (0=emergency, 2=critical, 3=error)
show logging | include "%ERR\|%CRIT\|%ALERT"

# Filter to specific interface
show logging | grep fc1/1

# Filter to zone-related events
show logging | grep -i zone

# Filter to FLOGI events
show logging | grep -i flogi
```

### Syslog Severity Reference

| Level | Name | Meaning |
|---|---|---|
| 0 | Emergency | System unusable |
| 1 | Alert | Immediate action required |
| 2 | Critical | Critical condition (hardware fault, fabric crash) |
| 3 | Error | Error condition (port errDisabled, zone conflict) |
| 4 | Warning | Warning condition (link flap, BB credit low) |
| 5 | Notice | Normal but significant (port up/down, zone activation) |
| 6 | Informational | FLOGI accepted, device login |
| 7 | Debugging | Verbose debug output |

### Key Log Messages

| Message | Meaning |
|---|---|
| `FC-5-PORT_STATUS_CHANGE: ... is down (...Link failure...)` | Physical link down |
| `ZONE-2-ZS_MERGE_FAIL: Zone set merge failure in vsan <id>` | Zone database conflict between switches — fabric merge issue |
| `FCDOMAIN-2-DOMAIN_CONFLICT: Domain conflict detected for vsan <id>` | Domain ID conflict |
| `FLOGI-5-FLOGI_ACCEPT: ... PWWN <wwpn> login on vsan <id>` | New device login |
| `FLOGI-5-FLOGI_REJECT: ... WWPN already exists` | Duplicate WWPN — investigate |
| `ENV-1-FAN_FAILED: Fan failure detected` | Fan failure — critical |

---

## Debug Commands

Debug commands generate verbose output on the active terminal. Always use with caution in production — turn off after use.

```bash
# Enable zone debug
debug zone all vsan 10

# Enable FLOGI debug
debug flogi all

# Enable FSPF debug
debug fspf all vsan 10

# Disable all debug
undebug all

# Confirm debug is cleared
show debug
```

Debug output appears in `show logging` and on the terminal session. Redirect to a file for large captures:

```bash
terminal monitor     # send log to this terminal
debug zone all vsan 10
# Reproduce the issue
undebug all
terminal no monitor
```

---

## show tech-support

For TAC escalation or complex issues, collect a full diagnostic bundle:

```bash
# Redirect to bootflash (takes 5-10 minutes)
show tech-support > bootflash:tech-support-<hostname>-<date>.txt

# Copy off-switch
copy bootflash:tech-support-<hostname>-<date>.txt scp://<user>@<server>/<path>/
```

The tech-support bundle includes running config, module status, interfaces, VSAN/zone DB, FCNS, FSPF, syslog, and process state — everything TAC needs for initial investigation.
