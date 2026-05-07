# RecoverPoint Security
## Role-Based Access Control

RecoverPoint has three built-in roles. Use individual named accounts, never shared credentials:

| Role | Capabilities |
|---|---|
| Administrator | Full configuration, failover, and system management |
| Security Officer | User management, audit log access — cannot change replication config |
| Monitor | Read-only; can view CG status, RPA health, and lag metrics |

Create accounts via RecoverPoint Management Console → System Settings → Users:

```bash
# Via RecoverPoint CLI
add_user -u svc_monitoring -r monitor -p '<password>'
add_user -u svc_srm_integration -r admin -p '<password>'
```

## API Token Management

For automation accounts using the REST API, use token-based auth rather than username/password in scripts:

```bash
# Create session token
curl -k -u admin:password -X POST https://<rpa-ip>/rest/users/sessions
# Response includes: {"sessionId": "<token>"}

# Use token in subsequent calls
curl -k -H "Authorization: Bearer <token>" https://<rpa-ip>/rest/consistency_groups
```

- Store API tokens in CyberArk or HashiCorp Vault — never hard-code in scripts
- Rotate tokens quarterly or on personnel change
- Scope dedicated API accounts to the minimum required role (Monitor for observability, Admin only for failover automation)

## Journal Encryption

Journal volumes hold continuous copies of production data — protect them:

- At-rest encryption is managed at the storage array level (not in RecoverPoint itself)
- Ensure journal volume LUNs are on encrypted arrays or datastores
- For PowerMax: verify journal vols are in an encrypted Storage Group
- For vSphere (RP4VM): place journal VMDKs on vSAN encrypted datastore or array-encrypted NFS

## Network Segmentation

| Traffic Type | Recommended Isolation |
|---|---|
| Production-to-replica replication | Dedicated WAN circuit or MPLS path; no internet traversal |
| RPA management | Dedicated management VLAN, accessible only from management jump hosts |
| RPA-to-array communication | SAN fabric or dedicated NFS management network |
| SRM ↔ RecoverPoint SRA | Management network; port 7225 |

## SSH Hardening

```bash
# Verify root login is disabled
grep PermitRootLogin /etc/ssh/sshd_config    # Should show: no

# Restrict SSH to management jump hosts only (RecoverPoint CLI)
set_system_ssh_restrictions -allow <jump_host_ip>/32
```

- SSH idle session timeout: 10 minutes (TMOUT=600 in /etc/profile)
- SSH host keys: document fingerprints in the CMDB entry for each RPA node

## Certificate Management

Replace the default self-signed management certificate:

1. Generate CSR on each RPA node
2. Sign with internal CA
3. Import via Management Console → System Settings → TLS Certificates

Track certificate expiry — RecoverPoint management console becomes inaccessible if the cert expires.

## Audit Log

RecoverPoint maintains a system audit log of all user actions:

```bash
# View audit log (RecoverPoint CLI)
get_audit_log -last 100
get_audit_log -from_date "2026-01-01" -to_date "2026-01-31"
```

Forward to SIEM via syslog: Management Console → System Settings → Syslog Notifications. Alert on:
- Any admin account login outside business hours
- `enable_image_access` events (indicates failover test or actual DR)
- User account creation or role changes
