# RASR — Escalation

## Escalation Tiers

| Tier | Scope | SLA Target | Owner |
|---|---|---|---|
| T1 — Operations | Known errors, standard recovery procedures | 1 hour initial response | On-call ops team |
| T2 — Infrastructure | Non-standard failures, media/image issues, agent faults | 2 hours | Infrastructure / DR team |
| T3 — Vendor (Dell EMC) | Product bugs, WinPE driver failures, unsupported hardware | 4 hours (severity 1) | Dell ProSupport |

---

## Common Failure Scenarios and Escalation Path

| Failure | Tier | Action |
|---|---|---|
| RASR backup job failed (standard error code) | T1 | Check log, retry, verify share access |
| Share authentication failure | T1 | Verify service account credentials, share permissions |
| Image age alert (backup not run in >8 days) | T1 | Trigger manual backup, investigate scheduler |
| Image integrity check failure (`/verify` returns non-zero) | T2 | Delete corrupt image, trigger new backup, investigate storage |
| RASR Agent service not starting | T2 | Check Windows Event Log, reinstall agent |
| WinPE fails to load at boot | T2 | Regenerate boot media, check ISO integrity |
| WinPE loads but cannot see local disk (PERC) | T2/T3 | Driver issue — inject PERC driver or escalate to Dell |
| Restore fails mid-way (network drop) | T2 | Retry with stable network, check share availability |
| Restore completes but OS does not boot | T2 | Boot WinRE, inject missing storage driver |
| Server hardware not recognized in WinPE | T3 | Escalate to Dell — unsupported hardware generation |
| RASR crashes or produces unexpected exit codes | T3 | Collect logs, open Dell ProSupport case |

---

## Information to Collect Before Escalating

Collect the following before opening a Dell support case or escalating to T3. Incomplete information delays resolution.

### RASR Logs

```powershell
# RASR logs default location
$logDir = "C:\Logs\RASR"
Get-ChildItem -Path $logDir -Filter "*.log" | Sort-Object LastWriteTime | Select-Object -Last 5

# Copy recent logs to a share for the support team
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$archive   = "\\support-share\incidents\RASR_$($env:COMPUTERNAME)_$timestamp"
New-Item -ItemType Directory -Path $archive | Out-Null
Copy-Item "$logDir\*.log" $archive

# Also collect RASR application event log
Get-EventLog -LogName Application -Source "RASR*" -Newest 50 | Export-Csv "$archive\RASR-AppEvents.csv" -NoTypeInformation
```
┌────────────────────────────────────────── RASR — Escalation ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     RASR — Escalation Path                                    │   │
│   │              L1 Triage: review logs, match to known issues in runbook (0–30 min)              │   │
│   │         L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)         │   │
│   │             Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)             │   │
│   │            Sev1 (data loss / production impact): page on-call + open critical case            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Information to Collect Before Escalating                           │   │
│   │                Product version: RASR version string from About / version command              │   │
│   │                                 Full log bundle: cybersense scan                              │   │
│   │                     Symptom timeline: when first occurred; any changes made                   │   │
│   │                Scope: single job / all jobs / all components — narrows root cause             │   │
│   │                    Error codes: exact error messages and exit codes from logs                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts     │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest       │
│  Vault         = isolated, air-gapped storage appliance receiving periodic replication copies         │
│  Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies      │
│  CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures        │
│  PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery      │
│  Air Gap       = physical or logical network isolation preventing attacker lateral movement to        │
│  Delta Set     = incremental changed blocks replicated from production to vault each cycle            │
│  Clean Room    = isolated recovery environment: separate vCenter, network, and workstations           │
│  Recovery Point= specific vault snapshot timestamp from which clean recovery is performed             │
│  Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac       │
│  Journal       = write-order-consistent journal on vault enabling point-in-time recovery              │
│  Scan Report   = CyberSense output: clean/suspect classification per file and block                   │
│  Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept                    │
│  RTO           = Recovery Time Objective; time from failover decision to restored service             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

Or from iDRAC web UI: **Maintenance** → **Lifecycle Log** → **Export**.

### System Information

