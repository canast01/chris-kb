---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# PowerScale — Escalation

<div class="kb-summary">
How to escalate Dell PowerScale (Isilon) issues to Dell Technologies support: what data to collect, how to run isi_gather_info, step-by-step case creation on dell.com/support, and the escalation path when progress stalls.

*Applies to: PowerScale (Isilon) OneFS 9.x*
</div>
![PowerScale — Escalation](../../../../../assets/storage-dell-powerscale-troubleshooting-escalation.svg)




---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
preescalation_selfcheck: "Pre-Escalation Self-Check" {shape: rectangle}
stepbystep_data_collection: "Step-by-Step Data Collection" {shape: rectangle}
how_to_open_the_case_on_dellcomsuppo: "How to Open the Case on dell.com/support" {shape: rectangle}
escalation_path: "Escalation Path" {shape: rectangle}
what_not_to_do: "What NOT to Do" {shape: rectangle}
useful_commands_for_case_updates: "Useful Commands for Case Updates" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> preescalation_selfcheck: investigate
symptom -> stepbystep_data_collection: investigate
symptom -> how_to_open_the_case_on_dellcomsuppo: investigate
symptom -> escalation_path: investigate
symptom -> what_not_to_do: investigate
symptom -> useful_commands_for_case_updates: investigate
preescalation_selfcheck -> resolution
stepbystep_data_collection -> resolution
how_to_open_the_case_on_dellcomsuppo -> resolution
escalation_path -> resolution
what_not_to_do -> resolution
useful_commands_for_case_updates -> resolution
```

## Before you begin

- **Access required:** SSH access to any PowerScale node (admin user or root); OneFS web admin UI access; Dell support account at dell.com/support linked to the cluster service tag
- **SupportAssist auto-cases:** PowerScale can automatically open Dell support cases for hardware faults if SupportAssist is configured. Check `isi phone_home settings view` to confirm call-home is active — if it is, a case may already exist before you call
- **Do NOT remove a SMARTFAILed node** without Dell direction — SMARTFAIL is a controlled removal process; removing the node before SMARTFAIL completes can leave data components without sufficient protection
- **Do NOT start a OneFS upgrade** during an active incident — upgrades in a degraded cluster state can fail mid-way and make the cluster config inconsistent

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command | Expected result |
|---|---|---|
| OneFS version | `isi version` | Note full version + build |
| Cluster node health | `isi status` | All nodes Online (`--`) |
| Storage pool health | `isi storagepool list` | All pools show healthy; no unprotected data |
| Active alerts | `isi alerts list --limit 50` | No CRITICAL or ERROR alerts |
| Drive health | `isi statistics drive` | No drives in DEAD or SMARTFAIL state |
| SyncIQ status | `isi sync policies list` | No policies in "needs attention" |
| Active jobs | `isi job list` | No stuck jobs (check job pause/error state) |
| SupportAssist | `isi phone_home settings view` | Enabled; last call-home successful |
| NFS/SMB access | Mount a share and write a test file | Write succeeds; read returns same data |

---

## Step-by-Step Data Collection

### 1. Get the OneFS version and cluster serial number

```bash
# SSH to any PowerScale node as admin
ssh admin@<node-ip>

# OneFS version (include in every case)
isi version

# Cluster name and serial numbers (required for case registration)
isi cluster identity view
isi license list   # shows cluster serial

# Node list with serial numbers
isi status -n
```


```text title="Expected output"
admin@192.168.1.50's password: 
Last login: Wed Jan 15 14:22:33 2025 from 10.0.0.45

OneFS Version: OneFS 9.4.0.0 (Build 9.4.0.0-123456)

Cluster Name: prod-isilon-01
Cluster Serial: K123456789ABC

Name                    Serial              Status
node1                   K123456789ABC       Up
node2                   K123456789ABD       Up
node3                   K123456789ABE       Up
node4                   K123456789ABF       Up
node5                   K123456789ABG       Up

