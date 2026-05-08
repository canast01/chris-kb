# Data Domain — Access Control

## RBAC — Role-Based Access Control

Data Domain has a built-in role model. Assign the minimum required role per user or group.

| Role | Access Level | Use Case |
|---|---|---|
| `sysadmin` | Full system administration | Break-glass account only; never used for day-to-day |
| `admin` | Full configuration access except security settings | Primary operational admin role |
| `backup-operator` | Read access + DD Boost storage unit access | Service account for backup software (Veeam, NBU, CommVault) |
| `user` | Read-only | Monitoring and reporting access |
| `security-officer` | Manages retention lock and compliance settings | Required for compliance mode operations |
| `auditor` | Read-only access to audit logs | Compliance review; SOC/audit team |

```bash
# Create a user and assign a role
user add <username> role backup-operator

# Assign LDAP group to a role
authentication roles assign role backup-operator group <ldap-group-name>

# List current users and roles
user show
```

## Retention Lock

Retention lock prevents modification or deletion of files for a configured period. It is an immutability layer on top of standard DDFS.

| Mode | Delete by Admin? | Use Case |
|---|---|---|
| Governance | Yes, with `security-officer` role | Internal retention policy enforcement |
| Compliance | No — files cannot be deleted during the retention period | SEC 17a-4, HIPAA, GDPR, PCI-DSS requirements |

```bash
# Enable governance retention lock
mtree retention-lock enable mode governance mtree /data/col1/<mtree-name>

# Enable compliance retention lock (irreversible for the MTree's life)
mtree retention-lock enable mode compliance mtree /data/col1/<mtree-name>

# Set retention period limits
mtree retention-lock set min-retention-period 30days mtree /data/col1/<mtree-name>
mtree retention-lock set max-retention-period 7years mtree /data/col1/<mtree-name>

# Show retention lock status on an MTree
mtree show retention-lock /data/col1/<mtree-name>
```

## Audit Logging

All administrative actions are logged to the DD audit log.

```bash
# View audit log
log view audit

# Forward audit and system logs to a syslog server
log host add <syslog-server-ip>
log host show

# Confirm syslog is working
log test <syslog-server-ip>
```

Log entries include: user logins, configuration changes, retention lock events, filesystem operations, and administrative commands. The audit log should be forwarded to a SIEM that retains logs for at least 12 months.

## Network Access Control

- Isolate DD management traffic on a dedicated management VLAN
- Restrict SSH and HTTPS access to the DD to admin jump hosts or bastion servers only
- NFS and CIFS export access should be restricted to the backup server IP addresses — not open to all hosts
- DD Boost traffic should use a dedicated backup network, not the production LAN
- Do not expose the DD management interface to the internet under any circumstances

## Security Incident Response

| Event | Action |
|---|---|
| Suspected unauthorised login | `log view audit` — review login events; disable the account immediately; change all shared credentials |
| Ransomware attempt on backup data | Check retention lock status on affected MTree — compliance-mode locked files cannot be encrypted by ransomware; isolate network access; open Dell support case |
| DD Boost credential compromise | Immediately change the DD Boost user password; update backup software; review `ddboost show clients` for unexpected clients |
| Disk failure (potential data exposure) | Dell replaces failed disks; D@RE ensures data on failed disks is unreadable without the encryption key |
