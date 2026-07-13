---
tags:
  - netapp
  - troubleshooting
search:
  boost: 1.5
description: "Superna Eyeglass diagnostic commands: check service health with igls adm status, trace SyncIQ and DFS sync errors, read Eyeglass log files, and verify DR..."
---
# Superna Eyeglass — Diagnostics

<div class="kb-summary">
Superna Eyeglass diagnostic commands: check service health with igls adm status, trace SyncIQ and DFS sync errors, read Eyeglass log files, and verify DR readiness score before opening a support case.

*Applies to: Superna Eyeglass 2.x*
</div>
![Superna Eyeglass — Diagnostics](../../../../../assets/storage-netapp-superna-eyeglass-troubleshooting-diagnostics.svg)

```d2
direction: right

A: "Eyeglass Alert" {shape: rectangle}
B: "igls adm status\nAll services running?" {shape: rectangle}
C: "C" {shape: rectangle}
D: "Check appliance resources\ndf -h; free -m" {shape: rectangle}
E: "igls dr readiness\nCheck score" {shape: rectangle}
F: "F" {shape: rectangle}
G: "igls synciq status\nFind failing policy" {shape: rectangle}
H: "igls config replication status\nCheck share/quota sync" {shape: rectangle}
I: "I" {shape: rectangle}
J: "isi sync jobs list\non PowerScale cluster" {shape: rectangle}
K: "Check OneFS API\ncurl https://cluster:8080/" {shape: rectangle}
L: "Read sync.log\n/var/log/eyeglass/" {shape: rectangle}
M: "Collect support bundle\nAdmin UI → Support Bundle" {shape: rectangle}

A -> B
C -> D
C -> E
F -> G
F -> H
I -> J
I -> K
H -> L
D -> L
J -> L
K -> L
L -> M
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_eyeglass_service_health: "Step 1 — Check Eyeglass service health" {shape: rectangle}
step_2_check_dr_readiness_score: "Step 2 — Check DR readiness score" {shape: rectangle}
step_3_check_synciq_on_the_powerscal: "Step 3 — Check SyncIQ on the PowerScale cluster" {shape: rectangle}
step_4_check_onefs_api_connectivity_: "Step 4 — Check OneFS API connectivity (Eyeglass to\ncluster)" {shape: rectangle}
step_5_read_eyeglass_log_files: "Step 5 — Read Eyeglass log files" {shape: rectangle}
log_locations: "Log locations" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_eyeglass_service_health: investigate
symptom -> step_2_check_dr_readiness_score: investigate
symptom -> step_3_check_synciq_on_the_powerscal: investigate
symptom -> step_4_check_onefs_api_connectivity_: investigate
symptom -> step_5_read_eyeglass_log_files: investigate
symptom -> log_locations: investigate
step_1_check_eyeglass_service_health -> resolution
step_2_check_dr_readiness_score -> resolution
step_3_check_synciq_on_the_powerscal -> resolution
step_4_check_onefs_api_connectivity_ -> resolution
step_5_read_eyeglass_log_files -> resolution
log_locations -> resolution
```

## Before you begin

- **Access:** SSH to the Eyeglass appliance as `admin`; Eyeglass Admin UI (`https://<eyeglass-ip>`); PowerScale admin credentials on both clusters
- **Gather first:** current DR readiness score from the Eyeglass dashboard, which SyncIQ policies are failing, and the exact error from the Eyeglass UI or igls output
- **Scope:** confirm whether the issue affects a single SyncIQ policy, all policies, DFS namespace sync, or the Eyeglass appliance itself
- **RAPA caution:** if RAPA has quarantined a directory, do not un-quarantine without confirming the threat is resolved with the security team
- **Do not fail over while DR score is degraded** without running the Eyeglass DR Assistant runbook — it checks pre-conditions before each step

---

## Step 1 — Check Eyeglass service health

