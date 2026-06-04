# RASR — Procedures

RASR (Ransomware Air-gap Secure Recovery) is the Dell end-to-end workflow for detecting ransomware, isolating clean vault copies, and recovering workloads into a clean-room environment using PowerProtect Data Manager (PPDM) and CyberSense.

---

## Run a Full Recovery Test

A full recovery test validates that vault replicas can be restored into the clean-room environment within the agreed RTO. Schedule in a maintenance window and raise a change ticket before starting.

1. Log in to the PPDM console at `https://<ppdm-ip>:8443` and navigate to **Cyber Recovery > Recovery Tests**.
2. Select the protection policy to test and click **Run Recovery Test**.
3. Choose the recovery point (vault snapshot) to recover from — select the most recent CyberSense-verified clean point.
4. Set the target as the clean-room vCenter (`vcsa-cleanroom.local`) and an isolated port group with no production network access.
5. Click **Start Test**; PPDM orchestrates VM registration on clean-room ESXi hosts.
6. Validate application services on the recovered VMs (ping, web probe, database connect test).
7. Log results in the DR runbook; click **End Recovery Test** to deregister and clean up clean-room VMs.
8. Retain the test report from **Reports > Recovery Test Summary** and attach it to the change ticket.

---

## Restore a Single VM

Use this procedure to recover an individual VM from a vault snapshot into either the clean room or a production-equivalent environment.

1. In PPDM, go to **Recovery > Virtual Machines** and search for the VM by name.
2. Select the desired restore point; confirm the CyberSense status column shows **Clean** before proceeding.
3. Click **Restore** and choose **Restore to New Location** to avoid overwriting the production VM.
4. Set target vCenter, datacenter, cluster, datastore, and network (use isolated network for clean-room; production network for normal restores).
5. Enable **Power on VM after restore** only after the VM is connected to the correct network segment.
6. Monitor the restore task in **Jobs > Active Jobs**; typical single-VM restore completes in 15–40 minutes depending on size.
7. Log in to the restored VM and confirm OS boot, application health, and data integrity.
8. Document the restore point used and recovery duration in the incident ticket.

---

## Restore File-Level from Backup

Use file-level recovery (FLR) to retrieve individual files or folders without restoring the full VM.

1. In PPDM, navigate to **Recovery > File-Level Recovery** and select the source VM.
2. Choose the restore point; wait for the backup mount to complete (PPDM mounts the VMDK as a virtual datastore).
3. Browse the mounted file system in the FLR browser panel; navigate to the target directory.
4. Select one or more files or folders and click **Restore**.
5. Choose **Restore to Original Location** (overwrites existing) or **Restore to Alternate Location** (specify a network path, e.g., `\\filsrv01\restore-staging\`).
6. Confirm the restore job completes in **Jobs** and verify file presence and permissions at the destination.
7. Unmount the backup after recovery — PPDM releases the mount automatically after 15 minutes of inactivity, or click **Unmount** in the FLR session panel.

---

## Configure Recovery Target

A recovery target defines where PPDM sends restored workloads. Configure targets for both the clean-room and any alternate production sites.

1. In PPDM, go to **Infrastructure > Asset Sources** and click **+ Add**.
2. Select **VMware vCenter Server** and enter the FQDN of the target vCenter (e.g., `vcsa-cleanroom.local`).
3. Enter service account credentials — account must have `Datastore.AllocateSpace` and `VirtualMachine.Interact.PowerOn` privileges.
4. Click **Verify** to test connectivity; resolve any certificate trust errors by importing the vCenter certificate under **Settings > Certificates**.
5. Once verified, the target appears as an available recovery destination when creating restore jobs.
6. Repeat for any additional recovery targets (e.g., DR-site vCenter `vcsa-dr.local`).
7. Validate by running a test restore of a non-critical VM to the new target.

---

## Validate Recovery Point

CyberSense scans vault copies for encryption signatures and file corruption. Always confirm a recovery point is clean before using it in a recovery.

1. In PPDM, navigate to **Cyber Recovery > CyberSense Reports**.
2. Select the protection policy and scroll to the most recent scan result.
3. Confirm the status is **Clean** — a **Suspect** or **Infected** status means that vault copy must not be used; select an earlier clean point.
4. Review the scan report detail: confirm the number of files scanned matches expectations and no high-entropy files are flagged.
5. Note the recovery point timestamp and its vault lock expiry date — the copy must not be expired before recovery is complete.
6. If no clean point exists within the RPO window, escalate to the Cyber Recovery team and invoke the incident escalation procedure.

```powershell
# Verify vault copy exists and its lock status via PPDM REST API
$base = "https://<ppdm-ip>:8443/api/v2"
$headers = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }
Invoke-RestMethod -Uri "$base/protection-copies?filter=policyName eq '<policy>'" `
  -Headers $headers | Select-Object -ExpandProperty content |
  Select-Object id, createTime, expirationTime, cyberSenseStatus
```

---

## Initiate Disaster Recovery Failover

Full DR failover moves production workloads from the primary site to the clean-room or DR site. This is a destructive production action — requires incident ticket and management authorisation.

