---
tags:
  - san
  - troubleshooting
search:
  boost: 1.5
---
# Cisco MDS — Troubleshooting Common Issues
![Cisco MDS — Troubleshooting Common Issues](../../../../assets/san-cisco-mds-troubleshooting-common-issues.svg)


```bash
# 1. Identify down or errDisabled interfaces
show interface brief

# 2. Identify missing host or storage logins
show flogi database

# 3. Check syslog for the fault event and timeline
show logging last 100

# 4. Rule out hardware faults
show environment

# 5. Confirm zoning is intact
show zoneset active vsan all

# 6. Check ISL and fabric topology
show topology
show trunk
show port-channel summary

# 7. Check domain IDs for conflict
show fcdomain domain-list vsan 10
```

```bash
# Check reason
show interface fc1/4
# Look for: "Port is in error-disabled state"

# Check log for the triggering event
show logging last 200 | grep -i "err\|disabled\|fc1/4"
```
```bash
interface fc1/4
  shutdown
  no shutdown

show interface fc1/4
# Confirm state returns to 'up'
```
```bash
# 1. Is the host HBA logged into the fabric?
show flogi database vsan 10 | grep <host-pwwn>

# 2. Is the storage target logged in?
show flogi database vsan 10 | grep <storage-pwwn>

# 3. Is there a zone pairing these two devices?
show zone member pwwn <host-pwwn> vsan 10

# 4. Is the zoneset containing that zone currently active?
show zoneset active vsan 10

# 5. Are both ports in the same VSAN?
show vsan membership interface fc<host-port>
show vsan membership interface fc<storage-port>
```
```mermaid
flowchart TD
  A["Host cannot see storage"] --> B{"Host pWWN in\nshow flogi database?"}
  B -->|"No"| B1["Check port state\nCheck VSAN assignment\nCheck cable / SFP"]
  B -->|"Yes"| C{"Storage pWWN in\nshow flogi database?"}
  C -->|"No"| C1["Check array port and\nVSAN membership"]
  C -->|"Yes"| D{"Zone containing\nboth devices exists?"}
  D -->|"No"| D1["Create zone with aliases\nAdd to zone set\nActivate zone set"]
  D -->|"Yes"| E{"Zone set\nactive?"}
  E -->|"No"| E1["zoneset activate name\nzoneset-name vsan N"]
  E -->|"Yes"| F{"Still failing?"}
  F -->|"Yes"| F1["Verify WWPNs match\nFLOGI pWWN exactly\nCheck enhanced zoning mode\nCheck IVR if different VSANs"]

  classDef decision fill:#b45309,stroke:#92400e,color:#fff
  classDef fix fill:#1e3a5f,stroke:#3b82f6,color:#e0f2fe
  class B,C,D,E,F decision
  class B1,C1,D1,E1,F1 fix
```
```bash
# Check zone status
show zone status vsan 10

# Check for pending changes in enhanced mode
zone commit vsan 10

# Retry activate
zoneset activate name <zoneset-name> vsan 10
```
```bash
# Check ISL port state
show interface fc2/1
show interface fc2/1 counters errors

# Check trunk state and VSAN allowance
show trunk

# Check port-channel membership if applicable
show port-channel summary

# Check for VSAN isolation reason
show vsan
show vsan <id>
```
```bash
show fcdomain vsan 10
show fcdomain domain-list vsan 10
```
```bash
# Identify flapping port
show logging last 200 | grep "link down\|link up\|flogi" | head -40

# Check error counters on the suspect port
show interface fc1/6 counters errors

# Check optical power levels
show interface fc1/6 transceiver
```
```bash
# Check overall CPU and memory
show system resources

# Find top CPU consumers
show processes cpu sort | head -20

# Check if caused by port flap storm (many FLOGI events)
show logging last 200 | grep -ci "link down"
```
```bash
# Always run this after every configuration change
copy running-config startup-config

# Verify startup config was updated
show startup-config | grep <changed-item>
```
```bash
checkpoint post-change
show checkpoint summary
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> A{Port channel\ndegraded?}
    S --> B{VSAN mismatch\nor isolation?}
    S --> C{BB credit\nstarvation errors?}
    S --> D{Zone conflict\nor host blocked?}
    S --> E{NP port not\nlogged in?}
    A -->|Yes| A1[show port-channel summary\nVerify member port states\nCheck SFP and cable]
    A1 --> A2[ISL / E_Port Issues]
    B -->|Yes| B1[show vsan membership\nshow trunk\nAlign VSAN list on both ends]
    B1 --> B2[ISL / E_Port Issues]
    C -->|Yes| C1[show interface counters\nIdentify slow-drain device\nEnable slow-drain detection]
    C1 --> C2[Performance Issues]
    D -->|Yes| D1{Host pWWN in\nflogi database?}
    D1 -->|No| D2[Check port VSAN · SFP · cable]
    D1 -->|Yes| D3[show zone active\nVerify both WWPNs zoned\nCommit pending changes]
    D3 --> D4[Zoning Issues]
    E -->|Yes| E1[show interface fc\nCheck NPV/NPIV config\nVerify FLOGI on parent port]
    E1 --> E2[Login Failures]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class A2,B2,C2,D4,E2 section
    class A,B,C,D,D1,E decision
    class S start
```

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Mds — Diagnostics](diagnostics/)
- [Mds — Escalation](escalation/)
- [Mds — Health Checks](../operations/health-checks/)
