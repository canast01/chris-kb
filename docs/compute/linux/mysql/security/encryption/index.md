# MySQL / MariaDB — Encryption

<div class="kb-summary">
MySQL encryption — InnoDB tablespace encryption (TDE), SSL/TLS for connections, encrypted backups, and keyring plugin configuration.
</div>

```text
┌───────────────────────────────────────── MySQL — Encryption ──────────────────────────────────────────┐
│                                                                                                       │
│   Two encryption layers: data-at-rest (InnoDB TDE) and data-in-transit (SSL/TLS connections)          │
│   TDE requires a keyring plugin; MySQL 8.0+ includes component_keyring_file                           │
│   Encrypted backups (xtrabackup --encrypt) protect backup files stored off-host                       │
│                                                                                                       │
│   InnoDB tablespace encryption (TDE)                                                                  │
│   Configure keyring: early-plugin-load=component_keyring_file in my.cnf                               │
│   Enable per table: ALTER TABLE t ENCRYPTION='Y'; or per schema with default_table_encryption=ON      │
│   Verify: SELECT * FROM information_schema.INNODB_TABLESPACES WHERE ENCRYPTION='Y'                    │
│                                                                                                       │
│   Connection encryption (SSL/TLS)                                                                     │
│   require_secure_transport=ON: rejects all non-TLS connections server-wide                            │
│   REQUIRE SSL on user account: forces TLS for that specific account                                   │
│   Verify: SHOW STATUS LIKE 'Ssl_cipher'; non-empty = current connection is encrypted                  │
│                                                                                                       │
│   Encrypted backups                                                                                   │
│   xtrabackup --encrypt=AES256 --encrypt-key-file=/path/to/key.enc: encrypts backup stream             │
│   mysqldump output: pipe through openssl enc -aes-256-cbc before writing to disk                      │
│   Store encryption keys separately from backup files                                                  │
│                                                                                                       │
│   Key terms:                                                                                          │
│   TDE          = Transparent Data Encryption; encrypts data files on disk; transparent to queries     │
│   Keyring      = plugin or component storing the master encryption key; required for TDE              │
│   require_secure_transport = server variable; enforces SSL/TLS for all connections                    │
│   ENCRYPTION='Y' = InnoDB tablespace flag; file-per-table tablespace encrypted with AES-256           │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## InnoDB Tablespace Encryption (TDE)

Requires a keyring plugin. MySQL 8.0+ includes `component_keyring_file`.

```ini
# /etc/mysql/mysql.conf.d/mysqld.cnf
early-plugin-load = keyring_file.so
keyring_file_data = /var/lib/mysql-keyring/keyring
```

```sql
-- Enable encryption for a table
CREATE TABLE sensitive (id INT, data VARCHAR(255)) ENCRYPTION='Y';

-- Encrypt an existing table
ALTER TABLE users ENCRYPTION='Y';

-- Check which tables are encrypted
SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS
FROM information_schema.TABLES
WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%';

-- Enable default encryption for all new InnoDB tables
SET GLOBAL default_table_encryption = ON;
```

## SSL/TLS for Client Connections

```bash
# Generate CA and server certs (if not auto-generated)
mysql_ssl_rsa_setup --datadir=/var/lib/mysql

# Verify SSL is active
mysql -u root -p -e "SHOW VARIABLES LIKE 'have_ssl';"
# Expect: have_ssl = YES
```

```sql
-- Confirm active connection uses SSL
STATUS;   -- look for "SSL: Cipher in use is ..."

-- Require SSL for all connections from a specific user
ALTER USER 'appuser'@'%' REQUIRE SSL;
```

## Binlog Encryption

```ini
[mysqld]
binlog_encryption = ON    # MySQL 8.0.14+
```

## Backup Encryption

```bash
# Percona XtraBackup with AES256
xtrabackup --backup --encrypt=AES256 \
  --encrypt-key-file=/etc/xtrabackup.key \
  --target-dir=/backup/xb-$(date +%F)
```

## Key Rotation

```sql
-- Rotate the master key (re-encrypts all tablespace keys)
ALTER INSTANCE ROTATE INNODB MASTER KEY;
```
