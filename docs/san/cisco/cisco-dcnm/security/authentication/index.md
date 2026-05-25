# Cisco DCNM — Authentication

> Part of the [Cisco DCNM](../../index.md) reference.

---

## Overview

DCNM supports local accounts, LDAP/Active Directory, TACACS+, and RADIUS for user authentication. Production environments should use LDAP or TACACS+ for all named users, with local admin as break-glass only.

---

## 1. Local Accounts

Managed under **Administration > Security > Local User Management**.

### Create a Local Account

1. Navigate to **Administration > Security > Local User Management > Add User**.
2. Enter username, password, and email.
3. Assign a role (see [Access Control](../access-control/index.md)).
4. Click **Save**.

### Password Policy

Configure under **Administration > Security > Password Policy**:

| Setting | Recommended Value |
|---|---|
| Minimum length | 12 characters |
| Uppercase required | Yes |
| Lowercase required | Yes |
| Numbers required | Yes |
| Special characters required | Yes |
| Maximum age | 90 days |
| Password history | 10 |
| Account lockout after | 5 failed attempts |
| Lockout duration | 30 minutes |

---

## 2. LDAP / Active Directory

Configure under **Administration > Security > Authentication > LDAP**.

### Configuration

| Field | Value |
|---|---|
| Server | `ldap.corp.example.com` |
| Port | 636 (LDAPS) |
| Base DN | `DC=corp,DC=example,DC=com` |
| Bind DN | `CN=dcnm-svc,OU=Service Accounts,DC=corp,DC=example,DC=com` |
| Bind password | Service account password |
| User attribute | `sAMAccountName` |
| Group base DN | `OU=DCNM-Groups,DC=corp,DC=example,DC=com` |
| Role attribute | `memberOf` |

### Import CA Certificate (for LDAPS)

```bash
ssh root@dcnm-dc1.corp.example.com

# Copy CA cert to DCNM
scp corp-ca.crt root@dcnm-dc1.corp.example.com:/tmp/

# Import into Java truststore
keytool -import -trustcacerts -alias corp-ldap-ca \
  -file /tmp/corp-ca.crt \
  -keystore /usr/java/default/jre/lib/security/cacerts \
  -storepass changeit -noprompt

# Restart DCNM to apply
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server restart
```

### Test LDAP Authentication

After saving LDAP settings, click **Test**. Enter a test AD user and password. DCNM will report success (including the groups resolved) or a specific error.

---

## 3. TACACS+ Integration

TACACS+ provides per-command accounting and is the preferred AAA method for MDS switches. DCNM itself can also authenticate via TACACS+:

Configure under **Administration > Security > Authentication > TACACS+**:

| Field | Value |
|---|---|
| Server 1 | `10.10.1.10` |
| Server 2 | `10.10.1.11` |
| Server port | 49 |
| Shared key | Stored in vault |
| Authentication type | PAP or CHAP |
| Role from TACACS+ | Enabled (uses AV-pair `cisco-av-pair=shell:roles*dcnm-role`) |

When TACACS+ is configured:
- DCNM sends user credentials to the TACACS+ server
- The TACACS+ server returns a role AV-pair that DCNM maps to a DCNM role
- If TACACS+ is unreachable, DCNM falls back to local accounts (ensure break-glass account exists)

---

## 4. Session Management

Configure under **Administration > Security > Session Settings**:

| Setting | Recommended Value |
|---|---|
| Session idle timeout | 15 minutes |
| Maximum session lifetime | 8 hours |
| Concurrent sessions per user | 3 |

REST API sessions: use `expirationTime` in the login call (in seconds). Always call `/rest/logout` at the end of automation scripts. Long-lived API tokens that are never invalidated accumulate and may cause session exhaustion.

---

## 5. Audit Trail

All authentication events are logged in DCNM's audit log:
- View under **Administration > Logs > Audit Logs**
- Filter by category: **Security**, event type: **Login/Logout**
- Export to CSV for SIEM ingestion

Authentication failures also appear in the DCNM server log:
```bash
grep -i "authentication\|login failed\|unauthorized" /var/log/dcnm/server.log | tail -50
```

---

## 6. TLS Certificate Management

Replace the default self-signed DCNM certificate:

```bash
ssh root@dcnm-dc1.corp.example.com

# Generate CSR
openssl req -new -newkey rsa:4096 -nodes \
  -keyout /tmp/dcnm.key \
  -out /tmp/dcnm.csr \
  -subj "/CN=dcnm-dc1.corp.example.com/O=Corp/C=AU" \
  -addext "subjectAltName=DNS:dcnm-dc1.corp.example.com"

# After CA signs and returns dcnm.crt:

# Import into DCNM keystore
openssl pkcs12 -export -in dcnm.crt -inkey /tmp/dcnm.key \
  -certfile intermediate-ca.crt \
  -name "dcnm" -out /tmp/dcnm.p12 -passout pass:changeit

keytool -importkeystore \
  -srckeystore /tmp/dcnm.p12 -srcstoretype pkcs12 -srcstorepass changeit \
  -destkeystore /usr/local/cisco/dcm/dcnm/conf/.dcnmkeystore \
  -deststoretype jks -deststorepass <keystore-password> \
  -alias dcnm -noprompt

# Restart DCNM to serve new certificate
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server restart

# Verify new certificate
openssl s_client -connect dcnm-dc1.corp.example.com:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates
```
