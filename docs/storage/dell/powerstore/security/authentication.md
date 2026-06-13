---
tags:
  - dell
  - security
---
# PowerStore — Authentication


<div class="kb-summary">
Authentication reference covering Authentication Methods, Local Account Management, LDAP / Active Directory Integration, REST API Token Authentication, Certificate-Based API Access and 4 more sections.

*Applies to: PowerStore 3.x*
</div>
```text
┌────────────────────────────────── Dell PowerStore — Authentication ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        PowerStore authentication: local accounts, LDAP/AD, RADIUS, and SAML SSO options       │   │
│   │        MFA: time-based OTP or hardware token required for all privileged admin accounts       │   │
│   │         Service accounts: dedicated accounts for automation; API tokens/keys preferred        │   │
│   │       Session: idle timeout enforced; concurrent session limits for admin role accounts       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Login → authenticate LDAP/SAML/local → MFA → authorise role → session                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           T-model           │  │          Block only         │  │        iSCSI/FC/NVMe        │   │
│   │           X-model           │  │         Block + File        │  │       Unified protocol      │   │
│   │            Metro            │  │       Sync replication      │  │       Zero-RPO stretch      │   │
│   │          Protection         │  │        Snapshot/Clone       │  │       Immutable snaps       │   │
│   │             Mgmt            │  │          PSM / REST         │  │         Unified pane        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Method      │     Use case     │  Config location  │       MFA        │     Priority     │   │
│   │     LDAP/AD      │  Staff accounts  │   Auth settings   │     Required     │     Primary      │   │
│   │     SAML SSO     │    Federated     │    SSO settings   │   IdP-enforced   │    Preferred     │   │
│   │      Local       │   Break-glass    │    Local users    │     Required     │  Emergency only  │   │
│   │    API token     │    Automation    │  Service account  │   N/A (token)    │    Automation    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerStore T/X appliance · NVMe drives · SAS expansion shelves · 10/25 GbE               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerStore         = Dell mid-range NVMe storage; T-model block-only, X-model unified block+file   │
│    PowerStore Manager = browser GUI and REST API endpoint for all PowerStore operations               │
│    Volume group       = logical collection of volumes sharing snapshot and replication policies       │
│    Protection policy  = assigned to volumes; defines snapshot schedule, retention, and replication    │
│    Metro volume       = synchronously replicated volume across two sites; zero RPO active-active      │
│    Snapshot           = space-efficient point-in-time copy; crash-consistent or app-consistent        │
│    Clone              = full writable copy of a volume or file system; independent lifecycle          │
│    Applied-to         = PowerStore host mapping; volumes are applied-to a host or host group object   │
│    Capacity license   = PowerStore uses usable-capacity licensing; licensed in TiB increments         │
│    Storage container  = PowerStore X-model; unified block and file from the same storage pool         │
│    Appliance          = single PowerStore node pair (dual controllers); scalable to 4 appliances      │
│    NVMe-oF            = NVMe over Fabrics; FC-NVMe or NVMe/TCP host connectivity on PowerStore        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Authentication Methods

PowerStore Manager (the web UI) and REST API support three authentication mechanisms:

| Method | Use Case | Notes |
|---|---|---|
| Local user accounts | Break-glass admin; initial setup | Built-in; no external dependencies |
| LDAP / Active Directory | Primary authentication for all named users | Recommended for all production systems |
| REST API token | Automation and scripting | Token-based; obtained via `login_session` |

Always configure LDAP/AD as the primary authentication source. Local accounts should be retained only as a break-glass mechanism, with the password stored in a privileged access vault (CyberArk, HashiCorp Vault, Thycotic).

## Local Account Management

PowerStore ships with a default `admin` account. Change the password immediately after initial configuration.

```bash
# Change the admin password via REST API
curl -k -X PATCH "https://<mgmt-ip>/api/rest/user/local/admin" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "<current>",
    "password": "<new-password>"
  }'

# List all local user accounts
curl -k -X GET "https://<mgmt-ip>/api/rest/user/local" \
  -H "DELL-EMC-TOKEN: <token>"

# Disable a local account (other than admin)
curl -k -X PATCH "https://<mgmt-ip>/api/rest/user/local/<user-id>" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"is_built_in": false, "is_default_password": false}'
```

Local account password policy defaults:

| Parameter | Default | Recommended |
|---|---|---|
| Minimum length | 8 characters | 16 characters |
| Complexity | Enabled (upper, lower, digit, special) | Retain |
| Maximum age | None | 90 days |
| Lockout after failed attempts | 5 attempts | 5 attempts |
| Lockout duration | 30 minutes | 30 minutes |

Configure password policy: PowerStore Manager → **Settings → Security → Password Policy**.

## LDAP / Active Directory Integration

### Configuration

```bash
# Configure LDAP via REST API (Active Directory example)
curl -k -X POST "https://<mgmt-ip>/api/rest/ldap" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "domain_name": "corp.example.com",
    "server_address": ["192.168.1.10", "192.168.1.11"],
    "protocol": "LDAPS",
    "port": 636,
    "bind_user": "CN=svc-powerstore-ldap,OU=Service Accounts,DC=corp,DC=example,DC=com",
    "bind_password": "<service-account-password>",
    "user_search_path": "OU=Users,OU=Corp,DC=corp,DC=example,DC=com",
    "group_search_path": "OU=Groups,OU=Corp,DC=corp,DC=example,DC=com",
    "user_id_attribute": "sAMAccountName",
    "group_name_attribute": "cn",
    "is_active_directory": true
  }'
