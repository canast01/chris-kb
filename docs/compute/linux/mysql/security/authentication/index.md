# MySQL / MariaDB — Authentication

<div class="kb-summary">
MySQL authentication — auth plugins (caching_sha2, mysql_native_password, auth_socket), SSL/TLS client certs, and password policy configuration.
</div>

## Authentication Plugins

| Plugin | MySQL version | Notes |
|---|---|---|
| `caching_sha2_password` | 8.0+ default | SHA-256 with RSA key exchange; requires SSL or RSA key |
| `mysql_native_password` | Legacy default | SHA1; weaker; still supported; required for older clients |
| `auth_socket` | Linux only | Authenticates by OS socket user; no password; `root@localhost` |

```sql
-- Check which plugin a user uses
SELECT user, host, plugin FROM mysql.user;

-- Change plugin for compatibility with old clients
ALTER USER 'appuser'@'%' IDENTIFIED WITH mysql_native_password BY 'Pass1!';

-- Use socket auth for root (password-free from OS root)
ALTER USER 'root'@'localhost' IDENTIFIED WITH auth_socket;
```

## Password Policy

```sql
-- View current policy
SHOW VARIABLES LIKE 'validate_password%';

-- Configure (MySQL 8.0+)
SET GLOBAL validate_password.policy = MEDIUM;  -- LOW / MEDIUM / STRONG
SET GLOBAL validate_password.length = 12;
SET GLOBAL validate_password.mixed_case_count = 1;
SET GLOBAL validate_password.number_count = 1;
SET GLOBAL validate_password.special_char_count = 1;
```

## SSL/TLS Client Certificate Authentication

```sql
-- Require SSL for a user
ALTER USER 'secure_user'@'%' REQUIRE SSL;

-- Require specific certificate CN
ALTER USER 'cert_user'@'%' REQUIRE SUBJECT '/CN=app-server-01';
```

```bash
# Connect with client certificate
mysql -u cert_user \
  --ssl-ca=/etc/mysql/ca-cert.pem \
  --ssl-cert=/etc/mysql/client-cert.pem \
  --ssl-key=/etc/mysql/client-key.pem
```

## Account Locking

```sql
-- Lock an account
ALTER USER 'appuser'@'%' ACCOUNT LOCK;

-- Unlock
ALTER USER 'appuser'@'%' ACCOUNT UNLOCK;

-- Auto-lock after failed attempts (MySQL 8.0+)
ALTER USER 'appuser'@'%' FAILED_LOGIN_ATTEMPTS 5 PASSWORD_LOCK_TIME 1;
```
