---
tags:
  - pure
  - security
---
# FlashBlade — Authentication


<div class="kb-summary">
Authentication reference covering Authentication Mechanisms Summary, Local Account Management, Active Directory Integration, LDAP Integration (Non-AD), SAML SSO Configuration and 3 more sections.
</div>
```text
┌────────────────────────────────── Pure FlashBlade — Authentication ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        FlashBlade authentication: local accounts, LDAP/AD, RADIUS, and SAML SSO options       │   │
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
│   │            Blades           │  │           NVMe+CPU          │  │         Parallel I/O        │   │
│   │             File            │  │           NFS/SMB           │  │        Scale-out NAS        │   │
│   │            Object           │  │           S3/Swift          │  │         Bucket store        │   │
│   │         Replication         │  │            Async            │  │          DR/backup          │   │
│   │           SafeMode          │  │         Locked snaps        │  │      Ransomware resist      │   │
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
│    Physical: FlashBlade//S or //E chassis · storage blades · 100 GbE network · Pure1 SaaS             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FlashBlade         = Pure massively parallel all-flash NAS and object platform; single namespace   │
│    Blade              = individual storage module in FlashBlade chassis; NVMe and CPU per blade       │
│    File system        = FlashBlade NFS/SMB export namespace; up to 4 PiB per file system              │
│    Object store       = S3-compatible bucket store on FlashBlade; versioning and lifecycle rules      │
│    purefb CLI         = REST CLI client for FlashBlade: purefb fs list, purefb array show commands    │
│    Replication        = async file or object replication between FlashBlade systems for DR            │
│    SafeMode           = admin-locked snapshots; protected from deletion even by local array admin     │
│    S3 multitenancy    = per-bucket policy and IAM-style access control for object storage             │
│    NFS Kerberos       = FlashBlade NFS supports krb5, krb5i, and krb5p security flavours              │
│    SMB multichannel   = FlashBlade uses SMB multichannel for improved Windows client performance      │
│    Inline compression = always-on data reduction; typically 2-10x for unstructured data               │
│    ActiveScale        = enterprise geo-distribution and erasure coding for large object workloads     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
FlashBlade Authentication — Data vs Management Plane
  Management plane (GUI / API / CLI):
    Browser ──► SAML SSO (IdP) ──► MFA ──► Purity//FB RBAC
    Script  ──► API token ──────────────► Purity//FB RBAC

  Data plane:
    NFS clients ──► Kerberos (AD) or AUTH_SYS (UID/GID)
    SMB clients ──► Active Directory (Kerberos / NTLM)
    S3 clients  ──► S3 access key + secret key

  Identity sources:
    ├── AD / LDAP ──► group membership ──► role mapping
    ├── Local accounts (break-glass only)
    └── API tokens (service accounts for automation)
```

> Part of the [FlashBlade Security](../index.md) reference.

---

This page covers all authentication mechanisms available in Purity//FB: local accounts, Active Directory integration for SMB and admin access, LDAP for NFS UID/GID mapping, SAML SSO for the management GUI, and API token management for automation.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Authentication Mechanisms Summary

| Mechanism | Use Case | Recommended? |
|---|---|---|
| Local accounts | Break-glass admin access; initial setup | Limited — local accounts only for named admins and emergency access |
| Active Directory (AD) | SMB share access; optional Kerberos for NFS; admin authentication via LDAP | Yes — required for SMB; recommended for NFS in AD environments |
| LDAP (non-AD) | NFS UID/GID mapping in Linux-only environments | Yes — for Linux-centric deployments without AD |
| SAML SSO | Management GUI and CLI authentication for admin users | Yes — enforces IdP-managed MFA; preferred for production |
| API tokens | REST API and CLI access for automation and service accounts | Yes — for all non-interactive access |
| Kerberos (NFS) | Encrypted and authenticated NFS sessions (krb5/krb5i/krb5p) | Yes — for environments requiring NFS in-flight authentication |

---

## Local Account Management

Local accounts are stored on the FlashBlade itself and do not depend on any external directory service. Use local accounts for the break-glass emergency admin account and for initial array setup before AD or SAML is configured.

```bash
# List all local admin accounts and their roles
purefb admin list

# Create a named local admin account
purefb admin create \
    --name s.jones \
    --role array_admin

# Create a storage operations account (lower privilege)
purefb admin create \
    --name p.smith \
    --role storage_admin

# Create a read-only account for monitoring tools
purefb admin create \
    --name svc-monitoring \
    --role readonly

# Set or change a password for an account
purefb admin update --name s.jones --password
# Enter password at the prompt — passwords are not echoed

# Delete a local account that is no longer needed
purefb admin delete --name old-admin
```

**Roles reference:**

