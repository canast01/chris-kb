# vCenter — Backup & Restore

## Backup Configuration

- Use the file-based backup built into the VCSA Appliance Management Interface (VAMI)
- Access via `https://<vcenter>:5480` → **Backup**
- Set a backup schedule — recommended: daily
- Set a retention period — recommended: keep at least 3 backup copies
- Configure a remote backup target: SFTP, FTP, FTPS, HTTP, or HTTPS
- Set and securely store the encryption password — required for restore

## Backup Review

- Confirm the most recent backup completed successfully
- Review backup job history in VAMI weekly
- Alert if a backup has not completed within the expected schedule
- Include backup status in the weekly health check

## Restore Requirements

- Encryption password must be available
- Backup target must be accessible
- Target ESXi host or content library must be ready to receive the VCSA OVA
- Time to restore depends on backup size and network speed

## Recovery Testing

- Test a restore to a non-production environment at least annually
- Document the restore procedure and time taken
- Confirm SSO, services, and integrations work after restore

## Backup Evidence for Audits

- Export backup history screenshots from VAMI
- Document backup target, schedule, and retention settings
- Store evidence in the change management or audit system

## When to Restore Versus Troubleshoot

Troubleshoot first if:
- Services can be restarted and recovered
- Disk space can be freed to restore normal function
- A single certificate or SSO issue can be repaired in place

Restore from backup if:
- Database is corrupt
- STS certificate cannot be repaired
- Services fail to start after all troubleshooting steps
- The appliance is unrecoverable after a hardware or VM failure

## Certificates to Track Before Any Restore

| Certificate | Location | Risk if Expired |
|---|---|---|
| vCenter Machine SSL | VAMI → Certificate Management | Browser warnings, API failures |
| VMCA Root Certificate | VAMI → Certificate Management | Breaks all VMCA-issued certs |
| STS Certificate | vSphere Client → SSO → Certificates | Login failures platform-wide |
| Solution User Certificates | VAMI → Certificate Management | Service-to-service auth failures |
| NSX Manager Certificate | NSX Manager → System | NSX UI and API failures |
| Aria Endpoint Certificates | Aria Suite Lifecycle | Integration and access failures |

## Certificate Expiration Tracking Schedule

- Review all certificate expiration dates monthly
- Flag certificates expiring within 60 days — plan replacement
- Escalate certificates expiring within 30 days — urgent action required
- Document next renewal date after each replacement

## Backup Procedures

- Use the file-based backup built into the VCSA Appliance Management Interface (VAMI)
- Access via `https://<vcenter>:5480` → **Backup**
- Set a backup schedule — recommended: daily
- Set a retention period — recommended: keep at least 3 backup copies
- Configure a remote backup target: SFTP, FTP, FTPS, HTTP, or HTTPS
- Set and securely store the encryption password — required for restore

### Backup Review

- Confirm the most recent backup completed successfully
- Review backup job history in VAMI weekly
- Alert if a backup has not completed within the expected schedule
- Include backup status in the weekly health check

### Restore Requirements

- Encryption password must be available
- Backup target must be accessible
- Target ESXi host or content library must be ready to receive the VCSA OVA
- Time to restore depends on backup size and network speed

### Recovery Testing

- Test a restore to a non-production environment at least annually
- Document the restore procedure and time taken
- Confirm SSO, services, and integrations work after restore

### Backup Evidence for Audits

- Export backup history screenshots from VAMI
- Document backup target, schedule, and retention settings
- Store evidence in the change management or audit system

### When to Restore Versus Troubleshoot

Troubleshoot first if:
- Services can be restarted and recovered
- Disk space can be freed to restore normal function
- A single certificate or SSO issue can be repaired in place

Restore from backup if:
- Database is corrupt
- STS certificate cannot be repaired
- Services fail to start after all troubleshooting steps
- The appliance is unrecoverable after a hardware or VM failure
