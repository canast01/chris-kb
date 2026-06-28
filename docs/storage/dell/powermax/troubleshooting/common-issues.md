---
tags:
  - dell
  - troubleshooting
search:
  boost: 2
---
# PowerMax — Common Issues


<div class="kb-summary">
Common Issues reference covering Common Issues, Incident Triage.

*Applies to: PowerMax 2500 / 8500*
</div>
![PowerMax — Common Issues](../../../../assets/storage-dell-powermax-troubleshooting-common-issues.svg)




```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}
incident_triage: "Incident Triage" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> common_issues: investigate
symptom -> incident_triage: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
common_issues -> resolution
incident_triage -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?])
    S --> B1{Host connectivity\nlost?}
    S --> B2{SRDF link\ndegraded?}
    S --> B3{TimeFinder clone\nsplit failed?}
    S --> B4{Performance alert\nresponse time spike?}
    S --> B5{Masking view\nmismatch?}

    B1 -->|Check FA port state| D1{Director or\nport faulted?}
    D1 -->|Yes| R1[See Common Issues —\nDirector port I/O errors]
    D1 -->|No| R2[See Common Issues —\nHost cannot see LUN]

    B2 -->|Check RDF group state| D2{Pair state\nSuspended / R1 Updated?}
    D2 -->|Yes| R3[See Common Issues —\nSRDF pair in Suspended state]
    D2 -->|Link down| R4[See Incident Triage —\nSRDF link check]

    B3 -->|Check SnapVX session count| D3{Session count\nat 256 limit?}
    D3 -->|Yes| R5[See Common Issues —\nSnapVX session count at 256]
    D3 -->|No| R6[See Incident Triage —\nEscalate to Dell TAC]

    B4 -->|Check FAST VP tier placement| D4{SLO violation\n>2ms latency?}
    D4 -->|Yes| R7[See Common Issues —\nPerformance SLO violations]
    D4 -->|Cache WP high| R8[See Incident Triage —\nPerformance path]

    B5 -->|Verify initiator group| D5{WWN in\ninitiator group?}
    D5 -->|No| R9[See Common Issues —\nHost cannot see LUN after MV creation]
    D5 -->|Zone missing| R10[See Incident Triage —\nFabric zone check]

    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8,R9,R10 section
    class B1,B2,B3,B4,B5,D1,D2,D3,D4,D5 decision
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

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| SRDF pair in `R1 Updated` or `Transmit Idle` | WAN link failure, R2 array unreachable, or RDF director port error | `symrdf -sid <SID> -rdfg <group> query`; check RDF port state with `symcfg -sid <SID> show`; inspect WAN link and switch port between arrays |
| SRDF pair in `Suspended` state | Manual suspend or automatic suspend triggered by I/O error on R2 | Confirm cause in Unisphere alerts; verify R2 is in a consistent state; resume with `symrdf -sid <SID> -rdfg <group> resume` |
| SnapVX session count at 256 per device | Accumulated snapshots not being expired; backup software snap retention too long | `symsnap list -sid <SID> -sg <sg>` to find stale sessions; `symsnap -sid <SID> -sg <sg> -snap <name> terminate` to remove; review backup software retention policy |
| Thin device subscription warning | Thin pool consumed capacity approaching 80–90%; thin devices over-allocated | `symcfg -sid <SID> -pool <pool> show`; expand pool with additional thin devices; identify over-consuming SGs with `symsg list -sid <SID>` |
| Director port I/O errors / link resets | SAN fabric event, failed SFP, cable issue, or host HBA problem | `symcfg -sid <SID> show` for port error counters; check switch interface statistics; inspect HBA and cable at host end |
| Host cannot see LUN after masking view creation | Incorrect port group, initiator WWN mismatch, or zone not active on fabric | Verify masking view with `symmask -sid <SID> list logins`; confirm host WWN is in initiator group; check fabric zone is active and port is online |
| Unisphere GUI inaccessible | Unisphere service stopped, vApp out of resources, or TLS certificate expired | Check Unisphere vApp VM health; restart Unisphere via `service dell-unisphere restart`; renew TLS cert if expired |
| Performance SLO violations (response time >2 ms) | Pool tier imbalance, FAST VP not migrating data, or I/O load spike | Review FAST VP tier placement in Unisphere → Performance; run `symstat -sid <SID>`; check for runaway workloads in storage groups |

## Incident Triage

When a host reports I/O errors, latency, or a LUN is inaccessible, work through this sequence before escalating.

```mermaid
flowchart TD
    SYMPTOM([Host reports I/O error\nor LUN inaccessible]) --> UNI_ALERT{"Unisphere alerts\nin last 30 min?"}
    UNI_ALERT -->|"Critical alert"| TRIAGE_ALERT["Note component and severity\nProceed to relevant check below"]
    UNI_ALERT -->|"No alert"| DIR_CHK{"symcfg show\nAll directors healthy?"}
    TRIAGE_ALERT --> DIR_CHK
    DIR_CHK -->|"Director faulted"| RAISE_P1["Raise P1 Dell case\nCapture symcfg show\nCheck hardware LEDs"]
    DIR_CHK -->|"OK"| SRDF_CHK{"symrdf list\nSRDF state normal?"}
    SRDF_CHK -->|"Suspended / R1 Updated"| SRDF_FIX["Check WAN link\nResume SRDF if safe\nMonitor resync"]
    SRDF_CHK -->|"OK"| DRIVE_CHK{"sympd list -failed\nFailed drive?"}
    DRIVE_CHK -->|"Drive failed"| DRIVE_FIX["Check RAID parity\nCapture drive state\nRaise Dell hardware case"]
    DRIVE_CHK -->|"OK"| PATH_CHK{"powermt display dev=all\nDead paths on host?"}
    PATH_CHK -->|"Dead paths"| PATH_FIX["Check SAN fabric port\nCheck HBA / cable\nCheck port group config"]
    PATH_CHK -->|"OK"| PERF_CHK{"symstat -type r2\nLatency spike?"}
    PERF_CHK -->|"High latency"| PERF_FIX["Check cache WP%\nIdentify hot SGs\nReview FAST VP tier"]
    PERF_CHK -->|"OK"| MASK_CHK{"symmask list logins\nHost sees LUN in MV?"}
    MASK_CHK -->|"LUN not visible"| MASK_FIX["Verify masking view\nCheck initiator WWN\nCheck fabric zone active"]
    MASK_CHK -->|"Yes"| ESCALATE["Collect diagnostics bundle\nOpen Dell TAC case\nP1 if production impacted"]

    classDef start fill:#15803d,stroke:#166534,color:#fff
    classDef decision fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef action fill:#b45309,stroke:#92400e,color:#fff
    classDef critical fill:#be123c,stroke:#9f1239,color:#fff
    class SYMPTOM start
    class UNI_ALERT,DIR_CHK,SRDF_CHK,DRIVE_CHK,PATH_CHK,PERF_CHK,MASK_CHK decision
    class SRDF_FIX,DRIVE_FIX,PATH_FIX,PERF_FIX,MASK_FIX action
    class RAISE_P1,TRIAGE_ALERT,ESCALATE critical
