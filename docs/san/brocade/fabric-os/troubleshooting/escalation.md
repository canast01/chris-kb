---
tags:
  - san
  - troubleshooting
search:
  boost: 1.5
---
# Brocade Fabric OS — Escalation

<div class="kb-summary">
How to escalate Brocade SAN switch issues to Broadcom TAC: what data to collect, how to run supportsave, step-by-step case creation on the Broadcom support portal, and the escalation path when progress stalls.

*Applies to: Brocade Fabric OS 9.x*
</div>
![Brocade Fabric OS — Escalation](../../../../assets/san-brocade-fabric-os-troubleshooting-escalation.svg)




---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
preescalation_selfcheck: "Pre-Escalation Self-Check" {shape: rectangle}
stepbystep_data_collection: "Step-by-Step Data Collection" {shape: rectangle}
how_to_open_the_case_on_broadcom_sup: "How to Open the Case on Broadcom Support Portal" {shape: rectangle}
escalation_path: "Escalation Path" {shape: rectangle}
what_not_to_do: "What NOT to Do" {shape: rectangle}
useful_commands_for_case_updates: "Useful Commands for Case Updates" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> preescalation_selfcheck: investigate
symptom -> stepbystep_data_collection: investigate
symptom -> how_to_open_the_case_on_broadcom_sup: investigate
symptom -> escalation_path: investigate
symptom -> what_not_to_do: investigate
symptom -> useful_commands_for_case_updates: investigate
preescalation_selfcheck -> resolution
stepbystep_data_collection -> resolution
how_to_open_the_case_on_broadcom_sup -> resolution
escalation_path -> resolution
what_not_to_do -> resolution
useful_commands_for_case_updates -> resolution
```

## Before you begin

- **Access required:** SSH access to each Brocade switch (admin credentials); Broadcom support account with the switch serial numbers registered
- **Do this first:** collect supportsave from ALL affected switches before touching anything. TAC will ask for it in their first response
- **Enforce a change freeze:** no zoning changes, no FOS upgrades, no port disabling during the incident. Every change adds a variable and delays diagnosis
- **Do NOT reboot** any switch unless Broadcom TAC explicitly instructs you to — reboots may break fabric stability and overwrite critical log data

---

## Pre-Escalation Self-Check

Run these from each switch's SSH session before opening the case.

| Check | Command | Expected result |
|---|---|---|
| FOS version | `version` | Note full version string (e.g. `v9.2.1d`) |
| Switch health | `switchstatusshow` | All LEDs/ports green; status HEALTHY |
| Fabric status | `fabricshow` | All expected switches present; no unknown domains |
| ISL status | `islshow` | All ISLs show state `Up` |
| Port errors | `porterrshow` | No ports with high CRC, loss-of-sync, or loss-of-signal counts |
| Zone config active | `cfgshow` | Active zone config matches expected baseline |
| Recent errors | `errshow` | Review last 20 entries for hardware faults or segmentation events |
| Principal switch | `fabricshow` | Only one principal switch per fabric; Domain ID stable |

---

## Step-by-Step Data Collection

Run on each affected Brocade switch. SSH as `admin`.

### 1. Get the FOS version and switch serial number

```bash
# FOS version — include in TAC case description
version

# Switch information — chassis model + serial number
switchshow | head -20

# For the full chassis serial number (required to open TAC case)
chassisshow | grep -i serial
```

### 2. Capture fabric state (before anything changes)

```bash
# Full fabric topology — shows all switches, domain IDs, and ISLs
fabricshow

# Zone configuration — active and saved databases
cfgshow

# ISL state — all inter-switch links
islshow

# Port-level error counters — look for CRC, loss-sync, loss-sig
porterrshow
```

Copy the full output of each command into a text file. Paste this into the TAC case description — it gives TAC an immediate view of the fabric state at the time of the issue.

### 3. Run supportsave on each affected switch (takes 2–5 minutes per switch)

```bash
# Configure the SCP destination first (do this once per switch)
ssave --scp <username>@<scp-server-ip>:<path>

# Run supportsave — generates a full diagnostic archive
supportsave

# The archive is transferred automatically to the SCP destination
# It includes: running config, all logs, zone database, port stats, SNMP history
```

Run supportsave on **every** switch in the affected fabric, not just the one that appears to be the source. Fabric issues often show on the downstream switch, not the root cause switch.

### 4. Capture the error log (timeline of events)

```bash
# Switch event log — last 100 entries; paste into TAC case
errshow | head -100

# For long-running incidents, save the full errshow to a file
errshow > /tmp/errshow-$(hostname)-$(date +%Y%m%d).txt
```

### 5. Write the timeline

```text
FOS version: v9.2.1d build 2023120
Switch affected: brocade-core-01.corp.local (Domain ID 1)
Switch serial: BRCxxxxxxx (from chassisshow)
Fabric: Fabric A (two-switch core-edge)
Issue first observed: 2026-06-14 14:30 UTC
Last known good state: 2026-06-14 09:00 UTC
Changes in the 24h before the issue:
  - 09:00: Firmware upgrade FOS 9.2.0 → 9.2.1d applied to brocade-edge-02
  - 14:25: brocade-core-01 reported "ISL E-Port Isolated" on port 16
  - 14:30: 12 hosts lost access to storage on fabric A
