# SANnav — Authentication

> Part of the [SANnav](../../) reference.

---

## Overview

SANnav supports three authentication methods: local accounts, LDAP/Active Directory, and (in newer versions) SAML-based SSO. Production environments should use LDAP or SSO for all user accounts, reserving local accounts as break-glass only.

---

## 1. Local Accounts

Local accounts are stored in the SANnav PostgreSQL database. Manage under **Administration > User Management > Local Users**.

### Creating a Local Account

1. Navigate to **Administration > User Management > Local Users > New User**.
2. Enter username, full name, and email address.
3. Set a strong initial password (meet SANnav's password policy: minimum 12 characters, upper/lower/number/special).
4. Assign a role (see [Access Control](../access-control/)).
5. Click **Save**.

### Password Policy Configuration

Navigate to **Administration > Security Settings > Password Policy**:

| Setting | Recommended Value |
|---|---|
| Minimum length | 12 |
| Require uppercase | Yes |
| Require lowercase | Yes |
| Require numbers | Yes |
| Require special characters | Yes |
| Maximum age (days) | 90 |
| Password history | 12 (cannot reuse last 12) |
| Account lockout threshold | 5 failed attempts |
| Lockout duration (minutes) | 30 |

### Break-Glass Account

Maintain exactly one local admin account as break-glass for when LDAP is unavailable:
- Username: `admin` or `sannav-breakglass`
- Password: stored in vault (e.g., HashiCorp Vault, CyberArk), not known to individual engineers
- Rotate quarterly
- All use must be logged (audited in SANnav audit trail)

---

## 2. LDAP / Active Directory Integration

Configure under **Administration > Server Settings > LDAP**.

### Configuration Parameters

| Parameter | Value |
|---|---|
| Authentication type | LDAP |
| Server hostname | `ldap.corp.example.com` |
| Port | 636 (LDAPS, preferred) |
| Base DN | `DC=corp,DC=example,DC=com` |
| Bind DN | `CN=sannav-svc,OU=Service Accounts,DC=corp,DC=example,DC=com` |
| User search base | `OU=SAN-Users,DC=corp,DC=example,DC=com` |
| User search attribute | `sAMAccountName` |
| Group search base | `OU=SAN-Groups,DC=corp,DC=example,DC=com` |
| Group member attribute | `member` |
| Follow referrals | Disabled (for single-domain environments) |

### LDAPS Certificate Trust

If the LDAP server uses a self-signed or internal CA certificate, import the CA certificate into SANnav:

```bash
# Copy CA cert to SANnav appliance
scp corp-ca.crt admin@sannav-dc1.corp.example.com:/tmp/

# SSH to appliance and import
ssh admin@sannav-dc1.corp.example.com

# Import CA certificate into Java truststore used by SANnav
sudo keytool -import -trustcacerts -alias corp-ldap-ca \
  -file /tmp/corp-ca.crt \
  -keystore /opt/sannav/jre/lib/security/cacerts \
  -storepass changeit -noprompt

# Restart SANnav to pick up new truststore
sudo sannav restart
```

### LDAP Group to Role Mapping

Navigate to **Administration > Server Settings > LDAP > Role Mapping**:

| AD Group | SANnav Role |
|---|---|
| `GRP-SANnav-SAN-Admins` | SAN Admin |
| `GRP-SANnav-SAN-Operators` | SAN Operator |
| `GRP-SANnav-SAN-Viewers` | SAN Viewer |

### Testing LDAP Authentication

1. Navigate to **Administration > Server Settings > LDAP > Test Connection** — validates the bind DN and password.
2. Navigate to **Administration > Server Settings > LDAP > Test User Authentication** — enter a test AD username and password to verify full authentication and group resolution.

If authentication fails:
- Verify DNS resolution: `nslookup ldap.corp.example.com` from SANnav appliance
- Verify LDAPS port 636 is reachable: `openssl s_client -connect ldap.corp.example.com:636`
- Verify the bind DN has read access to the user and group OUs
- Verify the CA certificate is trusted (if LDAPS)

---

## 3. Session Management

Configure session timeout and concurrent session limits under **Administration > Security Settings > Session**:

| Setting | Recommended Value |
|---|---|
| Session idle timeout | 15 minutes |
| Maximum session duration | 8 hours |
| Concurrent sessions per user | 2 |

Inactive sessions are automatically invalidated after the idle timeout. For API tokens (REST API): tokens have the same idle timeout; always call `/rest/logout` at the end of automation scripts to release the session.

---

## 4. Audit Trail

All authentication events (login, logout, failed login, password change) are recorded in the SANnav audit log. View under **Administration > Audit Log**:

- Filter by event type: `LOGIN`, `LOGOUT`, `LOGIN_FAILED`
- Filter by user
- Export to CSV for SIEM ingestion

The audit log is also written to the SANnav application log file:
```bash
grep "AUTH\|LOGIN\|LOGOUT" /opt/sannav/logs/server.log | tail -100
```

---

## 5. TLS for the SANnav Web UI

The SANnav web UI is served over HTTPS. By default, it uses a self-signed certificate. Replace this with a certificate from the corporate CA or a public CA:

```bash
# Generate CSR on SANnav appliance
ssh admin@sannav-dc1.corp.example.com

openssl req -new -newkey rsa:4096 -nodes \
  -keyout /tmp/sannav.key \
  -out /tmp/sannav.csr \
  -subj "/CN=sannav-dc1.corp.example.com/O=Corp/C=AU" \
  -addext "subjectAltName=DNS:sannav-dc1.corp.example.com"

# Send CSR to your CA for signing
# After receiving the signed cert (sannav.crt):

# Install certificate
sudo cp /tmp/sannav.key /opt/sannav/conf/ssl/sannav.key
sudo cp /tmp/sannav.crt /opt/sannav/conf/ssl/sannav.crt

# If intermediate CA cert is needed, create bundle:
cat sannav.crt intermediate-ca.crt > sannav-chain.crt
sudo cp /tmp/sannav-chain.crt /opt/sannav/conf/ssl/sannav.crt

# Reload nginx (SANnav's front-end web server)
sudo systemctl reload nginx

# Verify certificate is served correctly
openssl s_client -connect sannav-dc1.corp.example.com:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates
```

Track certificate expiry; renew at least 30 days before expiry. SANnav will issue a warning alert when the certificate is within the warning threshold if certificate monitoring is enabled.