| Role | Permissions |
|---|---|
| `array_admin` | Full access — system configuration, user management, all data operations |
| `storage_admin` | Manage filesystems, buckets, snapshots, replication; cannot modify system or user config |
| `ops_admin` | Read access plus alert acknowledgement; cannot modify configuration |
| `readonly` | Read-only view of all configuration and operational status |

**Break-glass account:**

Maintain exactly one local `array_admin` account as a break-glass credential for use when SAML/AD is unavailable. Store this credential in a PAM vault (CyberArk, HashiCorp Vault) with access restricted to the on-call escalation procedure. Name the account `break-glass` or similar to make its purpose obvious in audit logs.

```bash
purefb admin create --name break-glass --role array_admin
# Immediately store the password in the PAM vault — do not leave it written down
```

---

## Active Directory Integration

AD integration in Purity//FB serves two functions:

1. **SMB authentication** — Windows clients authenticate to FlashBlade SMB shares using their domain Kerberos tickets; FlashBlade must be joined to AD as a computer account
2. **Admin authentication via LDAP** — AD group membership is mapped to Purity//FB admin roles, enabling domain accounts to log into the FlashBlade management GUI and CLI

### Join FlashBlade to Active Directory

```bash
# Configure the AD join
purefb directory-service update \
    --enabled true \
    --uri "ldaps://dc01.example.com" \
    --base-dn "DC=example,DC=com" \
    --bind-user "CN=svc-pure-bind,OU=ServiceAccounts,DC=example,DC=com" \
    --bind-password "<bind_password>"

# Test the directory service connection
purefb directory-service test

# Verify the current directory service configuration
purefb directory-service list
```

**DNS requirement:** The FlashBlade management interface must be able to resolve the AD domain and domain controller FQDNs. Confirm DNS is configured before attempting the AD join:

```bash
purefb dns list
purefb dns-lookup --name dc01.example.com
```

**NTP requirement:** FlashBlade and AD domain controllers must have clocks within 5 minutes of each other (Kerberos 5-minute skew limit). Confirm NTP is configured:

```bash
purefb ntp list
```

### Map AD Groups to Purity Roles

After joining AD, create role mappings from AD security groups to Purity//FB roles. Assign all operational access to AD groups — remove individual local accounts for human admins once AD groups are validated.

```bash
# Map an AD group to the array_admin role
purefb admin add-group \
    --name "CN=pure-fb-admins,OU=Groups,DC=example,DC=com" \
    --role array_admin

# Map a group to storage_admin
purefb admin add-group \
    --name "CN=pure-storage-ops,OU=Groups,DC=example,DC=com" \
    --role storage_admin

# Map a group to readonly for monitoring
purefb admin add-group \
    --name "CN=pure-readonly,OU=Groups,DC=example,DC=com" \
    --role readonly

# List configured group-to-role mappings
purefb admin list --groups
```

**Validation:** Log out and log back in using a domain account that is a member of the `pure-fb-admins` group. Confirm the expected role is assigned before removing individual local admin accounts.

### SMB and Kerberos NFS

Once the FlashBlade is joined to AD, SMB shares automatically use Kerberos authentication — Windows clients presenting valid domain tickets can access shares without additional configuration. For NFS with Kerberos authentication:

```bash
# Enable NFS Kerberos authentication on a filesystem
# krb5 = authentication only
# krb5i = authentication + integrity
# krb5p = authentication + integrity + privacy (full encryption)
purefb filesystem update \
    --name prod-nfs \
    --nfs-rules "10.0.1.0/24(rw,no_root_squash,sec=krb5p)"
```

Kerberos NFS requires the NFS client to obtain a Kerberos ticket from the KDC (domain controller) — configure `/etc/krb5.conf` on Linux clients and ensure the client has a Kerberos keytab or principal.

---

## LDAP Integration (Non-AD)

For Linux-centric environments without Active Directory, configure LDAP directly (OpenLDAP, FreeIPA, etc.) for NFS UID/GID resolution. FlashBlade uses LDAP to resolve NFS user and group IDs to names for export policy enforcement.

```bash
# Configure LDAP for NFS UID/GID mapping
purefb directory-service update \
    --enabled true \
    --uri "ldap://ldap.example.com" \
    --base-dn "DC=example,DC=com" \
    --bind-user "CN=svc-pure-bind,DC=example,DC=com" \
    --bind-password "<bind_password>"

# Test the LDAP connection
purefb directory-service test
```

**UID/GID consistency:** Ensure NFS clients and the LDAP directory use consistent UID and GID assignments. Mismatched UIDs between the client and the LDAP directory cause incorrect ownership resolution on the FlashBlade, which can result in access denials even when export policy IP rules match.

---

## SAML SSO Configuration

SAML 2.0 SSO delegates FlashBlade GUI and CLI authentication to an enterprise IdP (Okta, Azure AD, Ping Identity, ADFS). The IdP enforces MFA, and group membership in the IdP is used to assign Purity//FB roles. This is the recommended authentication mechanism for production arrays where compliance requires MFA on privileged access.

