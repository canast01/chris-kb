---
tags:
  - san
  - troubleshooting
search:
  boost: 1.5
description: "Brocade FabricOS diagnostic commands: check hardware sensors and MAPS alerts with sensorshow and mapsdashboard, inspect per-port state and SFP optical..."
---
# FabricOS — Diagnostics

<div class="kb-summary">
Brocade FabricOS diagnostic commands: check hardware sensors and MAPS alerts with sensorshow and mapsdashboard, inspect per-port state and SFP optical levels with portshow and sfpshow, diagnose fabric segmentation with fabricshow and nsallshow, identify slow-drain devices and credit starvation with portbufshow, and collect the full supportsave diagnostic bundle for Broadcom TAC escalation.

*Applies to: Brocade FOS 9.x*
</div>
![FabricOS — Diagnostics](../../../../assets/san-brocade-fabric-os-troubleshooting-diagnostics.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "sensorshow: temp fan PSU status\nswitchstatusshow: overall health" {shape: rectangle}
D: "mapsdashboard --show\nmapsdb --show for threshold breach detail" {shape: rectangle}
E: "portshow slot/port: state speed credits\nsfpshow slot/port: Rx Tx power levels" {shape: rectangle}
F: "nsallshow: confirm WWN in name server\ncfgshow + zoneshow: verify zone membership" {shape: rectangle}
G: "fabricshow: domain IDs and principal switch\ntopologyshow: ISL topology" {shape: rectangle}
H: "portstatsshow slot/port: error counters\nportlogshow slot/port: FLOGI FLOGO RESET events" {shape: rectangle}
I: "portbufshow: BB credit zero count\nbottleneckmon --show: slow drain detection" {shape: rectangle}
J: "J" {shape: rectangle}
K: "Check hardware: fan replacement PSU swap\nEscalate to Broadcom TAC for blade" {shape: rectangle}
L: "Continue to errshow for software root cause" {shape: rectangle}
M: "Review MAPS category: PORT ISL SWITCH FABRIC\nIdentify threshold breach and affected resource" {shape: rectangle}
N: "N" {shape: rectangle}
O: "Replace SFP or check cable loss budget\nTest with sfpshow on remote port" {shape: rectangle}
P: "porttest loopback: disable port first\nPorttest PASS = HBA or cable issue" {shape: rectangle}
Q: "portloginshow: confirm FLOGI for this HBA WWN\nalishow: confirm alias includes correct WWN" {shape: rectangle}
R: "errshow for E_Port segmentation messages\nCheck domain ID conflict: switchshow on each switch" {shape: rectangle}
S: "portstatsreset to baseline, recheck after 5 min\nHigh CRC = cable or SFP; high Link Reset = HBA driver" {shape: rectangle}
T: "Identify zero-credit port: portbufshow on suspect ports\nIsolate slow-drain HBA: portdisable then monitor" {shape: rectangle}
U: "Collect supportsave before and after replacement\nOpen Broadcom TAC case" {shape: rectangle}
V: "supportsave -h scp-server -u user -d /backups/\nRun on both switches in HA pair" {shape: rectangle}
A: "FabricOS Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
B -> I
J -> K
J -> L
D -> M
N -> O
N -> P
F -> Q
G -> R
H -> S
I -> T
K -> U
L -> U
M -> U
O -> U
P -> U
Q -> U
R -> U
S -> U
T -> U
U -> V
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_environmental_sensors_a: "Step 1 — Check environmental sensors and switch health" {shape: rectangle}
step_2_port_diagnostics: "Step 2 — Port diagnostics" {shape: rectangle}
step_3_fabriclevel_diagnostics: "Step 3 — Fabric-level diagnostics" {shape: rectangle}
step_4_buffer_credit_diagnostics: "Step 4 — Buffer credit diagnostics" {shape: rectangle}
step_5_collect_tac_support_bundle: "Step 5 — Collect TAC support bundle" {shape: rectangle}
log_locations: "Log locations" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_environmental_sensors_a: investigate
symptom -> step_2_port_diagnostics: investigate
symptom -> step_3_fabriclevel_diagnostics: investigate
symptom -> step_4_buffer_credit_diagnostics: investigate
symptom -> step_5_collect_tac_support_bundle: investigate
symptom -> log_locations: investigate
step_1_check_environmental_sensors_a -> resolution
step_2_port_diagnostics -> resolution
step_3_fabriclevel_diagnostics -> resolution
step_4_buffer_credit_diagnostics -> resolution
step_5_collect_tac_support_bundle -> resolution
log_locations -> resolution
```

## Before you begin

- **Access:** SSH to the Fabric OS switch as admin; serial console access for unresponsive switches; SCP server or USB drive accessible for `supportsave`
- **Gather first:** the specific symptom (port offline, MAPS alert category, I/O error on which host and storage target, fabric segmentation message), the affected switch name and domain ID, and the approximate time the issue started
- **Scope:** confirm whether the issue affects one port, one switch, or the entire fabric — `switchstatusshow` gives an overall switch health verdict before drilling into specifics

---

## Step 1 — Check environmental sensors and switch health

```bash
# Overall switch health summary
switchstatusshow
# Expected: Switch Status: HEALTHY

# All environmental sensors
sensorshow

# Individual sensor categories
fanshow        # Fan tray status and RPM
psshow         # Power supply status and input voltage
tempshow       # Temperature sensors — blade, chassis, ASIC

# Recent error log entries
errshow | head -50
# Shows most recent fabric errors with timestamp, severity, and message

# Full RAS event log (detailed)
raslog --show | head -100

# Firmware and license status
firmwareshow
licenseshow
```


```text title="Expected output"
Switch Status: HEALTHY
Fabric Online: Yes
Fabric State: Stable
Uptime: 45 days 12:34:56

Fan Tray 1: OPERATIONAL, RPM: 8450
Fan Tray 2: OPERATIONAL, RPM: 8420
Fan Tray 3: OPERATIONAL, RPM: 8475

Power Supply 1: OPERATIONAL, Input Voltage: 120.5V
Power Supply 2: OPERATIONAL, Input Voltage: 120.3V

Blade Temperature: 42°C (Normal)
Chassis Temperature: 38°C (Normal)
ASIC Temperature: 51°C (Normal)

2024-01-15 14:22:33 WARNING Port 12 Link Down - Speed Mismatch Detected
2024-01-15 13:45:12 INFO Port 8 Link Up - 16Gbps
2024-01-14 22:18:47 ERROR Port 5 CRC Error Count: 127
2024-01-14 19:33:22 WARNING Temperature Threshold Approaching: 58°C
2024-01-14 15:12:05 INFO Fabric Reconfiguration Complete
...

RAS Event ID: 0x0000A2F1, Timestamp: 2024-01-15 14:22:33, Severity: WARNING
Message: Port 12 transitioned to offline state
RAS Event ID: 0x0000A2E8, Timestamp: 2024-01-15 13:45:12, Severity: INFO
Message: Port 8 link established at 16 Gbps
...

Firmware Version: v9.1.0a
Build: 9.1.0.0.0.0
License Status: VALID
License Expiration: 2025-06-30
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `switchstatusshow: command not found` | Verify you are logged into the Brocade switch directly (SSH to the switch IP, not a management station) and have admin privileges. |
    | `errshow: Permission denied` | Run commands with appropriate admin credentials; if using a service account, confirm it has diagnostic command privileges in the switch role configuration. |
    | `raslog: invalid option '--show'` | Use `raslog --dump` or `raslog` without flags; check firmware version as RAS command syntax varies between FOS versions. |
All sensors should report `OK`. A sensor in `FAILED`, `ABSENT`, or `OUT_OF_RANGE` state requires immediate attention. Temperature thresholds vary by platform — refer to the hardware installation guide for the specific chassis.

### MAPS dashboard

```bash
# Current health dashboard — summary of all MAPS categories
mapsdashboard --show

# All triggered MAPS alerts
mapsdb --show

# Active MAPS policy details
mapspolicy --show

# All MAPS rules and thresholds
mapsrule --show

# MAPS configuration for a specific port
mapsrule --show -ports <slot/port>
```


```text title="Expected output"
MAPS Dashboard Summary
======================
System Health:        CRITICAL
Fabric Health:        WARNING
Performance:          OK
Environmental:        OK
Last Update:          2024-01-15 14:32:18

Triggered MAPS Alerts (Active)
==============================
AlertID    Severity  Category         Timestamp            Message
--------   --------  ---------------  -------------------  ----------------------------------------
2847       CRITICAL  PortHealth       2024-01-15 14:28:03  Port 0/12: Link errors exceeded threshold
3102       WARNING   FabricHealth     2024-01-15 14:15:42  Switch temp approaching limit (78°C)
2901       INFO      Performance      2024-01-15 13:45:19  ISL utilization >85% on port 1/5

Active MAPS Policy
==================
Policy Name:          Default_Fabric_Policy
Status:               ENABLED
Rule Count:           24
Last Modified:        2024-01-10 09:22:15
Escalation Level:     2

MAPS Rules and Thresholds
==========================
RuleID  Category        Threshold    Operator  Action
------  ---------------  -----------  --------  -------
R001    LinkErrors       1000/min     >         Alert
R002    FrameDrops       500/min      >         Alert
R003    CRCErrors        100/min      >         Alert
R004    PortTemp         85°C         >         Alert
R005    FabricUtilization 90%         >         Alert
...

MAPS Configuration for Port 0/12
================================
Port:                 0/12
Monitoring:           ENABLED
Error Threshold:      1000 errors/min
Frame Drop Threshold: 500 frames/min
CRC Threshold:        100 errors/min
Status:               MONITORED
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `mapsdashboard: command not found` | Verify MAPS is installed and enabled with `switchstatusshow` and ensure your user role has MAPS permissions. |
    | `Error: Invalid port format <slot/port>` | Use the correct slot/port syntax (e.g., `mapsrule --show -ports 0/12`) and verify the port exists with `portshow`. |
    | `MAPS database locked or unavailable` | Wait 30 seconds for the database lock to clear, or restart the MAPS service with `mapsstatusshow` followed by `mapsstatusset --enable`. |
MAPS categories:

| Category | What it monitors |
|---|---|
| PORT | Per-port error counters, link state changes, CRC errors |
| ISL | ISL utilization, C3 discards, trunk health |
| SWITCH | Switch health, hardware faults |
| FABRIC | Principal switch changes, domain changes, fabric events |
| SECURITY | Failed login attempts, policy violations |
| CIRCUIT | FCoE or FCIP circuit health |

---

## Step 2 — Port diagnostics

### Port status and detail

```bash
# Full port detail — state, speed, connected WWN, buffer credits
portshow <slot/port>

# Port configuration — speed, state, trunk membership, QoS settings
portcfgshow <slot/port>

# Port error counter summary (all ports)
porterrshow

# Per-port detailed error counters
portstatsshow <slot/port>

# Reset port counters (do this after baselining, not before)
portstatsreset <slot/port>

# SFP optical levels — Tx/Rx power, temperature, voltage
sfpshow <slot/port>
sfpshow               # All installed SFPs
```


```text title="Expected output"
portshow 0/0
  portName:        0/0
  portType:        F-Port
  portState:       Online
  portSpeed:       16 Gbps
  Connected WWN:   50:00:09:73:a2:1c:4f:e1
  bufferCredit:    64
  framesSent:      2847361
  framesReceived:  3124589

portcfgshow 0/0
  portName:        0/0
  portType:        F-Port
  portState:       Online
  portSpeed:       16 Gbps
  trunkState:      Not Trunked
  qosEnabled:      No
  portCfgType:     F-Port

porterrshow
  Port  CRC    Enc    Disc   Bad    Timeout  Link   Unavail
  0/0   0      0      0      0      0        0      0
  0/1   2      0      1      0      0        0      0
  0/2   0      0      0      0      0        0      0
  0/3   145    3      8      1      2        0      0
  ...

portstatsshow 0/3
  portName:           0/3
  portState:          Online
  CRC Errors:         145
  Encoding Errors:    3
  Discards:           8
  Bad Eofs:           1
  Timeout Discards:   2
  Link Failures:      0

portstatsreset 0/3
(no output — command completes silently)

sfpshow 0/0
  portName:        0/0
  Vendor:          FINISAR
  Part Number:     FTLF8524P2BNV
  Serial Number:   PF2A2K4
  Tx Power:        -2.1 dBm
  Rx Power:        -8.4 dBm
  Temperature:     38.2°C
  Voltage:         3.28 V

sfpshow
  Port  Vendor    Part Number      Tx Power  Rx Power  Temp
  0/0   FINISAR   FTLF8524P2BNV    -2.1 dBm  -8.4 dBm  38.2°C
  0/1   FINISAR   FTLF8524P2BNV    -1.8 dBm  -9.2 dBm  39.1°C
  0/2   JDSU      PLRXPL-VE-S24    -3.4 dBm  -12.1 dBm 41.5°C
  0/3   FINISAR   FTLF8524P2BNV    -5.2 dBm  -15.8 dBm 42.8°C
  ...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Invalid slot/port number` | Verify the port exists with `portshow` and use the correct slot/port format (e.g., 0/0, not 0-0). |
    | `SFP not present` | Confirm the SFP module is fully seated in the port; reseat if necessary and retry `sfpshow`. |
    | `Permission denied` | Run |
### SFP optical levels

`sfpshow` output shows each SFP's measured Tx power, Rx power, temperature, and voltage.

| Field | Normal Range | Alarm Condition |
|---|---|---|
| Rx Power | -10 to 0 dBm (short-range) | Below -10 dBm = weak signal — SFP or cable |
| Tx Power | -4 to 0 dBm | Below -8 dBm = failing SFP |
| Temperature | 0–70°C | Above 80°C = SFP thermal issue |
| Voltage | 3.0–3.6V | Outside range = SFP power issue |

If Rx power is within range but Tx power is low, the SFP is failing. If Rx power is low but the remote Tx power is fine, the problem is the cable or the local SFP's receive path.

### Port event log

```bash
# Show recent events on a port
portlogshow <slot/port>

# Dump the full port log buffer
portlogdump <slot/port>
```


```text title="Expected output"
portlogshow 0/1
Time: 2024-01-15 14:23:45 UTC
Port: 0/1 (FC16/1)
Speed: 16Gbps
State: Online
Recent Events:
  14:23:42 - Link Up
  14:23:38 - Port Enabled
  14:22:15 - FLOGI completed with WWPN 50:00:14:40:5a:2b:c0:01
  14:21:50 - Portname: "Storage-Array-01"
  14:20:33 - Class 3 service established

portlogdump 0/1
Port Log Buffer Dump for slot 0, port 1:
Entry 0x0000: [14:23:45.123] Link Up Event - Speed negotiated: 16Gbps
Entry 0x0001: [14:23:42.456] FLOGI Accept received
Entry 0x0002: [14:23:38.789] Port initialization sequence started
Entry 0x0003: [14:22:15.012] Name Server Registration (NS_REG)
Entry 0x0004: [14:21:50.345] Fabric Login completed
Entry 0x0005: [14:20:33.678] Class 3 service parameters negotiated
Entry 0x0006: [14:19:22.901] Port enabled by user
...
Total entries: 247
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `portlogshow: Invalid slot/port format` | Use the correct format `<slot>/<port>` (e.g., `0/1` or `1/3`). |
    | `portlogdump: Port not found or offline` | Verify the port exists and is online with `portshow` before dumping logs. |
Common events in `portlogshow`:

| Event | Meaning |
|---|---|
| `FLOGI` | Host or target logged into the fabric — normal |
| `FLOGO` | Device logged out — HBA driver restart or cable pull |
| `RESET` | Link reset — normal during negotiation; not normal repeatedly |
| `LIP` | Loop Initialisation Primitive — FC-AL legacy; investigate on F_Port |
| `ERR` | Error event — check timestamp and error code |

### Port loopback test

```bash
# Disable the port before testing
portdisable <slot/port>

# Run internal loopback test (SFP may need to be removed — check platform docs)
porttest <slot/port>

# Re-enable the port after testing
portenable <slot/port>
```


```text title="Expected output"
Port 0/1 has been disabled.
Running internal loopback test on port 0/1...
Test Status: PASS
Loopback Test Result: No errors detected
Port 0/1 has been enabled.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `porttest: Port 0/1 is not disabled` | Run `portdisable <slot/port>` before executing the loopback test. |
    | `porttest: SFP not detected on port 0/1` | Remove and reseat the SFP transceiver, or consult platform documentation to confirm if the SFP must be physically removed for internal loopback testing. |
`porttest PASS` confirms switch port ASIC is functioning. `porttest FAIL` indicates switch hardware damage — escalate to Broadcom TAC.

### Fabric diagnostic (spinFab)

```bash
# Send test frames across the fabric between two switch ports
spinfab -ports <slot/port>,<slot/port>
```


```text title="Expected output"
Sending test frames from port 0/0 to port 1/5...
Test frames sent: 100
Test frames received: 100
Frame loss: 0%
Round-trip time (min/avg/max): 0.234ms / 0.412ms / 0.891ms
Link status: Up
Port 0/0 transmit rate: 8.5 Gbps
Port 1/5 receive rate: 8.5 Gbps
Test completed successfully
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `spinfab: Invalid port specification` | Verify port format is `slot/port` (e.g., `0/0`) and both ports exist on the fabric. |
    | `spinfab: Port not online` | Confirm both ports are in an online state using `portshow` before running the test. |
    | `spinfab: Connection timeout` | Check that the two ports have an active fabric link and no ISL issues are blocking traffic. |
---

## Step 3 — Fabric-level diagnostics

### Fabric and name server

```bash
# All switches in fabric — domain IDs, principal switch, WWN
fabricshow

# Physical ISL topology
topologyshow

# All devices registered in the name server
nsshow         # Local switch name server
nsallshow      # Name server across entire fabric

# Look up a specific device
nslookup <wwpn>

# FLOGI database — devices that have logged into the fabric
portloginshow
```


```text title="Expected output"
Switch Name: fabric-core-01
Switch Domain ID: 1
Principal Switch: Yes
Switch WWN: 20:00:00:05:1e:1f:a2:00

Switch Name: fabric-core-02
Switch Domain ID: 2
Principal Switch: No
Switch WWN: 20:00:00:05:1e:1f:a3:10

Switch Name: fabric-edge-01
Switch Domain ID: 3
Principal Switch: No
Switch WWN: 20:00:00:05:1e:1f:b4:20

Topology:
  fabric-core-01 (Domain 1) port 0 <-> fabric-core-02 (Domain 2) port 0
  fabric-core-01 (Domain 1) port 1 <-> fabric-edge-01 (Domain 3) port 1
  fabric-core-02 (Domain 2) port 1 <-> fabric-edge-01 (Domain 3) port 0

Name Server (Local):
  50:00:14:40:1b:2c:3d:4e  server-prod-01
  50:00:14:40:1b:2c:3d:5f  server-prod-02
  50:00:14:40:1b:2c:3d:60  storage-array-01
  50:00:14:40:1b:2c:3d:71  backup-host-01

FLOGI Sessions:
  Port 0/0: 50:00:14:40:1b:2c:3d:4e (server-prod-01) — Logged In
  Port 0/1: 50:00:14:40:1b:2c:3d:5f (server-prod-02) — Logged In
  Port 1/2: 50:00:14:40:1b:2c:3d:60 (storage-array-01) — Logged In
  Port 2/3: 50:00:14:40:1b:2c:3d:71 (backup-host-01) — Logged In
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nslookup: WWN not found in fabric name server` | Verify the WWPN is correct and the device has completed FLOGI; use `nsallshow` to confirm the device is registered across the fabric. |
    | `fabricshow: Fabric not stable — reconfiguration in progress` | Wait 30–60 seconds for fabric reconfiguration to complete, then retry the command. |
### ISL diagnostics

```bash
# ISL port status and throughput
islshow

# Trunk group membership and master port
trunkshow

# Per-port real-time throughput (ISL and host/storage ports)
portperfshow

# Detailed ISL statistics
portstatsshow <isl-slot/port>
```


```text title="Expected output"
ISL Port Information
    Port 0/0: Online    Speed: 16Gb    Distance: 1.2km
    Port 0/1: Online    Speed: 16Gb    Distance: 1.2km
    Port 0/2: Online    Speed: 8Gb     Distance: 1.2km
    Port 0/3: Offline   Speed: N/A     Distance: N/A
    Port 1/0: Online    Speed: 16Gb    Distance: 2.5km

Trunk Group Information
    TrunkGroup 1: Master Port 0/0, Members: 0/0, 0/1, 0/2
    TrunkGroup 2: Master Port 1/0, Members: 1/0, 1/1

Port Performance Statistics (Real-time)
    Port 0/0: Tx: 4.2 Gbps  Rx: 3.8 Gbps  Util: 26%
    Port 0/1: Tx: 3.9 Gbps  Rx: 4.1 Gbps  Util: 25%
    Port 1/2: Tx: 1.2 Gbps  Rx: 1.5 Gbps  Util: 9%
    Port 2/3: Tx: 0.0 Gbps  Rx: 0.0 Gbps  Util: 0%

ISL Statistics for Port 0/0
    Frames Transmitted: 2847392104
    Frames Received: 2834019847
    CRC Errors: 0
    Timeout Discards: 0
    Link Failures: 0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `portstatsshow: Invalid port specification` | Verify the ISL port exists using `islshow` and use correct slot/port format (e.g., `portstatsshow 0/0`). |
    | `Command not found: portperfshow` | Ensure you are logged into the Brocade switch directly via SSH/telnet; these commands only work on the switch CLI, not remote management interfaces. |
    | `Access denied: Insufficient user role` | Confirm your user account has admin or fabric-admin privileges using `userconfig --show`. |
### Routing and path

```bash
# FSPF routing topology
fspfshow

# Trace the path a specific target WWN would take
pathinfo <target-wwn>

# Domain routing table
routeshow
```


```text title="Expected output"
FSPF Routing Topology:
Fabric Port State Speed Class Trunk
  0/0   Online  16Gb  2     No
  0/1   Online  16Gb  2     No
  0/2   Online  8Gb   2     No
  0/3   Offline N/A   N/A   No
  1/0   Online  16Gb  2     Yes
  1/1   Online  16Gb  2     Yes

Path Information for WWN 50:00:14:40:5b:2a:3c:d1:
Hops: 3
Path: Domain 1 → Domain 5 → Domain 12
Latency: 4.2ms
Status: Active

Domain Routing Table:
Domain  NextHop  Cost  State
1       Local    0     Online
2       1        1     Online
5       1        2     Online
12      5        3     Online
8       1        4     Offline
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fspfshow: command not found` | Verify you are logged into the Brocade switch CLI (not the Linux shell) by checking the prompt shows `switch>` or `switch#`. |
    | `pathinfo: Invalid WWN format` | Ensure the target WWN is in colon-separated hexadecimal format (e.g., `50:00:14:40:5b:2a:3c:d1`) with exactly 16 hex pairs. |
---

## Step 4 — Buffer credit diagnostics

Buffer-to-buffer (BB) credits control flow on each FC link. Credit starvation causes I/O to stall. This is the primary mechanism behind slow-drain device impact.

```bash
# Show BB credit status on a port
portbufshow <slot/port>

# MAPS monitors for zero-credit conditions
mapsdb --show | grep -i credit
mapsdb --show | grep -i slow

# Bottleneck detection status
bottleneckmon --show

# Enable bottleneck detection if not active
bottleneckmon --enable
```


```text title="Expected output"
portbufshow 0/5
Port 0/5 BB_Credit: 16
Port 0/5 BB_Credit_Available: 16
Port 0/5 BB_Credit_Zero_Transitions: 0
Port 0/5 Transmit_Buffers: 32
Port 0/5 Receive_Buffers: 32

mapsdb --show | grep -i credit
Rule: Credit_Loss_Detected (enabled) — Threshold: 5 events/hour
Rule: Zero_Credit_Condition (enabled) — Threshold: 10 events/hour
Rule: Credit_Recovery_Time (enabled) — Threshold: 2000ms

mapsdb --show | grep -i slow
Rule: Slow_Port_Detection (enabled) — Threshold: 100ms latency
Rule: Slow_Link_Response (enabled) — Threshold: 50ms

bottleneckmon --show
Bottleneck Detection: Enabled
Last Check: 2024-01-15 14:32:18 UTC
Active Bottlenecks: 0
Monitoring Interval: 60 seconds

bottleneckmon --enable
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `portbufshow: Invalid port specification` | Verify the slot/port format matches your switch model (e.g., 0/5 for slot 0, port 5). |
    | `mapsdb: Database not initialized` | Run `mapsdb --init` to initialize the MAPS database before querying rules. |
    | `bottleneckmon: Feature not supported on this platform` | Confirm your Brocade switch model supports bottleneck monitoring (typically SAN switches with firmware 8.0+). |
When a port shows persistent zero BB credits, the connected device is not returning credits fast enough — it is the slow-drain device. Identify it, disable the port temporarily, and work with the host or storage team to resolve the queue depth or driver issue.

---

## Step 5 — Collect TAC support bundle

`supportsave` is the single most important thing to do when opening a Broadcom TAC case.

### supportsave — full diagnostic bundle

```bash
# Run supportsave with SCP parameters
supportsave -h <scp-server-ip> -u <username> -p <password> -d /backups/supportsave/

# Alternative: configure SCP destination interactively first
supportshow --ftp <ftp-server-ip>
supportsave
```


```text title="Expected output"
supportsave: Collecting system information...
supportsave: Gathering fabric topology data...
supportsave: Collecting switch logs and diagnostics...
supportsave: Compressing diagnostic bundle...
supportsave: Connecting to SCP server 192.168.1.50...
supportsave: Authenticating user 'backup_admin'...
supportsave: Transferring file supportsave_switch1_20240115_143022.tar.gz (487 MB)...
supportsave: Upload complete. File saved to /backups/supportsave/supportsave_switch1_20240115_143022.tar.gz
supportsave: Diagnostic bundle successfully transferred.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `supportsave: Unable to connect to SCP server 192.168.1.50:22 - Connection refused` | Verify the SCP server IP address is correct and the SSH/SCP service is running on port 22. |
    | `supportsave: Authentication failed for user 'backup_admin' - Permission denied (publickey,password)` | Confirm the username and password are correct, or configure SSH key-based authentication on the SCP server. |
    | `supportsave: Insufficient disk space on destination - /backups/supportsave/ has only 50 MB free` | Ensure the destination directory has at least 500 MB of free space available. |
`supportsave` takes 3–8 minutes on a director and produces a `.tar.gz` archive. Upload it to the TAC SR immediately. It contains:

- Running configuration, zone database, name server state
- All logs (RAS log, audit log, port logs)
- Port statistics, SFP data, SNMP trap history
- Platform diagnostics (ASIC registers, CP health)

### supportshow — console diagnostic dump

```bash
# Dump all diagnostics to console (capture with terminal logging enabled)
supportshow
```


```text title="Expected output"
Brocade Fabric OS Support Information Dump
===========================================
System Information
  Fabric OS Version: v9.1.0
  Serial Number: BRK20240156789
  Model: Brocade 6510
  System Uptime: 45 days, 3:22:15
  Current Time: 2024-01-15 14:32:47 UTC

Switch Information
  Switch Name: fabric-switch-01
  Switch IP: 192.168.1.100
  Domain ID: 1
  Fabric State: Online
  Fabric Role: Principal Switch

Port Statistics (First 8 ports shown)
  Port 0: Online, Speed 16Gbps, Frames TX: 2847392, Frames RX: 2851204
  Port 1: Online, Speed 16Gbps, Frames TX: 1923847, Frames RX: 1925103
  Port 2: Offline, Speed N/A, Frames TX: 0, Frames RX: 0
  Port 3: Online, Speed 8Gbps, Frames TX: 847392, Frames RX: 849201
  Port 4: Online, Speed 16Gbps, Frames TX: 3192847, Frames RX: 3194562
  ...

Memory and CPU
  Memory Usage: 68%
  CPU Usage: 12%
  Temperature: 38°C

Zoning Information
  Active Zone Set: prod-zones-v2
  Number of Zones: 24
  Number of Aliases: 18
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `supportshow: command not found` | Verify you are logged into the Brocade switch CLI directly (not a management interface) and have administrative privileges. |
    | `Error: Unable to write to /tmp — disk full` | Free up space on the switch filesystem using `eraseflash` or contact Brocade support to offload diagnostics via SFTP instead. |
Capture the output by enabling logging in your SSH client (PuTTY: Session → Logging; SecureCRT: File → Log Session) before running `supportshow`.

### Targeted data collection

```bash
# Port-specific issue — collect all port data
portshow <slot/port>
sfpshow <slot/port>
portstatsshow <slot/port>
portlogshow <slot/port>
portcfgshow <slot/port>

# Fabric segmentation — collect fabric state
fabricshow
topologyshow
islshow
portlogshow <isl-port>
errshow

# Zoning issue — collect zone database
cfgshow
zoneshow
alishow
nsshow
nsallshow

# Performance issue — collect throughput and credit data
portperfshow
islshow
portbufshow <slot/port>
porterrshow
```


```text title="Expected output"
Port 0/0:
  portName:                   0/0
  portType:                   F-Port
  portState:                  Online
  portSpeed:                  8Gb
  portStatus:                 OK
  sfpStatus:                  OK
  temperature:                32C
  txPower:                    -2.1dBm
  rxPower:                    -8.5dBm

Fabric Information:
  Fabric Name: fabric-prod-01
  Fabric State: Online
  Switch Count: 4
  Switch WWN: 10:00:00:60:e1:00:12:34
  Fabric Principal Switch: 10:00:00:60:e1:00:12:34

ISL Port Information:
  Port 0/24: Online, 8Gb, Connected to Switch 10:00:00:60:e1:00:56:78 Port 0/24
  Port 0/25: Online, 8Gb, Connected to Switch 10:00:00:60:e1:00:9a:bc Port 0/25

Zone Database:
  Zone Name: zone-prod-db
  Zone Members: 50:00:14:40:12:34:56:78, 50:00:14:40:87:65:43:21
  Zone Status: Active

Alias Database:
  Alias Name: alias-db-server
  Alias Members: 50:00:14:40:12:34:56:78

Port Performance (0/0):
  Frames Transmitted: 1,234,567,890
  Frames Received: 987,654,321
  Bytes Transmitted: 45,678,901,234
  Bytes Received: 38,901,234,567
  Link Failures: 0
  Loss of Sync: 0
  Credit Zero: 12
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `portshow: Invalid slot/port specification` | Verify the slot and port numbers are valid for your switch model (e.g., 0/0 through 0/47 for most Brocade switches). |
    | `fabricshow: Fabric offline or not initialized` | Ensure the switch is fully initialized and has completed fabric discovery; check `switchstatusshow` to confirm operational status. |
    | `zoneshow: Zone database locked or being updated` | Wait 30 seconds and retry, as zone changes may be in progress; use `cfgactivate` to commit pending changes if needed. |
---

## Log locations

| Log | Access Command | Contents |
|---|---|---|
| RAS log (hardware and fabric events) | `errshow` / `errdump` | Hardware alerts, fabric topology changes, port events |
| Audit log (security and config changes) | `auditlog --show` | Login events, zone changes, config modifications |
| Port event log | `portlogshow <slot/port>` | Per-port FLOGI, link state, errors |
| MAPS alerts | `mapsdb --show` | Threshold breach events across all monitored resources |
| System message log | `rasshow` | System-level RAS events with severity |
| Firmware download log | `firmwaredownloadstatus` | Firmware upgrade history and status |
| TAC bundle | `supportsave` | All-in-one — required for Broadcom TAC SR |

---

## See also

- [Fabric OS — Common Issues](../common-issues/)
- [Fabric OS — Escalation](../escalation/)
- [Fabric OS — Health Checks](../../operations/health-checks/)

## Verify resolution

- `switchstatusshow` returns `Switch Status: HEALTHY` with no degraded components
- `sensorshow` shows all sensors reporting `OK` (temperature, fan, PSU)
- `portshow <slot/port>` shows the affected port in `Online` state with expected speed and `No_Light` or `Online` — not `Faulty` or `No_Module`
- `sfpshow <slot/port>` shows Rx power within the normal range (-10 to 0 dBm for short-range)
- `errshow | head -20` shows no new ERROR-level events since the fix was applied
- `nsallshow | grep <wwpn>` confirms the host or target WWN is registered in the fabric name server
- `mapsdashboard --show` shows no active threshold violations in the affected port or category