1. Declare a DR event in the ITSM tool; open the DR runbook and confirm Integrity Lock two-person authorisation is in place to open the vault.
2. In PPDM, go to **Cyber Recovery > Vault** and click **Open Vault** — requires two authorised users to confirm.
3. Navigate to **Recovery > Virtual Machines** and select all VMs in scope for failover.
4. Choose the most recent clean CyberSense-verified recovery point for each VM.
5. Set target as clean-room vCenter with isolated network; do not connect to production network until validation is complete.
6. Click **Restore All**; monitor job progress in **Jobs > Active Jobs**.
7. Once VMs are online, run application health checks; then update DNS or load balancer records to redirect traffic to clean-room IPs.
8. Notify stakeholders and begin planning failback once production environment is confirmed clean.

---

## Monitor Recovery Progress

During any active recovery operation, use the PPDM Jobs dashboard and PowerShell to track progress and identify stalls.

1. In PPDM, open **Jobs > All Jobs** and filter by **Type = Restore** and **Status = Running**.
2. Click a job to see the step-by-step progress: copy data, register VM, power on.
3. Monitor throughput in the job detail — if throughput drops to near 0 MB/s for more than 5 minutes, check the vault network link and proxy resources.
4. On the PPDM server, check the agent log for errors:

```powershell
# Tail the PPDM agent log on the target proxy
Get-Content "C:\Program Files\Dell\PPDM\Logs\agent.log" -Tail 50 -Wait
```

5. Check clean-room ESXi host resource availability — ensure no datastore is above 85% capacity and no host is CPU/memory constrained.
6. If a job stalls for more than 30 minutes, cancel it, investigate the cause, and restart from step 1.
7. After completion, confirm the job status in PPDM shows **Completed** (not **Completed with Warnings**); investigate any warnings before closing the incident.

---

## Generate Recovery Report

Post-recovery and post-test reports are required for compliance and continuous improvement.

1. In PPDM, navigate to **Reports > Recovery Test Summary** (for test runs) or **Reports > Restore Activity** (for production recoveries).
2. Set the date range to cover the test or recovery window and click **Generate**.
3. Export the report as PDF or CSV using the **Export** button in the top-right corner.
4. Capture the following metrics: number of VMs recovered, recovery point used, total data restored (GB), elapsed recovery time, and any errors or warnings.
5. Compare elapsed recovery time against the defined RTO — document any gap and root-cause actions.
6. Attach the report to the change ticket or incident record in the ITSM tool.
7. Review findings in the next DR working group meeting; update the DR runbook with any procedure adjustments.

---

```powershell
# Step 1: Verify agent is running
Get-Service RASRAgent   # must be Running

# Step 2: Check available space on recovery share before capture
$share = "\\nas01\rasr-images\prod\$(hostname)"
if (-not (Test-Path $share)) { New-Item -ItemType Directory -Path $share }

# Step 3: Trigger capture via RASR Console (GUI)
#   Start → Dell OpenManage → Recovery and System Restore
#   → Backup → Create New Backup → select share path → Start

# OR trigger via command line (if supported by installed version)
& "C:\Program Files\Dell\RASR\RASRCmd.exe" /backup /target:$share /name:"$(hostname)_prod_$(Get-Date -Format yyyyMMdd)_001"

# Step 4: Monitor progress
Get-Content "C:\Program Files\Dell\RASR\Logs\RASRAgent.log" -Tail 20 -Wait

# Step 5: Verify image created
Get-ChildItem $share | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```text
┌────────────────────────────────────────── RASR — Procedures ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Routine Procedures              │  │                DR Procedures                │   │
│   │          Add new protection source           │  │              Initiate failover              │   │
│   │           Modify retention policy            │  │               Validate replica              │   │
│   │          Expire old recover points           │  │              Redirect host I/O              │   │
│   │             Add storage capacity             │  │         Test failover (non-disrupt)         │   │
│   │           Service account rotation           │  │            Failback to production           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Change Control Requirements for RASR                             │   │
│   │           All changes to protection policies require change ticket with rollback plan         │   │
│   │                      Failover tests must be scheduled in maintenance window                   │   │
│   │              Firmware/software upgrades need 48 h pre-approval and backup snapshot            │   │
│   │                  Post-change: verify jobs run successfully for 2 backup cycles                │   │
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
RASR Console → Media → Create New Media
  → Select output: ISO file
  → Output path: \\nas01\rasr-images\media\rasr-media-15G-$(Get-Date -Format yyyyMM).iso
  → Build

After creation:
  1. Map new ISO in iDRAC and verify it boots to WinPE.
  2. Confirm network driver loads and share is reachable.
  3. Replace old ISO reference in documentation and iDRAC pre-mapped media.
```
```powershell
$share     = "\\nas01\rasr-images\prod"
$keepDaily = 7    # days
$keepWeekly = 4   # weeks

Get-ChildItem $share -Recurse -Filter "*.wim" |
  Where-Object { $_.Name -notmatch "_weekly|_post-patch" -and $_.LastWriteTime -lt (Get-Date).AddDays(-$keepDaily) } |
  ForEach-Object {
    Write-Host "Removing: $($_.FullName) [$(($_.Length / 1GB).ToString('F1')) GB]"
    # Remove-Item $_.FullName   # uncomment after dry-run review
  }

# Review output before uncommenting Remove-Item
```
