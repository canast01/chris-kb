# RASR — Health Checks


<div class="kb-summary">
> Part of the [RASR Operations](../index.md) reference.
</div>

---

Regular health checks verify that RASR is ready to perform a recovery — before an incident occurs. Run these on a monthly cadence and after any change to protected servers.

## Quick Health Check (5 minutes)

Run on each RASR-protected server:

```powershell
# Collect all key indicators in one pass
$rasrKey = "HKLM:\SOFTWARE\Dell\RASR"
$share   = "\\nas01\rasr-images\prod\$(hostname)"

[PSCustomObject]@{
    Server          = hostname
    AgentStatus     = (Get-Service RASRAgent).Status
    AgentVersion    = (Get-ItemProperty $rasrKey -ErrorAction SilentlyContinue).Version
    LastBackup      = (Get-ItemProperty $rasrKey -ErrorAction SilentlyContinue).LastBackupTime
    LastResult      = (Get-ItemProperty $rasrKey -ErrorAction SilentlyContinue).LastBackupResult
    BackupAge_h     = [math]::Round(((Get-Date) - [datetime](Get-ItemProperty $rasrKey).LastBackupTime).TotalHours, 1)
    ShareReachable  = (Test-Path $share)
    LatestImage     = (Get-ChildItem $share -Filter "*.wim" -ErrorAction SilentlyContinue |
                       Sort-Object LastWriteTime -Descending | Select-Object -First 1).Name
} | Format-List
```
┌──────────────────────────────────────── RASR — Health Checks ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 RASR — Health Check Procedures                                │   │
│   │                 Run these checks daily/weekly to confirm protection is working                │   │
│   │                                         cybersense scan                                       │   │
│   │                  Review job completion rate — target 100%; investigate failures               │   │
│   │                         Check replication/backup lag against RPO target                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   │      Check       │  What to verify  │      Expected     │    Frequency     │  Action if bad   │   │
│   │    Job status    │All jobs complete │    100% success   │      Daily       │ Triage failures  │   │
│   │    Lag / RPO     │ Replication lag  │    < RPO target   │      Daily       │  Tune bandwidth  │   │
│   │     Capacity     │ Repo space used  │     < 80% full    │      Weekly      │ Expand or expire │   │
│   │   Restore test   │  Random restore  │    Data intact    │     Monthly      │ Fix backup chain │   │
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
```sql

### 4. VSS Writer Health

```powershell
# Check VSS writers are in stable state
$writers = vssadmin list writers 2>&1
$failed = $writers | Select-String "State: \[8\] Failed"
if ($failed) {
    Write-Warning "FAIL: VSS writers in failed state:"
    $failed
} else {
    Write-Host "PASS: All VSS writers stable"
}
```

### 5. iDRAC Media Mapping Test

Test via iDRAC web UI (cannot be scripted without Redfish):

```text
iDRAC → Configuration → Virtual Media → Verify ISO is mapped
iDRAC → Overview → Boot → Boot Next = Virtual Optical Drive
(Optional: perform test boot in next maintenance window)
```

```bash
# Via Redfish API
curl -sk -u root:<password> \
  https://<idrac-ip>/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia \
  | python3 -m json.tool
```

## Fleet-Wide Health Check

Run monthly across all RASR-protected servers:

```powershell
$servers = @("app01", "app02", "db01", "web01")   # update per environment

$report = foreach ($server in $servers) {
    try {
        $result = Invoke-Command -ComputerName $server -ScriptBlock {
            $k = "HKLM:\SOFTWARE\Dell\RASR"
            $lastBkp = [datetime](Get-ItemProperty $k -ErrorAction Stop).LastBackupTime
            @{
                Agent   = (Get-Service RASRAgent).Status
                AgeH    = [math]::Round(((Get-Date) - $lastBkp).TotalHours, 1)
                Result  = (Get-ItemProperty $k).LastBackupResult
            }
        } -ErrorAction Stop

        [PSCustomObject]@{
            Server  = $server
            Agent   = $result.Agent
            AgeH    = $result.AgeH
            Result  = $result.Result
            Status  = if ($result.Agent -eq "Running" -and $result.Result -eq "Success" -and $result.AgeH -lt 26) {"OK"} else {"REVIEW"}
        }
    } catch {
        [PSCustomObject]@{ Server = $server; Agent = "UNREACHABLE"; AgeH = 0; Result = "N/A"; Status = "REVIEW" }
    }
}

$report | Sort-Object Status -Descending | Format-Table
```

## Health Check Sign-Off

Document results monthly in the DR register:

```text
Date: ___________  Performed by: ___________
Servers checked: ___ / ___
Servers passing all checks: ___ / ___
Issues found: ___________
Actions taken: ___________
Next check due: ___________
```