License Status: Valid
Expiration Date: 2026-03-15
```

!!! warning "Common errors"
    **`ssh: connect to host <node-ip> port 22: Connection timed out`** — Verify the node IP is correct, the node is powered on, and network connectivity exists from your admin workstation to the management network.
    **`Permission denied (publickey,password).`** — Confirm you are using the correct admin credentials and that SSH password authentication is enabled on the cluster (check SSH settings in WebUI under Cluster Management > Security).
    **`isi: command not found`** — Ensure you are logged in as the admin user on a PowerScale node; this command is not available on non-OneFS systems or non-admin accounts.
### 2. Run isi_gather_info (full cluster diagnostic bundle)

```bash
# SSH to any node — isi_gather_info collects from all nodes automatically
isi_gather_info

# Bundle is written to /ifs/data/Isilon_Support/
ls -lh /ifs/data/Isilon_Support/

# Copy to a local workstation for upload to Dell case
scp admin@<node-ip>:/ifs/data/Isilon_Support/<bundle-filename>.tar.gz /tmp/
```


```text title="Expected output"
Gathering system information from all nodes...
Node 1: Collecting hardware inventory
Node 2: Collecting hardware inventory
Node 3: Collecting hardware inventory
Collecting cluster configuration
Collecting event logs
Collecting performance metrics
Bundle creation complete: /ifs/data/Isilon_Support/isilon_support_info_10.1.2024_14-32-18.tar.gz

total 2.3G
-rw-r--r-- 1 root root 2.3G Oct  1 14:32 isilon_support_info_10.1.2024_14-32-18.tar.gz
-rw-r--r-- 1 root root 1.8G Sep 28 09:15 isilon_support_info_09.28.2024_09-18-42.tar.gz

admin@192.168.1.50's password: 
isilon_support_info_10.1.2024_14-32-18.tar.gz          100% 2.3GB   45.2MB/s   00:51
```

!!! warning "Common errors"
    **`ssh: connect to host <node-ip> port 22: Connection timed out`** — Replace `<node-ip>` with the actual cluster node IP address and verify network connectivity to that node.
    **`scp: /ifs/data/Isilon_Support/<bundle-filename>.tar.gz: No such file or directory`** — Run `isi_gather_info` first to generate the bundle, or check the actual bundle filename with `ls /ifs/data/Isilon_Support/`.
This bundle contains: OneFS logs, cluster config, hardware inventory, performance stats, alert history, and job state from every node.

### 3. Capture current cluster status

```bash
# Node and drive states
isi status

# Storage pools and capacity
isi storagepool list

# Drive statistics (I/O errors, SMARTFAIL drives)
isi statistics drive | head -100

# Active alerts
isi alerts list --limit 100

# Active OneFS background jobs
isi job list

# SyncIQ policy status
isi sync policies list
isi sync reports list
```


```text title="Expected output"
Cluster Name: isilon-prod-01
Cluster Health: BALANCED
Nodes: 8 (all online)
Total Capacity: 450.2 TB
Used Capacity: 287.5 TB
Available Capacity: 162.7 TB

Name                    Tier    Nodes   Capacity        Usage           Health
System                  SSD     8       89.3 TB         45.2 TB         BALANCED
Capacity-1              HDD     8       360.9 TB        242.3 TB        BALANCED

Drive Statistics:
Node    Slot    Model           Status  Read_Errors  Write_Errors  SMARTFAIL
1       0       ST8000NM0055    OK      0            0              No
1       1       ST8000NM0055    OK      2            0              No
2       3       ST8000NM0055    SMARTFAIL 847       156            Yes
3       5       ST8000NM0055    OK      0            0              No
4       7       ST8000NM0055    OK      1            0              No

