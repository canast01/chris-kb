---
tags:
  - operations
  - vcenter
  - vmware
  - vsphere-8
---
# vCenter — Backup & Restore

<div class="kb-summary">
Backup & Restore reference covering Alert on Backup Failure, Restore Procedure, Recovery Scenarios, Certificates to Track Before Any Restore, vCenter High Availability (vCHA) vs. Backup and 1 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>
![vCenter — Backup & Restore](../../../../assets/virtualization-vmware-vcenter-operations-backup-restore.svg)

## Restore from File-Based Backup

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

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

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

---

## See also

- [vCenter — Procedures](procedures/)
- [vCenter Troubleshooting — Common Issues](../troubleshooting/common-issues/)
- [vCenter — Health Checks](health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
