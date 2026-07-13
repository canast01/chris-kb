---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
description: "Common COD issues — capacity activation failures, allocation errors, and licensing troubleshooting."
---
# COD — Common Issues

<div class="kb-summary">
Common COD issues — capacity activation failures, allocation errors, and licensing troubleshooting.

*Applies to: Cloud for Desktop (COD)*
</div>
![COD — Common Issues](../../../../../assets/storage-dell-cod-troubleshooting-common-issues.svg)

> Part of the [COD](../index.md) reference.

---

| Symptom | Likely Cause | First Action |
|---|---|---|
| COD license not activating | Wrong SID in license file; license already consumed; SYMCLI version mismatch | Verify SID: `symcfg -sid <SID> show`; check `symlicense -sid <SID> list` for existing licenses |
| Capacity shows as unavailable after license applied | Array still binding new devices; may take several minutes | Wait 5–10 minutes; run `symcfg discover`; check Unisphere for device enumeration progress |
| `symlicense install` fails with permission error | Solutions Enabler running under user without SYMCLI admin rights | Run as root or with an account holding StorageAdmin role in Unisphere |
| COD drives not visible after activation | Firmware needs to enumerate new devices; requires `symcfg discover` | `symcfg -sid <SID> discover` — triggers device rediscovery; check Unisphere for newly available devices |
| License key rejected (wrong SID) | License file was issued for a different array SID | Contact Dell License Management portal or account team for re-issuance to correct SID |
| Capacity available in SYMCLI but not usable in Unisphere | New devices not yet bound to a thin pool | Add newly discovered devices to the appropriate thin pool via Unisphere or SYMCLI |
| CloudIQ shows COD headroom as 0 but license portal shows available | CloudIQ telemetry not reflecting latest license activation | Allow 30–60 minutes for CloudIQ to refresh; confirm SCG is forwarding telemetry |
| COD activation audit trail missing | Activation performed without a change ticket or outside SYMCLI | Review SYMCLI audit log; correlate with Unisphere session logs; update CMDB retroactively |

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
R1: "See Issue Reference —\nCapacity request delayed: raise SR in console" {shape: rectangle}
R2: "See Issue Reference —\nReview contracted SLA response time" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "See Issue Reference —\nLicense key rejected: contact Dell for re-issue" {shape: rectangle}
R4: "See Issue Reference —\nsymlicense install: run as StorageAdmin" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "See Issue Reference —\nCOD drives not visible: upgrade firmware first" {shape: rectangle}
R6: "See Issue Reference —\nCapacity available in SYMCLI: bind to thin pool" {shape: rectangle}
D4: "D4" {shape: rectangle}
R7: "See Issue Reference —\nCloudIQ shows 0 headroom: allow 60 min refresh" {shape: rectangle}
R8: "See Issue Reference —\nKey duplicate: do not apply again; contact Dell" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}
B4: "B4" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
D4 -> R7
D4 -> R8
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

- [Cod — Diagnostics](../diagnostics/)
- [Cod — Escalation](../escalation/)
- [Cod — Health Checks](../../operations/health-checks/)
