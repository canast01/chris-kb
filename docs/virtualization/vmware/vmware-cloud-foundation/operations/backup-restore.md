---
tags:
  - operations
  - vcf
  - vmware
---
# VCF Operations — Backup & Restore


<div class="kb-summary">
VMware Cloud Foundation backup protects the management plane components: SDDC Manager, NSX Manager, and vCenter Server. Each component has its own backup mechanism and must be restored in the correct sequence.

*Applies to: VCF 4.x / 5.x*
</div>

 This page covers configuration, scheduling, restore procedures, and validation.

---

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Management Plane Backup Overview

| Component | Backup Mechanism | Backup Target |
|---|---|---|
| SDDC Manager | Built-in backup (sftp / nfs) | SFTP or NFS share |
| NSX Manager | Built-in file-based backup | SFTP server |
| vCenter Server | File-Based Backup (FBB) | SFTP, FTP, NFS, HTTP, SCP |
| vSAN | No standalone backup — configuration embedded in vCenter + cluster | VCSA backup sufficient |
| ESXi host profiles | Host Profile export | File system / SDDC Manager |

> **Restore sequence (critical):** SDDC Manager → NSX Manager → vCenter Server. Restoring out of order will cause component relationship failures.

---

## Backup Architecture

```mermaid
flowchart TD
    subgraph VCF["VCF Management Domain"]
        SDDC[SDDC Manager] -- "Generates backup\n(tar.gz)" --> SFTP_S
        NSX[NSX Manager\nCluster] -- "File-based backup\n(tar.gz)" --> SFTP_S
        VCSA[vCenter Server\nAppliance] -- "File-based backup\n(tar.gz)" --> SFTP_S
    end

    SFTP_S[(SFTP / NFS\nBackup Target)]

    subgraph DR["DR / Restore"]
        SFTP_S --> R1[Restore SDDC Manager]
        R1 --> R2[Restore NSX Manager]
        R2 --> R3[Restore vCenter]
    end
```
```text
┌───────────────────────────── VMware Cloud Foundation — Backup & Restore ──────────────────────────────┐
│                                                                                                       │
│  VCF backup covers SDDC Manager, all vCenters, and NSX managers; each component                       │
│  has its own backup mechanism; orchestrated via SDDC Manager.                                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             SDDC Manager Backup              │  │                vCenter Backup               │   │
│   │          SFTP-based external backup          │  │             File-based via VAMI             │   │
│   │           Schedule: daily minimum            │  │              SFTP or SCP target             │   │
│   │        Config: domains + credentials         │  │               Schedule: daily               │   │
│   │       Encryption: optional passphrase        │  │            All domains backed up            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SDDC Manager backup is critical; without it domain topology cannot be recovered.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              NSX Manager Backup              │  │              Restore Procedure              │   │
│   │         NSX UI: Operations > Backup          │  │            Restore SDDC Mgr first           │   │
│   │         SFTP target: external server         │  │            Then restore vCenters            │   │
│   │           Per-domain NSX backed up           │  │          Then restore NSX managers          │   │
│   │        Encryption passphrase: store!         │  │          Validate: all services up          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Backup target SFTP server must be on management network; store passphrase in                         │
│  separate secure location from backup files.                                                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager backup= JSON export of all domain topology and credentials                              │
│  SFTP          = Secure File Transfer Protocol; backup transport                                      │
│  Passphrase    = encrypts NSX backup; must be stored separately                                       │
│  File-based    = VCSA native backup; config + DB; not full image                                      │
│  Restore order = SDDC Mgr → vCenter → NSX; sequence is critical                                       │
│  Domain topology= SDDC Mgr stores which hosts/clusters/domains exist                                  │
│  NSX backup    = includes all routing, firewall, segment config                                       │
│  vCenter backup= inventory, policies, permissions, alarms                                             │
│  vSAN VMs      = backed up separately via VADP tools                                                  │
│  Encryption    = backup passphrase; AES encryption of backup files                                    │
│  VAMI          = vCenter Appliance Management; port 5480; backup UI                                   │
│  RPO           = daily backup = 24h RPO for config; VMs = per backup tool                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## NSX Manager Backup

### Configure via NSX UI

1. Log in to **NSX Manager** (`https://<nsx-manager-vip>`).
2. Navigate to **System → Backup & Restore**.
3. Click **Edit** next to **SFTP Server**.

| Field | Value |
|---|---|
| Protocol | SFTP |
| IP / FQDN | `backup-srv.corp.example.com` |
| Port | 22 |
| Username | `nsx-backup` |
| Directory | `/vcf/nsx/` |
| Passphrase | (encryption passphrase) |
| Backup Frequency | Hourly |

4. Click **Save**, then **Backup Now** to test.

### Configure via NSX API

