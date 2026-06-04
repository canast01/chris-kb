# Data Protection — Data Encryption

```bash
# Check if encrypted
cryptsetup isLuks /dev/sdb && echo "LUKS" || echo "Not encrypted"

# List open encrypted volumes
dmsetup ls --target crypt

# Dump LUKS header info
cryptsetup luksDump /dev/sdb
```text
┌────────────────────────────────── Data Protection — Data Encryption ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Encrypt all sensitive data at rest and all data in transit regardless of classification    │   │
│   │           At rest: AES-256 minimum; managed via KMS or HSM; keys rotated on schedule          │   │
│   │    In transit: TLS 1.2 minimum, 1.3 preferred; no unencrypted admin protocols (Telnet/FTP)    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Encryption at Rest              │  │            Encryption in Transit            │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │        Linux: LUKS volume encryption         │  │            TLS 1.3 for HTTPS APIs           │   │
│   │           Windows: BitLocker + TPM           │  │             SSH for admin access            │   │
│   │         Storage array native encrypt         │  │            IPsec site-to-site VPN           │   │
│   │             Cloud: AWS KMS / AKV             │  │            mTLS for service mesh            │   │
│   │           DB: TDE (Transparent DE)           │  │            LDAPS (not plain LDAP)           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    LUKS       = Linux Unified Key Setup; block device encryption; key stored in LUKS header           │
│    BitLocker  = Windows full-volume encryption; TPM stores key; recoverable via AD/Azure AD           │
│    TDE        = Transparent Data Encryption; DB-level encryption; transparent to application          │
│    AKV        = Azure Key Vault; managed HSM for keys, secrets, and certificates in Azure             │
│    mTLS       = Mutual TLS; both client and server present certificates; service-to-service auth      │
│    TPM        = Trusted Platform Module; chip that stores BitLocker key; ties disk to hardware        │
│    Cipher     = Algorithm used for encryption; AES-256-GCM is standard for new deployments            │
│    TLS 1.3    = Latest TLS version; removes weak ciphers; mandatory for public-facing services        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
```
```sql
CREATE DATABASE ENCRYPTION KEY WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE <cert-name>;
ALTER DATABASE <dbname> SET ENCRYPTION ON;

SELECT db_name(database_id), encryption_state, percent_complete
FROM sys.dm_database_encryption_keys;
```
