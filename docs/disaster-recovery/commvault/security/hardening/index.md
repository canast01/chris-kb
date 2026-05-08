# Commvault — Hardening

## Network Security

| Port | Purpose | Restriction |
|---|---|---|
| 8400/TCP | CommServe communication | Restrict to admin management subnets |
| 8403/TCP | MediaAgent data movement | Allow from client subnets to MediaAgent IPs only |
| 443/HTTPS | Command Center web UI | Restrict to admin subnets |

## Security Hardening Checklist

- [ ] RBAC configured — all users assigned to roles via AD groups
- [ ] No shared admin credentials
- [ ] Encryption enabled for all regulated data policies
- [ ] DDB encryption enabled
- [ ] 2FA enabled for Command Center
- [ ] CommServe management ports (8400, 8403) firewall-restricted
- [ ] CyberArk integration active for service account passwords
- [ ] Audit log forwarded to SIEM; alerts configured
- [ ] CommServe OS and SQL Server on supported, patched versions
