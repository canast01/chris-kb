---
tags:
  - security
  - windows
---
# SQL Server — Encryption

<div class="kb-summary">
SQL Server encryption — Transparent Data Encryption (TDE), Always Encrypted, column-level encryption, TLS for connections, and backup encryption.

*Applies to: Windows Server 2019 / 2022*
</div>

```text
┌─────────────────────────────────────── SQL Server — Encryption ───────────────────────────────────────┐
│                                                                                                       │
│   TDE encrypts data files and logs at rest; I/O encrypted transparently with no app changes required  │
│   Always Encrypted: column-level encryption; key never leaves client; SQL Server sees ciphertext      │
│   Back up TDE certificate immediately after creation — losing it means losing database access         │
│                                                                                                       │
│   TDE setup sequence                                                                                  │
│   1. USE master; CREATE MASTER KEY ENCRYPTION BY PASSWORD = '...'                                     │
│   2. CREATE CERTIFICATE TDE_Cert WITH SUBJECT = 'TDE Certificate'                                     │
│   3. USE app_prod; CREATE DATABASE ENCRYPTION KEY WITH ALGORITHM = AES_256                            │
│   4. ALTER DATABASE app_prod SET ENCRYPTION ON                                                        │
│   5. Verify: sys.dm_database_encryption_keys; encryption_state = 3 = encrypted                        │
│   6. BACKUP CERTIFICATE TDE_Cert TO FILE with PRIVATE KEY                                             │
│                                                                                                       │
│   Always Encrypted                                                                                    │
│   Column Master Key (CMK): stored in Windows Certificate Store or Azure Key Vault                     │
│   Column Encryption Key (CEK): encrypted by CMK; stored in SQL Server as ciphertext                   │
│   Application driver must support Always Encrypted; SQL Server never decrypts the data                │
│                                                                                                       │
│   TLS and backup encryption                                                                           │
│   TLS: configure via SQL Server Configuration Manager; Force Encryption = Yes                         │
│   Verify: sys.dm_exec_connections WHERE session_id = @@SPID; encrypt_option = TRUE                    │
│   Backup encryption: WITH ENCRYPTION (ALGORITHM = AES_256, SERVER CERTIFICATE = TDE_Cert)             │
│                                                                                                       │
│   Key terms:                                                                                          │
│   TDE           = Transparent Data Encryption; encrypts .mdf/.ldf/.ndf files and backups at rest      │
│   Always Encrypted = client-side column encryption; SQL Server processes only ciphertext              │
│   CMK           = Column Master Key; stored outside SQL Server; protects CEKs                         │
│   CEK           = Column Encryption Key; stored in SQL Server; encrypted by CMK                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Local Administrator or Domain Admin on target hosts
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Transparent Data Encryption (TDE)

TDE encrypts data and log files at rest. I/O is encrypted/decrypted transparently.

```sql
-- 1. Create master key in master database
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'MasterKeyPass1!';

-- 2. Create certificate
CREATE CERTIFICATE TDE_Cert WITH SUBJECT = 'TDE Certificate';

-- 3. Create database encryption key
USE app_prod;
CREATE DATABASE ENCRYPTION KEY
  WITH ALGORITHM = AES_256
  ENCRYPTION BY SERVER CERTIFICATE TDE_Cert;

-- 4. Enable TDE
ALTER DATABASE app_prod SET ENCRYPTION ON;

-- 5. Verify
SELECT db_name(database_id), encryption_state, percent_complete
FROM sys.dm_database_encryption_keys;
-- encryption_state: 3 = encrypted
```

**Back up the certificate immediately** — losing it means losing access to the database.

```sql
BACKUP CERTIFICATE TDE_Cert TO FILE = 'D:\Cert\TDE_Cert.cer'
  WITH PRIVATE KEY (FILE = 'D:\Cert\TDE_Cert.pvk', ENCRYPTION BY PASSWORD = 'CertPass1!');
```

## Always Encrypted

Column-level encryption where the encryption key never leaves the client. SQL Server only sees ciphertext.

```sql
-- Enabled via SQL Server Management Studio wizard
-- Column Master Key (CMK): stored in Windows Certificate Store or Azure Key Vault
-- Column Encryption Key (CEK): encrypted by CMK; stored in SQL Server
-- Application must use Always Encrypted-enabled driver
```

## TLS for Client Connections

```powershell
# Configure via SQL Server Configuration Manager
# Protocols for MSSQLSERVER → Properties → Certificate → select cert
# Force Encryption = Yes
```

```sql
-- Verify connection is encrypted
SELECT encrypt_option FROM sys.dm_exec_connections WHERE session_id = @@SPID;
```

## Backup Encryption

```sql
BACKUP DATABASE app_prod
  TO DISK = 'D:\Backup\app_prod_enc.bak'
  WITH COMPRESSION,
       ENCRYPTION (ALGORITHM = AES_256, SERVER CERTIFICATE = TDE_Cert);
```

---

## See also

- [Sql Server — Hardening](hardening/)
- [Sql Server — Authentication](authentication/)
- [Sql Server — Access Control](access-control/)
