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

Store the backup passphrase in the secrets manager. Backup files should be stored on an encrypted backup target or an encrypted datastore.

## Audit Logging

InsightIQ logs admin actions (user logins, configuration changes, cluster add/remove) in the appliance logs. Forward to SIEM via syslog.

```bash
# /etc/rsyslog.d/insightiq.conf
*.* @@<SIEM-IP>:514    # TCP syslog to SIEM

sudo systemctl restart rsyslog
```

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
