---
tags:
  - aws
  - operations
description: "EVS backup strategy: SDDC Manager configuration backup, vCenter VAMI backup, NSX-T config backup, VM workload backup options (Veeam, VADP, cloud-native)..."
---
# Amazon EVS — Backup & Restore

<div class="kb-summary">
EVS backup strategy: SDDC Manager configuration backup, vCenter VAMI backup, NSX-T config backup, VM workload backup options (Veeam, VADP, cloud-native), and restoration procedures. AWS manages host hardware; you manage the VMware data layer.

*Applies to: Amazon EVS*
</div>
![Amazon EVS — Backup & Restore](../../../../assets/cloud-aws-evs-operations-backup-restore.svg)

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


```text title="Expected output"
{"accessToken":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbmlzdHJhdG9yQHZzcGhlcmUubG9jYWwiLCJleHAiOjE3MDk4MzIwMDB9.a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6","expiresIn":3600}
{"id":"backup-config-001","server":"<transfer-family-endpoint>.server.transfer.us-east-1.amazonaws.com","port":22,"username":"sddc-backup","directoryPath":"/backups/sddc-manager","schedule":{"enabled":true,"frequency":"DAILY","hourOfDay":2},"status":"CONFIGURED","lastModified":"2024-03-07T14:22:15Z"}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command (already present) or import the SDDC Manager CA certificate into your system trust store.
    **`jq: command not found` or `json.load(sys.stdin).get: error`** — Ensure python3 is installed and the JSON parsing syntax matches your Python version; test with `python3 -c "import json; print(json.dumps({'test':'ok'}))"`.
    **`{"error":"Invalid token","code":401}`** — Verify the SDDC Manager credentials (username/password) are correct and the `/v1/tokens` endpoint is accessible; check network connectivity to `sddc-manager.vcf.internal`.
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


```text title="Expected output"
Backup task ID: 550e8400-e29b-41d4-a716-446655440000
RUNNING 
RUNNING 
RUNNING 
COMPLETED 2024-01-15T14:32:18.000Z
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or ensure your CA certificate is in the system trust store.
    **`jq: command not found` or `python3: command not found`** — Install the required JSON parser (python3 is already used here) or verify it's in your PATH with `which python3`.
    **`Authorization: Bearer: command not found`** — Ensure the `TOKEN` environment variable is set before running the script with `export TOKEN="your_bearer_token"`.
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


```text title="Expected output"
2024-01-15T09:42:31.000Z 5.1.2 backup-sddc-prod-20240115-094231.tar.gz
2024-01-14T22:18:47.000Z 5.1.2 backup-sddc-prod-20240114-221847.tar.gz
2024-01-13T14:05:12.000Z 5.1.1 backup-sddc-prod-20240113-140512.tar.gz
2024-01-12T03:33:55.000Z 5.1.1 backup-sddc-prod-20240112-033355.tar.gz
2024-01-11T18:47:22.000Z 5.0.3 backup-sddc-prod-20240111-184722.tar.gz
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present; if still failing, verify `${SDDC_URL}` is correct and reachable).
    **`curl: (401) Unauthorized`** — Ensure `${TOKEN}` is set and valid by running `echo $TOKEN` and regenerating the API token if expired.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1`** — Verify the API endpoint returns valid JSON by testing `curl -sk -H "Authorization: Bearer ${TOKEN}" "${SDDC_URL}/v1/backups"` directly without piping to Python.
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