ID      Severity  Message                                    Time
1847    CRITICAL  Drive 2:3 SMARTFAIL detected              2024-01-15 14:32:18
1846    WARNING   Node 4 CPU utilization 89%                2024-01-15 14:28:45
1845    WARNING   Replication lag on cluster-dr: 2.3 hours  2024-01-15 13:15:22

ID      Job_Type              Status      Progress  Start_Time
4521    Rebalance             RUNNING     67%       2024-01-15 10:22:00
4520    Snapshot_Delete       COMPLETED   100%      2024-01-15 09:15:00
4519    Collect_Diagnostics   QUEUED      0%        2024-01-15 14:45:00

Policy_Name              Status    Target_Cluster    Last_Sync
prod-to-dr              ENABLED   cluster-dr        2024-01-15 14:30:22
archive-weekly          ENABLED   archive-vault     2024-01-15 08:00:00

Report_ID  Policy_Name      Status      Duration  Bytes_Transferred
2847       prod-to-dr       COMPLETED   1h 23m    156.7 GB
2846       archive-weekly   COMPLETED   4h 12m    892.3 GB
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure the OneFS CLI tools are installed and the PATH includes `/usr/local/bin` or run commands directly as `/usr/local/bin/isi`.
    **`Error: Invalid credentials or insufficient permissions`** — Verify your user account has cluster admin privileges and authentication is configured (check `isi auth status`).
    **`Connection refused on port 8080`** — Confirm the OneFS management service is running with `systemctl status isilon-mgmt` and the cluster is not in maintenance mode.
### 4. Collect SupportAssist phone-home status

```bash
# SupportAssist configuration
isi phone_home settings view

# Send a test notification to confirm connectivity
isi phone_home send --type test

# Check last auto-case if SupportAssist triggered one
isi events list | grep -i "support\|case\|esrs" | tail -20
```


```text title="Expected output"
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled: true
Enabled:ist_phone_home send --type test
Test notification sent successfully to ESRS gateway (203.0.113.45)
Delivery confirmed at 2024-01-15T14:32:18Z

2024-01-15T14:28:42Z INFO: SupportAssist case auto-created: CASE-2847561 (Disk utilization warning)
2024-01-15T13:15:09Z INFO: ESRS phone-home transmission successful (seq: 4521)
2024-01-15T12:47:33Z WARNING: SupportAssist threshold breach detected on node-3
2024-01-15T11:22:15Z INFO: Case CASE-2847501 closed by Dell support
2024-01-15T10:05:44Z INFO: ESRS connectivity restored after maintenance window
2024-01-15T09:18:27Z INFO: SupportAssist auto-case suppressed (duplicate condition)
2024-01-15T08:33:51Z INFO: Phone-home transmission queued (offline mode)
2024-01-15T07:12:19Z WARNING: ESRS gateway unreachable, retrying in 300s
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure you are logged into the PowerScale cluster CLI or SSH session with appropriate admin credentials.
    **`Error: ESRS gateway unreachable`** — Verify network connectivity to the ESRS gateway and check firewall rules allow outbound HTTPS (port 443) to Dell support servers.
    **`Permission denied`** — Run the command with root or admin-level privileges using `sudo` or ensure your user account has SupportAssist configuration rights.
### 5. Write the timeline

```text
OneFS version: 9.5.0.0 build XXXXXXXX
Cluster: prod-ps-01 (cluster serial: XXXXXXXX)
Nodes: 12 nodes (4x F200, 4x H600, 4x A300 archive tier)
Protection level: N+2:1 on all pools
Issue first observed: 2026-06-14 14:00 UTC
Last known healthy state: 2026-06-14 12:00 UTC
Changes in 24h before the issue:
  - 12:00: Node 7 showed drive fault alert (Drive Bay 3: SSD DEAD)
  - 14:00: Node 7 entered SMARTFAIL state automatically
  - 14:05: isi status shows Node 7 in "SMARTFAILING" state; other nodes Online
  - 14:10: isi storagepool list shows "H600 pool: DEGRADED - 1 device in SMARTFAIL"
