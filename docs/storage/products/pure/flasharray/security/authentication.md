---
tags:
  - pure
  - security
description: "Authentication reference covering Authentication Architecture, Local Accounts, Active Directory (AD), LDAP (Non-AD), SAML SSO and 4 more sections."
---
# FlashArray — Authentication

<div class="kb-summary">
Authentication reference covering Authentication Architecture, Local Accounts, Active Directory (AD), LDAP (Non-AD), SAML SSO and 4 more sections.

*Applies to: FlashArray Purity 6.x*
</div>
![FlashArray — Authentication](../../../../../assets/storage-pure-flasharray-security-authentication.svg)

![FlashArray — Authentication — Diagram](../../../../../assets/storage-pure-flasharray-security-authentication-diagram.svg)

FlashArray supports multiple identity sources for admin authentication: local accounts, Active Directory (AD), LDAP, and SAML SSO. All authentication is role-based — every admin account is bound to one of the four built-in Purity roles. API tokens are the recommended credential type for automation and monitoring integrations.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Authentication Architecture

![Authentication Architecture](../../../../../assets/storage-pure-flasharray-security-authentication-mermaid-svg.svg)

## Local Accounts

Local accounts are stored on the array itself and are independent of any directory service. Use them for break-glass access and initial setup. Minimise the number of local accounts in production — prefer AD or LDAP for human admin access.

```bash
# Create a local admin account with a specific role
pureadmin create --role storage_admin jsmith

# Set the account password (interactive prompt)
pureadmin setattr jsmith --password

# List all admin accounts and their roles
pureadmin list

# List accounts with lockout status
pureadmin list --lockout

# Lock an account (temporary lockout)
pureadmin reset jsmith --lockout

# Unlock a locked account
pureadmin refresh --clear jsmith

# Change a user's role
pureadmin setattr jsmith --role readonly

# Delete a local account
pureadmin delete jsmith
```


```text title="Expected output"
Admin account jsmith created successfully with role storage_admin
Password set for admin account jsmith
Name                Role              Type
jsmith              storage_admin     local
admin               system_admin      local
readonly_user       readonly          local
monitor_account     monitor           local

Name                Lockout Status    Locked Since
jsmith              unlocked          —
admin               unlocked          —
readonly_user       unlocked          —
monitor_account     locked            2024-01-15 14:32:18 UTC

Admin account jsmith locked successfully
Admin account jsmith unlocked successfully
Role for admin account jsmith changed to readonly
Admin account jsmith deleted successfully
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Admin account 'jsmith' already exists` | Use `pureadmin delete jsmith` first, or choose a different username. |
    | `Error: Invalid role 'readonly'. Valid roles are: system_admin, storage_admin, monitor, readonly` | Correct the role name in the `--role` parameter to match one of the valid options. |
    | `Error: Cannot delete system_admin account 'admin'` | Only local admin accounts can be deleted; the default system_admin account is protected. |
**Default `pureuser` account:**

The factory default local admin account is `pureuser` with a default password printed on the array's label. It has `array_admin` privileges. After configuring AD/LDAP authentication and validating that at least two AD accounts can log in successfully:

1. Change the `pureuser` password to a strong randomly-generated credential
2. Store it in the organisation's PAM vault (CyberArk, HashiCorp Vault, etc.) as break-glass access
3. Restrict who knows the password — it should be emergency-only

Do not delete `pureuser` — it is the only guaranteed fallback if directory service integration fails.

---

## Active Directory (AD)

AD integration allows domain accounts to log into the array using their existing AD credentials, with role assignment driven by AD group membership.

### Configuration

```bash
# Join the array to Active Directory
puredirectoryservice setattr \
    --base-dn "DC=example,DC=com" \
    --bind-user "svc-pure-bind" \
    --bind-password "<bind_password>" \
    --domain "example.com" \
    --uri "ldaps://dc01.example.com"

# Verify the directory service configuration
pureds list

# Test AD connectivity and bind credentials
pureds check
```


