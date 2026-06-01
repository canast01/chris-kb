# NSX — Authentication


<div class="kb-summary">
Authentication reference covering Local Accounts, LDAP / Active Directory Authentication, NSX Role Reference, API Authentication, Multi-Factor Authentication (MFA) and 2 more sections.
</div>

## Local Accounts

NSX Manager ships with three built-in local accounts:

| Account | Role | Purpose |
|---|---|---|
| `admin` | Enterprise Admin | Full management; primary operational account |
| `audit` | Auditor (read-only) | Compliance and read-only review |
| `guestuser1` | Not used | Disabled by default |

### Password Policy

Configure from: **System → Users and Roles → User Management → Password Policy**

| Parameter | Recommended Value |
|---|---|
| Minimum password length | 20 characters |
| Maximum password lifetime | 90 days |
| Minimum uppercase letters | 1 |
| Minimum lowercase letters | 1 |
| Minimum digits | 1 |
| Minimum special characters | 1 |
| Password history | 10 |
| Maximum failed login attempts | 5 |
| Account lockout duration | 15 minutes |

Set via API:

```bash
curl -sk -u 'admin:password' \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "api_failed_auth_lockout_period": 900,
    "api_failed_auth_reset_period": 900,
    "api_max_requests": 100,
    "cli_failed_auth_lockout_period": 900,
    "cli_max_auth_failures": 5,
    "minimum_password_length": 20
  }' \
  "https://<nsx-manager>/api/v1/node/aaa/auth-policy"
```
┌──────────────────────────────────────── NSX — Authentication ─────────────────────────────────────────┐
│                                                                                                       │
│  NSX SSO via vCenter, local admin, LDAP identity source, and API token auth.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           vCenter SSO Integration            │  │             Local Admin Account             │   │
│   │             NSX uses vCenter SSO             │  │           admin user local to NSX           │   │
│   │          AD identity source in SSO           │  │            audit user: read-only            │   │
│   │        Users log into NSX UI via SSO         │  │            guestuser1/2: limited            │   │
│   │         vSphere role → NSX role map          │  │            Change admin password            │   │
│   │            MFA via SSO Radius/RSA            │  │           Disable root if possible          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SSO for UI access; API token or basic auth for automation; AD for ops.                               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              API Authentication              │  │              Security Hardening             │   │
│   │           Basic auth (admin:pass)            │  │          Password complexity policy         │   │
│   │        Bearer token via /api/session         │  │           Account lockout after 5           │   │
│   │          Principal Identity for ops          │  │             Session idle timeout            │   │
│   │          Client certificates option          │  │            Log all auth attempts            │   │
│   │          vIDM integration optional           │  │            Alert on failed logins           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NSX Manager VMs, vCenter SSO, AD/LDAP, Radius/RSA, management network                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SSO         = Single Sign-On; vCenter embedded auth used by NSX                                      │
│  Principal Identity = long-lived API credential for automation services                               │
│  Bearer token= JWT session token from /api/session/create; short-lived                                │
│  vIDM        = VMware Identity Manager; optional ext auth for NSX                                     │
│  Local admin = NSX-local admin account; break-glass if SSO fails                                      │
│  audit user  = read-only local NSX account for compliance review                                      │
│  MFA         = Multi-Factor Auth; configured in vCenter SSO policy                                    │
│  Radius      = remote auth server for MFA OTP tokens                                                  │
│  Client cert = X.509 cert used as API client auth credential                                          │
│  Password policy = NSX local: min length, complexity, rotation                                        │
│  Lockout     = account disabled after N failed login attempts                                         │
│  Session timeout = idle session expiry; configurable in NSX                                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Use LDAPS (port 636) in production. If using LDAP (port 389) with STARTTLS, set `"use_starttls": true` and provide the CA certificate.

### Test LDAP Connectivity

```bash
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"search_query": "nsxadmin", "cursor": "0"}' \
  "https://<nsx-manager>/api/v1/aaa/ldap/search"

# Expected: returns the matching user object from AD
```

### Assign Roles to LDAP Users or Groups

**System → Users and Roles → Role Assignments → Add**

Use group-based assignment — assign roles to AD security groups, not individual users. This allows role changes via AD group membership without touching NSX.

```bash
# Assign Enterprise Admin role to an AD group
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "roles": [{
      "role": "enterprise_admin"
    }],
    "name": "CN=NSX-Admins,OU=Groups,DC=corp,DC=local",
    "type": "remote_group",
    "identity_source_type": "LDAP",
    "identity_source_id": "<ldap-source-id>"
  }' \
  "https://<nsx-manager>/api/v1/aaa/role-bindings"
```

---

## NSX Role Reference

