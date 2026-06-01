# vCenter — Backup & Restore

```text
VCSA Backup & Restore Architecture
════════════════════════════════════════════════════════

  Backup Flow (file-based, VAMI)
  ┌─────────────────────────────────────────────────┐
  │  VCSA                                           │
  │  ┌───────────────────────────────────────────┐  │
  │  │ vCenter DB (vPostgres)                    │  │
  │  │ SSO config / identity sources / roles     │  │ ──── VAMI Backup
  │  │ Certificates (VMCA, STS, Machine SSL)     │  │      Scheduler
  │  │ Alarm definitions / scheduled tasks       │  │      (daily, 02:00)
  │  └───────────────────────────────────────────┘  │
  └────────────────────┬────────────────────────────┘
                       │ SFTP / FTPS / HTTPS
                       ▼
              ┌────────────────────┐
              │  Backup Target     │
              │  (SFTP server /    │
              │   NFS / S3)        │
              │                    │
              │  Retention: 7 days │
              │  Encryption: AES   │
              └────────────────────┘

  Restore Flow (full appliance redeploy)
  ┌───────────┐    ┌──────────────────┐    ┌────────────────┐
  │  VCSA ISO │    │  Stage 1         │    │  Stage 2       │
  │  (same or │───▶│  Deploy new VCSA │───▶│  Import backup │
  │   newer   │    │  on target ESXi  │    │  Enter encrypt │
  │   version)│    │  Set IP/FQDN     │    │  password      │
  └───────────┘    └──────────────────┘    └───────┬────────┘
                                                   │ 30-60 min
                                                   ▼
                                           ┌────────────────┐
                                           │  Stage 3       │
                                           │  Validate:     │
                                           │  services, SSO │
                                           │  hosts, API    │
                                           └────────────────┘
```
┌────────────────────────────────── vCenter Server — Backup & Restore ──────────────────────────────────┐
│                                                                                                       │
│  vCenter provides built-in file-based backup via VAMI; image-level backup via                         │
│  third-party tools using VADP; restore rebuilds the appliance from backup files.                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Backup Methods                │  │                 Backup Scope                │   │
│   │          File-based: VAMI schedule           │  │          Config: inventory + policy         │   │
│   │         Protocols: FTP/FTPS/HTTP/SCP         │  │              Events & tasks DB              │   │
│   │         Image-based: 3rd party tools         │  │         Stats DB excluded by default        │   │
│   │           Schedule: daily minimum            │  │           Certs included in backup          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  File-based backup exports VCSA config; restore deploys a new VCSA then imports.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Restore Procedure               │  │               Validation Steps              │   │
│   │             Deploy new VCSA OVA              │  │           Verify host connectivity          │   │
│   │           Point to backup location           │  │            Check SSO login works            │   │
│   │           Stage 1: appliance setup           │  │           Confirm inventory intact          │   │
│   │            Stage 2: data restore             │  │           Validate alarms/policies          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Backup target must be reachable from VCSA management network; backup files are                       │
│  compressed tarballs; restore needs network access to backup server.                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VAMI         = vCenter Appliance Management Interface; port 5480                                     │
│  File-based   = VCSA native backup; transfers config + DB to remote server                            │
│  Image-based  = full VMDK snapshot backup; requires quiescing or powered-off                          │
│  VADP         = vStorage APIs for Data Protection; 3rd-party backup API                               │
│  SCP          = Secure Copy; encrypted file transfer for backup destination                           │
│  Stage 1/2    = two-phase restore: deploy appliance, then restore config                              │
│  Stats DB     = performance metrics DB; excluded from default backup scope                            │
│  Retention    = number of backup copies to keep; set in VAMI scheduler                                │
│  Encryption   = backup password encrypts the tarball at rest                                          │
│  RTO          = target restore time; typically <1h for file-based restore                             │
│  Quiescing    = VADP flush; ensures consistent VM disk state during backup                            │
│  Tarball      = compressed archive format used by VCSA file-based backup                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

Include in weekly health check:
- Confirm last backup completed successfully (green status in VAMI)
- Confirm backup files exist on target (SSH to backup server and list directory)
- Confirm retention is working (old files being pruned)

### Alert on Backup Failure

Create a vCenter alarm or monitoring rule to alert if the backup job has not completed within 25 hours. Backup failure silently means no recovery path exists.

---

## Restore Procedure

Restore is a full appliance redeploy — you are deploying a new VCSA and importing the backup into it. The original VCSA must be powered off or removed before the restored appliance takes over.

```mermaid
graph TD
    start(["Restore required"])
    prereq["Gather: ISO, backup file,\nencryption password, target ESXi"]
    stage1["Stage 1 — Deploy new VCSA\nRun installer → Restore mode\nSet network, FQDN, root password"]
    stage2["Stage 2 — Import Backup\nProvide SFTP/FTP location\nEnter encryption password\nSelect backup timestamp"]
    wait["Appliance deploys and\nimports data (30–60 min)"]
    stage3["Stage 3 — Post-restore validation\nService status, SSO login,\nhost connectivity, integrations"]
    done(["vCenter restored"])

    start --> prereq --> stage1 --> stage2 --> wait --> stage3 --> done

    classDef step fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef gate fill:#15803d,stroke:#166534,color:#fff

    class stage1,stage2,stage3,prereq step
    class start,done gate
    class wait step
```

