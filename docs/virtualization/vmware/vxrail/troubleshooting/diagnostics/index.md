---
tags:
  - troubleshooting
  - vmware
  - vxrail
---
# VxRail — Diagnostics

<div class="kb-summary">
Diagnostic data collection for VxRail clusters: VxRail Manager log paths, ESXi host log grep patterns, iDRAC hardware diagnostics, and Dell support bundle generation. Includes a decision tree for selecting the right log source for each symptom type.

*Applies to: VxRail 7.x / 8.x*
</div>

```text
┌──────────────────────────────────────── VxRail — Diagnostics ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────┐       │
│   │  Four diagnostic data sources — choose based on symptom type                             │        │
│   │  VxRail Manager logs  → plugin issues, LCM failures, API errors                         │         │
│   │  ESXi host logs       → vSAN I/O errors, storage path issues, hostd failures             │        │
│   │  iDRAC diagnostics    → hardware faults: disk, PSU, fan, NIC, memory                    │         │
│   │  Dell support bundle  → full cluster snapshot for escalation to Dell GSS                 │        │
│   └───────────────────────────────────────────────────────────────────────────────────────────┘       │
│                                                                                                       │
│   VxRail Plugin issue?     vSAN/storage issue?     Hardware fault?      Escalating to Dell?           │
│         │                        │                       │                     │                      │
│         ▼                        ▼                       ▼                     ▼                      │
│   VxRail Mgr logs         vmkernel.log           iDRAC SEL / getsel     Generate support              │
│   mystic.log              grep LSOM/DOM          getsysinfo             bundle via Plugin             │
│   lcm.log                 vSAN health UI         vCenter HW view        or API; attach to             │
│   access.log              vm-support bundle      racadm sensors         Dell case                     │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Mystic service   = VxRail Manager daemon; its logs are in /var/log/mystic/                          │
│   LSOM             = Local Log-Structured Object Manager; vSAN storage layer; errors in vmkernel      │
│   DOM              = Distributed Object Manager; vSAN object distribution layer                       │
│   hostd            = ESXi host management daemon; logs VM and host management operations              │
│   iDRAC SEL        = System Event Log; chronological record of all hardware events on the node        │
│   vm-support       = ESXi built-in command that collects a full diagnostic bundle                     │
│   Support bundle   = Dell/VxRail compressed archive of all logs for a case submission                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Diagnostic Decision Tree

Use this tree to select the correct log source before spending time in the wrong place.

```text
  Start: What is the symptom?
  │
  ├─► VxRail Plugin unavailable or shows errors in vCenter
  │       └─► VxRail Manager logs: mystic.log → access.log
  │
  ├─► LCM pre-check failure or upgrade stuck / failed
  │       └─► VxRail Manager logs: lcm.log → mystic.log
  │
  ├─► vSAN object degraded, absent, or health check failing
  │       └─► ESXi vmkernel.log (grep VSAN / LSOM / DOM)
  │           + vSAN Health UI in vCenter
  │
  ├─► Storage path APD or PDL condition
  │       └─► ESXi vmkernel.log (grep APD / PDL / NMP)
  │           + esxcli storage core path list
  │
  ├─► ESXi host management errors or VMs not responding
  │       └─► ESXi hostd.log (grep error / fail)
  │           + vm-support bundle for full capture
  │
  ├─► Hardware alarm: disk / PSU / fan / NIC / memory
  │       └─► iDRAC: racadm getsel + getsysinfo
  │           + vCenter host → Monitor → Hardware
  │
  └─► Preparing for Dell support case (any severity)
          └─► Generate Dell VxRail support bundle
              + vm-support on affected ESXi hosts
              + Export iDRAC SEL as attachment
```

---

## VxRail Manager Logs

### SSH Access and Log Paths

```bash
# SSH to VxRail Manager
ssh mystic@<vxrail-manager-ip>

# List all available log files with sizes
sudo ls -lh /var/log/mystic/
```

### mystic.log — Main Service Log

The primary log for all VxRail Manager operations: plugin registration, API calls, node discovery, and service health.

```bash
# View the last 500 lines
sudo tail -500 /var/log/mystic/mystic.log

# Filter for errors and exceptions
sudo tail -500 /var/log/mystic/mystic.log | grep -i "error\|exception\|critical\|fail"

