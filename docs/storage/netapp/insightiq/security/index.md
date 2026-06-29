---
tags:
  - netapp
  - security
---
# InsightIQ Security

<div class="kb-summary">
InsightIQ Security reference covering Authentication, OneFS Service Account Security, Database Backup Encryption, Audit Logging, Security Hardening Checklist.

*Applies to: InsightIQ*
</div>

```d2
direction: down

external: External / Untrusted {shape: rectangle}
authentication: "Authentication" {shape: rectangle}
database_backup_encryption: "Database Backup Encryption" {shape: rectangle}
audit_logging: "Audit Logging" {shape: rectangle}
security_hardening_checklist: "Security Hardening Checklist" {shape: rectangle}
core: "InsightIQ Core" {shape: hexagon}

external -> authentication: traffic in
authentication -> database_backup_encryption
database_backup_encryption -> audit_logging
audit_logging -> security_hardening_checklist
security_hardening_checklist -> core: secured path
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Authentication

InsightIQ supports local accounts and LDAP/Active Directory integration. LDAP integration is strongly preferred for production environments to enable centralised account management and audit.

### Local Accounts

Local accounts should be limited to:
- The initial admin account used during deployment
- A break-glass account in case LDAP is unavailable

Do not use local accounts for day-to-day operations.

### LDAP / Active Directory Integration

Rotate the service account password on the 12-month schedule. Update the credential in InsightIQ immediately after rotation.

## Database Backup Encryption

InsightIQ database backups contain performance data and should be encrypted at rest.

```bash
# Encrypted backup using GPG
pg_dump -U iiq iiq | gzip | gpg --cipher-algo AES256 \
  --compress-algo none --symmetric \
  --batch --passphrase-fd 0 > /backup/iiq_$(date +%Y%m%d).sql.gz.gpg <<< "$BACKUP_PASSPHRASE"
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`gpg: problem with the agent: Permission denied`** — Ensure the GPG agent has proper permissions by running `gpg-connect-agent /bye` or set `export GPG_TTY=$(tty)` before the command.
    **`pg_dump: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory`** — Verify the PostgreSQL service is running with `systemctl status postgresql` and the IIQ database is accessible.
    **`bash: /backup: Permission denied`** — Create the backup directory with write permissions using `mkdir -p /backup && chmod 755 /backup` or run the command with appropriate sudo privileges.
Store the backup passphrase in the secrets manager. Backup files should be stored on an encrypted backup target or an encrypted datastore.

## Audit Logging

InsightIQ logs admin actions (user logins, configuration changes, cluster add/remove) in the appliance logs. Forward to SIEM via syslog.

```bash
# /etc/rsyslog.d/insightiq.conf
*.* @@<SIEM-IP>:514    # TCP syslog to SIEM

sudo systemctl restart rsyslog
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Job for rsyslog.service failed because the control process exited with error code.`** — Validate the rsyslog.conf syntax with `sudo rsyslogd -N1` before restarting to identify configuration errors.
    **`Failed to restart rsyslog.service: Unit rsyslog.service not found.`** — Ensure rsyslog is installed with `sudo apt-get install rsyslog` (Debian/Ubuntu) or `sudo yum install rsyslog` (RHEL/CentOS).
Key events to monitor in SIEM:
- User login failures
- Admin configuration changes
- Cluster connection changes

## Security Hardening Checklist

- [ ] LDAP/AD integration enabled; local accounts disabled for non-break-glass users
- [ ] HTTPS enforced; internal CA-signed certificate in place
- [ ] Network access restricted to ops management subnet
- [ ] `svc-insightiq` service account is read-only; password in secrets manager
- [ ] Database backups encrypted at rest and stored on external backup target
- [ ] Syslog forwarding to SIEM configured
- [ ] NTP configured (prevents certificate errors)
- [ ] Stale user accounts removed (monthly review)
- [ ] InsightIQ OS and packages patched on standard patch cycle
