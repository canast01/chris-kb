# Data Encryption

Encryption protects data at rest, in transit, and during processing against unauthorised access.

## Encryption Requirements by Classification

| Level | At Rest | In Transit | Key Management |
|---|---|---|---|
| Restricted | AES-256 mandatory | TLS 1.2+ mandatory | HSM or enterprise KMS |
| Confidential | AES-256 mandatory | TLS 1.2+ mandatory | Enterprise KMS |
| Internal | Recommended | Recommended | Standard key store |
| Public | Optional | Optional | N/A |

## Encryption at Rest

**Linux — LUKS:**
```bash
# Check if encrypted
cryptsetup isLuks /dev/sdb && echo "LUKS" || echo "Not encrypted"

# List open encrypted volumes
dmsetup ls --target crypt

# Dump LUKS header info
cryptsetup luksDump /dev/sdb
```
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

**Storage arrays:**
- **ONTAP**: `security key-manager show` — confirm key manager connected; `volume show -fields encryption-state`
- **Pure FlashArray**: always-on encryption — confirm via `purecli array get`
- **PowerMax**: DARE — verify in Unisphere → Array Settings → Encryption

## Encryption in Transit

```bash
# Verify TLS version
openssl s_client -connect <host>:443 -tls1_2
openssl s_client -connect <host>:443 -tls1_3

# Check nginx config
grep -E "ssl_protocols|ssl_ciphers" /etc/nginx/nginx.conf

# Comprehensive TLS audit
./testssl.sh <host>:443
```

**Disable weak protocols (nginx):**
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
```

## Database Encryption

**MSSQL — TDE:**
```sql
CREATE DATABASE ENCRYPTION KEY WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE <cert-name>;
ALTER DATABASE <dbname> SET ENCRYPTION ON;

SELECT db_name(database_id), encryption_state, percent_complete
FROM sys.dm_database_encryption_keys;
```

## Key Rotation Schedule

| Key Type | Frequency |
|---|---|
| TLS/SSL certificates | Annual (external); 2-year (internal) |
| AWS KMS CMK | Annual (automatic) |
| Azure Key Vault keys | 90 days (rotation policy) |
| Database encryption keys | Annual or on personnel change |

## Verification Checklist

- [ ] All production volumes confirmed encrypted at rest
- [ ] All external services confirmed TLS 1.2+ only
- [ ] Certificate expiry monitoring in place
- [ ] Key management system operational (HSM/KMS health checked)
- [ ] Encryption key backup confirmed and tested
