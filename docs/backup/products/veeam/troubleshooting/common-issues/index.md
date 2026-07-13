---
tags:
  - troubleshooting
  - veeam
search:
  boost: 2
description: "Most Veeam job failures fall into a small set of categories: VMware snapshot issues, repository space problems, proxy connectivity timeouts, and Veeam..."
---
# Veeam — Common Issues

<div class="kb-summary">
Most Veeam job failures fall into a small set of categories: VMware snapshot issues, repository space problems, proxy connectivity timeouts, and Veeam service instability.

*Applies to: Veeam 12.x*
</div>

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

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
A: "Backup job failed — cannot connect to guest" {shape: rectangle}
B: "Repository full" {shape: rectangle}
C: "Restore fails — no valid restore point" {shape: rectangle}
D: "Tape job error" {shape: rectangle}
A1: "A1" {shape: rectangle}
A2: "Check proxy TCP 2500-3300 and VMware Tools — see\nTriage Decision Tree" {shape: rectangle}
A3: "Check VSS writer state and quiesce settings on guest" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "Trigger capacity tier offload manually — see\nRepository Out of Space" {shape: rectangle}
B3: "Reduce retention or delete orphaned backup files" {shape: rectangle}
C1: "C1" {shape: rectangle}
C2: "Check retention policy and catalog — restore point\nmay be expired" {shape: rectangle}
C3: "Check vPower NFS service and mount server access —\nsee Instant VM Recovery" {shape: rectangle}
D1: "D1" {shape: rectangle}
D2: "Check media manager and tape library connectivity" {shape: rectangle}
D3: "Check media expiry and tape slot inventory" {shape: rectangle}
E: "E" {shape: rectangle}
E1: "Restart VBR service and check Windows Event Log —\nsee VBR Service Crash / Instability" {shape: rectangle}

S -> A
S -> B
S -> C
S -> D
A1 -> A2
A1 -> A3
B1 -> B2
B1 -> B3
C1 -> C2
C1 -> C3
D1 -> D2
D1 -> D3
E -> E1
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

```d2
direction: right

fail: "Job failure or warning\ndetected" {shape: rectangle}
openStats: "Open Job Statistics\nExpand failed task\nRead Reason field" {shape: rectangle}
q1: "q1" {shape: rectangle}
snapQ: "Creating or\ncommitting?" {shape: rectangle}
netQ: "Proxy Timeout\n/ Network Error" {shape: rectangle}
spaceQ: "Repository\nOut of Space" {shape: rectangle}
ivrQ: "Instant VM Recovery\nVM Not Starting" {shape: rectangle}
svcQ: "VBR Service\nCrash / Instability" {shape: rectangle}
copyQ: "Backup Copy Job\nNever Completes" {shape: rectangle}
sbQ: "SureBackup Fails" {shape: rectangle}
snapCreate: "Check VMware Tools\nDisable app-aware\nto isolate quiesce issue" {shape: rectangle}
snapCommit: "Check vCenter for\nstuck snapshot\nVerify datastore space" {shape: rectangle}

fail -> openStats
q1 -> snapQ
q1 -> netQ
q1 -> spaceQ
q1 -> ivrQ
q1 -> svcQ
q1 -> copyQ
q1 -> sbQ
snapQ -> snapCreate
snapQ -> snapCommit
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