```bash
# SSH to the Eyeglass appliance
ssh admin@<eyeglass-hostname>

# Check all Eyeglass services are running
igls adm status
# Expected output (healthy):
#   Eyeglass Services:     Running
#   SyncIQ Monitor:        Running
#   DFS Sync Service:      Running
#   RAPA Service:          Running
#   Database:              Running
# Any service showing "Stopped" — restart with: igls adm restart <service-name>

# Check Eyeglass version
igls version

# Check license validity
igls license status
# Expected: Status: Licensed, with expiry date > today
```


```text title="Expected output"
admin@eyeglass-prod-01:~$ igls adm status
Eyeglass Services:     Running
SyncIQ Monitor:        Running
DFS Sync Service:      Running
RAPA Service:          Running
Database:              Running
admin@eyeglass-prod-01:~$ igls version
Eyeglass Version: 5.4.2.1
Build: 20240115-084532
admin@eyeglass-prod-01:~$ igls license status
Status: Licensed
License Key: EG-5K4X9-M2L7P-9QR3T
Expiry Date: 2025-06-30
Days Remaining: 187
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Connection refused` | Verify the Eyeglass hostname/IP is correct and the appliance is reachable with `ping <eyeglass-hostname>`. |
    | `RAPA Service:         Stopped` | Restart the service with `igls adm restart rapa` and verify with `igls adm status`. |
    | `Status: Expired` | Contact NetApp support or your reseller to renew the license key using `igls license update <new-key>`. |
**If a service is stopped:**
1. Check appliance disk space: `df -h /opt/superna/` — full disk can crash services
2. Check memory: `free -m` — if swap is high, the appliance may need a reboot
3. Restart the specific service: `igls adm restart synciq-monitor` (for SyncIQ monitor)

---

## Step 2 — Check DR readiness score

```bash
# Overall DR readiness score
igls dr readiness
# Expected: Ready (100%)
# If < 80%: one or more categories below are degraded

# SyncIQ policy replication status (Eyeglass view)
igls synciq status
# Each policy shows: Name, Status, Last Run, Policy Progress
# Problem statuses: "Error: Job Failed", "Stopped", "Paused"

# Configuration replication (shares, exports, quotas)
igls config replication status
# Shows: each policy, last sync time, status
# Problem: "Out of Sync", "Error"

# DFS namespace sync status
igls dfs status
# Shows: each DFS namespace, current target, sync state

# RAPA protection status
igls rapa status
# Shows: monitored paths, quarantine events (if any)
```


```text title="Expected output"
# Overall DR readiness score
igls dr readiness
DR Readiness Score: 95%
Status: Ready
  SyncIQ Replication: Healthy (98%)
  Configuration Sync: Healthy (100%)
  DFS Namespaces: Healthy (92%)
  RAPA Protection: Healthy (94%)
Last Updated: 2024-01-15 14:32:18 UTC

# SyncIQ policy replication status
igls synciq status
Policy Name              Status          Last Run              Progress
dr-policy-prod-01        Running         2024-01-15 14:28:00   87%
dr-policy-prod-02        Completed       2024-01-15 13:15:22   100%
dr-policy-archive        Completed       2024-01-15 12:00:45   100%
dr-policy-test           Error: Job Failed 2024-01-15 11:30:12   0%

# Configuration replication status
igls config replication status
Policy                   Last Sync              Status
config-sync-primary      2024-01-15 14:31:05    In Sync
config-sync-secondary    2024-01-15 14:30:52    In Sync
quota-sync-hourly        2024-01-15 14:00:00    In Sync

# DFS namespace sync status
igls dfs status
DFS Namespace            Current Target         Sync State
\\corp.local\data        isilon-dr-02.local     Synchronized
\\corp.local\archive     isilon-dr-02.local     Synchronized

# RAPA protection status
igls rapa status
Monitored Path                    Status              Quarantine Events
/ifs/data/sensitive               Protected           0
/ifs/compliance/legal             Protected           2
/ifs/backups/incremental          Protected           0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Job Failed` | Check the SyncIQ job logs with `igls synciq logs dr-policy-test` to identify network, authentication, or capacity issues on the target cluster. |
    | `Out of Sync` | Verify network connectivity between clusters and ensure the Eyeglass service is running on both source and target with `igls service status`. |
    | `Connection refused on port 8443` | Confirm the Eyeglass management interface is accessible and the target cluster IP/hostname is correctly configured in `igls config show`. |
