---
tags:
  - security
  - windows
---
# SQL Server — Access Control

<div class="kb-summary">
SQL Server access control — logins vs users, server/database roles, GRANT/DENY/REVOKE, schema ownership, and auditing current permissions.
</div>

```text
┌───────────────────────────────────── SQL Server — Access Control ─────────────────────────────────────┐
│                                                                                                       │
│   Login = server-level principal; authenticates to the SQL Server instance                            │
│   User = database-level principal; mapped to a login; holds permissions within one database           │
│   sysadmin bypasses all permission checks — restrict to DBAs only; never use for app accounts         │
│                                                                                                       │
│   Login and user creation                                                                             │
│   CREATE LOGIN appuser WITH PASSWORD = '...'; (SQL auth)                                              │
│   CREATE LOGIN [DOMAIN\user] FROM WINDOWS; (Windows auth)                                             │
│   USE db; CREATE USER appuser FOR LOGIN appuser; (map login to db user)                               │
│                                                                                                       │
│   Server-level roles                                                                                  │
│   sysadmin: full control; equivalent to root — restrict tightly to DBA accounts only                  │
│   dbcreator: create/alter/drop databases; securityadmin: manage logins and permissions                │
│   serveradmin: server config only; bulkadmin: BULK INSERT operations                                  │
│                                                                                                       │
│   Database-level roles                                                                                │
│   db_owner: full control; db_datareader: SELECT all; db_datawriter: INSERT/UPDATE/DELETE              │
│   db_ddladmin: CREATE/ALTER/DROP objects, no data access; db_securityadmin: manage roles              │
│                                                                                                       │
│   Fine-grained permissions                                                                            │
│   GRANT EXECUTE ON dbo.usp_Proc TO user; DENY SELECT ON dbo.CreditCards TO user                       │
│   Audit: sys.database_permissions JOIN sys.database_principals                                        │
│                                                                                                       │
│   Key terms:                                                                                          │
│   login          = instance-level security principal; authenticates with password or Kerberos         │
│   user           = database-level mapping of a login; holds object-level permissions                  │
│   sysadmin       = server role with unrestricted access; bypasses all GRANT/DENY checks               │
│   DENY           = overrides GRANT; even if user has role granting SELECT, DENY wins                  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Login vs User

- **Login**: server-level principal — authenticates to SQL Server instance
- **User**: database-level principal — mapped to a login; has permissions within a database

```sql
-- Create a login
CREATE LOGIN appuser WITH PASSWORD = 'StrongPass1!';

-- Create a database user mapped to that login
USE app_prod;
CREATE USER appuser FOR LOGIN appuser;
```

## Server-Level Roles

| Role | Permissions |
|---|---|
| `sysadmin` | Full control; equivalent to root — restrict tightly |
| `dbcreator` | Create, alter, drop databases |
| `securityadmin` | Manage logins and permissions |
| `serveradmin` | Server config only |
| `bulkadmin` | BULK INSERT operations |

```sql
ALTER SERVER ROLE dbcreator ADD MEMBER dba_user;
```

## Database-Level Roles

| Role | Permissions |
|---|---|
| `db_owner` | Full control over database |
| `db_datareader` | SELECT on all tables |
| `db_datawriter` | INSERT, UPDATE, DELETE on all tables |
| `db_ddladmin` | CREATE/ALTER/DROP objects; no data access |
| `db_securityadmin` | Manage roles and permissions |

```sql
USE app_prod;
ALTER ROLE db_datareader ADD MEMBER appuser;
ALTER ROLE db_datawriter ADD MEMBER appuser;
```

## Fine-Grained GRANT / DENY

```sql
-- Grant execute on a specific stored procedure
GRANT EXECUTE ON dbo.usp_ProcessOrder TO appuser;

-- Deny direct table access (force through stored procedures)
DENY SELECT ON dbo.CreditCards TO appuser;
```

## Auditing Permissions

```sql
-- Server-level role memberships
SELECT r.name AS role, m.name AS member
FROM sys.server_role_members rm
JOIN sys.server_principals r ON r.principal_id = rm.role_principal_id
JOIN sys.server_principals m ON m.principal_id = rm.member_principal_id;

-- Database permissions
SELECT pr.name AS principal, pe.class_desc, pe.permission_name, pe.state_desc
FROM sys.database_permissions pe
JOIN sys.database_principals pr ON pr.principal_id = pe.grantee_principal_id
ORDER BY principal, permission_name;
```
