---
tags:
  - aws
  - operations
---
# Amazon EVS — Backup & Restore

<div class="kb-summary">
EVS backup strategy: SDDC Manager configuration backup, vCenter VAMI backup, NSX-T config backup, VM workload backup options (Veeam, VADP, cloud-native), and restoration procedures. AWS manages host hardware; you manage the VMware data layer.
</div>

```text
┌──────────────────────────────────── Amazon EVS — Backup & Restore ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   SDDC Manager config backup: SFTP target (S3 via Transfer Family or on-prem SFTP); daily    │    │
│   │   vCenter config backup: vCenter VAMI → Backup; SFTP/SCP target; excludes VM disk data       │    │
│   │   NSX-T config backup: NSX Manager → System → Backup; captures all policies and DFW rules    │    │
│   │   VM workload backup: Veeam (VADP), AWS Backup, or cloud-native app-level backup             │    │
│   │   AWS manages: bare-metal host hardware; no ESXi OS-level backup required                    │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager backup = VCF configuration backup covering domains, hosts, and topology data            │
│  VAMI          = vCenter Appliance Management Interface; HTTPS management UI at port 5480             │
│  vCenter VCSA backup = VCSA file-based backup to SFTP/SCP/FTP; does not include VM disk data          │
│  NSX-T backup  = Full export of NSX-T configuration: segments, policies, DFW, gateways                │
│  VADP          = vStorage APIs for Data Protection; enables agentless VM backup via Veeam             │
│  S3            = AWS object storage; primary backup destination for EVS configuration data            │
│  Transfer Family = AWS managed SFTP service with S3 backend; acts as SFTP target for VCF              │
│  RTO           = Recovery Time Objective; max acceptable downtime; drives backup frequency            │
│  RPO           = Recovery Point Objective; max acceptable data loss; drives retention count           │
│  Veeam         = Backup software using VADP to quiesce and snapshot VMs inside EVS cluster            │
│  AWS Backup    = Native AWS backup service; can protect EVS VMs via integration agents                │
│  Retention     = Number of backup copies kept; minimum 3 for production environments                  │
│  Encryption token = Password protecting the VCSA backup; required for restore — store in vault        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Backup Architecture

EVS is a shared-responsibility model for backup. AWS and VMware each own different layers.

**What AWS manages (you do not back up):**

- Bare-metal host hardware: if a host fails, AWS replaces the hardware
- ESXi OS image: AWS re-provisions ESXi from an AWS-managed AMI when a host is replaced
- EVS environment metadata: stored in AWS and recoverable via the EVS API

**What you must back up:**

| Component | Tool | Backup Target | Frequency |
|---|---|---|---|
| SDDC Manager configuration | SDDC Manager built-in backup | SFTP (Transfer Family → S3 or on-prem SFTP) | Daily |
| vCenter database and config | vCenter VAMI file-based backup | SFTP/SCP target | Daily |
| NSX-T configuration | NSX Manager built-in backup | SFTP target | Daily or after changes |
| VM workloads | Veeam or AWS Backup | S3 / EBS / on-prem repo | Daily (full weekly, incremental daily) |
| HCX configuration | HCX Manager export | SFTP / local backup | After changes |

The most critical recovery order is: SDDC Manager → vCenter → NSX-T → VM workloads. If SDDC Manager is lost without a backup, VCF domain management is unrecoverable without VMware Support engagement.

## SDDC Manager Configuration Backup

SDDC Manager backs up its configuration database (VCF domains, hosts, VLANs, network topology) to an SFTP server. This backup is required for SDDC Manager restore if the appliance is lost.

**Configure SFTP backup target:**

```bash
SDDC_URL="https://sddc-manager.vcf.internal"
TOKEN=$(curl -sk -X POST "${SDDC_URL}/v1/tokens" \
  -H "Content-Type: application/json" \
  -d '{"username":"administrator@vsphere.local","password":"P@ssw0rd"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('accessToken',''))")

curl -sk -X PUT \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "${SDDC_URL}/v1/system/backup-configuration" \
  -d '{
    "server": "<transfer-family-endpoint>.server.transfer.us-east-1.amazonaws.com",
    "port": 22,
    "username": "sddc-backup",
    "password": "SFTPpassword123!",
    "directoryPath": "/backups/sddc-manager",
    "schedule": {
      "enabled": true,
      "frequency": "DAILY",
      "hourOfDay": 2
    }
  }'