### Prerequisites

- Encryption password (from your password vault)
- Access to the backup target (SFTP/FTP/HTTPS server with backup files)
- A target ESXi host or cluster to deploy the new VCSA onto
- VCSA ISO for the **same version** as the backup (or a supported upgrade version)
- DNS record for the vCenter FQDN pointing to the new IP (if changing)

### Stage 1 — Deploy the New VCSA

1. Mount the VCSA ISO on a Windows/Linux/macOS workstation
2. Launch the installer:
   - Windows: `\vcsa-ui-installer\win32\installer.exe`
   - Linux: `./vcsa-ui-installer/lin64/installer`
3. Select **Restore**
4. Step through the installer wizard:
   - Provide the target ESXi host credentials
   - Accept the SSL certificate of the target host
   - Configure network settings (IP, FQDN, gateway, DNS)
   - Set a new root password for the appliance

### Stage 2 — Import Backup Data

5. On the **Backup Details** screen:
   - Enter backup server protocol, address, and path
   - Enter backup server credentials
   - Enter the encryption password
   - Select the specific backup timestamp to restore from
6. The installer will connect to the backup target and validate the backup file
7. Confirm the restore preview and click **Finish**
8. The installer deploys the appliance, imports the backup, and starts services (typically 30–60 minutes)

### Stage 3 — Post-Restore Validation

```bash
# SSH to restored vCenter appliance

# Confirm all services started
service-control --status --all

# Check for any service failures
service-control --status vpxd
service-control --status vmware-vpostgres
service-control --status vmware-stsd

# Check disk usage
df -h
```

```powershell
# PowerCLI — confirm connection and inventory
Connect-VIServer -Server <vcenter-fqdn>
Get-VMHost | Select-Object Name, ConnectionState, PowerState
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled
```

Post-restore checklist:
- [ ] vSphere Client accessible at `https://<vcenter>/ui`
- [ ] SSO login working for both `administrator@vsphere.local` and AD accounts
- [ ] All ESXi hosts show Connected in vCenter
- [ ] DRS and HA active on all clusters
- [ ] Backup job reconfigured and tested on restored appliance
- [ ] NSX, Aria, and Veeam integrations verified
- [ ] VAMI accessible at `https://<vcenter>:5480`

---

## Recovery Scenarios

### When to Troubleshoot In Place

Troubleshoot first if:
- A single service (vpxd, vmware-sts) can be restarted successfully
- Disk space can be freed to restore normal function
- A single certificate or SSO issue can be repaired using `certificate-manager`
- Database is accessible and only needs a service restart

### When to Restore from Backup

Restore from backup if:
- PostgreSQL database is corrupt (vpxd fails to start with DB connection errors)
- STS signing certificate is expired and cannot be repaired in place
- Multiple services fail to start after full service restart attempt
- The appliance VM is unrecoverable (hardware failure, corrupt disk)
- Partition table or Photon OS is corrupt

### Recovery Time Estimates

| Recovery Path | Estimated RTO |
|---|---|
| Service restart (vpxd, STS) | 5–15 minutes |
| In-place certificate replacement | 30–60 minutes + maintenance window |
| Full restore from backup (small environment) | 60–90 minutes |
| Full restore from backup (large environment) | 2–4 hours |

---

## Certificates to Track Before Any Restore

| Certificate | Location | Risk if Expired |
|---|---|---|
| vCenter Machine SSL | VAMI → Certificate Management | Browser warnings, API failures |
| VMCA Root Certificate | VAMI → Certificate Management | Breaks all VMCA-issued certs |
| STS Certificate | vSphere Client → SSO → Certificates | Login failures platform-wide |
| Solution User Certificates | VAMI → Certificate Management | Service-to-service auth failures |
| NSX Manager Certificate | NSX Manager → System | NSX UI and API failures |
| Aria Endpoint Certificates | Aria Suite Lifecycle | Integration and access failures |

Review all certificate expiration dates monthly. Flag certificates expiring within 60 days for planned replacement. Escalate certificates expiring within 30 days as urgent.

---

## vCenter High Availability (vCHA) vs. Backup

vCHA provides active/passive failover but is **not a substitute for file-based backup**:

| Scenario | vCHA Protects? | Backup Protects? |
|---|---|---|
| Active node hardware failure | Yes — failover to passive | Yes (via restore) |
| Database corruption on active | No — replicated to passive | Yes |
| Accidental mass permission deletion | No — replicated to passive | Yes |
| Ransomware/OS corruption | No | Yes (if backup is offsite) |
| Site-level failure (both nodes) | No | Yes |

If vCHA is deployed, maintain file-based backup regardless. The backup encryption password must be stored off-site and separate from vCenter access.

---

## Backup Audit Evidence

For compliance or audit:
- Export backup history screenshot from VAMI → Backup
- Document backup target, schedule, retention, and encryption password storage location
- Record annual restore test results (date, time taken, issues found, validated by)
- Store all evidence in your ITSM or change management system

Recovery test cadence: test restore to a non-production environment at minimum annually, ideally every 6 months. Document time taken and any issues encountered.
