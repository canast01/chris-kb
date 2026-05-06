# NetBackup Security

## NetBackup Access Control (NBAC)

NBAC provides role-based access using OS groups or LDAP/AD integration:

```bash
# Enable NBAC (requires restart of NetBackup services)
nbac_admin -enable

# List current NBAC users and roles
nbac_admin -list_users
nbac_admin -list_roles
```

Built-in roles:
| Role | Capabilities |
|---|---|
| NBU_Admin | Full NetBackup administration |
| NBU_Operator | Start/stop jobs; no policy configuration |
| NBU_Vault_Operator | Vault and tape management |
| NBU_User | Restore own data (self-service) |
| NBU_SAN_Admin | SAN client and storage configuration |

Map AD groups to NBAC roles:
```bash
nbac_admin -add_user -user "domain\\nbu_admins" -role NBU_Admin
nbac_admin -add_user -user "domain\\nbu_operators" -role NBU_Operator
```

## NetBackup Certificate Authority

All clients authenticate to the master server via certificates issued by the NetBackup CA:

```bash
# List all certificates in the NetBackup CA
nbcertcmd -listCACertDetails

# Re-issue client certificate (if expired or lost)
nbcertcmd -getCertificate -server <master_server> -force

# Check certificate expiry across all clients
nbcertcmd -listCerts | grep -E "Host|Expiry"
```

Certificates expire by default after 5 years — set up monitoring to alert 90 days before expiry.

## Backup Data Encryption

Enable encryption at the policy level:

```bash
# Create an encryption key file
nbkm -createKey -keyGroupName backupkeys

# Enable encryption in policy (Admin Console):
# Policy Attributes → Use Encryption → select key group
```

| Encryption Mode | Location | CPU Impact |
|---|---|---|
| Client-side | Client host | High (on production server) |
| Media server-side | Media server | Low (off client) |
| Storage-level | Array/appliance | None (hardware) |

Mandate client-side or media-server-side encryption for all policies covering PII or regulated data.

## Audit Logging

```bash
# Enable audit logging
nbauditreport -enable

# View audit report
nbauditreport -reporttype all -startdate <date> -enddate <date>

# Output to file
nbauditreport -reporttype all -startdate 2026-01-01 > /tmp/nbu_audit.txt
```

Forward to SIEM: configure `nblog` syslog output or use a log shipper agent pointing to `/usr/openv/netbackup/logs/audit/`.

## Hardening Checklist

- [ ] NBAC enabled; all access via AD group mappings
- [ ] NetBackup CA deployed; all client certificates valid
- [ ] Encryption enabled for policies covering regulated data
- [ ] Master server firewall: only ports 1556, 13724, 13782 open from authorised subnets
- [ ] PBX service disabled on client hosts where not required
- [ ] nbauditreport reviewed weekly; forwarded to SIEM
- [ ] CyberArk AAM integration for all service account credentials
- [ ] OpsCenter access restricted to backup admin AD group
- [ ] SSH to master server limited to management jump hosts only

## Firewall Ports

| Source | Destination | Port | Purpose |
|---|---|---|---|
| Master | Media, Clients | 13724, 13782 | bpcd, bpbrm |
| Clients | Master | 1556 | vnetd |
| OpsCenter | Master | 1556 | Reporting |
| Admin workstation | Admin Console | 1556 | Management |
