# Jira — Encryption


<div class="kb-summary">
Jira encryption spans transport security (TLS), at-rest storage, attachment handling, and database encryption. The approach differs between Data Center (self-managed) and Cloud deployments.
</div>

---

## Transport Encryption (TLS)

### Jira Data Center — TLS Configuration

Jira Data Center runs on Apache Tomcat. TLS is typically terminated at a load balancer or reverse proxy (nginx, Apache HTTP Server, or F5). Do not configure TLS directly on Tomcat in production.

#### nginx Reverse Proxy (Recommended)

```nginx
# /etc/nginx/sites-available/jira
server {
    listen 80;
    server_name jira.corp.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name jira.corp.example.com;

    ssl_certificate     /etc/ssl/certs/jira.corp.example.com.crt;
    ssl_certificate_key /etc/ssl/private/jira.corp.example.com.key;

    # TLS hardening
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:20m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-Frame-Options SAMEORIGIN always;
    add_header Referrer-Policy strict-origin-when-cross-origin always;

    # Proxy to Jira
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_read_timeout 300s;
        client_max_body_size 100m;  # Match Jira attachment limit
    }
}
```
```text
┌────────────────────────────────────────── Jira — Encryption ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Jira Encryption — In Transit and At Rest                           │   │
│   │               In transit: TLS 1.2+ via reverse proxy; Tomcat internal HTTP only               │   │
│   │             At rest: DB encryption with dm-crypt/LUKS or PostgreSQL TDE extension             │   │
│   │               JIRA_HOME: NFS datastore encrypted at storage or hypervisor level               │   │
│   │             Secrets: DB password in dbconfig.xml; store in Vault or encrypted env             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Every data path must be encrypted: browser, app-to-DB, and storage volumes                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  In Transit                  │  │                   At Rest                   │   │
│   │             TLS 1.2+ at LB/proxy             │  │              DB: dm-crypt/LUKS              │   │
│   │             HTTP Tomcat internal             │  │             NFS: storage encrypt            │   │
│   │             LDAP: LDAPS port 636             │  │             Backup: GPG encrypt             │   │
│   │             DB: SSL JDBC sslmode             │  │             VM: vSphere encrypt             │   │
│   │            HSTS: enabled at proxy            │  │             Vault: secret store             │   │
│   │              Cert: RSA 2048 min              │  │             Key rotation: annual            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Reverse proxy VM · Jira app VMs · PostgreSQL VM encrypted disk · NFS datastore                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.2+     = minimum TLS version; disable TLS 1.0/1.1 at proxy level                               │
│  HSTS         = Strict-Transport-Security header; forces HTTPS after first visit                      │
│  LDAPS        = LDAP over SSL port 636; encrypts directory sync                                       │
│  SSL JDBC     = sslmode=require in dbconfig.xml JDBC URL                                              │
│  dm-crypt     = Linux kernel encryption; LUKS partition on DB data volume                             │
│  LUKS         = Linux Unified Key Setup; standard partition encryption                                │
│  GPG backup   = gpg --symmetric backup.tar.gz; passphrase stored in Vault                             │
│  vSphere encrypt = VM-level encryption using vSphere Native Key Provider                              │
│  Vault        = HashiCorp Vault; stores dbconfig.xml DB password                                      │
│  dbconfig.xml = Jira DB connection config; in JIRA_HOME; contains JDBC URL                            │
│  Key rotation = annual encryption key change; planned maintenance window                              │
│  TDE          = Transparent Data Encryption at PostgreSQL level (pgcrypto)                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### LDAPS for Directory Connectivity

All LDAP connections must use LDAPS (port 636) or StartTLS.

```bash
# Import LDAP CA certificate into Jira's JVM truststore
$JAVA_HOME/bin/keytool -import \
  -alias corp-ldap-ca \
  -file /etc/ssl/certs/corp-ca.crt \
  -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit \
  -noprompt

# Verify the certificate was imported
$JAVA_HOME/bin/keytool -list \
  -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit | grep corp-ldap-ca

# Test LDAPS connectivity
ldapsearch -H ldaps://dc.corp.example.com:636 \
  -D "CN=jira-svc,OU=ServiceAccounts,DC=corp,DC=example,DC=com" \
  -W \
  -b "DC=corp,DC=example,DC=com" \
  "(sAMAccountName=testuser)" cn mail
```

---

## Database Encryption

### At-Rest Encryption (Data Center)

Jira stores all data (issues, comments, field values, attachments metadata) in a relational database. Encrypt the database volume and enable database-native TDE where supported.

**PostgreSQL with TDE (pgcrypto for column encryption):**

```sql
-- Enable pgcrypto extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Example: Encrypt a custom field column
-- Note: Jira stores data in genericvalue/propertyentry tables
-- Column-level encryption typically applied to sensitive custom field tables

