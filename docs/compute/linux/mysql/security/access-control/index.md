---
tags:
  - linux
  - security
---
# MySQL / MariaDB — Access Control

<div class="kb-summary">
MySQL access control — user creation, GRANT/REVOKE, privilege hierarchy, role-based access, and auditing who has access to what.
</div>

```text
┌─────────────────────────────────────── MySQL — Access Control ────────────────────────────────────────┐
│                                                                                                       │
│   MySQL access control: user accounts are scoped to user@host — same username, different hosts        │
│   Principle of least privilege: each app gets its own account with only required privileges           │
│   Roles (MySQL 8.0+) simplify bulk privilege assignment across multiple service accounts              │
│                                                                                                       │
│   User management                                                                                     │
│   CREATE USER 'app'@'10.0.1.%' IDENTIFIED BY 'pass': restricts access to subnet only                  │
│   GRANT SELECT, INSERT, UPDATE ON db.* TO 'app'@'host': grant minimum required privileges             │
│   REVOKE ALL ON db.* FROM 'app'@'host': remove all privileges without dropping the user               │
│   DROP USER 'app'@'host': removes user account entirely                                               │
│                                                                                                       │
│   Privilege hierarchy                                                                                 │
│   Global (*.*)  → Database (db.*)  → Table (db.table)  → Column level                                 │
│   SUPER, PROCESS, REPLICATION SLAVE: powerful admin privs; restrict to DBA accounts only              │
│   SHOW GRANTS FOR 'user'@'host': audit what a specific account can do                                 │
│                                                                                                       │
│   Roles (MySQL 8.0+)                                                                                  │
│   CREATE ROLE 'app_rw'; GRANT SELECT, INSERT, UPDATE ON db.* TO 'app_rw'                              │
│   GRANT 'app_rw' TO 'user'@'host': assign role to user; SET DEFAULT ROLE to activate at login         │
│   SELECT * FROM information_schema.APPLICABLE_ROLES: shows roles available to current session         │
│                                                                                                       │
│   Key terms:                                                                                          │
│   user@host    = MySQL account identifier; 'app'@'%' matches all hosts, 'app'@'10.0.1.%' restricts    │
│   GRANT OPTION  = allows a user to grant their own privileges to others; rarely needed                │
│   mysql.user   = system table storing account definitions and hashed credentials                      │
│   FLUSH PRIVILEGES = reloads grant tables; needed after direct mysql.user table edits                 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## User Management

```sql
-- Create user restricted to app server subnet
CREATE USER 'appuser'@'10.0.1.%' IDENTIFIED BY 'StrongPassword1!';

-- Create read-only reporting user
CREATE USER 'reporter'@'10.0.2.10' IDENTIFIED BY 'ReportPass1!';

-- Drop user
DROP USER 'olduser'@'%';

-- Change password
ALTER USER 'appuser'@'10.0.1.%' IDENTIFIED BY 'NewPass1!';
```

## GRANT Statements

```sql
-- Application user: DML on one database
GRANT SELECT, INSERT, UPDATE, DELETE ON app_prod.* TO 'appuser'@'10.0.1.%';

-- Read-only access
GRANT SELECT ON reporting.* TO 'reporter'@'10.0.2.10';

-- DBA user: all on all
GRANT ALL PRIVILEGES ON *.* TO 'dba'@'localhost' WITH GRANT OPTION;

-- Apply changes
FLUSH PRIVILEGES;
```

## Roles (MySQL 8.0+)

```sql
-- Create a role
CREATE ROLE 'app_read', 'app_write';
GRANT SELECT ON app_prod.* TO 'app_read';
GRANT INSERT, UPDATE, DELETE ON app_prod.* TO 'app_write';

-- Assign role to user
GRANT 'app_read', 'app_write' TO 'appuser'@'10.0.1.%';
SET DEFAULT ROLE ALL TO 'appuser'@'10.0.1.%';
```

## Auditing Privileges

```sql
-- What can a specific user do?
SHOW GRANTS FOR 'appuser'@'10.0.1.%';

-- All users and their hosts
SELECT user, host, authentication_string FROM mysql.user;

-- All grants across all users
SELECT * FROM information_schema.USER_PRIVILEGES;

-- Object-level grants
SELECT * FROM information_schema.SCHEMA_PRIVILEGES WHERE GRANTEE LIKE '%appuser%';
```

## Privilege Hierarchy

| Level | Scope | Example |
|---|---|---|
| Global | All databases | `GRANT ALL ON *.*` |
| Database | One schema | `GRANT SELECT ON db.*` |
| Table | One table | `GRANT SELECT ON db.table` |
| Column | Specific columns | `GRANT SELECT (col1, col2) ON db.table` |