```text title="Expected output"
Directory service configuration updated successfully.
Base DN: DC=example,DC=com
Domain: example.com
URI: ldaps://dc01.example.com
Bind user: svc-pure-bind

Name                  Enabled  Type      URI                        Base DN
directory-service     true     LDAP      ldaps://dc01.example.com   DC=example,DC=com

Checking directory service connectivity...
✓ LDAP server reachable at ldaps://dc01.example.com:636
✓ Bind credentials validated
✓ Base DN accessible
Directory service check passed
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unable to connect to ldaps://dc01.example.com:636` | Verify the DC hostname is resolvable and the LDAP port is open in the firewall. |
    | `Error: Invalid bind credentials for user svc-pure-bind` | Confirm the bind user exists in Active Directory and the password is correct and not expired. |
    | `Error: Base DN "DC=example,DC=com" not found` | Ensure the Base DN matches your Active Directory forest structure (check with `dsquery` or ADSI Edit on a domain controller). |
### Group-to-Role Mapping

Create AD security groups that correspond to Purity roles, then map them:

| AD Group (example) | Purity Role | Who |
|---|---|---|
| `CN=pure-array-admins,OU=Groups,DC=example,DC=com` | `array_admin` | Storage team leads; break-glass admins |
| `CN=pure-storage-admins,OU=Groups,DC=example,DC=com` | `storage_admin` | Day-to-day provisioning engineers |
| `CN=pure-ops-admins,OU=Groups,DC=example,DC=com` | `ops_admin` | Operations and on-call engineers |
| `CN=pure-readonly,OU=Groups,DC=example,DC=com` | `readonly` | Monitoring; application teams; audit accounts |

```bash
# Map an AD group to a Purity role
pureadmin setattr --role array_admin \
    --group "CN=pure-array-admins,OU=Groups,DC=example,DC=com"

pureadmin setattr --role storage_admin \
    --group "CN=pure-storage-admins,OU=Groups,DC=example,DC=com"

pureadmin setattr --role ops_admin \
    --group "CN=pure-ops-admins,OU=Groups,DC=example,DC=com"

pureadmin setattr --role readonly \
    --group "CN=pure-readonly,OU=Groups,DC=example,DC=com"

# Verify the group mappings are active
pureadmin list
```


```text title="Expected output"
Setting role array_admin for group CN=pure-array-admins,OU=Groups,DC=example,DC=com
Setting role storage_admin for group CN=pure-storage-admins,OU=Groups,DC=example,DC=com
Setting role ops_admin for group CN=pure-ops-admins,OU=Groups,DC=example,DC=com
Setting role readonly for group CN=pure-readonly,OU=Groups,DC=example,DC=com

Name                                              Role              Type
CN=pure-array-admins,OU=Groups,DC=example,DC=com array_admin       group
CN=pure-storage-admins,OU=Groups,DC=example,DC=com storage_admin    group
CN=pure-ops-admins,OU=Groups,DC=example,DC=com   ops_admin         group
CN=pure-readonly,OU=Groups,DC=example,DC=com     readonly          group
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: LDAP group not found` | Verify the AD group DN is correct and LDAP/AD is configured and reachable on the array. |
    | `Error: Invalid role name` | Use only valid Purity roles (array_admin, storage_admin, ops_admin, readonly) in the --role parameter. |
    | `Error: User does not have permission to set admin attributes` | Run the command as a user with array_admin privileges or via SSH key authentication with sufficient permissions. |
### Validation Steps

Before removing or disabling local accounts after AD integration:

1. Log out of the current session
2. Log in with a domain account that is a member of a mapped group
3. Verify the role is correctly applied: `pureadmin list` should show the domain account and its role
4. Test login from a second domain account in a different role group
5. Confirm break-glass `pureuser` credentials are vaulted, then proceed to restrict shared local accounts

---

## LDAP (Non-AD)

For environments using OpenLDAP, Red Hat Directory Server, or similar LDAP providers:

```bash
# Configure LDAP directory service
puredirectoryservice setattr \
    --base-dn "dc=example,dc=com" \
    --bind-user "cn=svc-pure,ou=service-accounts,dc=example,dc=com" \
    --bind-password "<password>" \
    --uri "ldap://ldap01.example.com:389"

# For LDAP over TLS (recommended)
puredirectoryservice setattr \
    --uri "ldaps://ldap01.example.com:636"

# Verify
pureds list
pureds check
```


```text title="Expected output"
Setting directory service attributes...
Directory service configured successfully.

Setting directory service attributes...
Directory service configured successfully.

Name: example.com
URI: ldaps://ldap01.example.com:636
Base DN: dc=example,dc=com
Bind User: cn=svc-pure,ou=service-accounts,dc=example,dc=com
Status: configured

Checking directory service connectivity...
Connection Status: OK
Bind Status: OK
Search Base Status: OK
Response Time: 42ms
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Connection refused (111)` | Verify the LDAP server is running and accessible on the specified hostname and port, and check firewall rules between the array and LDAP server. |
    | `Error: Invalid bind credentials` | Confirm the bind-user DN and password are correct and that the service account has not been locked or expired in the directory. |
    | `Error: TLS certificate verification failed` | Import the LDAP server's CA certificate to the array's trust store or disable certificate verification if using self-signed certificates in a test environment. |
