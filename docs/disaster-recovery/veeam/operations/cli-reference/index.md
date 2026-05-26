# Veeam — CLI Reference

## Backup Infrastructure Topology

The Veeam component hierarchy governs how jobs are routed, where data lands, and which components need to be healthy for a job to succeed.

```mermaid
flowchart TD
    subgraph controlPlane [Control Plane]
        vbr["Veeam Backup &\nReplication Server\n(job orchestration + config DB)"]
        vone["Veeam ONE\n(monitoring + reporting)"]
        vbr --> vone
    end

    subgraph dataPath [Data Path — Site A]
        proxy1["Backup Proxy 1\n(hot-add / SAN)"]
        proxy2["Backup Proxy 2\n(NBD fallback)"]
        sobr[("SOBR\nScale-Out Backup Repo\n(performance tier — fast disk)")]
        proxy1 --> sobr
        proxy2 --> sobr
    end

    subgraph offsite [Offsite / Cloud Tier]
        obj[("Object Storage\nS3 / Azure Blob\n(capacity tier — immutable)")]
        tape[("Tape Library\n(archival)")]
    end

    vcenter(["VMware vCenter\nSource VMs"])
    vcenter --> proxy1
    vcenter --> proxy2
    vbr --> proxy1
    vbr --> proxy2
    sobr -->|"capacity tier offload\n(after retention threshold)"| obj
    sobr -->|"tape offload"| tape

    classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
    classDef host fill:#15803d,stroke:#166534,color:#fff
    classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
    class vbr,vone,proxy1,proxy2 ctrl
    class sobr,tape store
    class vcenter host
    class obj cloud
```

---

## Jobs

Jobs are the primary operational unit in Veeam.

```powershell
# List all backup jobs with last result
Get-VBRJob | Select Name, JobType, LastResult, NextRun

# Find failed jobs
Get-VBRJob | Where-Object { $_.LastResult -eq "Failed" }

# Start a job manually
Start-VBRJob -Job (Get-VBRJob -Name "prod-vm-daily")

# Stop a running job
Stop-VBRJob -Job (Get-VBRJob -Name "prod-vm-daily")
```

---

## Sessions & History

```powershell
# List recent sessions, newest first
Get-VBRBackupSession | Sort-Object CreationTime -Descending | Select -First 20

# Show session result and duration for a job
Get-VBRBackupSession | Where-Object { $_.JobName -eq "prod-vm-daily" } |
  Select JobName, State, Result, CreationTime, EndTime
```

---

## Restore Points

```powershell
# List restore points for a VM
Get-VBRRestorePoint -Name "vm01" | Select Name, CreationTime, IsCorrupted

# Find latest restore point for a VM
Get-VBRRestorePoint -Name "vm01" | Sort-Object CreationTime -Descending | Select -First 1

# Find restore points for all VMs in a job
Get-VBRBackup -Name "prod-vm-daily" | Get-VBRRestorePoint
```

---

## VM Restore

```powershell
# Instant VM recovery to original location
$rp = Get-VBRRestorePoint -Name "vm01" | Sort-Object CreationTime -Descending | Select -First 1
Start-VBRRestoreVM -RestorePoint $rp -Reason "DR test"

# Full VM restore
Start-VBRVMFLRRestore -RestorePoint $rp

# File-level restore (Windows)
Start-VBRWindowsFileRestore -RestorePoint $rp
```

---

## Infrastructure

```powershell
# List repositories with free/total space
Get-VBRRepository | Select Name,
  @{N="FreeTB"; E={[math]::Round($_.FreeSpace/1TB,2)}},
  @{N="TotalTB"; E={[math]::Round($_.TotalSpace/1TB,2)}}

# List proxies
Get-VBRViProxy

# List protected VMs
Get-VBRProtectedVM
```

---

## Configuration Backup

```powershell
# Export configuration backup
Export-VBRConfiguration -Path "C:\vbr-config-backup.xml"

# Check last config backup
Get-VBRConfigurationDatabaseBackup
```
