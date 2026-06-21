---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# RecoverPoint — Common Issues
![RecoverPoint — Common Issues](../../../../assets/storage-dell-recoverpoint-troubleshooting-common-issues.svg)


```bash
# Via boxmgmt SSH to RPA
boxmgmt cg check_cg <CG-name>
boxmgmt list cg
boxmgmt system status
```

```bash
boxmgmt cg check_cg <CG-name>
boxmgmt system performance
```
```bash
boxmgmt cg enable_image_access <CG-name> <copy-name>
boxmgmt cg recover_production <CG-name>
```

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?])
    S --> B1{Journal full\nreplication paused?}
    S --> B2{RPA cluster\ndegraded?}
    S --> B3{Consistency group\nsuspended?}
    S --> B4{Failover test\nfailed?}
    S --> B5{Link bandwidth\nsaturated?}

    B1 -->|Check journal capacity| D1{Journal volume\nabove 80 percent?}
    D1 -->|Yes| R1[See Symptom Table —\nCG suspended: expand journal volume]
    D1 -->|Splitter offline| R2[See Symptom Table —\nSplitter offline: re-register splitter]

    B2 -->|Check boxmgmt system status| D2{RPA in\nfault state?}
    D2 -->|Yes| R3[See Symptom Table —\nHigh lag: check RPA performance and WAN]
    D2 -->|VM not running| R4[See Physical Infrastructure —\nRPA virtual appliance: check ESXi host]

    B3 -->|Check CG state with boxmgmt| D3{CG suspended\nor in error?}
    D3 -->|Image stuck| R5[See Symptom Table —\nImage stuck: force release image access]
    D3 -->|Journal full| R6[See Symptom Table —\nExpand journal volume before resuming]

    B4 -->|Verify image access enabled| D4{Image accessible\nfor test copy?}
    D4 -->|No| R7[See Commands —\nEnable image access via boxmgmt]
    D4 -->|CG not consistent| R8[See Symptom Table —\nCG suspended: resolve before testing]

    B5 -->|Check WAN utilisation| D5{Replication lag\ngrowing?}
    D5 -->|WAN saturated| R9[See Symptom Table —\nHigh lag: throttle or upgrade WAN link]
    D5 -->|Compression off| R10[See Commands —\nGet compression stats and enable compression]

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

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Recoverpoint — Diagnostics](diagnostics/)
- [Recoverpoint — Escalation](escalation/)
- [Recoverpoint — Health Checks](../operations/health-checks/)
