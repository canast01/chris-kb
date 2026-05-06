# NetBackup Security

NetBackup Access Control (NBAC) provides role-based access using OS-level groups or external LDAP/AD integration, separating admin, operator, and restore-only roles. All clients authenticate to the master server using certificates issued by the NetBackup Certificate Authority (NetBackup CA), eliminating shared-secret authentication and supporting automated certificate rotation. Data can be encrypted at the client side (CPU overhead on client) or at the media server side, with AES-256 as the enforced standard for any policy covering sensitive data.

**Security checklist**

- [ ] NBAC enabled; no local `bp.conf` bypass accounts
- [ ] NetBackup CA deployed; all client certificates valid and not expired
- [ ] Client-side or media-server-side encryption enabled for PII/regulated policies
- [ ] Audit logging enabled: `nbauditreport` output reviewed weekly
- [ ] Master server firewall: only required ports open (1556, 13724, 13782)
- [ ] Unused services (PBX on non-required hosts) disabled
- [ ] CyberArk AAM integration: NetBackup service account passwords rotated per policy
- [ ] OpsCenter access restricted to backup admin group via LDAP role mapping