---

## Step 3 — Check SyncIQ on the PowerScale cluster

When Eyeglass shows a SyncIQ policy failing, verify directly on the PowerScale cluster:

```bash
# SSH to the production PowerScale cluster
ssh admin@<production-cluster>

# List all SyncIQ policies
isi sync policies list
# Shows: Name, Enabled, Action, Target Host, Schedule, Last Result

# List currently running or recently completed jobs
isi sync jobs list
# Look for: State = "failed" or "error"; note the policy name and error detail

# Check reports for a specific failing policy
isi sync reports list --policy-name <policy-name> --limit 5
# Shows: start time, end time, result, files transferred, error message

# Check SyncIQ policy configuration
isi sync policies view <policy-name>
# Verify: target host, target path, source path, schedule

# On the DR cluster: check target status
ssh admin@<dr-cluster>
isi sync targets list
# Shows target policies and their last sync time
```


```text title="Expected output"
admin@prod-cluster1:~# isi sync policies list
Name                     Enabled  Action  Target Host        Schedule         Last Result
backup-daily-nightly     Yes      sync    dr-cluster.local   Every day at 2am  Success
backup-hourly-critical   Yes      sync    dr-cluster.local   Every hour       Failed
archive-weekly-cold      No       sync    archive.local      Every Sunday     Success
repl-finance-data        Yes      sync    dr-cluster.local   Every 6 hours    Success

admin@prod-cluster1:~# isi sync jobs list
ID       Policy Name              State    Start Time           Progress
12847    backup-hourly-critical   failed   2024-01-15 14:32:10  100%
12846    backup-daily-nightly     running  2024-01-15 14:28:45  67%
12845    repl-finance-data        success  2024-01-15 14:15:22  100%

admin@prod-cluster1:~# isi sync reports list --policy-name backup-hourly-critical --limit 5
Start Time           End Time             Result   Files Xferred  Error
2024-01-15 14:32:10  2024-01-15 14:35:22  failed   45821          Connection timeout to target host
2024-01-15 14:26:10  2024-01-15 14:29:15  failed   0              Target path does not exist: /ifs/backup/hourly
2024-01-15 14:20:10  2024-01-15 14:23:08  success  89234          -
2024-01-15 14:14:10  2024-01-15 14:17:45  success  87912          -
2024-01-15 14:08:10  2024-01-15 14:11:32  success  88456          -

admin@prod-cluster1:~# isi sync policies view backup-hourly-critical
Name:                    backup-hourly-critical
Enabled:                 Yes
Action:                  sync
Target Host:             dr-cluster.local
Target Path:             /ifs/backup/hourly
Source Path:             /ifs/data/critical
Schedule:                Every hour
Last Run:                2024-01-15 14:32:10
Last Result:             Failed
Throttle Enabled:        Yes
Throttle Rate (MB/s):    500

admin@prod-cluster1:~# ssh admin@dr-cluster
admin@dr-cluster:~# isi sync targets list
Target Host        Policy Name              Last Sync Time       Status
dr-cluster.local   backup-daily-nightly     2024-01-15 14:28:45  Active
dr-cluster.local   backup-hourly-critical   2024-01-15 14:20:10  Inactive
dr-cluster.local   repl-finance-data        2024-01-15 14:15:22  Active
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Connection timeout to target host` | Verify network connectivity between clusters with `ping <dr-cluster>` and confirm firewall rules allow port 8080 for SyncIQ. |
    | `Target path does not exist: /ifs/backup/hourly` | Create the target directory on the DR cluster with `isi |
**Common SyncIQ failure patterns:**
- `"Source path not found"` → files moved since the policy was created; update source path in Eyeglass → Configuration Replication
- `"Target host unreachable"` → network issue between clusters; check ICMP and TCP 445 between cluster SmartConnect zones
- `"Authentication failure"` → credentials used by SyncIQ to reach DR cluster have expired; re-enter in the SyncIQ policy

---

## Step 4 — Check OneFS API connectivity (Eyeglass to cluster)

Eyeglass communicates with PowerScale clusters via the OneFS REST API (HTTPS port 8080).

```bash
# From the Eyeglass appliance — test API reachability
curl -sk https://<production-cluster-smartconnect>:8080/
# Expected: HTTP 200 or redirect to API root (not connection refused)