```bash
NSX_MGR="nsx-manager.corp.example.com"
NSX_USER="admin"
NSX_PASS="NSXAdminPassword"

# Configure backup
curl -sk -u "$NSX_USER:$NSX_PASS" \
  -X PUT "https://$NSX_MGR/api/v1/cluster/backups/config" \
  -H "Content-Type: application/json" \
  -d '{
    "backup_enabled": true,
    "remote_file_server": {
      "server": "backup-srv.corp.example.com",
      "port": 22,
      "protocol": {"protocol_name": "sftp"},
      "directory_path": "/vcf/nsx/",
      "authentication": {
        "authentication_scheme": {
          "scheme_name": "PASSWORD",
          "username": "nsx-backup",
          "password": "SFTPPassword"
        }
      }
    },
    "backup_schedule": {
      "resource_type": "IntervalBackupSchedule",
      "seconds_between_backups": 3600
    },
    "passphrase": "BackupEncryptionPassphrase"
  }'

# Trigger manual backup
curl -sk -u "$NSX_USER:$NSX_PASS" \
  -X POST "https://$NSX_MGR/api/v1/cluster/backups?action=start"

# List available backups
curl -sk -u "$NSX_USER:$NSX_PASS" \
  "https://$NSX_MGR/api/v1/cluster/restore/backuptimestamps" | jq '.results[] | {backup_id, timestamp}'
```

---

## vCenter Server File-Based Backup (FBB)

### Configure via VAMI

1. Access vCenter VAMI: `https://<vcsa-fqdn>:5480`
2. Navigate to **Backup**.
3. Click **Configure**.

| Field | Value |
|---|---|
| Backup Protocol | SFTP |
| Server | `backup-srv.corp.example.com` |
| Port | 22 |
| Username | `vcsa-backup` |
| Password | (store in vault) |
| Backup Directory | `/vcf/vcenter/` |
| Encrypt backup | Yes |
| Backup Password | (encryption passphrase) |
| Schedule | Daily at 02:00 |
| Retention | 3 copies |

4. Click **Save**, then **Backup Now** to validate.

### Trigger Backup via REST API

```bash
VCSA="vcenter.corp.example.com"

# Authenticate (returns session ID)
SESSION=$(curl -sk -u "administrator@vsphere.local:vSpherePassword" \
  -X POST "https://$VCSA/rest/com/vmware/cis/session" \
  -H "Content-Type: application/json" | tr -d '"')

# Create backup job
curl -sk -H "vmware-api-session-id: $SESSION" \
  -X POST "https://$VCSA/rest/appliance/recovery/backup/job" \
  -H "Content-Type: application/json" \
  -d '{
    "spec": {
      "location_type": "SFTP",
      "location": "sftp://backup-srv.corp.example.com/vcf/vcenter/",
      "location_user": "vcsa-backup",
      "location_password": "SFTPPassword",
      "parts": ["common", "seat"],
      "backup_password": "BackupEncryptionPassphrase",
      "comment": "Scheduled backup"
    }
  }' | jq '.value.id'
```

---

## vSAN Configuration Backup

vSAN configuration is captured as part of the vCenter backup (all cluster settings are stored in the vCenter database). No separate backup is required for vSAN data — only for configuration.

To extract vSAN configuration details for documentation or recovery reference:

```powershell
# Connect to vCenter
Connect-VIServer -Server vcenter.corp.example.com -User administrator@vsphere.local -Password "vSpherePassword"

# Export vSAN cluster configuration
$Cluster = Get-Cluster "VCF-Cluster-01"
$vsanView = Get-VsanView -Id "VsanVcClusterConfigSystem-vsan-cluster-config-system"
$Config   = $vsanView.VsanClusterGetConfig($Cluster.Id)
$Config | ConvertTo-Json -Depth 10 | Out-File "vsan-config-$(Get-Date -Format yyyyMMdd).json"

# Also capture disk group layout
Get-VsanDiskGroup -Cluster $Cluster | Select-Object VMHost, @{N='CacheDisks';E={$_.CacheDisk.CanonicalName}}, @{N='CapacityDisks';E={$_.DataDisk.CanonicalName -join ','}} | Export-Csv "vsan-diskgroups-$(Get-Date -Format yyyyMMdd).csv"
```

---

## Restore Procedure

### Restore Sequence

