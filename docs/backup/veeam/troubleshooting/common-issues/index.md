---
tags:
  - troubleshooting
  - veeam
search:
  boost: 2
---
# Veeam — Common Issues


<div class="kb-summary">
Most Veeam job failures fall into a small set of categories: VMware snapshot issues, repository space problems, proxy connectivity timeouts, and Veeam service instability.

*Applies to: Veeam 12.x*
</div>
![Veeam — Common Issues](../../../../assets/backup-veeam-troubleshooting-common-issues-index.svg)


 The first step for any failure is to open the job statistics view in the console — the task-level error message and reason field usually point to the root cause without needing to open log files.

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
triage_decision_tree: "Triage Decision Tree" {shape: rectangle}
repository_out_of_space: "Repository Out of Space" {shape: rectangle}
instant_vm_recovery_vm_not_starting: "Instant VM Recovery — VM Not Starting" {shape: rectangle}
vbr_service_crash_instability: "VBR Service Crash / Instability" {shape: rectangle}
backup_copy_job_never_completes: "Backup Copy Job Never Completes" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> triage_decision_tree: investigate
symptom -> repository_out_of_space: investigate
symptom -> instant_vm_recovery_vm_not_starting: investigate
symptom -> vbr_service_crash_instability: investigate
symptom -> backup_copy_job_never_completes: investigate
diagnostic_flow -> resolution
triage_decision_tree -> resolution
repository_out_of_space -> resolution
instant_vm_recovery_vm_not_starting -> resolution
vbr_service_crash_instability -> resolution
backup_copy_job_never_completes -> resolution
```

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> A[Backup job failed — cannot connect to guest]
    S --> B[Repository full]
    S --> C[Restore fails — no valid restore point]
    S --> D[Tape job error]
    S --> E[Veeam B&R service crashed]
    A --> A1{Proxy reachable?}
    A1 -->|No| A2[Check proxy TCP 2500-3300 and VMware Tools — see Triage Decision Tree]
    A1 -->|Yes| A3[Check VSS writer state and quiesce settings on guest]
    B --> B1{SOBR offload configured?}
    B1 -->|Yes| B2[Trigger capacity tier offload manually — see Repository Out of Space]
    B1 -->|No| B3[Reduce retention or delete orphaned backup files]
    C --> C1{Restore point visible in console?}
    C1 -->|No| C2[Check retention policy and catalog — restore point may be expired]
    C1 -->|Yes| C3[Check vPower NFS service and mount server access — see Instant VM Recovery]
    D --> D1{Tape library online?}
    D1 -->|No| D2[Check media manager and tape library connectivity]
    D1 -->|Yes| D3[Check media expiry and tape slot inventory]
    E --> E1[Restart VBR service and check Windows Event Log — see VBR Service Crash / Instability]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class A,B,C,D,E,A2,A3,B2,B3,C2,C3,D2,D3,E1 section
    class A1,B1,C1,D1 decision
    class S start
```

---

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Triage Decision Tree

```mermaid
flowchart TD
    fail(["Job failure or warning\ndetected"])
    fail --> openStats["Open Job Statistics\nExpand failed task\nRead Reason field"]
    openStats --> q1{Error category}

    q1 -->|"Snapshot / VSS\nerror"| snapQ{"Creating or\ncommitting?"}
    q1 -->|"Network /\nconnection\nerror"| netQ["Proxy Timeout\n/ Network Error"]
    q1 -->|"No space /\nquota"| spaceQ["Repository\nOut of Space"]
    q1 -->|"IVR VM\nnot booting"| ivrQ["Instant VM Recovery\nVM Not Starting"]
    q1 -->|"VBR service\ncrash"| svcQ["VBR Service\nCrash / Instability"]
    q1 -->|"Copy job\nnever finishes"| copyQ["Backup Copy Job\nNever Completes"]
    q1 -->|"SureBackup\nfailed"| sbQ["SureBackup Fails"]

    snapQ -->|"Creating"| snapCreate["Check VMware Tools\nDisable app-aware\nto isolate quiesce issue"]
    snapQ -->|"Committing"| snapCommit["Check vCenter for\nstuck snapshot\nVerify datastore space"]

    classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff
    class openStats,netQ,spaceQ,ivrQ,svcQ,copyQ,sbQ,snapCreate,snapCommit action
    class q1,snapQ decision
    class fail terminal
```