curl -sk https://<dr-cluster-smartconnect>:8080/
# Same check for DR cluster

# Test with credentials (basic auth)
curl -sk -u admin:<password> "https://<cluster>:8080/platform/1/cluster/config"
# Expected: JSON with cluster name, nodes list, OneFS version

# Verify DNS resolution of SmartConnect zone from the appliance
nslookup <cluster-smartconnect-zone>
# Should resolve to one of the node IP addresses
```


```text title="Expected output"
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   284  100   284    0     0   1847      0 --:--:-- --:--:-- --:--:--  0:00:00
<!DOCTYPE html><html><head><title>OneFS API</title></head><body><h1>OneFS API Gateway</h1></body></html>

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   284  100   284    0     0   1923      0 --:--:-- --:--:-- --:--:-- 0:00:00
<!DOCTYPE html><html><head><title>OneFS API</title></head><body><h1>OneFS API Gateway</h1></body></html>

{"cluster": {"name": "prod-cluster-01", "nodes": [1, 2, 3, 4], "onefs_version": {"release": "9.4.0.0", "build": "B_9_4_0_0_047(RELEASE)"}}, "status": "ok"}

Server:		10.20.1.10
Address:	10.20.1.10#53

Name:	prod-cluster-sc.example.com
Address:	192.168.10.45
Address:	192.168.10.46
Address:	192.168.10.47
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to 192.168.10.45 port 8080: Connection refused` | Verify the OneFS cluster API service is running with `isi status -s` on the cluster, and confirm port 8080 is not blocked by firewall rules between Eyeglass and the cluster. |
    | `curl: (60) SSL certificate problem: self signed certificate` | The `-k` flag should suppress this, but if it persists, ensure you are using the exact SmartConnect FQDN and that SSL certificate validation is disabled with `-k` in the curl command. |
    | `nslookup: can't resolve '<cluster-smartconnect-zone>': No address associated with hostname` | Verify the SmartConnect zone name is correct and that DNS is properly configured on the Eyeglass appliance (check `/etc/resolv.conf` and test with `dig` or `host` as alternatives). |
---

## Step 5 — Read Eyeglass log files

```bash
# SSH to the Eyeglass appliance
ssh admin@<eyeglass-hostname>

# Main sync service log — shows share/export/quota replication activity
tail -100 /var/log/eyeglass/sync.log | grep -i "error\|fail\|warn"

# Failover event log — shows pre-checks, failover steps, and results
tail -100 /var/log/eyeglass/failover.log | grep -i "error\|fail\|step"

# DNS integration log (DFS failover changes DNS delegation)
tail -100 /var/log/eyeglass/dns.log | grep -i "error\|fail"

# RAPA event log
tail -100 /var/log/eyeglass/rapa.log | grep -i "quarantine\|detect\|alert"

# Main Eyeglass application log
grep -i "error\|exception" /opt/superna/log/eyeglass.log | tail -100

# Collect all logs in one snapshot for SR attachment
{
  echo "=== igls dr readiness ==="
  igls dr readiness
  echo "=== igls synciq status ==="
  igls synciq status
  echo "=== igls config replication status ==="
  igls config replication status
  echo "=== igls dfs status ==="
  igls dfs status
  echo "=== igls rapa status ==="
  igls rapa status
  echo "=== igls version ==="
  igls version
} > /tmp/eyeglass-diag-$(date +%F-%H%M).txt
```


