# Veeam Security

Veeam implements role-based access control through five built-in roles: Veeam Backup Administrator (full control), Veeam Backup Operator (run jobs), Veeam Restore Operator (restore only), Veeam Backup Viewer (read-only), and Veeam Tape Operator. Roles are assigned to AD users or groups in the VBR console under Users and Roles. Immutable backups are achieved via Linux hardened repositories (using `chattr +i` on backup files) or S3 Object Lock — both prevent deletion or modification for the configured immutability period, protecting against ransomware.

**Security checklist**

- [ ] RBAC: operators mapped to AD groups — no shared service account logins to console
- [ ] Encryption enabled on all jobs writing to cloud or off-site repositories (AES-256)
- [ ] Linux hardened repository: VBR connects as a non-root user; `su` disabled
- [ ] S3 Object Lock (if using object storage capacity tier): `Compliance` mode with retention period matching policy
- [ ] MFA enabled for Veeam Backup Enterprise Manager (if deployed)
- [ ] Audit log: review `C:\ProgramData\Veeam\Backup\Audit.log` monthly
- [ ] CyberArk integration: Veeam service account and infrastructure credentials retrieved via CCP
- [ ] Veeam Backup Server: Windows Firewall restricts management port (9392) to admin subnets only