Veeam uses ports 2500–3300 (TCP) for data channel communication between VBR, proxies, and repositories.

**Check proxy resource exhaustion:** if the proxy CPU or RAM is at capacity, tasks queue and eventually time out. Increase max concurrent tasks or add a proxy.

---

## Repository Out of Space

**Symptom:** Job fails with "not enough free disk space on the repository" or "Veeam backup files have been detected outside of the quota."

```powershell
# Check repository free space
Get-VBRBackupRepository | Select Name, FriendlyPath, Path,
  @{N="FreeMB";E={[math]::Round($_.GetContainer().CachedFreeSpace / 1MB)}}
```

**Immediate remediation:**

1. Check if SOBR capacity tier offload is configured and working — manually trigger offload if needed.
2. Identify large backup chains that can be reduced:

```powershell
# Find largest backup chains
Get-VBRBackup | Select JobName, @{N="SizeGB";E={[math]::Round(($_.GetStorageFiles() | Measure-Object -Property Stats -Sum).Sum.DataSize / 1GB, 1)}} | Sort-Object SizeGB -Descending
```

3. Reduce retention policy on some jobs to free space sooner.
4. Delete orphaned backup files (Backups → Orphaned → Remove from disk).

---

## Instant VM Recovery — VM Not Starting

**Symptom:** Instant recovery completes but the recovered VM does not boot, cannot be accessed over the network, or vNIC is not working.

**Check in order:**

1. **Datastore access from recovery proxy** — the proxy needs direct access to the backup repository to mount the NFS datastore used for instant recovery.
2. **Network configuration of the recovered VM** — Instant Recovery places the VM in a publish network by default. Verify it is connected to the correct port group.
3. **Veeam vPower NFS service** — if the NFS service is not running on the proxy, the virtual disk cannot be mounted:

```cmd
# On the Veeam proxy — check the vPower NFS service
Get-Service -Name VeeamVssProvider
Get-Service -Name VeeamNFSSvc
```

---

## VBR Service Crash / Instability

**Symptom:** Jobs fail to start, Veeam console cannot connect, or the VBR service restarts repeatedly.

```cmd
# Check Windows Event Log on the VBR server
Get-EventLog -LogName Application -Source "Veeam*" -Newest 50 | Select TimeGenerated, Message | Format-List

# Check Veeam service log
Get-Content "C:\ProgramData\Veeam\Backup\Svc.VeeamBackup.log" -Tail 100
```

**Restart the VBR service:**

```cmd
# Restart the Veeam Backup Service (all running jobs will be interrupted and resume from checkpoint)
net stop "Veeam Backup Service"
net start "Veeam Backup Service"
```

---

## Backup Copy Job Never Completes

**Symptom:** The backup copy job runs continuously, never reaching a "Success" state, or transfers a tiny amount of data each cycle.

**Check:**

1. **WAN Accelerator stats** — if using WAN Acceleration, check if the cache is populated and the source/target accelerators are connected.
2. **Target repository reachability** — test port 2500–3300 from the source repository server to the target.
3. **Retention difference** — the copy job may be waiting for a full restore point that matches the target retention window.
4. **Seeding** — for a new backup copy job over a slow WAN, seed the initial full backup locally and ship it to the remote site (Veeam seeding procedure).

---

## SureBackup Fails

**Symptom:** SureBackup verification job reports "VM failed to start" or "application test script failed."

```powershell
# Check virtual lab network mapping
Get-VBRVirtualLab | Select Name, Platform, Description
```

1. Verify the **virtual lab network mapping** — the VLan used inside the isolated lab must be mapped to a real port group.
2. Check **test credentials** — SureBackup uses guest credentials to run verification scripts; confirm they are correct and the account is not locked.
3. For application-aware tests (SQL, Exchange), confirm the VM's application services started within the timeout window (default 2 minutes; increase if needed for slow VMs).
4. Check the SureBackup session log for the specific task that failed — it lists which VM and which test step failed.

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Veeam — Diagnostics](../diagnostics/)
- [Veeam — Escalation](../escalation/)
- [Veeam — Health Checks](../../operations/health-checks/)
