# Data Encryption

Encryption protects data at rest, in transit, and during processing against unauthorised access.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Data Encryption Overview                    │
├───────────────────────┬─────────────────────────┬───────────────────┤
│    At Rest            │      In Transit          │  Key Management  │
│                       │                          │                  │
│ LUKS (Linux)          │ TLS 1.2+ mandatory       │ AWS KMS / Azure  │
│ BitLocker (Windows)   │ Disable TLS 1.0/1.1      │ Key Vault        │
│ ONTAP vol encryption  │ Cipher: AES-256-GCM      │ HSM for restrict │
│ Pure: always-on       │                          │ Annual rotation  │
│ MSSQL TDE             │ openssl s_client verify  │                  │
└───────────┬───────────┴───────────┬──────────────┴──────────┬───────┘
            │                       │                         │
            └───────────────────────┴─────────────────────────┘
                                    │
                                    ▼
                       ┌────────────────────────┐
                       │  Verification Checklist │
                       │  cert expiry monitored  │
                       │  KMS health checked     │
                       │  key backup tested      │
                       └────────────────────────┘
```

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

**Windows — BitLocker:**
```powershell
# Check status all volumes
Get-BitLockerVolume | Select-Object MountPoint, VolumeStatus, EncryptionMethod, ProtectionStatus

# Enable on a drive
Enable-BitLocker -MountPoint "D:" -EncryptionMethod XtsAes256 -RecoveryPasswordProtector

# Back up recovery key to AD
Backup-BitLockerKeyProtector -MountPoint "C:" -KeyProtectorId (Get-BitLockerVolume C:).KeyProtector[0].KeyProtectorId
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
