# SnapCenter Security
## RBAC

SnapCenter implements role-based access control at the application level, layered on top of ONTAP-level permissions.

### Built-in Roles

| Role | Access Level |
|---|---|
| SnapCenter Admin | Full access — all operations, settings, user management |
| Infrastructure Admin | Storage connections, hosts, plugins — no backup/restore operations |
| Application Backup and Clone Admin | Create/modify policies, resource groups, run backups, clones, restores |
| Backup and Clone Viewer | Read-only view of jobs, backups, resource groups — no modifications |

### Custom Roles

Create custom roles to delegate specific operations to application teams:

```powershell
# Create a custom role
Add-SmRole -RoleName "Oracle-Restore-Only" -Description "Oracle DBA can restore and clone only"

# Add permissions to the role
Set-SmRole -RoleName "Oracle-Restore-Only" -AllowedOperations "RestoreFromBackup","Clone"

# Assign an AD user to the role
Add-SmUser -UserName "domain\ora-dba01" -RoleName "Oracle-Restore-Only"
```

Assign RBAC at the resource or resource-group level — a user can be granted access to specific resource groups without seeing all resources in SnapCenter.

## Authentication

- SnapCenter GUI and API use local accounts or Active Directory accounts
- Multi-factor authentication (MFA): SnapCenter 6.0+ supports MFA via SAML 2.0 integration with an IdP (AD FS, Okta, Azure AD)
- Service accounts used for ONTAP connections should use dedicated accounts with minimum ONTAP RBAC permissions — not personal admin accounts
- Plugin hosts use OS-level credentials for agent communication; store credentials in SnapCenter Credential Store (Settings → Credentials), not in plaintext scripts

## TLS and Certificate Management

- SnapCenter web server uses TLS 1.2 minimum; configure in IIS → SSL Settings
- Replace the default self-signed certificate with a CA-signed certificate for production deployments:
  1. Generate a CSR from IIS on the SnapCenter Server
  2. Submit to internal CA or public CA
  3. Import signed certificate and update the IIS HTTPS binding on port 8146
- Verify the certificate is trusted by all automation hosts and browsers used to access the GUI

## ONTAP Service Account Security

SnapCenter connects to ONTAP using credentials stored in the SnapCenter Credential Store. Best practices:

```bash
# On ONTAP — create a dedicated SnapCenter service account with minimum permissions
security login role create -role sc-backup-role -cmddirname "DEFAULT" -access none -vserver <admin-svm>
security login role create -role sc-backup-role -cmddirname "volume" -access all -vserver <admin-svm>
security login role create -role sc-backup-role -cmddirname "snapshot" -access all -vserver <admin-svm>
security login role create -role sc-backup-role -cmddirname "snapmirror" -access all -vserver <admin-svm>
security login role create -role sc-backup-role -cmddirname "lun" -access all -vserver <admin-svm>

# Create the service account
security login create -username svc-snapcenter -application ontapi -authmethod password -role sc-backup-role -vserver <admin-svm>
security login create -username svc-snapcenter -application http -authmethod password -role sc-backup-role -vserver <admin-svm>
```

## Audit Logging

- All SnapCenter user operations (login, job trigger, policy change, restore, clone) are written to the audit log
- Access audit log: Settings → Settings → Audit Logs in the GUI, or query via REST API
- Export audit logs to a SIEM: configure syslog forwarding from the Windows Server (use Windows Event Forwarding or a Splunk/Elastic agent on the SnapCenter Server)
- Audit log tampering protection: SnapCenter 6.1+ signs audit log entries with a hash chain for integrity verification

## Hardening Checklist

- [ ] Default `admin` password changed from installation default; stored in a secrets vault
- [ ] AD groups used for SnapCenter access; no individual AD user accounts unless required
- [ ] MFA enabled if SnapCenter 6.0+ is deployed and an IdP is available
- [ ] Default self-signed TLS certificate replaced with CA-signed certificate on port 8146
- [ ] TLS 1.2 minimum enforced in IIS
- [ ] ONTAP service account uses least-privilege custom role (not `vsadmin` or `admin`)
- [ ] Plugin host credentials stored in SnapCenter Credential Store; no plaintext passwords in scripts
- [ ] Audit log review included in weekly operational checks
- [ ] SnapCenter Server VM is hardened per Windows Server CIS benchmark; not used for other workloads
- [ ] Network access to port 8146 restricted to admin workstations and automation hosts (firewall or NSG rule)