# Watch live (useful during active troubleshooting)
sudo tail -f /var/log/mystic/mystic.log
```

**What to look for:**
- `ERROR` lines immediately after the Mystic service starts (startup failures)
- `ConnectionRefused` or `Timeout` (VxRail Manager cannot reach vCenter or ESXi hosts)
- `PluginRegistrationFailed` (plugin not registering with vCenter)
- `NodeDiscovery` errors (node not responding to VxRail Manager health poll)

### lcm.log — LCM Upgrade Log

All LCM lifecycle operations are recorded here: pre-check results, upgrade phase transitions, and failure details.

```bash
# View the last 200 lines
sudo tail -200 /var/log/mystic/lcm.log

# Filter for errors, failures, and exceptions
sudo tail -200 /var/log/mystic/lcm.log | grep -i "error\|fail\|exception\|timeout"

# Search for a specific upgrade run by date
sudo grep "2026-06-02" /var/log/mystic/lcm.log | grep -i "error\|fail"
```

**What to look for:**
- Pre-check failure messages with the failing check name (match to resolution table in Common Issues)
- `TIMEOUT` during firmware or VIB stages (iDRAC or ESXi unreachable)
- Phase transitions: `PRECHECK → DOWNLOAD → STAGING → UPGRADE → POSTCHECKS`
- Any phase that does not advance for more than 30 minutes is likely stuck

### access.log — API Access Log

Records all REST API calls to VxRail Manager, including status codes.

```bash
# View recent API calls
sudo tail -200 /var/log/mystic/access.log

# Find 500-series server errors (VxRail Manager API errors)
sudo grep " 5[0-9][0-9] " /var/log/mystic/access.log | tail -50

# Find authentication failures (401)
sudo grep " 401 " /var/log/mystic/access.log | tail -20
```

**What to look for:**
- `500` responses on LCM or support bundle endpoints
- `401` responses (credential issues from vCenter or external tools)
- Repeated requests to the same endpoint timing out

---

## ESXi Host Logs

### Accessing ESXi Logs

```bash
# SSH to the affected ESXi host
ssh root@<esxi-host-ip>

# Log files are in /var/log/ on ESXi
ls /var/log/
```

### vmkernel.log — vSAN and Storage Layer

The kernel-level log. All vSAN I/O errors, storage path events, and network issues are recorded here.

```bash
# vSAN-related events (VSAN, LSOM, DOM components)
tail -100 /var/log/vmkernel.log | grep -i "vsan\|LSOM\|DOM"

# Storage path APD and PDL conditions
tail -100 /var/log/vmkernel.log | grep -i "APD\|PDL\|NMP\|path"

# Network-related kernel errors
tail -100 /var/log/vmkernel.log | grep -i "vmnic\|uplink\|link down"

# Search over a wider window
grep -i "LSOM\|error" /var/log/vmkernel.log | tail -200
```

**What to look for:**

| Pattern | Meaning |
|---|---|
| `LSOM: disk ... failed` | Local disk failure — check iDRAC SEL for hardware fault |
| `DOM: component ... absent` | vSAN object component is absent; check if hosting node is offline |
| `NMP: no more paths` | All paths to a device are dead — PDL condition |
| `APD START` | All Paths Down — storage device temporarily unreachable |
| `vmnic ... link state changed to down` | NIC link dropped — check cable and switch port |
| `VSAN: network partition` | Nodes cannot communicate on vSAN vmkernel network |

### hostd.log — Host Management Daemon

Logs VM power operations, vCenter connection status, and host management errors.

```bash
# Filter for errors and failures
tail -100 /var/log/hostd.log | grep -i "error\|fail"

# Watch during a specific operation (maintenance mode entry, VM migration)
tail -f /var/log/hostd.log

# Find vCenter connection events
grep -i "vpxd\|vCenter\|connect" /var/log/hostd.log | tail -50
```

**What to look for:**
- `Failed to connect to vCenter` (host lost connection to vCenter)
- `Unable to enter maintenance mode` (DRS or vSAN preventing maintenance mode)
- `Task failed` with a specific error message (useful for correlating with vCenter tasks)

### vm-support Bundle Collection

Collect the full ESXi diagnostic bundle for Dell support cases.

```bash
# Collect full support bundle (writes to /tmp/ on the ESXi host)
# This takes 2–5 minutes and does not impact running VMs
vm-support -n -w /tmp/

