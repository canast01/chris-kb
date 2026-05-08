# Aria Suite Lifecycle — Hardening

## Default Password

Change the default `admin` password immediately after deployment:
1. LCM → Settings → Local Users → admin → Change Password
2. Store the new password in CyberArk or enterprise vault

**Locker Master Password**: set during initial LCM configuration. If lost, all certificates and passwords in the Locker become inaccessible — requires re-import. Store securely in an offline vault.

## Certificate Management via Locker

All product certificates should be managed through the Locker — not by direct file replacement on appliances:

```
LCM → Locker → Certificates → Import Certificate
```