SupportAssist: case auto-created (Dell case number XXXXXXXX)
Steps already taken:
  - Did NOT remove Node 7 or pull the failed drive
  - Did NOT initiate manual SMARTFAIL on additional nodes
  - SyncIQ: replication from prod-ps-01 to dr-ps-01 still running
Blast radius: H600 pool degraded; data protected at N+1 only; one more drive failure = data at risk
```

---

## How to Open the Case on dell.com/support

1. Go to **dell.com/support** and sign in with your Dell account.

2. Click **My Cases** → **Create New Case**.

3. Under **Product**, select your PowerScale cluster by service tag (cluster serial number from `isi license list`).

4. Under **Severity**, select:
   - **Severity 1 — Production Down**: NFS/SMB access is completely unavailable; a node is offline with unprotected data; SMARTFAIL cannot complete; data loss is imminent; no workaround
   - **Severity 2 — Degraded Performance**: A node or drive is in SMARTFAIL and data is at N+1 protection; SyncIQ replication is failing; performance is significantly degraded; workaround is incomplete
   - **Severity 3 — Non-Critical Issue**: A storage pool is in a degraded but protected state; a background job is stuck; a specific protocol is partially failing; workaround exists
   - **Severity 4 — General Question**: How-to question, pre-upgrade review, capacity planning

5. In the **Summary** field: symptom + scope. Example: `PowerScale prod-ps-01 — Node 7 in SMARTFAIL, H600 pool degraded to N+1, drive failure risk imminent`.

6. In the **Description** field, paste:
   - OneFS version and cluster serial from Step 1
   - `isi status` and `isi storagepool list` output from Step 3
   - The alert details from Step 3
   - The timeline from Step 5
   - Note any Dell SupportAssist auto-case number if one was already created

7. Under **Attachments**, upload the `isi_gather_info` bundle from Step 2.

8. Click **Submit**. You receive a case number immediately.

9. **Severity 1 only:** call Dell support after submission:
    - North America: +1 800 945 3355 (24×7 for production-down)
    - Reference the case number and state "Severity 1 — PowerScale node SMARTFAIL, data at risk" at the start of the call.

---

## Escalation Path

![PowerScale — Escalation — Diagram](../../../../../assets/storage-dell-powerscale-troubleshooting-escalation-diagram.svg)

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Remove a SMARTFAILed node before SMARTFAIL completes | SMARTFAIL is a data migration process; removing the node early leaves data components without sufficient protection copies | Let SMARTFAIL complete fully (`isi status` shows node removed); only then power off and remove the node |
| Pull a drive from a node showing as DEAD without Dell guidance | A DEAD drive may still hold the only copy of a component if SMARTFAIL has not yet migrated it | Confirm with Dell that the drive's data has been migrated to other drives before any physical removal |
| Reformat or rebuild a node without Dell direction | Rebuilding destroys all node data; in a degraded cluster this can push the cluster below its protection threshold | Only reformat/rebuild with explicit Dell instructions and after confirming all data is protected on other nodes |
| Disable SupportAssist during an active incident | SupportAssist provides Dell with real-time cluster telemetry that accelerates diagnosis | Keep SupportAssist enabled; if connectivity is an issue, arrange an alternate network path for call-home |
| Start a OneFS upgrade during an active degraded state | Upgrades in a degraded cluster can fail mid-way, leaving the cluster in an inconsistent version state | Wait for the cluster to return to a fully healthy state before initiating any upgrade |
| Run `isi job delete` on active protection or SMARTFAIL jobs | Cancelling a SMARTFAIL or FlexProtect job stops the data migration and leaves the cluster in a partially protected state | Let Dell direct any job cancellation; only stop jobs that Dell explicitly identifies as stuck |

---

## Useful Commands for Case Updates

```bash
# SSH to any PowerScale node as admin — paste these into every case update