```

| LDAP Parameter | Recommended Setting | Notes |
|---|---|---|
| Protocol | LDAPS | Use LDAP over SSL; do not use plain LDAP in production |
| Port | 636 | Standard LDAPS port |
| Bind user | Dedicated service account | Minimum permissions: read-only user in the search paths |
| User search path | Narrowest OU containing storage admin users | Avoid searching the entire directory |
| Group search path | Narrowest OU containing storage admin groups | |

### Mapping AD Groups to PowerStore Roles

After LDAP is configured, map Active Directory security groups to PowerStore roles:

```bash
# Map an AD group to the Administrator role
curl -k -X POST "https://<mgmt-ip>/api/rest/ldap_domain_role_mapping" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ldap_domain_id": "<ldap-domain-id>",
    "group_cn": "GRP-Storage-Admins",
    "role_name": "Administrator"
  }'

# Map an AD group to the StorageOperator role
curl -k -X POST "https://<mgmt-ip>/api/rest/ldap_domain_role_mapping" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ldap_domain_id": "<ldap-domain-id>",
    "group_cn": "GRP-Storage-Operators",
    "role_name": "StorageOperator"
  }'

# Map read-only monitoring group
curl -k -X POST "https://<mgmt-ip>/api/rest/ldap_domain_role_mapping" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ldap_domain_id": "<ldap-domain-id>",
    "group_cn": "GRP-Storage-Monitoring",
    "role_name": "Viewer"
  }'
```

### Testing LDAP Configuration

Before relying on LDAP for all authentication, test with a named user:

```bash
# Test LDAP connectivity from a management host
ldapsearch -H ldaps://192.168.1.10:636 \
  -D "CN=svc-powerstore-ldap,OU=Service Accounts,DC=corp,DC=example,DC=com" \
  -w '<bind-password>' \
  -b "OU=Users,OU=Corp,DC=corp,DC=example,DC=com" \
  "(sAMAccountName=<test-username>)"

# Log in to PowerStore Manager with an AD account to confirm authentication works
# before disabling the local admin account
```

## REST API Token Authentication

The PowerStore REST API uses session-based token authentication via the `login_session` endpoint. Tokens are valid for the duration of the session or until explicitly logged out.

```bash
# Obtain a token
TOKEN=$(curl -ks -X POST "https://<mgmt-ip>/api/rest/login_session" \
  -H "Content-Type: application/json" \
  -c /tmp/pstore_cookies.txt \
  -d '{"username":"admin","password":"<password>"}' \
  | jq -r '.token')

# Use the token in subsequent calls
curl -k -X GET "https://<mgmt-ip>/api/rest/volume" \
  -H "DELL-EMC-TOKEN: ${TOKEN}"

# Log out (invalidates the token)
curl -k -X DELETE "https://<mgmt-ip>/api/rest/login_session" \
  -H "DELL-EMC-TOKEN: ${TOKEN}"
```

For automation, use a dedicated service account with the minimum required role:

| Integration | Recommended Role | Rationale |
|---|---|---|
| Veeam / PPDM / Commvault | StorageOperator | Needs snapshot create/delete; no user management |
| Ansible automation | StorageOperator | Provisioning operations; no security changes |
| Monitoring scripts (read-only) | Viewer | Read-only health and capacity checks |
| Terraform (full IaC) | Administrator | Requires create/delete on all resource types |
| SRM integration | StorageOperator | Needs to manage replication sessions |

## Certificate-Based API Access

PowerStore supports client certificate authentication for automated integrations that require certificate-based mutual TLS (mTLS). This is an alternative to username/password token exchange.

Configuration: PowerStore Manager → **Settings → Security → Certificates → Client Certificates → Import**.

## Session Management

| Parameter | Default | Recommended Configuration |
|---|---|---|
| Session idle timeout | 30 minutes | 15 minutes for privileged users |
| Maximum session duration | None | 8 hours (require re-authentication for extended sessions) |
| Concurrent sessions per user | Unlimited | Review if audit requirements mandate single-session enforcement |

Configure under PowerStore Manager → **Settings → Security → Session Management**.

## Multi-Factor Authentication

PowerStore Manager does not natively enforce MFA. To require MFA for storage administration:

1. Route all PowerStore management access through a privileged access workstation (PAW) or jump host
2. Enforce MFA on the jump host using your corporate IdP (Azure AD Conditional Access, Duo, Okta)
3. Ensure the jump host is the only network source permitted to access the PowerStore management IP (firewall rule restricting port 443 to jump host IPs)

This provides MFA coverage even though MFA is enforced at the jump host rather than on PowerStore itself.

## NAS File Authentication

NAS servers support separate authentication for file-level access (independent of array management authentication):

| Protocol | Authentication Method |
|---|---|
| SMB (Windows shares) | Active Directory domain authentication; Kerberos |
| NFS v3 | Host-based access control (IP allow/deny); UID/GID |
| NFS v4.1 | Kerberos (krb5, krb5i, krb5p) for identity and optional integrity/encryption |
| FTP | Local NAS user accounts or LDAP-mapped accounts |

For SMB with AD:
```bash
# Join the NAS server to the Active Directory domain
curl -k -X POST "https://<mgmt-ip>/api/rest/smb_server" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nas_server_id": "<nas-server-id>",
    "netbios_name": "NASSERVER01",
    "domain": "corp.example.com",
    "organizational_unit": "OU=Storage,OU=Servers,DC=corp,DC=example,DC=com",
    "administrator": "domain-admin-account",
    "password": "<domain-admin-password>"
  }'
```
---

## Related Reference

- [Standard LDAP Integration](../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