```

**Trigger an immediate on-demand backup:**

```bash
TASK_ID=$(curl -sk -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "${SDDC_URL}/v1/backups/tasks" \
  -d '{"elements":[{"resourceType":"SDDC_MANAGER"}]}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

echo "Backup task ID: ${TASK_ID}"

watch -n 15 "curl -sk -H 'Authorization: Bearer ${TOKEN}' \
  ${SDDC_URL}/v1/tasks/${TASK_ID} | \
  python3 -c \"import sys,json; d=json.load(sys.stdin); print(d.get('status',''), d.get('completionTimestamp',''))\""
```

**List available backups:**

```bash
curl -sk -H "Authorization: Bearer ${TOKEN}" \
  "${SDDC_URL}/v1/backups" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for b in d.get('elements', []):
    print(b.get('timestamp',''), b.get('vcfVersion',''), b.get('fileName',''))
"
```

**SFTP target options for EVS:**

- AWS Transfer Family SFTP with S3 backend: recommended for EVS environments; SFTP endpoint backed by S3; requires IAM user with SSH key pair
- On-premises SFTP server via Direct Connect: alternative when on-prem backup infrastructure already exists

**Restore SDDC Manager from backup:**

1. Deploy a fresh SDDC Manager OVA (must match the VCF version of the backup)
2. SDDC Manager UI → Administration → Backup and Restore → Restore
3. Provide SFTP credentials and select the backup file by timestamp
4. SDDC Manager rebuilds domain inventory, host records, and VLAN topology from backup

## vCenter DB Backup

vCenter backup via VAMI captures the vCenter database, inventory, and configuration. It does not include VM disk data (VMDK files) — that is covered by the VM workload backup.

**Configure backup schedule via VAMI UI:**

1. Browse to `https://vcenter.vcf.internal:5480`
2. Recovery → Backup → Configure backup schedule
3. Set protocol to SFTP, enter the Transfer Family endpoint and credentials
4. Set retention count (minimum 3 for production)
5. Enable encryption and store the encryption password in AWS Secrets Manager

**Configure backup schedule via VAMI API:**

```bash
VAMI_URL="https://vcenter.vcf.internal:5480"
VCENTER_PASS="P@ssw0rd"

curl -sk -X POST "${VAMI_URL}/api/appliance/recovery/backup/schedules/daily-backup" \
  --user "root:${VCENTER_PASS}" \
  -H "Content-Type: application/json" \
  -d '{
    "enable": true,
    "recurrence_info": {
      "minute": 0,
      "hour": 1
    },
    "retention_info": {
      "max_count": 7
    },
    "backup_password": "BackupEncryptPass123!",
    "location_type": "SFTP",
    "location": "sftp://<transfer-family-endpoint>/backups/vcenter",
    "location_user": "vcenter-backup",
    "location_password": "SFTPpassword123!",
    "parts": ["seat", "common"]
  }'
```

**Trigger an immediate vCenter backup:**

```bash
curl -sk -X POST "${VAMI_URL}/api/appliance/recovery/backup/job" \
  --user "root:${VCENTER_PASS}" \
  -H "Content-Type: application/json" \
  -d '{
    "backup_password": "BackupEncryptPass123!",
    "location_type": "SFTP",
    "location": "sftp://<transfer-family-endpoint>/backups/vcenter",
    "location_user": "vcenter-backup",
    "location_password": "SFTPpassword123!",
    "parts": ["seat", "common"],
    "comment": "manual-backup"
  }'
```

**Restore vCenter from backup:**

1. Run the vCenter Server Appliance Installer
2. Select Stage 2 → select "Restore" instead of "Install"
3. Provide SFTP backup location and encryption password
4. vCenter is restored to the backed-up state

## NSX-T Config Backup

NSX-T backup captures all NSX-T configuration: logical segments, gateways, Distributed Firewall rules, transport zones, profiles, and cluster state. NSX-T does not back up data plane state — it backs up policy configuration.

**Configure SFTP backup via NSX Manager UI:**

NSX Manager → System → Backup & Restore → Configure → Provide SFTP target and credentials → Enable scheduling

**Configure via API:**

```bash
NSX_URL="https://nsx-manager.vcf.internal"
NSX_PASS="VMware1!VMware1!"

curl -sk -X PUT -u "admin:${NSX_PASS}" \
  -H "Content-Type: application/json" \
  "${NSX_URL}/api/v1/cluster/backups/config" \
  -d '{
    "server": "<transfer-family-endpoint>.server.transfer.us-east-1.amazonaws.com",
    "port": 22,
    "username": "nsx-backup",
    "password": "SFTPpassword123!",
    "directory_path": "/backups/nsx-manager",
    "schedule": {
      "resource_type": "IntervalBackupSchedule",
      "seconds_between_backups": 86400
    },
    "passphrase": "NSXbackupEncrypt123!"
  }'
```

**Trigger an immediate NSX-T on-demand backup:**

```bash
curl -sk -X POST -u "admin:${NSX_PASS}" \
  "${NSX_URL}/api/v1/cluster/backups?action=request_backup" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('backup_id',''))"
```

**List NSX-T backups:**

```bash
curl -sk -u "admin:${NSX_PASS}" \
  "${NSX_URL}/api/v1/cluster/backups/history" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for b in d.get('results', []):
    print(b.get('timestamp',''), b.get('backup_id',''), b.get('status',''))
"
```

NSX-T backup includes all policies, segments, firewall rules, and gateway configuration. It does not include fabric-level state (transport nodes are re-associated after restore). After NSX-T restore, you must re-push host transport node configuration.

## VM Workload Backup

VM workloads on EVS require an independent backup solution. Three approaches are commonly used:

| Approach | Tool | Where backup runs | Where data lands | Best for |
|---|---|---|---|---|
| VADP (agentless) | Veeam Backup & Replication | VM on EVS or on-prem | S3, EBS, or on-prem repo | Full VM backup with instant recovery |
| AWS Backup | AWS native service | AWS-managed | S3 / EBS | Simple compliance-driven backup without dedicated Veeam |
| Cloud-native | App-level (e.g. RDS snapshots, S3 versioning) | App/service level | S3 or app-native | Stateless apps or apps with native backup capability |

**Veeam Backup for EVS (VADP):**

```text
Veeam B&R server (VM on EVS or on-prem)
  → connects to vCenter via VADP API
  → creates VM snapshot
  → Veeam proxy reads changed blocks (CBT)
  → compresses and deduplicates
  → writes to backup repository (S3 or EBS via Veeam scale-out repo)

Recovery options:
  Instant VM Recovery: mount VM directly from backup and power on in EVS
  Full restore: restore VMDK to vSAN datastore
  Disk-level restore: restore individual VMDK to a running VM
```

Veeam on S3 repository configuration (Veeam UI):

1. Backup Infrastructure → Add Repository → Object Storage → Amazon S3
2. Create an S3 bucket in the same region as EVS (reduces data transfer cost)
3. Set immutability (S3 Object Lock) on the backup bucket for ransomware protection
4. Configure capacity tier for archival to S3 Glacier Instant Retrieval after 30 days

**AWS Backup for EVS VMs:**

AWS Backup can protect EVS VMs using the VMware integration. This requires the AWS Backup gateway deployed as a VM in the EVS cluster.

1. AWS Console → AWS Backup → Backup vaults → Create vault
2. AWS Backup → Gateways → Create gateway → deploy OVA in EVS vCenter
3. Associate gateway with the EVS vCenter
4. Create a backup plan targeting the EVS VM resource group
5. AWS Backup manages snapshots and retention; restores to the same or alternate EVS cluster

## Restore Procedures

**Restore SDDC Manager from backup:**

1. Deploy fresh SDDC Manager OVA (same VCF version as backup)
2. SDDC Manager UI → Administration → Backup and Restore → Restore
3. Provide SFTP credentials and select backup file
4. SDDC Manager rebuilds domain inventory from backup

**Restore vCenter from backup:**

1. Deploy fresh vCenter appliance using the vCSA Installer
2. Stage 2 → Restore → provide SFTP backup location and encryption password
3. vCenter is restored; all inventory, DRS rules, and HA settings are recovered

**Restore NSX-T from backup:**

1. NSX Manager → System → Backup & Restore → Restore
2. Provide SFTP location and passphrase
3. NSX Manager restores all policy configuration
4. Re-push host transport node configuration (NSX Manager → System → Fabric → Nodes)

**Restore a VM from Veeam:**

```text
Veeam → Home → Restore → VMware VMs → Restore from backup
  → Entire VM restore: select backup date and restore point
  → Instant VM Recovery: mount and power on from backup without full restore
  → Disk-level restore: attach individual VMDK to running VM
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