# OneFS version
isi version

# Node health overview
isi status

# Storage pool health (protection status)
isi storagepool list

# Drive states (DEAD/SMARTFAIL drives)
isi statistics drive | grep -E "DEAD|SMARTFAIL|ERROR"

# Active alerts
isi alerts list --limit 50

# Active background jobs
isi job list

# SyncIQ replication status
isi sync policies list
```


```text title="Expected output"
OneFS Version: OneFS 9.4.0.0 (Build 9.4.0.0_1234567)

Cluster Health: HEALTHY
Nodes: 6 online, 0 offline
CPU Load: 12.3% average
Memory: 87.2% utilized

Name                    Status      Protection  Usable Capacity
Tier_1_SSD              BALANCED    +2d:1n      45.2 TB
Tier_2_NL_SAS           BALANCED    +2d:1n      892.5 TB
Tier_3_Archive          BALANCED    +3d:1n      1.2 PB

(no DEAD or SMARTFAIL drives detected)

ID    Severity  Message                                    Raised
1847  CRITICAL  Node 4: Disk /dev/sdq SMARTFAIL detected  2024-01-15 09:23:14
1843  WARNING   Replication lag: Policy 'DR_Backup' 4.2GB  2024-01-15 08:47:02
1839  INFO      Cluster capacity at 78% utilization       2024-01-15 06:15:33

Job ID  Type              State      Progress  Elapsed
4521    Rebalance         RUNNING    34%       2h 14m
4519    Snapshot Cleanup  COMPLETED  100%      47m
4518    Disk Verify       RUNNING    67%       5h 22m

Policy Name         Source Path  Target Cluster  Last Sync       Status
DR_Backup           /ifs/data    dr-cluster-01   2024-01-15 10:02  SYNCED
Archive_Weekly      /ifs/archive archive-01      2024-01-14 23:30  SYNCED
```

!!! warning "Common errors"
    **`isi: command not found`** — Verify SSH session is connected to a PowerScale node (not a generic Linux server) and the admin user has OneFS CLI access.
    **`Permission denied`** — Ensure you are logged in as the admin user or a role with cluster monitoring privileges; use `isi auth list` to verify your current permissions.
    **`Connection refused on port 22`** — Confirm the PowerScale node IP is reachable and SSH is enabled; check firewall rules and verify the node is not in maintenance mode with `isi_nodes -l`.
---

## Support SLA Reference

| Tier | Severity | Definition | Initial Response SLA |
|---|---|---|---|
| ProSupport Plus | P1 — Production Down | NFS/SMB unavailable; node offline; data at risk | < 2 hours (24×7) |
| ProSupport Plus | P2 — Degraded | Node/drive in SMARTFAIL; N+1 protection only; workaround partial | < 4 hours (24×7) |
| ProSupport Plus | P3 — Non-Critical | Specific protocol issue; background job stuck; workaround exists | Next business day |
| ProSupport Plus | P4 — General | How-to, planning, capacity review | Next business day |
| ProSupport | P1 | As above | < 4 hours (24×7) |
| ProSupport | P2–P4 | As above | Next business day |

---

## See also

- [PowerScale — Diagnostics](../diagnostics/)
- [PowerScale — Common Issues](../common-issues/)

---

## Verify resolution

- Run `isi status` and confirm all nodes are Online (no SMARTFAIL or Degraded state)
- Run `isi storagepool list` and confirm all pools show their full protection level (N+2:1 or configured policy)
- Run `isi statistics drive` and confirm no drives in DEAD or SMARTFAIL state
- Run `isi alerts list --limit 20` and confirm no active CRITICAL or ERROR alerts
- Confirm NFS/SMB client access is restored: mount a share and write/read a test file
- Check `isi sync reports list` to confirm SyncIQ replication has resumed and the last run succeeded
- Run `isi_gather_info` again and attach to the Dell case as the post-resolution bundle
