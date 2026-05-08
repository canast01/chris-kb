# Veeam — Hardening

## Network Security

| Port | Purpose | Restriction |
|---|---|---|
| 9392/TCP | VBR console communication | Restrict to admin management subnets |
| 2500–3300/TCP | Data transfer (proxy) | Open between proxies and repositories only |
| 443/TCP | vCenter API | VBR to vCenter |
| 6160/TCP | Veeam Installer Service | Between VBR server and managed components |

## Security Hardening Checklist

- [ ] RBAC configured with AD groups — no shared admin logins
- [ ] Encryption enabled on all jobs writing to cloud or off-site targets
- [ ] Linux hardened repository deployed for immutable local backups
- [ ] S3 Object Lock in Compliance mode for cloud capacity tier
- [ ] Encryption keys exported and stored in CyberArk/offline vault
- [ ] VBR console port (9392) restricted to admin subnets via firewall
- [ ] CyberArk integration active for infrastructure credentials
- [ ] Audit log forwarded to SIEM; alerts configured
- [ ] Veeam ONE alert for any backup job failing > 2 consecutive times
