---
tags:
  - dell
  - security
description: "Authentication reference covering Authentication Methods, Local Account Management, LDAP / Active Directory Integration, REST API Token Authentication..."
---
# PowerStore — Authentication

<div class="kb-summary">
Authentication reference covering Authentication Methods, Local Account Management, LDAP / Active Directory Integration, REST API Token Authentication, Certificate-Based API Access and 4 more sections.

*Applies to: PowerStore 3.x*
</div>
![PowerStore — Authentication](../../../../../assets/storage-dell-powerstore-security-authentication.svg)

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


```text title="Expected output"
{"id":"admin","name":"Administrator","role":"administrator","is_built_in":true,"is_default_password":false,"password_expiration_days":90,"last_password_change":"2024-01-15T08:32:14Z"}
{"id":"admin","name":"Administrator","role":"administrator","is_built_in":true,"is_default_password":false}
{"id":"svc_backup","name":"Backup Service","role":"operator","is_built_in":false,"is_default_password":false}
{"id":"monitor_user","name":"Monitoring User","role":"viewer","is_built_in":false,"is_default_password":true}
{"id":"audit_admin","name":"Audit Administrator","role":"administrator","is_built_in":false,"is_default_password":false}
{"id":"svc_backup","name":"Backup Service","role":"operator","is_built_in":false,"is_default_password":false,"last_modified":"2024-01-16T10:45:22Z"}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification, or import the PowerStore certificate into your system's trusted CA store.
    **`{"error":"Invalid or expired token","error_code":"401"}`** — Regenerate the DELL-EMC-TOKEN by authenticating first with valid credentials and extract the token from the login response.
    **`{"error":"Cannot modify built-in user account","error_code":"403"}`** — Ensure the `<user-id>` is not 'admin' or another built-in account; only custom local users can be disabled via this endpoint.
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


```text title="Expected output"
{
  "id": "ldap-config-001",
  "domain_name": "corp.example.com",
  "server_address": [
    "192.168.1.10",
    "192.168.1.11"
  ],
  "protocol": "LDAPS",
  "port": 636,
  "bind_user": "CN=svc-powerstore-ldap,OU=Service Accounts,DC=corp,DC=example,DC=com",
  "user_search_path": "OU=Users,OU=Corp,DC=corp,DC=example,DC=com",
  "group_search_path": "OU=Groups,OU=Corp,DC=corp,DC=example,DC=com",
  "user_id_attribute": "sAMAccountName",
  "group_name_attribute": "cn",
  "is_active_directory": true,
  "status": "configured",
  "created_at": "2024-01-15T10:32:47Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to the curl command to skip SSL verification (already present in the example, but ensure it's not removed in production without proper CA certificate validation).
    **`{"error": "Invalid token", "code": 401}`** — Regenerate the DELL-EMC-TOKEN via the PowerStore management interface and ensure it has not expired or been revoked.
    **`{"error": "LDAP bind failed", "code": 400}`** — Verify the bind_user DN and bind_password are correct, and confirm the service account has permission to query the Active Directory domain.
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


```text title="Expected output"
{
  "id": "5f8c3a2b-1e4d-47f9-8c2a-9d7e1b5c3f2a",
  "ldap_domain_id": "3c9e2f1a-5b7d-4e8c-9a1b-2c3d4e5f6a7b",
  "group_cn": "GRP-Storage-Admins",
  "role_name": "Administrator",
  "created_at": "2024-01-15T09:23:47Z"
}
{
  "id": "6g9d4b3c-2f5e-48g0-9d3b-0e8f2c6d4g3b",
  "ldap_domain_id": "3c9e2f1a-5b7d-4e8c-9a1b-2c3d4e5f6a7b",
  "group_cn": "GRP-Storage-Operators",
  "role_name": "StorageOperator",
  "created_at": "2024-01-15T09:23:48Z"
}
{
  "id": "7h0e5c4d-3g6f-49h1-0e4c-1f9g3d7e5h4c",
  "ldap_domain_id": "3c9e2f1a-5b7d-4e8c-9a1b-2c3d4e5f6a7b",
  "group_cn": "GRP-Storage-Monitoring",
  "role_name": "Viewer",
  "created_at": "2024-01-15T09:23:49Z"
}
```

!!! warning "Common errors"
    **`{"error_code": 401, "message": "Invalid or expired token"}`** — Regenerate the DELL-EMC-TOKEN using the authentication endpoint and ensure it has not exceeded its expiration window.
    **`{"error_code": 404, "message": "LDAP domain not found"}`** — Verify the ldap_domain_id exists by listing configured LDAP domains with `GET /api/rest/ldap_domain` and use the correct domain ID.
    **`{"error_code": 400, "message": "Invalid role_name"}`** — Confirm the role_name is one of the valid PowerStore roles (Administrator, StorageOperator, Viewer, OperatorMonitor) and check for typos.
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


```text title="Expected output"
# extended LDIF
#
# LDAPv3
# base <OU=Users,OU=Corp,DC=corp,DC=example,DC=com> with scope subtree
# filter: (sAMAccountName=jsmith)
# requesting: ALL
#

# jsmith, Users, Corp, corp.example.com
dn: CN=John Smith,OU=Users,OU=Corp,DC=corp,DC=example,DC=com
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: John Smith
sAMAccountName: jsmith
userPrincipalName: jsmith@corp.example.com
mail: jsmith@corp.example.com
memberOf: CN=PowerStore-Admins,OU=Groups,OU=Corp,DC=corp,DC=example,DC=com

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

!!! warning "Common errors"
    **`ldap_sasl_bind(SIMPLE): Can't contact LDAP server (-1)`** — Verify the LDAP server IP (192.168.1.10) is reachable and port 636 is open using `telnet 192.168.1.10 636` or `nc -zv 192.168.1.10 636`.
    **`ldap_bind: Invalid credentials (49)`** — Confirm the bind DN path and password are correct; test with a known working service account credential.
    **`ldap_search_ext: No such object (32)`** — Verify the base DN path `OU=Users,OU=Corp,DC=corp,DC=example,DC=com` exists in Active Directory and matches your domain structure exactly.
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


```text title="Expected output"
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwOTMyMTYwMH0.a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "expires_in": 3600
}
[
  {
    "id": "vol-001a2b3c-4d5e-6f7g-8h9i-0j1k2l3m4n5o",
    "name": "prod-db-vol-01",
    "size": 1099511627776,
    "state": "Ready",
    "protection_policy_id": "pp-default"
  },
  {
    "id": "vol-002x9y8z-7w6v-5u4t-3s2r-1q0p9o8n7m6l",
    "name": "backup-vol-02",
    "size": 549755813888,
    "state": "Ready",
    "protection_policy_id": "pp-backup"
  }
]
(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl commands to skip certificate verification, or import the PowerStore management certificate into your CA bundle.
    **`jq: parse error: Cannot index string with string "token"`** — Verify the login credentials are correct and the API endpoint is responding with valid JSON; check the response with `curl -ks ... | cat` to inspect raw output.
    **`{"error":"Invalid or expired token"}`** — Ensure the token variable is properly set by testing `echo $TOKEN` before the GET request, and verify the token hasn't expired (default 3600 seconds).
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

```text title="Expected output"
{
  "id": "smb_server_1",
  "nas_server_id": "nas_1",
  "netbios_name": "NASSERVER01",
  "domain": "corp.example.com",
  "organizational_unit": "OU=Storage,OU=Servers,DC=corp,DC=example,DC=com",
  "domain_joined": true,
  "domain_join_status": "SUCCESS",
  "created_at": "2024-01-15T09:42:33.847Z",
  "updated_at": "2024-01-15T09:42:45.123Z",
  "admin_user": "domain-admin-account",
  "workgroup": null
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification, or import the PowerStore management certificate into your system's trusted CA store.
    **`{"error_code": "INVALID_FIELD", "message": "Invalid domain credentials"}`** — Verify the domain admin account exists, password is correct, and the account has permissions to join computers to the specified organizational unit.
    **`{"error_code": "INVALID_FIELD", "message": "NAS server not found"}`** — Confirm the `nas_server_id` value matches an existing NAS server by querying `/api/rest/nas_server` first.
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing

---

## See also

- [Powerstore — Access Control](../access-control/)
- [Powerstore — Hardening](../hardening/)
- [Powerstore — Encryption](../encryption/)