**LDAP attribute mapping considerations:**

Purity uses the `memberOf` attribute (or equivalent) to determine group membership for role assignment. Verify that your LDAP directory populates `memberOf` on user objects, or configure the appropriate group attribute mapping. Consult the Purity//FA Administration Guide for the specific attribute names if your LDAP schema differs from the default.

---

## SAML SSO

SAML 2.0 SSO allows admin logins to be federated through an enterprise Identity Provider (IdP) such as Okta, Azure AD (Entra ID), or ADFS. SAML support requires Purity//FA 6.0 or later.

### Overview

In SAML terminology, FlashArray acts as the **Service Provider (SP)** — it redirects authentication requests to the IdP and accepts SAML assertions in return. The IdP authenticates the user (including enforcing MFA if configured) and returns a signed assertion specifying the user's identity and group memberships. Purity maps those group memberships to roles using the same AD group-to-role mapping as described above.

### Configuration Steps

1. **Export the FlashArray SP metadata** from the Purity GUI:
   - Navigate to `Settings > Access > Single Sign-On`
   - Download the SP metadata XML file

2. **Register FlashArray as an application in your IdP:**
   - In Okta: create a new SAML 2.0 application; upload or paste the SP metadata
   - In Azure AD: create an enterprise application; configure SAML SSO with the FlashArray metadata
   - In ADFS: add a Relying Party Trust using the SP metadata

3. **Configure the IdP to pass group membership claims** in the SAML assertion — this is what drives role assignment in Purity

4. **Import IdP metadata into Purity:**
   ```bash
   # Configure SAML with IdP metadata URL
   puredirectoryservice saml setattr \
       --idp-metadata-url "https://idp.example.com/metadata"
   
   # Or import from a local file
   puredirectoryservice saml setattr \
       --idp-metadata-file /tmp/idp_metadata.xml
   
   # Enable SSO
   pureadmin global enable --single-sign-on
   ```

5. **Validate SSO login** before disabling local accounts — log out and log back in using the IdP-authenticated path from the Purity GUI

### SAML Fallback

If SAML is misconfigured or the IdP is unavailable, local account login remains functional. Always maintain a vaulted `pureuser` break-glass credential for this scenario.

---

## API Token Authentication

API tokens are the recommended authentication method for automation, monitoring integrations, scripts, and service accounts. Tokens are long-lived credentials tied to a specific admin account; they bypass the interactive login flow and do not require a username/password exchange.

```bash
# Create a service account and generate an API token
pureadmin create --role readonly svc-monitoring
pureadmin apitoken create svc-monitoring
# Save the displayed token securely — it cannot be retrieved again after creation

# Create a service account with a storage_admin role for provisioning automation
pureadmin create --role storage_admin svc-terraform
pureadmin apitoken create svc-terraform

# List all accounts and their API token status
pureadmin list --api-token

# Expose (display) an existing token — requires array_admin privilege
pureadmin list --api-token --expose

# Delete an API token (disables API access for the account without deleting the account)
pureadmin delete svc-monitoring --api-token

# Delete the account entirely
pureadmin delete svc-old-automation
```


```text title="Expected output"
Account svc-monitoring created with role readonly
API token created for svc-monitoring: T-5a8f9c2e1b4d7f6a9e3c8b1d4f7a9e2c
Account svc-terraform created with role storage_admin
API token created for svc-terraform: T-2f7a9e3c8b1d4f7a9e2c5a8f9c2e1b4d

Name                 Role              API Token Status
svc-monitoring       readonly          active
svc-terraform        storage_admin     active
pureuser_local       array_admin       active

Name                 Role              API Token
svc-monitoring       readonly          T-5a8f9c2e1b4d7f6a9e3c8b1d4f7a9e2c
svc-terraform        storage_admin     T-2f7a9e3c8b1d4f7a9e2c5a8f9c2e1b4d
pureuser_local       array_admin       T-8b1d4f7a9e2c5a8f9c2e1b4d4f7a9e3c

API token deleted for account svc-monitoring
Account svc-old-automation deleted
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Account svc-monitoring already exists` | Check if the account exists first with `pureadmin list` or use a different service account name. |
    | `Error: Insufficient privileges to expose API tokens` | Ensure your current user has array_admin role; use `pureadmin list --self` to verify your permissions. |
    | `Error: Account svc-old-automation not found` | Verify the account name exists with `pureadmin list` before attempting deletion. |
