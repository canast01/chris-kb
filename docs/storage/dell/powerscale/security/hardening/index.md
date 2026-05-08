# PowerScale — Hardening

> Security baselines and compliance configuration for Dell PowerScale.

## Hardening Checklist

- [ ] Change the default `root` and `admin` passwords immediately after cluster initialisation
- [ ] Disable SSH for non-administrative users; restrict SSH to management VLAN source IPs via firewall rules
- [ ] Enable HTTPS-only access to the OneFS web administration GUI; disable HTTP
- [ ] Configure session timeout on the web UI (recommended: 15 minutes)
- [ ] Enable audit logging for protocol access (NFS, SMB) and configuration changes
- [ ] Forward audit events to a centralised SIEM via syslog
- [ ] Restrict `root` squash on all NFS exports unless there is a specific technical requirement
- [ ] Apply SmartQuota hard limits to all user-accessible directories to prevent runaway consumption
- [ ] Enable SMB signing (`isi smb settings global modify --server-signing required`) for all Windows client access
- [ ] Review and restrict access zone IP pool source ranges to the specific client subnets for that zone
- [ ] Enable at-rest encryption (SED drives) if node hardware supports it; configure through Dell factory order
- [ ] Disable unused protocols per access zone (e.g., disable FTP, HDFS, S3 if not in use)
