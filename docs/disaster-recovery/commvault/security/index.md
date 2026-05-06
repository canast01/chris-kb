# CommVault Security

CommVault RBAC is implemented through User Groups mapped to roles (Master, Tenant Admin, Operator, End User) with permissions scoped to specific client groups, storage policies, or subclients — enabling least-privilege access for different teams without sharing admin credentials. All backup data encryption is configured at the storage policy level using AES-256; options include client-side encryption (CPU overhead on client), MediaAgent-side (off-client), and at-rest encryption in the storage library. DDB encryption is a separate option that encrypts the deduplication database itself.

**Security checklist**

- [ ] RBAC: all user access scoped to minimum required entity groups
- [ ] No shared admin accounts — individual named accounts for each operator
- [ ] Encryption enabled on storage policies covering PII or regulated data (AES-256)
- [ ] DDB encryption enabled for any DDB storing sensitive workload data
- [ ] Two-factor authentication (2FA) enabled for Command Center web login
- [ ] Audit trail: CommServe audit log reviewed monthly; forwarded to SIEM via syslog
- [ ] CyberArk integration: CommVault service account passwords managed via CCP
- [ ] CommServe access: management ports (8400, 8403) restricted to admin subnets via firewall