```

- [ ] Check Unisphere Dashboard immediately for any active alerts flagged in the last 30 minutes — note alert severity and affected component
- [ ] Run `symcfg -sid XXXX show` to confirm array directors and ports are all healthy; look for any director in a degraded or faulted state
- [ ] Check SRDF state: `symrdf list -sid XXXX` — an unexpected `Suspended` or `R1 Updated` state may indicate the cause of host impact
- [ ] Check for failed drives: `sympd list -sid XXXX -failed` — a drive failure can cause I/O latency during rebuild
- [ ] Check host multipath status from the affected host: `powermt display dev=all` — look for dead paths or asymmetric path counts
- [ ] Check Fibre Channel port errors in Unisphere → Hardware → Directors → Ports for CRC errors or login/logout counts
- [ ] Run `symstat -sid XXXX -type r2` to check real-time array I/O statistics for throughput and latency anomalies
- [ ] Review the event log: Unisphere → System → Audit Log and filter by time of the incident

| Question | Answer |
|---|---|
| Which hosts are affected and what is the LUN device ID? | |
| What is the current SRDF state for relevant RDF groups? | |
| Are there active Unisphere alerts at the time of the incident? | |
| What is the host multipath path count and state? | |
| Are there director or port fault indicators in Unisphere? | |

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Powermax — Diagnostics](diagnostics/)
- [Powermax — Escalation](escalation/)
- [Powermax — Health Checks](../operations/health-checks/)