**Using a token for REST API access:**

```bash
# Authenticate using an API token header (no session cookie required)
curl -sk \
    -H "x-auth-token: <api_token>" \
    "https://<array_ip>/api/2.x/arrays" | jq .

# Or obtain a session token via login endpoint
curl -sk -X POST \
    -H "api-token: <api_token>" \
    "https://<array_ip>/api/2.x/login" \
    -c /tmp/fa_session.txt

curl -sk \
    -b /tmp/fa_session.txt \
    "https://<array_ip>/api/2.x/volumes" | jq .
```


```text title="Expected output"
{
  "items": [
    {
      "id": "0b6c1234-5678-90ab-cdef-1234567890ab",
      "name": "flasharray-prod-01",
      "version": "6.4.2",
      "revision": "202401.1",
      "status": "healthy",
      "capacity": 107374182400,
      "space": {
        "total_physical": 53687091200,
        "total_provisioned": 32212254720
      }
    }
  ],
  "continuation_token": null
}
# Session login successful
# Set-Cookie: session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
{
  "items": [
    {
      "id": "vol-8f2a9c1d",
      "name": "prod-db-vol-01",
      "size": 1099511627776,
      "provisioned": 1099511627776,
      "serial": "ABC123DEF456"
    },
    {
      "id": "vol-7e1b8d2c",
      "name": "prod-db-vol-02",
      "size": 2199023255552,
      "provisioned": 2199023255552,
      "serial": "ABC123DEF457"
    }
  ],
  "continuation_token": null
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip SSL verification, or import the array's CA certificate into your system trust store. |
    | `{"error_code":"401000","message":"Invalid API token"}` | Verify the API token is correct and has not expired; regenerate it in the Pure1 management interface if needed. |
    | `curl: (6) Could not resolve host` | Confirm the array IP address is correct and reachable from your network; check DNS resolution or use the FQDN instead. |
**Token security guidelines:**

- Store all API tokens in a secrets manager (HashiCorp Vault, AWS Secrets Manager, CyberArk) — never in plaintext config files or environment variables in CI systems
- Create one token per integration/tool — do not share tokens between multiple automation systems
- Rotate tokens at least annually; rotate immediately if a system is decommissioned or a credentials leak is suspected
- Assign the minimum necessary role — use `readonly` for monitoring, `storage_admin` for provisioning, and `array_admin` only if account management is required
- Audit active API tokens quarterly: `pureadmin list --api-token`

---

## Session and Password Policies

Global login policies apply to all local and directory-service accounts.

```bash
# Show global admin settings
pureadmin global list

# Show lockout policy
pureadmin global list --lockout

# Set maximum failed login attempts before lockout
pureadmin global setattr --max-login-attempts 5

# Set lockout duration (e.g., 30 minutes)
pureadmin global setattr --lockout-duration 30m

# Set minimum password length for local accounts
pureadmin global setattr --min-password-length 16

# Set CLI/GUI session idle timeout (minutes)
purearray setattr --idle-timeout 15
```


```text title="Expected output"
Global Admin Settings:
  max_login_attempts: 3
  lockout_duration: 15m
  min_password_length: 12
  session_idle_timeout: 20
  password_expiration_days: 90

Lockout Policy:
  enabled: true
  max_attempts: 3
  lockout_duration: 15m
  attempt_reset_interval: 1h

