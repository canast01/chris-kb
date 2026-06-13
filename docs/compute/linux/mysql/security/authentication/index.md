---
tags:
  - linux
  - security
---
# MySQL / MariaDB — Authentication

<div class="kb-summary">
MySQL authentication — auth plugins (caching_sha2, mysql_native_password, auth_socket), SSL/TLS client certs, and password policy configuration.

*Applies to: RHEL / Ubuntu LTS*
</div>

```text
┌─────────────────────────────────────── MySQL — Authentication ────────────────────────────────────────┐
│                                                                                                       │
│   MySQL 8.0 default plugin: caching_sha2_password (SHA-256); legacy clients may need native_password  │
│   auth_socket: Linux-only; authenticates by OS user matching MySQL user; used for root@localhost      │
│   SSL/TLS client certificates add a second factor beyond username/password                            │
│                                                                                                       │
│   Authentication plugins                                                                              │
│   caching_sha2_password: SHA-256 with RSA key exchange; requires SSL or RSA public key exchange       │
│   mysql_native_password: SHA1-based legacy plugin; weaker; use only for old client compatibility      │
│   auth_socket: validates OS socket user = MySQL user; no password; secure for local root access       │
│                                                                                                       │
│   Plugin configuration                                                                                │
│   ALTER USER 'user'@'host' IDENTIFIED WITH caching_sha2_password BY 'pass': set plugin per user       │
│   default_authentication_plugin=mysql_native_password: server-wide fallback for legacy clients        │
│   SELECT user, plugin FROM mysql.user: audit which plugin each account uses                           │
│                                                                                                       │
│   SSL and client certificates                                                                         │
│   REQUIRE SSL: forces TLS for a user account; connection rejected without TLS                         │
│   REQUIRE X509: requires valid client certificate; adds mutual TLS to the account                     │
│   Generate certs: openssl req / openssl x509; configure ssl-ca, ssl-cert, ssl-key in my.cnf           │
│                                                                                                       │
│   Password policy                                                                                     │
│   validate_password component: enforces length, complexity, dictionary checks                         │
│   default_password_lifetime: force periodic rotation; set 0 to disable automatic expiry               │
│   ALTER USER 'user'@'host' PASSWORD EXPIRE: immediately expires; user must change on next login       │
│                                                                                                       │
│   Key terms:                                                                                          │
│   caching_sha2 = MySQL 8.0 default auth plugin; faster than native_password with RSA caching          │
│   auth_socket  = OS-level authentication; Linux socket validates connecting OS user identity          │
│   REQUIRE X509 = account-level mutual TLS enforcement; client must present a valid certificate        │
│   validate_password = server plugin enforcing password complexity and minimum length rules            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

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