# List the generated bundle file
ls -lh /tmp/*.tgz

# SCP the bundle to a management workstation
# Run from the management workstation:
scp root@<esxi-host-ip>:/tmp/esx-<hostname>-<timestamp>.tgz ./
```

The `vm-support` bundle includes: vmkernel.log, hostd.log, vpxa.log, network config, storage config, and a snapshot of running process state.

---

## iDRAC Diagnostics

### Accessing iDRAC

```bash
# SSH to the node's iDRAC
ssh root@<node-idrac-ip>

# Alternatively, use racadm remotely from a management host
racadm -r <idrac-ip> -u root -p <password> <command>
```

### getsel — System Event Log

The SEL is the primary source of truth for hardware faults. All disk failures, PSU events, fan failures, and memory errors are recorded here with timestamps.

```bash
# View the last 30 SEL entries
racadm getsel | tail -30

# Filter for critical and warning events
racadm getsel | grep -i "critical\|warning\|fault"

# Clear the SEL (only after capturing current entries for the case)
racadm clrsel
```

**What to look for:**

| SEL Entry Pattern | Meaning |
|---|---|
| `Physical Disk ... Predictive Failure` | Disk is reporting imminent failure — plan replacement |
| `Physical Disk ... Failed` | Disk has failed — replace immediately |
| `Power Supply ... Failure` | PSU failed — check and replace |
| `Power Supply ... Input Lost` | PSU lost AC input — check power feed |
| `Fan ... Failure` | Fan failed — check physical fan; risk of thermal shutdown |
| `Memory ... Correctable ECC` | Single-bit memory error — monitor for accumulation |
| `Memory ... Uncorrectable ECC` | Multi-bit memory error — DIMM must be replaced |
| `Network interface ... link down` | NIC link lost — check cable and switch |

### getsysinfo — System Summary

```bash
# Full system information including fault summary
racadm getsysinfo

# Filter for faults and warnings
racadm getsysinfo | grep -i "fault\|warning\|critical"

# Get power supply status
racadm getsysinfo -t pwrsupply

# Get fan status
racadm getsysinfo -t fan

# Get temperature readings
racadm getsysinfo -t temp
```

### Additional iDRAC Diagnostic Commands

```bash
# Check storage controller and disk health
racadm storage get pdisks -o -p State,PredictiveFailureState,MediaType

# Check RAID / PERC controller status
racadm storage get controllers -o

# Get NIC link status
racadm getniccfg -n NIC.Integrated.1-1

# Reboot iDRAC if it is unresponsive (does not reboot the host)
racadm racreset

# Generate iDRAC Telemetry report (iDRAC 9 and later)
racadm diagnostics run -t QuickTest
```

---

## Dell VxRail Support Bundle Generation

### Via VxRail Plugin (UI Path)

Navigate to: **VxRail Plugin → Support → Generate Support Bundle**

The bundle generation takes 10–20 minutes. A download link appears when complete. The bundle includes:

- VxRail Manager logs (`mystic.log`, `lcm.log`, `access.log`)
- Node health data for all nodes in the cluster
- iDRAC logs from all nodes
- ESXi log excerpts from all nodes

### Via VxRail Manager API

```bash
# SSH to VxRail Manager
ssh mystic@<vxrail-manager-ip>

# Trigger bundle generation
curl -sk -X POST \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  -H "Content-Type: application/json" \
  "https://localhost/rest/vxm/v1/support/bundle"
# Returns a JSON body with a job_id

# Poll job status (replace <job-id> with the returned value)
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://localhost/rest/vxm/v1/requests/<job-id>" | python3 -m json.tool

# When status shows COMPLETED, download the bundle
curl -sk -O \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://localhost/rest/vxm/v1/support/bundle/download"
```

### What Each Log Source Reveals

| Log Source | Best For | When to Use |
|---|---|---|
| mystic.log | Plugin errors, node discovery, API failures | VxRail plugin issues; node not appearing in VxRail Manager |
| lcm.log | LCM pre-check details, upgrade stage failures | Any LCM pre-check failure or stuck upgrade |
| access.log | REST API call history and error codes | Debugging API integrations; tracking who/what called VxRail API |
| vmkernel.log | vSAN I/O path errors, disk failures, network drops | vSAN degraded/absent objects; APD/PDL conditions |
| hostd.log | vCenter connectivity, VM operations, host management | Host disconnected from vCenter; maintenance mode failures |
| iDRAC SEL | Hardware fault timeline | Any hardware alarm; planning disk/PSU/fan replacement |
| vm-support bundle | Full ESXi snapshot for Dell support | Escalating ESXi-level issues; Dell requires this for P1 cases |
| VxRail support bundle | Full cluster snapshot for Dell support | Escalating to Dell GSS; required for all support cases |

---

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