| Role | Permissions | Typical Assignee |
|---|---|---|
| `enterprise_admin` | Full read/write on all objects | NSX administrators |
| `network_engineer` | Networking read/write; no security | Network engineers |
| `security_admin` | DFW policies and groups; no infrastructure | Security team |
| `operator` | Read-only + restart services, clear stats | NOC / L1 operations |
| `auditor` | Read-only across all objects | Compliance, audit |
| `lb_admin` | Load balancer management only | Application teams |

### Principle of Least Privilege

- NOC teams: `operator` role — can view all, restart degraded services
- Network engineers: `network_engineer` — configure segments, gateways, routing
- Security team: `security_admin` — manage DFW; cannot modify underlay
- Administrators: `enterprise_admin` — limited to named individuals, not shared
- No AD accounts with `enterprise_admin` in day-to-day use; break-glass only

---

## API Authentication

NSX-T REST API supports multiple authentication methods:

### Basic Auth (Simple)

```bash
curl -sk -u 'admin:Password123!' \
  "https://nsx-manager.example.local/api/v1/cluster/status"
```

Acceptable for scripts running from a secured automation host. Use a dedicated service account, not the shared admin.

### Session-Based Auth (Preferred for Automation)

```bash
# Create session (returns Set-Cookie header)
curl -sk -u 'admin:Password123!' \
  -X POST \
  -c /tmp/nsx-session.txt \
  "https://nsx-manager.example.local/api/v1/aaa/session"

# Use session cookie for subsequent requests
curl -sk \
  -b /tmp/nsx-session.txt \
  "https://nsx-manager.example.local/api/v1/cluster/status"

# Invalidate session when done
curl -sk -u 'admin:Password123!' \
  -X DELETE \
  -b /tmp/nsx-session.txt \
  "https://nsx-manager.example.local/api/v1/aaa/session"
```

### Client Certificate Authentication (Most Secure)

Register a client certificate for automation accounts. NSX validates the certificate presented by the API client:

```bash
# Generate client key and CSR
openssl req -newkey rsa:2048 -nodes \
  -keyout nsx-automation.key \
  -out nsx-automation.csr \
  -subj "/CN=nsx-automation/O=corp"

# Submit CSR to internal CA and get certificate (nsx-automation.crt)

# Register the certificate with NSX Manager
curl -sk -u 'admin:Password123!' \
  -X POST \
  -H "Content-Type: application/json" \
  -d "{
    \"pem_encoded\": \"$(cat nsx-automation.crt | awk '{printf \"%s\\\\n\", $0}')\"
  }" \
  "https://nsx-manager.example.local/api/v1/trust-management/certificates?action=import"

# Bind the certificate to a principal identity (service account)
curl -sk -u 'admin:Password123!' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "name": "automation-account",
    "node_id": "automation-host-01",
    "role": "network_engineer",
    "certificate_id": "<cert-id-from-above>",
    "is_protected": true
  }' \
  "https://nsx-manager.example.local/api/v1/aaa/principal-identities"

# Use certificate for API calls (no password needed)
curl -sk \
  --cert nsx-automation.crt \
  --key nsx-automation.key \
  "https://nsx-manager.example.local/api/v1/cluster/status"
```

---

## Multi-Factor Authentication (MFA)

NSX-T does not natively enforce MFA at the API or CLI level. Enforce MFA at the network boundary:

- Require all NSX Manager access through a PAM (Privileged Access Management) system that enforces MFA
- Use a VPN with MFA to reach the management network where NSX Manager lives
- Configure NSX Manager firewall to only accept management connections from the PAM/jump-host subnet

For LDAP-integrated users, MFA is enforced by the AD identity provider (e.g., Azure AD Conditional Access, Duo) and applies when users authenticate through web-based flows.

---

## Audit Logging for Authentication Events

NSX Manager logs authentication events. Forward these to SIEM:

```bash
# Enable audit log export (NSX Manager CLI)
nsxcli
set service syslog exporter siem-01 level info protocol TLS server 10.0.0.100 port 6514
```

Key events to alert on:

| Log Message | Severity | SIEM Alert |
|---|---|---|
| `Login failed for user admin` (>3/min) | High | Brute force attempt |
| `User admin logged in` | Medium | Admin login (baseline, alert if unusual hours) |
| `Role assignment added` | High | Privilege escalation |
| `LDAP configuration changed` | Critical | Identity source tampering |
| `User account locked out` | Medium | Failed login threshold hit |

Audit log location on NSX Manager: `/var/log/vmware/nsx-manager/audit.log`

```bash
# View recent auth events on NSX Manager node
tail -100 /var/log/vmware/nsx-manager/audit.log | grep -i "login\|auth\|role"
```
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