-- Verify encrypted tablespace (Linux dm-crypt/LUKS)
-- The database data directory should reside on an encrypted volume
```

**LUKS encryption for PostgreSQL data directory:**

```bash
# Verify PostgreSQL data directory is on encrypted volume
df /var/lib/postgresql/14/main
lsblk -o NAME,FSTYPE,MOUNTPOINT,SIZE | grep dm-

# Check LUKS status
cryptsetup status /dev/mapper/pgdata
```

**MS SQL Server TDE:**

```sql
-- Enable TDE on Jira database (SQL Server)
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'StrongPassword123!';

CREATE CERTIFICATE JiraTDECert
WITH SUBJECT = 'Jira Database TDE Certificate';

USE jiradb;
CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE JiraTDECert;

ALTER DATABASE jiradb SET ENCRYPTION ON;

-- Verify TDE status
SELECT db.name, db.is_encrypted, dm.encryption_state
FROM sys.databases db
LEFT JOIN sys.dm_database_encryption_keys dm ON db.database_id = dm.database_id
WHERE db.name = 'jiradb';
```

---

## Attachment Storage Encryption

### Data Center — Local Attachment Storage

Attachments are stored in the Jira home directory (`/var/atlassian/application-data/jira/data/attachments/`). Encrypt this volume.

```bash
# Check current attachment home
grep "attachments" /var/atlassian/application-data/jira/dbconfig.xml

# Verify attachment directory is on encrypted volume
df /var/atlassian/application-data/jira/data/attachments/
lsblk -o NAME,FSTYPE,MOUNTPOINT | grep $(df /var/atlassian/application-data/jira/ | awk 'NR==2{print $1}')

# Set correct permissions on attachment directory
chown -R jira:jira /var/atlassian/application-data/jira/data/attachments/
chmod 750 /var/atlassian/application-data/jira/data/attachments/
```

### Data Center — S3-Compatible Object Storage (v9+)

```properties
# jira-config.properties — S3 attachment storage
jira.attachment.storage.type=s3
jira.s3.bucket=jira-attachments-prod
jira.s3.region=eu-west-1
# Use IAM role — no access keys in config
```

**S3 Bucket Policy — Enforce Encryption:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyUnencryptedObjectUploads",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::jira-attachments-prod/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "aws:kms"
        }
      }
    },
    {
      "Sid": "DenyNonTLSRequests",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::jira-attachments-prod",
        "arn:aws:s3:::jira-attachments-prod/*"
      ],
      "Condition": {
        "Bool": {"aws:SecureTransport": "false"}
      }
    }
  ]
}
```

---

## Jira Cloud Encryption

Jira Cloud (Atlassian) handles encryption transparently:

| Layer | Mechanism |
|---|---|
| Data at rest | AES-256 (AWS EBS/S3 with KMS) |
| Database | Encrypted RDS with KMS CMK |
| Attachments | S3 with server-side encryption (SSE-S3 or SSE-KMS) |
| Transport | TLS 1.2+ (enforced, TLS 1.0/1.1 disabled) |
| Backup | Encrypted with Atlassian-managed keys |

**Customer-managed encryption keys (Atlassian Access Premium):**

Available via Atlassian's BYOK programme — contact Atlassian for configuration. Once enabled:

- Atlassian cannot read customer data without the customer's key.
- Key revocation immediately prevents Atlassian access.

---

## Email Notifications Encryption

```properties
# jira-config.properties — SMTP with TLS
jira.mail.smtp.host=mail.corp.example.com
jira.mail.smtp.port=587
jira.mail.smtp.ssl=false
jira.mail.smtp.starttls=true
jira.mail.smtp.auth=true
```

Administration → System → Mail → Outgoing Mail:

- Always use STARTTLS (port 587) or SMTPS (port 465)
- Authenticate with a dedicated service account
- Verify the mail server certificate

---

## Encryption Checklist

| Control | Data Center | Cloud |
|---|---|---|
| TLS 1.2+ on all endpoints | Configure at proxy | Managed by Atlassian |
| TLS 1.0/1.1 disabled | Configure at proxy | Done |
| HSTS header configured | Configure at proxy | Done |
| Database volume encrypted | Configure on host | Managed by Atlassian |
| Attachment volume encrypted | Configure on host | Managed by Atlassian |
| LDAP uses LDAPS/StartTLS | Configure in Jira | N/A (Cloud IdP) |
| SMTP uses STARTTLS/SMTPS | Configure in Jira | Configure in Jira |
| S3 bucket encryption enforced | Configure in AWS | Managed by Atlassian |
| Backups encrypted | Configure on host | Managed by Atlassian |
| Certificate expiry monitoring | Configure alerting | Managed by Atlassian |

---

## Related Pages

- [Jira — Authentication](../authentication/index.md)
- [Jira — Access Control](../access-control/index.md)
- [Jira — Hardening](../hardening/index.md)
