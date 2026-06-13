---
tags:
  - san
  - troubleshooting
---
# Cisco MDS — Troubleshooting Diagnostics

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
```text
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
```bash
# View on-board flash log (persistent across reloads)
show logging onboard

# Filter to specific event type
show logging onboard stack-trace
show logging onboard error-stats
show logging onboard temperature-history
```
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
```bash
# FSPF link state database
show fspf database vsan 10

# FSPF interface cost and state
show fspf interface fc2/1 vsan 10

# FSPF neighbors
show fspf neighbors vsan 10
```
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
```bash
interface fc2/48
  switchport mode SD
  no shutdown
```
```bash
no monitor session 1

# Verify cleared
show monitor session all
```
```bash
# Capture 200 packets matching a specific host
ethanalyzer local interface mgmt capture-filter "host 192.168.1.50" limit-captured-frames 200

# Write capture to file on bootflash
ethanalyzer local interface mgmt capture-filter "host 192.168.1.50" write bootflash:mgmt-capture.pcap limit-captured-frames 500

# Copy pcap off-switch for Wireshark analysis
copy bootflash:mgmt-capture.pcap scp://<user>@<server>/<path>/
```
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
```bash
terminal monitor     # send log to this terminal
debug zone all vsan 10
# Reproduce the issue
undebug all
terminal no monitor
```
```bash
# Redirect to bootflash (takes 5-10 minutes)
show tech-support > bootflash:tech-support-<hostname>-<date>.txt

# Copy off-switch
copy bootflash:tech-support-<hostname>-<date>.txt scp://<user>@<server>/<path>/
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

