# RASR — Escalation

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
```text
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
```
```text
Emergency contact sequence:
1. On-call ops → acknowledge within 15 min
2. Infrastructure lead → engage within 30 min
3. Dell ProSupport Sev1 call → open immediately
4. Application owner → notify of outage and ETA
5. Incident commander → declare P1, open bridge
```