```text title="Expected output"
{
  "id": "daily-backup",
  "enable": true,
  "recurrence_info": {
    "minute": 0,
    "hour": 1,
    "day_of_week": null
  },
  "retention_info": {
    "max_count": 7
  },
  "location_type": "SFTP",
  "location": "sftp://<transfer-family-endpoint>/backups/vcenter",
  "location_user": "vcenter-backup",
  "parts": ["seat", "common"],
  "status": "SCHEDULED"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification (already present in example, but ensure it's not removed).
    **`{"error":{"messages":["Authentication failed"],"error_code":"com.vmware.appliance.recovery.backup.error.authentication_failed"}}`** — Verify vCenter root password is correct and user has backup permissions via `curl -sk -X GET "${VAMI_URL}/api/appliance/system/version" --user "root:${VCENTER_PASS}"`.
    **`{"error":{"messages":["Cannot connect to SFTP location"],"error_code":"com.vmware.appliance.recovery.backup.error.location_connection_failed"}}`** — Confirm SFTP endpoint is reachable and credentials are valid by testing connectivity: `sftp -o StrictHostKeyChecking=no vcenter-backup@<transfer-family-endpoint>`.
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


```text title="Expected output"
{
  "value": {
    "id": "backup-job-20240115-4a7c9e2f",
    "state": "RUNNING",
    "progress": 0,
    "start_time": "2024-01-15T14:32:18.456Z",
    "backup_type": "MANUAL",
    "location_type": "SFTP",
    "location": "sftp://s-a1b2c3d4e5f6g7h8i.server.transfer.us-east-1.amazonaws.com/backups/vcenter",
    "parts": ["seat", "common"],
    "comment": "manual-backup",
    "estimated_remaining_time": 1847
  }
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification (already present in the example, but ensure it's not removed).
    **`{"error": "Invalid location_type or malformed SFTP URL"}`** — Verify the SFTP endpoint format matches `sftp://hostname/path` and that the transfer family endpoint is correctly specified without extra protocols.
    **`{"error": "Authentication failed for location_user"}`** — Confirm the SFTP credentials (location_user and location_password) are correct and the vCenter backup user has write permissions on the remote SFTP path.
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


```text title="Expected output"
{
  "server": "s-1a2b3c4d5e6f7g8h9.server.transfer.us-east-1.amazonaws.com",
  "port": 22,
  "username": "nsx-backup",
  "directory_path": "/backups/nsx-manager",
  "schedule": {
    "resource_type": "IntervalBackupSchedule",
    "seconds_between_backups": 86400
  },
  "passphrase": "NSXbackupEncrypt123!",
  "_links": {
    "self": {
      "href": "/api/v1/cluster/backups/config"
    }
  }
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag (already present) or import the NSX Manager's CA certificate into your system trust store.
    **`{"httpStatus":401,"error_code":401,"module_name":"common","error_message":"Invalid credentials"}`** — Verify the NSX admin password in `NSX_PASS` matches the current credentials and the user has backup configuration permissions.
    **`{"httpStatus":400,"error_code":400,"module_name":"common","error_message":"Invalid SFTP server configuration"}`** — Test SFTP connectivity with `sftp -P 22 nsx-backup@<transfer-family-endpoint>.server.transfer.us-east-1.amazonaws.com` and confirm the directory path exists and is writable.
**Trigger an immediate NSX-T on-demand backup:**

```bash
curl -sk -X POST -u "admin:${NSX_PASS}" \
  "${NSX_URL}/api/v1/cluster/backups?action=request_backup" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('backup_id',''))"
```


```text title="Expected output"
backup-20240315-143827-a7f9c2e1-9d4a-4b2c-8f3a-6e1d2c9b5a4f
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host`** — Verify the NSX_URL environment variable is set correctly and the NSX Manager hostname is resolvable.
    **`curl: (60) SSL certificate problem: self signed certificate`** — The `-k` flag should bypass this, but if it persists, ensure your curl version supports the flag or check NSX Manager certificate validity.
    **`KeyError: 'backup_id'`** — Confirm the NSX Manager API response includes a `backup_id` field; check NSX version compatibility and that the backup request was accepted (HTTP 200/202).
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


```text title="Expected output"
2024-01-15T09:42:33.521Z backup-20240115-094233 SUCCEEDED
2024-01-14T14:18:47.892Z backup-20240114-141847 SUCCEEDED
2024-01-13T09:15:12.445Z backup-20240113-091512 SUCCEEDED
2024-01-12T22:33:05.178Z backup-20240112-223305 FAILED
2024-01-11T09:42:18.634Z backup-20240111-094218 SUCCEEDED
2024-01-10T14:27:51.209Z backup-20240110-142751 SUCCEEDED
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in the example, but ensure NSX_URL uses https://).
    **`curl: (7) Failed to connect to host:port: Connection refused`** — Verify NSX_URL environment variable is set correctly and the NSX manager is reachable on the network.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1`** — Confirm NSX_PASS credentials are correct; an authentication failure returns HTML error instead of JSON.
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

## See also

- [Amazon EVS — Procedures](../procedures/)
- [Amazon EVS — Common Issues](../../troubleshooting/common-issues/)
- [Amazon EVS — Health Checks](../health-checks/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
