---
tags:
  - networking
  - troubleshooting
search:
  boost: 1.5
---
# FC Troubleshooting

<div class="kb-summary">
FC Troubleshooting reference covering Diagnostic Flow, Quick Diagnostics, Common Issues Reference, Error Counter Interpretation (Brocade), Log Locations.
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
quick_diagnostics: "Quick Diagnostics" {shape: rectangle}
common_issues_reference: "Common Issues Reference" {shape: rectangle}
error_counter_interpretation_brocade: "Error Counter Interpretation (Brocade)" {shape: rectangle}
log_locations: "Log Locations" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> quick_diagnostics: investigate
symptom -> common_issues_reference: investigate
symptom -> error_counter_interpretation_brocade: investigate
symptom -> log_locations: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
quick_diagnostics -> resolution
common_issues_reference -> resolution
error_counter_interpretation_brocade -> resolution
log_locations -> resolution
verify_resolution -> resolution
```

## Before you begin

- **Access:** Network admin credentials; console or SSH to devices
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Diagnostic Flow

```d2
direction: right

B: "B" {shape: rectangle}
C: "Check SFP, cable, port state" {shape: rectangle}
D: "D" {shape: rectangle}
E: "HBA not logged in — driver, speed, SFP" {shape: rectangle}
F: "F" {shape: rectangle}
G: "Fix zone — add missing WWPN, activate" {shape: rectangle}
H: "H" {shape: rectangle}
I: "Add host to storage host group" {shape: rectangle}
J: "J" {shape: rectangle}
K: "Rescan HBAs, reload multipath" {shape: rectangle}
L: "Check OS disk/filesystem layer" {shape: rectangle}
A: "Host cannot see LUN" {shape: rectangle}

B -> C
D -> E
F -> G
H -> I
J -> K
J -> L
```

## Quick Diagnostics

```bash
# Brocade — overall fabric health
fabricshow
switchshow
porterrshow

# Brocade — nameserver (who is logged in)
nsshow
nsallshow

# Brocade — zone config
cfgshow
zoneshow

# Cisco MDS — fabric login table
show flogi database vsan 10
show fcns database vsan 10
show zoneset active vsan 10

# Linux — multipath state
multipath -ll
cat /proc/scsi/scsi

# ESXi — path state
esxcli storage core path list
esxcli storage core adapter list
```

## Common Issues Reference

| Symptom | Likely cause | First check |
|---|---|---|
| Host sees no LUNs | FLOGI failed or zone missing | `nsshow` — is WWPN registered? |
| LUNs disappeared suddenly | Link down or SFP fault | `portshow` / switch LED / `porterrshow` |
| Intermittent path drops | Marginal SFP or cable | `porterrshow` — CRC errors, loss-of-sync |
| Slow I/O on FC | Port congestion (BB_Credit exhaustion) | `portbuffershow` on Brocade |
| Only one of two paths active | Zone missing on second fabric | Check both fabric A and B zoning independently |
| New server cannot see storage | Zone not created / activated | Create zone, add to cfgsave, activate |
| Zone exists but still no access | WWPN typo in zone | `zoneshow` — compare WWPNs character by character |
| HBA not seen after reboot | Driver not loading or HBA disabled | `dmesg | grep -i qla` or `lpfc` |

## Error Counter Interpretation (Brocade)

```bash
porterrshow
```

| Counter | Acceptable | Investigate if |
|---|---|---|
| CRC | 0 | > 0 in last hour |
| Loss of Signal | 0 | Any increment |
| Loss of Sync | 0 | > 5 in last hour |
| Encoding Errors | 0 | Any increment |
| Too Many RDYs | 0 | Any — BB_Credit issue |

## Log Locations

| Platform | Log |
|---|---|
| Brocade | `raslog` (CLI) / Brocade SANnav |
| Cisco MDS | `show logging` / DCNM |
| Linux HBA (QLogic) | `/var/log/messages` — `qla2xxx` |
| Linux HBA (Emulex) | `/var/log/messages` — `lpfc` |
| ESXi | `esxcli storage core path list` / `vmkwarning.log` |

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Fabric Login](../fabric-login/)
- [Paths](../paths/)
- [Wwns](../wwns/)
- [Zoning](../zoning/)
- [Fibre Channel — Overview](../)