```mermaid
sequenceDiagram
    participant Ops as Operations
    participant SDDC as SDDC Manager
    participant NSX as NSX Manager
    participant VCSA as vCenter Server

    Note over Ops: Disaster recovery initiated

    Ops->>SDDC: Deploy SDDC Manager OVA
    SDDC-->>Ops: Appliance online
    Ops->>SDDC: Initiate restore from backup
    SDDC-->>Ops: SDDC Manager restored

    Ops->>NSX: Deploy NSX Manager OVA(s)
    NSX-->>Ops: Appliance(s) online
    Ops->>NSX: Restore from backup\n(API /cluster/restore)
    NSX-->>Ops: NSX Manager restored

    Ops->>VCSA: Deploy VCSA OVA via\nvCenter Recovery wizard
    VCSA-->>Ops: Appliance online
    Ops->>VCSA: Stage 2: point to backup\nand restore
    VCSA-->>Ops: vCenter restored

    Ops->>Ops: Validate all components\nand workload connectivity
```

### Step 1 — Restore SDDC Manager

1. Deploy a new SDDC Manager OVA with the same IP, FQDN, and sizing as the original.
2. In the SDDC Manager UI: **Administration → Backup & Restore → Restore**.
3. Provide SFTP credentials and select the backup to restore from.
4. Monitor the restore task until completion.

### Step 2 — Restore NSX Manager

```bash
# Point the new NSX Manager appliance at the SFTP backup location
curl -sk -u "admin:NSXAdminPassword" \
  -X POST "https://<new-nsx-manager>/api/v1/cluster/restore?action=start" \
  -H "Content-Type: application/json" \
  -d '{
    "backup_timestamp": "<timestamp-from-backuptimestamps-api>",
    "passphrase": "BackupEncryptionPassphrase",
    "remote_file_server": {
      "server": "backup-srv.corp.example.com",
      "port": 22,
      "protocol": {"protocol_name": "sftp"},
      "directory_path": "/vcf/nsx/",
      "authentication": {
        "authentication_scheme": {
          "scheme_name": "PASSWORD",
          "username": "nsx-backup",
          "password": "SFTPPassword"
        }
      }
    }
  }'

# Monitor restore progress
curl -sk -u "admin:NSXAdminPassword" \
  "https://<new-nsx-manager>/api/v1/cluster/restore/status" | jq '{status, step, total_steps}'
```

### Step 3 — Restore vCenter Server

Use the **vCenter Server Installer** (ISO mounted on a management workstation):

```text
1. Mount VMware-VCSA-<version>.iso
2. Run: installer/win32/installer.exe (Windows) or installer/mac/Installer.app
3. Select "Restore"
4. Stage 1: Deploy new appliance (same IP, FQDN, sizing)
5. Stage 2: Connect to backup source (SFTP) and select backup
6. Enter backup encryption passphrase
7. Complete restore — appliance reboots with restored state
```

---

## Validation Steps

```powershell
# Connect to restored vCenter
Connect-VIServer -Server vcenter.corp.example.com -User administrator@vsphere.local -Password "vSpherePassword"

# Verify cluster and host inventory
Get-Cluster | Select-Object Name, @{N='Hosts';E={($_ | Get-VMHost).Count}}
Get-VMHost  | Select-Object Name, ConnectionState, PowerState

# Verify vSAN health
Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system" |
  ForEach-Object { $_.VsanQueryVcClusterHealthSummary($cluster.Id,$null,$null,$true,$null,$null,'defaultView') } |
  Select-Object overallHealth

# Check all management VMs are running
Get-VM | Where-Object {$_.Name -match "vcenter|nsx|sddc|vrops|vrli|vra"} |
  Select-Object Name, PowerState
```

```bash
# Validate NSX data plane after restore
curl -sk -u "admin:NSXAdminPassword" \
  "https://nsx-manager.corp.example.com/api/v1/transport-nodes/status-summary" \
  | jq '{up_count, degraded_count, down_count}'

# Check NSX Manager cluster status
curl -sk -u "admin:NSXAdminPassword" \
  "https://nsx-manager.corp.example.com/api/v1/cluster/status" \
  | jq '{control_cluster_status, mgmt_cluster_status}'
```

```bash
# SDDC Manager — validate domain health
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<sddc-manager>/v1/domains" | jq '.elements[] | {id, name, status}'

# Check all workload domains
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<sddc-manager>/v1/hosts" | jq '.elements[] | {hostName, status}'
```

---

## Backup Schedule Reference

| Component | Frequency | Retention | Target |
|---|---|---|---|
| SDDC Manager | Hourly | 14 days | SFTP |
| NSX Manager | Hourly | 14 days | SFTP |
| vCenter Server | Daily at 02:00 | 7 copies | SFTP |
| vSAN config export | Weekly | 90 days | File archive |
| Host profiles | After any change | Versioned | SDDC Manager |

> **Test restores:** Run a full restore simulation quarterly in an isolated environment. An untested backup is not a backup.

## See also

- [VCF — Procedures](procedures/)
- [VCF Troubleshooting — Common Issues](../troubleshooting/common-issues/)
- [VCF — Health Checks](health-checks/)
