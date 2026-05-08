# Nexus Dashboard — Authentication

> Part of the [Nexus Dashboard](../../) reference.

---

## Overview

Nexus Dashboard uses Keycloak as its internal identity provider. It supports local accounts, LDAP/Active Directory, TACACS+, RADIUS, and SAML 2.0 SSO. Production environments should use LDAP or SAML for named user accounts, with a single local admin account reserved as break-glass.

---

## 1. Local Accounts

Local accounts are managed under **Admin Console > Security > Local Users**.

### Creating a Local Account

1. Navigate to **Admin Console > Security > Local Users > Add User**.
2. Enter username, full name, and email.
3. Set a strong initial password.
4. Assign a role (see [Access Control](../access-control/)).
5. Click **Save**.

### Password Policy

Configure under **Admin Console > Security > Security Settings > Password Policy**:

| Setting | Recommended Value |
|---|---|
| Minimum length | 12 characters |
| Require uppercase | Yes |
| Require lowercase | Yes |
| Require numbers | Yes |
| Require special characters | Yes |
| Maximum age | 90 days |
| Password history | 12 (cannot reuse last 12) |
| Account lockout after | 5 failed attempts |
| Lockout duration | 30 minutes |

### Break-Glass Account

Maintain exactly one local admin account as break-glass:
- Username: `admin` (default) or `nd-breakglass`
- Password: stored in vault (HashiCorp Vault, CyberArk) — not known to individual engineers
- Rotate quarterly
- All use must be recorded in the audit trail
- Used only when LDAP/SAML is unavailable

---

## 2. LDAP / Active Directory

Configure under **Admin Console > Security > Authentication > Login Domains > Add**:

| Field | Value |
|---|---|
| Domain name | `CORP-AD` |
| Type | Active Directory |
| Server address | `ldap.corp.example.com` |
| Port | 636 (LDAPS) |
| Base DN | `DC=corp,DC=example,DC=com` |
| Bind DN | `CN=nd-svc,OU=Service Accounts,DC=corp,DC=example,DC=com` |
| Bind password | Service account password |
| User attribute | `sAMAccountName` |
| Group search base | `OU=ND-Groups,DC=corp,DC=example,DC=com` |

### Import CA Certificate for LDAPS

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Import corporate CA certificate for LDAPS trust
acs certificates import-ca --cert /tmp/corp-ca.crt --name corp-ldap-ca

# Verify
acs certificates show-ca
```

Alternatively, import via GUI: **Admin Console > Security > Certificates > Trusted Certificates > Add**.

### LDAP Role Mapping

Navigate to **Admin Console > Security > Roles > LDAP Role Mapping**:

| AD Group | ND Role |
|---|---|
| `GRP-ND-Admins` | Admin |
| `GRP-ND-SAN-Operators` | Operator (site-scoped to SAN fabrics) |
| `GRP-ND-ReadOnly` | Viewer |

### Test LDAP Authentication

1. Navigate to **Admin Console > Security > Authentication > Login Domains > [CORP-AD] > Test**.
2. Enter a test AD username and password.
3. ND reports: success (including groups resolved and role assigned) or a specific error.

---

## 3. TACACS+

Configure under **Admin Console > Security > Authentication > Login Domains > Add > TACACS+**:

| Field | Value |
|---|---|
| Server 1 | `10.10.1.10` |
| Server 2 | `10.10.1.11` |
| Server port | 49 |
| Shared key | Vault-stored; enter at configuration time |
| Default role | Viewer (fallback if no AV-pair returned) |

Role assignment from TACACS+:
- Configure the TACACS+ server (e.g., Cisco ISE) to return AV-pair: `cisco-av-pair=nd-role=Admin`
- ND maps the `nd-role` attribute value to an ND role

---

## 4. SAML 2.0 (SSO)

SAML 2.0 integration allows engineers to use corporate SSO (Okta, ADFS, Ping) to log into ND.

### Configuration

1. Navigate to **Admin Console > Security > Authentication > Login Domains > Add > SAML**.
2. Download the ND Service Provider metadata XML.
3. Import this XML into your IdP as a new SAML application.
4. Configure the IdP to include a `Role` attribute in the SAML assertion (e.g., `nd-admin`, `nd-operator`).
5. In ND: map the IdP role attribute values to ND roles under **Security > Roles > SAML Role Mapping**.
6. Set SAML as the primary or default login domain.

After SAML is configured, the ND login page shows a **Single Sign-On** button that redirects to the corporate IdP. On successful authentication, users are returned to ND with the mapped role.

---

## 5. Session Management

Configure under **Admin Console > Security > Security Settings > Session**:

| Setting | Recommended Value |
|---|---|
| Session idle timeout | 15 minutes |
| Maximum session lifetime | 8 hours |
| Concurrent sessions per user | 3 |

REST API tokens: tokens are created on login and expire after the session lifetime or on explicit logout. Automation scripts must call the logout endpoint when done to release tokens. Accumulated uncleaned sessions do not consume significant resources in ND (Keycloak manages sessions), but cleaning up is good practice.

---

## 6. TLS Certificate Management for the ND UI

By default, ND generates a self-signed certificate. Replace it with a corporate CA certificate:

```bash
# Step 1: Generate CSR (on any host with OpenSSL)
openssl req -new -newkey rsa:4096 -nodes \
  -keyout nd-dc1.key \
  -out nd-dc1.csr \
  -subj "/CN=nd-dc1.corp.example.com/O=Corp/C=AU" \
  -addext "subjectAltName=DNS:nd-dc1.corp.example.com,DNS:nd-dc1-1.corp.example.com,DNS:nd-dc1-2.corp.example.com,DNS:nd-dc1-3.corp.example.com"

# Step 2: Submit CSR to corporate CA; receive signed certificate

# Step 3: Create bundle with intermediate CA cert
cat nd-dc1.crt intermediate-ca.crt > nd-dc1-bundle.crt

# Step 4: Import into ND
ssh ndadmin@nd-dc1-1.corp.example.com

acs certificates import \
  --key /tmp/nd-dc1.key \
  --cert /tmp/nd-dc1-bundle.crt \
  --name nd-dc1-cert

# Step 5: Activate
acs certificates activate --name nd-dc1-cert

# Verify
openssl s_client -connect nd-dc1.corp.example.com:443 \
  -servername nd-dc1.corp.example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
```

Include all node hostnames in the SAN extension so direct node access (not via VIP) also presents a valid certificate.

---

## 7. Audit Trail

All authentication events are recorded in the ND audit log:
- View under **Admin Console > Operations > Audit Logs**
- Filter by: category **Security**, event type **Login**, **Logout**, **Login_Failed**
- Export to CSV for SIEM ingestion or quarterly review

Authentication events also appear in ND platform logs:
```bash
ssh ndadmin@nd-dc1-1.corp.example.com
acs system logs --component security --tail 100 | grep -i "login\|auth"
```
