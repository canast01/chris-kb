# Upgrade Readiness Checklist

Validates that infrastructure is in a safe state before any upgrade or patching activity begins. Complete all checks and obtain explicit go/no-go sign-off before proceeding.

## Pre-Upgrade Gate Criteria

```mermaid
flowchart LR
    A[Change Approved\nin ITSM] --> B[Backups\nVerified]
    B --> C[Rollback Plan\nDocumented]
    C --> D[Health Checks\nPassing]
    D --> E[Maintenance Window\nCommunicated]
    E --> F{Go / No-Go\nDecision}
    F -->|Go| G[Proceed with Upgrade]
    F -->|No-Go| H[Defer — remediate\nblocker first]
```

## 1. Change Management

| Check | Criteria | Verified By |
|---|---|---|
| Change ticket approved | CAB approval in ITSM | Change Manager |
| Maintenance window scheduled | Communicated ≥48h in advance | Owner |
| Stakeholders notified | Email / ticket sent | Owner |
| Vendor support available | TAC case open if high-risk | Owner |
| Rollback plan documented | Step-by-step with time estimate | Engineer |

## 2. Backup Verification

!!! warning "No upgrade without verified backup"
    A backup that has not been tested is not a backup. Verify restore capability, not just job completion.

```bash
# Veeam — verify last backup job succeeded
Get-VBRSession | Where-Object {$_.JobName -like "*HOSTNAME*"} | Select-Object -Last 5

# NetBackup
bperror -backstat -l -d "$(date -d '24 hours ago' +'%m/%d/%Y %H:%M:%S')"

# Confirm VM snapshot exists pre-upgrade
Get-VM -Name "HOSTNAME" | Get-Snapshot
```

| Backup Type | Required Age | Verified |
|---|---|---|
| Full VM backup / BMR | < 24 hours | ☐ |
| Application-consistent backup | < 24 hours | ☐ |
| Database backup | < 4 hours (if DB host) | ☐ |
| Config export (network device) | < 7 days | ☐ |

## 3. System Health Checks

```bash
# Linux
uptime                              # load < 2x CPU count
df -h                               # disk usage < 80%
free -h                             # available memory > 20%
systemctl --failed                  # no failed units
journalctl -p err -n 50 --no-pager # no critical errors

# Check for pending reboots (RHEL/Rocky)
needs-restarting -r && echo "No reboot pending" || echo "Reboot pending"

# Windows
Get-EventLog -LogName System -EntryType Error -Newest 20
(Get-PendingReboot).IsRebootPending

# VMware ESXi
esxcli system health status get
esxcli storage core path list | grep -c "Active (I/O)"
```

| Health Check | Pass Criteria |
|---|---|
| CPU load | < 80% sustained |
| Memory free | > 20% |
| Disk free | > 20% on all volumes |
| Failed services | None |
| Error log (last 1h) | No critical / hardware errors |
| HW alarms | No active hardware alerts |
| Replication lag | Within SLA |

## 4. Network and Connectivity

```bash
ping -c 3 <gateway>
ping -c 3 <dns-server>
ping -c 3 <ntp-server>

# NTP sync (drift < 1s)
chronyc tracking | grep "System time"

# DNS resolution
nslookup <hostname>.example.com
```

## 5. Vendor Compatibility Matrix

```bash
# VMware HCL — check driver/firmware compatibility before ESXi upgrade
esxcli software vib list | grep -E "bnx|igb|i40e|lpfc|nfnic|enic"
esxcli hardware firmware get
```

| Dependency | Current Version | Compatible With Upgrade | Checked |
|---|---|---|---|
| Hypervisor version | | | ☐ |
| Driver versions | | | ☐ |
| Firmware versions | | | ☐ |
| Application compatibility | | | ☐ |
| Storage array interop | | | ☐ |

## 6. Pre-Upgrade Snapshot (VMs)

```bash
# Take quiesced snapshot immediately before change
New-Snapshot -VM "HOSTNAME" \
  -Name "pre-upgrade-CHG-XXXX-$(Get-Date -Format yyyyMMdd)" \
  -Description "Pre-upgrade snapshot — CHG-XXXX" \
  -Quiesce \
  -Memory:$false

# Verify
Get-VM -Name "HOSTNAME" | Get-Snapshot | Select-Object Name, Created, SizeMB
```

!!! note "Snapshot retention"
    Remove pre-upgrade snapshots within 48 hours of successful completion. Stale snapshots degrade VM performance and consume datastore space.

## 7. Rollback Plan

```text
Rollback Plan — CHG-XXXX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
System:           <hostname>
Upgrade:          <from version> → <to version>
Rollback method:  [ ] Snapshot  [ ] Backup restore  [ ] Config revert
Snapshot name:    pre-upgrade-CHG-XXXX-YYYY-MM-DD
Estimated time:   <X> minutes
Rollback trigger: Service fails to start / error rate > 5% / app team reports failures
Decision authority: <name / role>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Go / No-Go Sign-Off

| Category | Status | Signed Off By |
|---|---|---|
| Change approved | ☐ Go / ☐ No-Go | |
| Backup verified | ☐ Go / ☐ No-Go | |
| Rollback plan documented | ☐ Go / ☐ No-Go | |
| System health passing | ☐ Go / ☐ No-Go | |
| Vendor compatibility confirmed | ☐ Go / ☐ No-Go | |
| Maintenance window active | ☐ Go / ☐ No-Go | |
| **Final Decision** | ☐ **GO** / ☐ **NO-GO** | |
