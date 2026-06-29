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

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "See Symptom Table —\nCG suspended: expand journal volume" {shape: rectangle}
R2: "See Symptom Table —\nSplitter offline: re-register splitter" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "See Symptom Table —\nHigh lag: check RPA performance and WAN" {shape: rectangle}
R4: "See Physical Infrastructure —\nRPA virtual appliance: check ESXi host" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "See Symptom Table —\nImage stuck: force release image access" {shape: rectangle}
R6: "See Symptom Table —\nExpand journal volume before resuming" {shape: rectangle}
D4: "D4" {shape: rectangle}
R7: "See Commands —\nEnable image access via boxmgmt" {shape: rectangle}
R8: "See Symptom Table —\nCG suspended: resolve before testing" {shape: rectangle}
D5: "D5" {shape: rectangle}
R9: "See Symptom Table —\nHigh lag: throttle or upgrade WAN link" {shape: rectangle}
R10: "See Commands —\nGet compression stats and enable compression" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}
B4: "B4" {shape: rectangle}
B5: "B5" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
D4 -> R7
D4 -> R8
D5 -> R9
D5 -> R10
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

- [Recoverpoint — Diagnostics](../diagnostics/)
- [Recoverpoint — Escalation](../escalation/)
- [Recoverpoint — Health Checks](../../operations/health-checks/)
