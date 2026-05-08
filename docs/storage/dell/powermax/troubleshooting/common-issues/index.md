# PowerMax — Common Issues

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