**SAML configuration is performed in the Purity//FB GUI under Settings > Access > Single Sign-On.**

High-level steps:

1. **Configure the Service Provider (SP) in Pure1 / Purity//FB GUI**
   - Navigate to **Settings > Access > Single Sign-On**
   - Download the FlashBlade SP metadata (Entity ID, ACS URL, SP certificate)

2. **Configure the Identity Provider (IdP)**
   - In your IdP (Okta, Azure AD, ADFS), create a new SAML 2.0 application
   - Upload or paste the FlashBlade SP metadata
   - Configure attribute mapping to pass the user's role group as a SAML assertion attribute
   - Assign the Pure Storage SAML application to the relevant user groups

3. **Upload IdP metadata to FlashBlade**
   - Download the IdP SAML metadata XML from your IdP
   - Upload to FlashBlade via **Settings > Access > Single Sign-On > IdP Configuration**

4. **Map IdP role attributes to Purity//FB roles**
   - Configure attribute-based role mapping in the FlashBlade SSO settings
   - Typical mapping: `pure-fb-admins` group attribute → `array_admin` role

5. **Test and validate**
   - Log into the FlashBlade GUI — the browser should redirect to the IdP login page
   - Log in with a domain account that is a member of the `pure-fb-admins` group
   - Confirm the expected role is shown in the FlashBlade GUI
   - Keep the break-glass local account active until SSO is validated

```bash
# Verify SSO is configured (CLI shows SSO enabled/disabled status)
purefb array list --sso
```

**SAML failover:** If the IdP is unreachable, SSO authentication will fail for all domain users. The local break-glass account bypasses SSO and provides emergency access. Ensure the break-glass password is current and stored in the PAM vault before enabling SSO-only mode.

---

## API Token Management

API tokens authenticate REST API calls and CLI sessions for automation, monitoring, and backup integrations. Each admin account can have one API token. Tokens do not expire by default — rotate them on a defined schedule and revoke immediately when a service account is decommissioned.

```bash
# List all accounts and show their API token status
purefb admin apitoken list

# Create an API token for an admin account
purefb admin apitoken create --name svc-veeam
# Output:
#   api_token: <token_value>
# Save the token immediately — it is shown only at creation and cannot be retrieved later

# Revoke an API token without deleting the account
purefb admin apitoken delete --name svc-old-monitoring

# Delete an account and its token
purefb admin delete --name svc-decommissioned
```

**Service account token standards:**

| Service Account | Role | Token Rotation Schedule |
|---|---|---|
| `svc-veeam` | `storage_admin` | 90 days |
| `svc-commvault` | `storage_admin` | 90 days |
| `svc-monitoring` | `readonly` | 180 days |
| `svc-automation` | `storage_admin` | 90 days |
| `break-glass` | `array_admin` | On use; otherwise 90 days |

**Rotation procedure:**

1. Create a new API token for the service account: `purefb admin apitoken create --name <account>`
2. Update the token in the consuming system (Veeam plugin, monitoring tool, etc.)
3. Verify the new token works by running a test API call
4. Revoke the old token: `purefb admin apitoken delete --name <account>` (this overwrites the existing token — step 1 already replaced it, so deletion in this context means the old value is gone after step 1)

**Authenticating with an API token (REST API example):**

```bash
# Use x-auth-token header for API calls
curl -s -k \
    -X GET "https://<fb-management-ip>/api/2.12/arrays" \
    -H "x-auth-token: <api_token>" | jq .

# Or log in with username/password to get a session token, then use it
curl -s -k -X POST "https://<fb-management-ip>/api/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"pureuser","password":"<password>"}' \
    -c /tmp/fb_session.txt

curl -s -k "https://<fb-management-ip>/api/2.12/filesystems" \
    -b /tmp/fb_session.txt | jq .
```

---

## Authentication Audit and Review

Run the following checks quarterly and before any access control review:

```bash
# List all local accounts and their roles
purefb admin list

# List all API tokens and their last-used timestamps
purefb admin apitoken list

# Review AD/LDAP group-to-role mappings
purefb admin list --groups

# Review directory service configuration
purefb directory-service list

# Check audit log for recent authentication events
purefb audit list | grep -i "login\|auth\|token" | head -40
```

**Quarterly review checklist:**

- [ ] Confirm all local accounts are accounted for — no orphaned accounts from departed staff
- [ ] Confirm all API tokens have a documented owner and current integration
- [ ] Revoke API tokens for any decommissioned integrations
- [ ] Confirm AD/LDAP group-to-role mappings match current access requirements
- [ ] Confirm break-glass account credentials are current in the PAM vault
- [ ] Confirm SAML SSO is functioning — log in with a domain account as a test
- [ ] Review audit log for any unexpected login attempts or API token use from unrecognised source IPs
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
