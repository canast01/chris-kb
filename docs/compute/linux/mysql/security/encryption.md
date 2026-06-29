---
tags:
  - linux
  - security
---
# MySQL / MariaDB — Encryption

<div class="kb-summary">
MySQL encryption — InnoDB tablespace encryption (TDE), SSL/TLS for connections, encrypted backups, and keyring plugin configuration.

*Applies to: RHEL / Ubuntu LTS*
</div>
![MySQL / MariaDB — Encryption](../../../../assets/compute-linux-mysql-security-encryption.svg)

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

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


```text title="Expected output"
xtrabackup: recognized server arguments: --datadir=/var/lib/mysql --port=3306
xtrabackup: recognized client arguments: --socket=/var/run/mysqld/mysqld.sock
230415 14:32:18 Backup created in directory '/backup/xb-2024-04-15'
230415 14:32:18 MySQL binlog position: filename 'mysql-bin.000042', position '1847293'
230415 14:32:45 [00] Encrypting backup with AES256...
230415 14:32:52 [00] Encryption completed
230415 14:32:52 Backup successfully prepared
230415 14:32:53 All done! Backup saved in '/backup/xb-2024-04-15'
```

!!! warning "Common errors"
    **`xtrabackup: error: failed to read encryption key from '/etc/xtrabackup.key': Permission denied`** — Ensure the key file is readable by the MySQL/backup user with `chmod 400 /etc/xtrabackup.key && chown mysql:mysql /etc/xtrabackup.key`.
    **`xtrabackup: error: Target directory '/backup/xb-2024-04-15' already exists`** — Remove the existing backup directory or use a unique target directory name with a different timestamp or suffix.
    **`xtrabackup: error: Failed to connect to MySQL server on 'localhost' (111)`** — Verify MySQL is running with `systemctl status mysql` and check socket/port connectivity.
## Key Rotation

```sql
-- Rotate the master key (re-encrypts all tablespace keys)
ALTER INSTANCE ROTATE INNODB MASTER KEY;
```

---

## See also

- [Mysql — Hardening](../hardening/)
- [Mysql — Authentication](../authentication/)
- [Mysql — Access Control](../access-control/)