(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Invalid command 'purearray setattr'. Did you mean 'pureadmin global setattr'?` | Replace `purearray setattr` with `pureadmin global setattr --idle-timeout 15` to use the correct command syntax. |
    | `Error: lockout-duration must be in format: <number>[s|m|h|d]. Got: 30m` | Ensure the duration format is valid; use lowercase units like `30m` for 30 minutes or `1h` for 1 hour. |
    | `Error: max-login-attempts must be between 1 and 10. Got: 5` | Verify the value is within the supported range; common values are 3–5 attempts before lockout. |
**Recommended policy settings:**

| Setting | Recommended Value | Rationale |
|---|---|---|
| Max login attempts | 5 | Prevents brute-force without locking out accidental mistypers |
| Lockout duration | 30 minutes | Sufficient deterrent; short enough to avoid support burden |
| Minimum password length | 16 characters | Aligns with NIST SP 800-63B guidance |
| Session idle timeout | 15 minutes | Limits exposure from unattended sessions |

---

## Audit Logging

Purity logs all authentication events and administrative actions. Logs are stored locally and should be forwarded to an external syslog/SIEM immediately — locally stored logs can potentially be altered by a compromised `array_admin` account.

**What is logged:**

- All successful and failed login attempts (CLI, GUI, REST API)
- All configuration changes with the account name, timestamp, and command
- All data operations: volume create/delete/connect, snapshot create/delete, replication changes
- API token creation and deletion events
- SafeMode-related operations

```bash
# View the audit log on the array
pureaudit list

# Filter by user
pureaudit list --filter 'user = "jsmith"'

# Filter by command
pureaudit list --filter 'command="purevol"'

# Filter for volume deletion events
pureaudit list --filter 'command="purevol" and subcommand="destroy"'

# Show last 20 entries
pureaudit list --limit 20 --sort time-

# Configure syslog forwarding (UDP — not recommended for production)
puresyslog create --uri udp://<syslog_ip>:514 siem-syslog

# Configure syslog forwarding with TLS (recommended)
puresyslog create --uri tls://<syslog_ip>:6514 siem-syslog-tls

# List syslog destinations
puresyslog list
```


```text title="Expected output"
ID                                   USER     COMMAND  SUBCOMMAND  TIMESTAMP                 DETAILS
550e8400-e29b-41d4-a716-446655440000 admin    system   login       2024-01-15T09:23:47Z      SSH login from 192.168.1.50
550e8400-e29b-41d4-a716-446655440001 jsmith   purevol  create      2024-01-15T10:15:22Z      Volume 'prod-db-01' created
550e8400-e29b-41d4-a716-446655440002 jsmith   purevol  modify      2024-01-15T10:18:45Z      Volume size increased to 500GB
550e8400-e29b-41d4-a716-446655440003 jsmith   purevol  destroy     2024-01-15T11:02:33Z      Volume 'test-vol-backup' deleted
550e8400-e29b-41d4-a716-446655440004 mchen    purehost add         2024-01-15T11:45:12Z      Host 'web-server-03' added

ID                                   USER     COMMAND  SUBCOMMAND  TIMESTAMP                 DETAILS
550e8400-e29b-41d4-a716-446655440001 jsmith   purevol  create      2024-01-15T10:15:22Z      Volume 'prod-db-01' created
550e8400-e29b-41d4-a716-446655440002 jsmith   purevol  modify      2024-01-15T10:18:45Z      Volume size increased to 500GB
550e8400-e29b-41d4-a716-446655440003 jsmith   purevol  destroy     2024-01-15T11:02:33Z      Volume 'test-vol-backup' deleted

ID                                   USER     COMMAND  SUBCOMMAND  TIMESTAMP                 DETAILS
550e8400-e29b-41d4-a716-446655440001 jsmith   purevol  create      2024-01-15T10:15:22Z      Volume 'prod-db-01' created
550e8400-e29b-41d4-a716-446655440002 jsmith   purevol  modify      2024-01-15T10:18:45Z      Volume size increased to 500GB
550e8400-e29b-41d4-a716-446655440003 jsmith   purevol  destroy     2024-01-15T11:02:33Z      Volume 'test-vol-backup' deleted

ID                                   USER     COMMAND  SUBCOMMAND  TIMESTAMP                 DETAILS
550e8400-e29b-41d4-a716-446655440003 jsmith   purevol  destroy     2024-01-15T11:02:33Z      Volume 'test-vol-backup' deleted

ID                                   USER     COMMAND  SUBCOMMAND  TIMESTAMP                 DETAILS
550e8400-e29b-41d4-a716-446655440004 mchen    purehost add         2024-01-15T11:45:12Z
```
**SIEM integration note:** When forwarding to a SIEM, use TLS syslog (`tls://`) to protect log integrity in transit. Configure the SIEM to alert on repeated failed login attempts, API token creation by non-standard accounts, and SafeMode-related audit events.
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements

---

## See also

- [FlashArray — Access Control](../access-control/)
- [FlashArray — Hardening](../hardening/)
- [FlashArray — Encryption](../encryption/)