```powershell
# Collect basic system info for Dell support
$info = @{
    Hostname        = $env:COMPUTERNAME
    OS              = (Get-WmiObject Win32_OperatingSystem).Caption
    OSBuild         = (Get-WmiObject Win32_OperatingSystem).BuildNumber
    RASRVersion     = (Get-Item "C:\Program Files\Dell\RASR\rasrutil.exe").VersionInfo.FileVersion
    DellModel       = (Get-WmiObject Win32_ComputerSystem).Model
    ServiceTag      = (Get-WmiObject Win32_BIOS).SerialNumber
    RASRService     = (Get-Service DellRASR -ErrorAction SilentlyContinue).Status
    LastErrorCode   = $LASTEXITCODE
}

$info | ConvertTo-Json | Out-File "C:\Temp\RASR-SystemInfo.json"
$info
```

### Error Codes to Include

| RASR Exit Code | Meaning | Include in ticket |
|---|---|---|
| 1 | General error | Yes + full log |
| 3 | Destination not accessible | Yes + network trace |
| 4 | Insufficient space | Yes + `df` / disk utilization |
| 5 | Image corrupt | Yes + `/verify` output |
| 6 | Restore target disk not found | Yes + `diskpart list disk` output |
| 10 | Authentication failure | Yes + account audit trail |

---

## Dell EMC Support Contacts

### Dell ProSupport

| Channel | Details |
|---|---|
| Web portal | [https://www.dell.com/support](https://www.dell.com/support) |
| Phone (US) | 1-800-945-3355 |
| Phone (EMEA) | Varies by country — see Dell support site |
| Chat | Available via support.dell.com (ProSupport contracts) |

### Opening a Support Case

1. Log in to [Dell TechDirect](https://techdirect.dell.com) (partner/enterprise account).
2. Click **Service Requests** → **Create Service Request**.
3. Enter the server **Service Tag** (7-character code on physical label, or retrieved via `(Get-WmiObject Win32_BIOS).SerialNumber`).
4. Select:
   - **Product Line:** PowerEdge Server
   - **Category:** Software — Systems Management
   - **Sub-category:** OpenManage / RASR
5. Set severity:
   - **Severity 1 (Critical):** Production server unrecoverable, live outage
   - **Severity 2 (High):** Recovery blocked, backup failing on production server
   - **Severity 3 (Medium):** Non-production issue or workaround available
6. Attach all collected logs and system info.

### Severity 1 — Emergency Escalation Protocol (Failed Server Recovery)

When a production server is down and RASR recovery has failed:

1. **Declare P1 incident** in your ITSM tool.
2. Call Dell ProSupport directly — do not use web-only submission for Sev1.
3. State: "Production server unrecoverable. RASR bare-metal restore failed. Service Tag: XXXXXXX."
4. Dell will engage an on-site technician if hardware is confirmed faulty.
5. Simultaneously, initiate backup escalation:
   - Does the server have a VM equivalent (cold standby)?
   - Can the workload be failed over to DR site?
   - Invoke DR runbook for the affected service.

```text
Emergency contact sequence:
1. On-call ops → acknowledge within 15 min
2. Infrastructure lead → engage within 30 min
3. Dell ProSupport Sev1 call → open immediately
4. Application owner → notify of outage and ETA
5. Incident commander → declare P1, open bridge
```

---

## RASR Diagnostic Checklist

Use this checklist to systematically diagnose RASR failures before escalating.

| Step | Check | Command/Action |
|---|---|---|
| 1 | RASR Agent running? | `Get-Service DellRASR` |
| 2 | Recent RASR logs exist? | `dir C:\Logs\RASR\` |
| 3 | Exit code of failed run? | Check log tail for "Exit code" |
| 4 | Network share accessible? | `Test-Path \\nas01\rasr-images\SERVER01` |
| 5 | Share credentials valid? | `net use \\nas01\rasr-images\SERVER01 /user:...` |
| 6 | Sufficient share space? | `Get-PSDrive` / check NAS capacity |
| 7 | RASR binary intact? | `Get-Item "C:\Program Files\Dell\RASR\rasrutil.exe"` |
| 8 | RASR version supported for OS? | See [version matrix](../../operations/install-upgrade/index.md) |
| 9 | Windows ADK installed? | Check if needed for media creation failures |
| 10 | Existing image integrity? | `rasrutil.exe /verify /source <image>` |
| 11 | Boot media up to date? | Check media creation date vs RASR install date |
| 12 | WinPE network drivers load? | Boot test via iDRAC virtual media |
