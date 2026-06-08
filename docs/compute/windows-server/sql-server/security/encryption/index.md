# SQL Server — Encryption

<div class="kb-summary">
SQL Server encryption — Transparent Data Encryption (TDE), Always Encrypted, column-level encryption, TLS for connections, and backup encryption.
</div>

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