Steps already taken:
  - fabricshow: brocade-edge-02 now shows as unknown domain (not in fabric)
  - ISL between core-01 port 16 and edge-02 port 0 is now disabled (zoning conflict)
  - Did NOT change any zone configuration or reboot switches
Blast radius: 12 hosts on fabric A cannot see storage; VMs on those hosts have I/O stalled
```

---

## How to Open the Case on Broadcom Support Portal

1. Go to **support.broadcom.com** and sign in with your Broadcom account. If you do not have one: click **Register** and use your company email — your switch serial numbers must be registered under your account for entitlement.

2. Click **Open a New Case** in the top navigation.

3. Under **Select Product Family**, choose **Brocade** → **Brocade Fibre Channel Switches**.

4. Under **Product**, select your switch model (e.g. Brocade G720, Brocade X7).

5. Under **Serial Number**, enter the chassis serial number from `chassisshow`. This is required to validate your support entitlement.

6. Under **Severity**, select:
   - **Severity 1 — Critical**: Fabric completely down; all hosts on this fabric cannot access storage; VMs have I/O stalled; production outage; no workaround
   - **Severity 2 — High**: Partial fabric degradation; some hosts affected; ISLs down but alternate paths still exist; production impact with temporary workaround
   - **Severity 3 — Medium**: Single switch or port issue; fabric topology intact; no immediate data path loss
   - **Severity 4 — Low**: How-to question, pre-upgrade planning, or non-urgent configuration review

7. In the **Summary** field: switch model + symptom + scope. Example: `Brocade G720 core-01 Domain 1 — ISL isolated after FOS 9.2.1d upgrade; 12 hosts lost fabric-A storage access at 14:30 UTC`.

8. In the **Description** field, paste:
   - FOS version and switch serial from Step 1
   - fabricshow output showing the isolation
   - errshow output around the time of failure
   - The timeline from Step 5
   - What you have already tried

9. Under **Attachments**, upload:
   - The supportsave archive from each affected switch (one ZIP per switch)
   - The errshow text file from Step 4

10. Click **Submit**. You will receive a case number by email immediately.

11. **Severity 1 only:** call Broadcom TAC after submission:
    - Find the number for your region at **support.broadcom.com → Contact Support**
    - State "Severity 1 — fabric down, hosts have no storage access" at the start of the call.
    - Have the case number and switch serial number ready.

---

## Escalation Path

![Brocade Fabric OS — Escalation — Diagram](../../../../assets/san-brocade-fabric-os-troubleshooting-escalation-diagram.svg)

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Change or commit zone configuration during investigation | Changes enforcement state; makes TAC diagnosis harder | Freeze all zone changes until TAC gives explicit go-ahead |
| Reboot the principal switch during an active incident | Can cause domain ID conflicts and worsen fabric stability | Only reboot if TAC says it is safe and has seen the current supportsave |
| Replace SFPs or ISL cables without TAC guidance | The fault may be in switch firmware, not hardware | Let TAC confirm the hardware is the root cause first |
| Upgrade FOS during the incident | Adds variables; may not fix the issue; can worsen state | Only upgrade FOS if TAC confirms it is the fix and provides the build |
| Disable and re-enable ISL ports randomly | Can trigger additional segmentation events | Follow TAC's specific port sequence |
| Remove switches from the fabric manually | Loses diagnostic data from those switches | Keep all switches connected; let TAC analyse the full topology |

---

## Useful Commands for Case Updates

Paste these into case replies to show TAC the current state.

```bash
# Fabric topology (paste after every significant change or update)
fabricshow

# ISL state
islshow

# Port state with speed and status
switchshow

# Error log snapshot
errshow | head -50

# Port error counters (flag any high CRC or loss-of-sync)
porterrshow

# Zone config — confirm active config name
cfgshow | grep -E "cfg:|Defined|Effective"

# SNMP trap history (shows hardware events)
snmpconfig --show

# Firmware revision
version
```

---

## Support Tiers and SLA Reference

| Severity | Definition | Initial Response SLA |
|---|---|---|
| Sev 1 — Critical | Fabric down; all hosts without storage; production outage | 30 minutes (24×7) |
| Sev 2 — High | Partial fabric degradation; alternate paths exist | 4 hours |
| Sev 3 — Medium | Single switch/port issue; no I/O impact | 1 business day |
| Sev 4 — Low | How-to, planning, non-urgent configuration | 2 business days |

---

## See also

- [Brocade Fabric OS — Diagnostics](../diagnostics/)
- [Brocade Fabric OS — Common Issues](../common-issues/)

---

## Verify resolution

- Run `fabricshow` and confirm all expected switches appear with correct domain IDs
- Run `islshow` and confirm all ISLs show `Up`
- Run `porterrshow` and confirm port error counters are not incrementing
- Verify all initiator-target zones are active: `cfgshow` shows the expected active config
- On the affected hosts: run an I/O test (e.g. `dd if=/dev/sdb bs=1M count=100 of=/dev/null`) and confirm storage is accessible
- Monitor `errshow` for 15 minutes and confirm no new fabric isolation or port fault events