```text title="Expected output"
admin@eyeglass-prod01's password: 
2024-01-15 14:32:18 WARN [SyncManager] Quota sync delayed for \\netapp-cluster1\vol_finance (retry 2/5)
2024-01-15 14:31:45 ERROR [ReplicationEngine] Failed to replicate share config for share_hr_backup: Connection timeout to secondary cluster
2024-01-15 14:30:22 WARN [SnapshotMgr] Snapshot creation took 45s (threshold: 30s) on vol_marketing

2024-01-15 13:58:10 INFO [FailoverMgr] STEP 1: Pre-check validation started
2024-01-15 13:58:15 INFO [FailoverMgr] STEP 2: DNS delegation update in progress
2024-01-15 13:58:22 ERROR [FailoverMgr] STEP 3: Failed to update DFS namespace root - Access denied to AD domain controller

2024-01-15 12:45:33 WARN [DNSIntegration] DNS update queued for eyeglass.corp.local (10.45.120.15)
2024-01-15 12:44:18 ERROR [DNSIntegration] Failed to reach DNS server 10.20.5.10 - Connection refused

2024-01-15 11:22:05 INFO [RAPA] Quarantine triggered for vol_prod_data: 847 suspicious file modifications detected
2024-01-15 11:21:40 ALERT [RAPA] Ransomware-like activity detected on share_backup_01: 12 executables written to protected directory

2024-01-15 10:15:42 ERROR [EyeglassApp] Exception in thread "SyncWorker-3": java.net.SocketTimeoutException: Connection timeout
2024-01-15 10:14:18 WARN [EyeglassApp] Low memory condition detected (78% heap usage)

=== igls dr readiness ===
DR Readiness Status: READY
  Primary Cluster: netapp-cluster1.corp.local (192.168.1.50)
  Secondary Cluster: netapp-cluster2.corp.local (192.168.1.51)
  Replication Lag: 2.3 seconds
  Last Sync: 2024-01-15 14:35:22 UTC

=== igls synciq status ===
SyncIQ Policy Status:
  policy_hourly_shares: RUNNING (847 MB/s, ETA 3m 22s)
  policy_daily_quotas: IDLE (Last run: 2024-01-15 02:15:00, Duration: 18m 45s)
  policy_config_sync: IDLE (Last run: 2024-01-15 14:30:00, Duration: 2m 15s)

=== igls config replication status ===
Configuration Replication: HEALTHY
  Shares: 127 replicated, 0 failed
  Exports: 89 replicated, 0 failed
  Quotas: 342 replicated, 2 pending

=== igls dfs status ===
DFS Namespace Status:
```
---

## Log locations

| Component | Path | What to look for |
|---|---|---|
| Sync service | `/var/log/eyeglass/sync.log` | Share/export/quota sync errors |
| Failover events | `/var/log/eyeglass/failover.log` | Pre-check failures, step errors |
| DNS changes | `/var/log/eyeglass/dns.log` | DFS delegation update failures |
| RAPA events | `/var/log/eyeglass/rapa.log` | Quarantine events, threat detections |
| Main app log | `/opt/superna/log/eyeglass.log` | Application-level errors |
| Support bundle | Admin UI → Admin → Support Bundle | Full diagnostic archive for Superna SR |

---

## See also

- [Superna Eyeglass — Common Issues](../common-issues/)
- [Superna Eyeglass — Escalation](../escalation/)
- [Superna Eyeglass — Health Checks](../../operations/health-checks/)

## Verify resolution

- `igls dr readiness` returns `Ready (100%)`
- `igls synciq status` shows all policies as `Running` or `Finished`
- `igls config replication status` shows all policies as `Synced`
- DR readiness score remains stable at ≥ 90% for 30 minutes after the fix
- If RAPA was involved: verify the quarantine is released and users can access the affected share
