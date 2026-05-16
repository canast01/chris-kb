# Horizon — Escalation

---

## Before Opening a VMware Support Case

Collect the following:

| Item | How to Collect |
|---|---|
| Horizon support bundle | Horizon Console → Help → Download Support Bundle |
| UAG log bundle | UAG Admin UI REST API or SSH to appliance |
| Affected user session ID | Horizon Console → Monitor → Sessions → select session → ID |
| Desktop VM name | Note the exact VM name from Horizon Console |
| vCenter events for affected VM | vCenter → [VM] → Monitor → Events |
| Horizon Agent logs from guest | `C:\ProgramData\VMware\VDM\logs\` from inside VM |
| Horizon version | Horizon Console → Help → About |
| vSphere version | vCenter → About |
| App Volumes version | App Volumes Manager → About (if App Volumes involved) |
| Symptom timeline | When first reported, what changed before issue began |
| Pool configuration screenshot | Pool settings including protocol and clone type |

---

## Severity Definitions

| Severity | Condition |
|---|---|
| Sev 1 | All users unable to connect — complete VDI outage |
| Sev 2 | Partial outage — specific pool or site down, significant user impact |
| Sev 3 | Single user or desktop issue, intermittent problems |
| Sev 4 | General question, minor cosmetic issue, feature request |

For Sev 1: create case online, then immediately call VMware Support to request phone bridge.

---

## Additional Diagnostic Steps Before Escalation

```powershell
# Export last 24 hours of Connection Server events:
Get-WinEvent -LogName "Application" -MaxEvents 500 |
  Where-Object { $_.ProviderName -like "*VMware*" -and 
                 $_.TimeCreated -gt (Get-Date).AddHours(-24) } |
  Select-Object TimeCreated, LevelDisplayName, Message |
  Export-Csv "horizon-cs-events-$(Get-Date -Format yyyyMMdd-HHmm).csv" -NoTypeInformation

# Export active session list
Get-HVLocalSession | Export-Csv "horizon-sessions.csv" -NoTypeInformation
```

---

## Engage VMware Support

1. **Portal:** customerconnect.vmware.com → Log Case
   - Product: VMware Horizon
   - Version: [current version]
   - Component: Connection Server / UAG / Agent / App Volumes (specify)
   - Problem: [describe symptom and impact]

2. **Attach:** support bundle, event exports, symptom description

3. **For Sev 1:** after creating case, call VMware Support and reference the case number for immediate phone assistance

---

## Escalation Within VMware

| Path | Trigger |
|---|---|
| Technical Account Manager | Contract with TAM — contact directly for priority handling |
| Critical Escalation Team | Sev 1 not resolved within SLA — request escalation via Support portal |
| Engineering escalation | Bug suspected — request escalation to Horizon engineering team |

---

## Useful Resources

- Horizon Documentation: docs.vmware.com/horizon
- Horizon Compatibility Matrix: interopmatrix.vmware.com
- VMware KB for Horizon: kb.vmware.com (search "VMware Horizon")
- Horizon Community Forum: communities.vmware.com/community/vmtn/horizon
- Horizon ADMX GPO templates: downloaded with Connection Server installer
