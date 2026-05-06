# Data Domain — Security

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

## Hardening Checklist

- [ ] Change the default `sysadmin` password immediately on commissioning
- [ ] Disable SSH root login: `adminaccess set ssh root disabled`
- [ ] Restrict management access to specific subnets: `adminaccess set allowed-hosts <subnet>`
- [ ] Enable HTTPS only (disable HTTP): `adminaccess set http-auth disabled`
- [ ] Configure LDAP authentication — do not rely solely on local accounts for day-to-day access
- [ ] Set a login banner: `adminaccess set login-banner "Authorised access only"`
- [ ] Set session timeout: `adminaccess set idle-timeout 15`
- [ ] Disable unused protocols (VTL, NFS, CIFS) if not in use on this system
- [ ] Restrict DD Boost client access by IP if feasible: restrict in the backup software and via network ACL
- [ ] Enable syslog forwarding to the central log collector
- [ ] Enable AutoSupport but verify no sensitive data is included in bundles

## Encryption at Rest (D@RE)

Data Domain supports software-based encryption of all on-disk data.

```bash
# Check current encryption status
encryption status

# Enable encryption (must be done before data is written — cannot encrypt retroactively)
encryption enable

# Configure key management — DDOS supports:
#   - Internal key manager (built-in, no external dependency)
#   - RSA DPM (Dell Key Management)
#   - KMIP-compatible external key managers (Thales, Vormetric, etc.)

# Set key manager to internal (default for standalone deployments)
encryption change-key-manager internal

# View current key manager configuration
encryption show config
```

**Important:** Enabling encryption after data is already written requires a full filesystem rebuild. Always enable D@RE at initial commissioning before writing any backup data.

DDOS D@RE is FIPS 140-2 certified (AES-256 in CBC mode).

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

## LDAP and Authentication Security

```bash
# Verify LDAP status and connectivity
authentication ldap status

# Disable local `sysadmin` login if LDAP is fully operational
# (Keep break-glass credentials documented in a secure vault)
adminaccess set admin-auth-method ldap

# Force all management access through LDAP groups
authentication roles assign role admin group <ad-group-storage-admins>
```

## Network Security

- Isolate DD management traffic on a dedicated management VLAN
- Restrict SSH and HTTPS access to the DD to admin jump hosts or bastion servers only
- NFS and CIFS export access should be restricted to the backup server IP addresses — not open to all hosts
- DD Boost traffic should use a dedicated backup network, not the production LAN
- Do not expose the DD management interface to the internet under any circumstances

## FIPS Compliance

DDOS is FIPS 140-2 validated for the D@RE encryption module. To confirm:

```bash
encryption status  # look for "FIPS Mode: Enabled" in the output
system show        # confirm DDOS version — cross-reference with NIST CMVP certificate
```

## Security Incident Response

| Event | Action |
|---|---|
| Suspected unauthorised login | `log view audit` — review login events; disable the account immediately; change all shared credentials |
| Ransomware attempt on backup data | Check retention lock status on affected MTree — compliance-mode locked files cannot be encrypted by ransomware; isolate network access; open Dell support case |
| DD Boost credential compromise | Immediately change the DD Boost user password; update backup software; review `ddboost show clients` for unexpected clients |
| Disk failure (potential data exposure) | Dell replaces failed disks; D@RE ensures data on failed disks is unreadable without the encryption key |
