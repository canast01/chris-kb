---
tags:
  - linux
  - security
---
# MySQL / MariaDB — Hardening

<div class="kb-summary">
MySQL hardening — removing defaults, binding to specific interfaces, disabling LOAD DATA LOCAL, audit plugin, and CIS benchmark key controls.

*Applies to: RHEL / Ubuntu LTS*
</div>
![MySQL / MariaDB — Hardening](../../../../assets/compute-linux-mysql-security-hardening.svg)

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Post-Install Hardening Steps

```bash
# 1. Run secure installation wizard
sudo mysql_secure_installation
# Sets root password, removes anonymous users, disables remote root, removes test DB

# 2. Verify no anonymous users remain
mysql -u root -p -e "SELECT user, host FROM mysql.user WHERE user='';"

# 3. Verify no remote root access
mysql -u root -p -e "SELECT user, host FROM mysql.user WHERE user='root' AND host != 'localhost';"
```


```text title="Expected output"
Securing the MySQL server deployment.

Connecting to MySQL using a password.
Enter password: 

Validate Password Component status:
Status: INSTALLED
Validate password will check your password and improve security.

Please set the password for root here.
New password: 
Re-enter new password: 
The 'validate_password' component is installed on the server.
The subsequent steps will run with the existing configuration
of the 'validate_password' component.
By default, a MySQL user is created as follows:
   user name: root
   password: [your new password]
   ... All done!

Empty set (0.00 sec)

Empty set (0.00 sec)
```

!!! warning "Common errors"
    **`ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)`** — Verify the root password you entered is correct and was set during mysql_secure_installation.
    **`ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock'`** — Ensure the MySQL service is running with `sudo systemctl start mysql` or `sudo service mysql start`.
## Configuration Hardening (`mysqld.cnf`)

```ini
[mysqld]
# Bind to specific IP — never 0.0.0.0 in production
bind-address = 127.0.0.1

# Disable LOAD DATA LOCAL (file exfiltration risk)
local_infile = OFF

# Disable symbolic links
symbolic-links = 0

# Restrict file operations to datadir
secure_file_priv = /var/lib/mysql-files/

# Disable general query log in production (contains all queries including passwords)
general_log = OFF

# Enable slow query log for tuning
slow_query_log = ON
long_query_time = 2
```

## OS-Level Controls

```bash
# MySQL process should run as mysql user
ps aux | grep mysqld   # uid should be mysql

# Datadir permissions
ls -la /var/lib/mysql   # should be mysql:mysql 750

# Restrict config file
sudo chmod 640 /etc/mysql/mysql.conf.d/mysqld.cnf
sudo chown root:mysql /etc/mysql/mysql.conf.d/mysqld.cnf
```


```text title="Expected output"
mysql       1247  0.3  2.1 1234567 89012 ?        Ssl  09:15   0:42 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid
root        5678  0.0  0.0  12345  2048 pts/0    S+   09:22   0:00 grep --color=auto mysqld
total 48
drwxr-x---  6 mysql mysql  4096 Jan 15 10:30 .
drwxr-xr-x 13 root  root   4096 Jan 15 10:25 ..
-rw-r-----  1 mysql mysql  1234 Jan 15 10:30 ib_logfile0
-rw-r-----  1 mysql mysql  1234 Jan 15 10:30 ib_logfile1
-rw-r-----  1 mysql mysql 12582912 Jan 15 10:30 ibdata1
drwxr-x---  2 mysql mysql  4096 Jan 15 10:30 mysql
drwxr-x---  2 mysql mysql  4096 Jan 15 10:30 performance_schema
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`chmod: cannot access '/etc/mysql/mysql.conf.d/mysqld.cnf': No such file or directory`** — Verify the correct config path with `find /etc -name mysqld.cnf` as it may be in `/etc/mysql/conf.d/` or `/etc/my.cnf` depending on your distribution.
    **`chown: changing ownership of '/etc/mysql/mysql.conf.d/mysqld.cnf': No such file or directory`** — Ensure the file exists and the parent directory is readable; check if MySQL is installed with `dpkg -l | grep mysql-server` or `rpm -qa | grep mysql`.
## Audit Logging

```sql
-- MySQL Enterprise Audit (commercial) or MariaDB Audit Plugin
INSTALL PLUGIN server_audit SONAME 'server_audit.so';
SET GLOBAL server_audit_logging = ON;
SET GLOBAL server_audit_events = 'CONNECT,QUERY_DDL,QUERY_DML';
SET GLOBAL server_audit_file_path = '/var/log/mysql/audit.log';
```

## Key CIS Benchmark Controls

| Control | Check |
|---|---|
| No anonymous accounts | `SELECT user FROM mysql.user WHERE user=''` → 0 rows |
| No remote root | `SELECT host FROM mysql.user WHERE user='root' AND host != 'localhost'` → 0 rows |
| `local_infile = OFF` | `SHOW VARIABLES LIKE 'local_infile'` → OFF |
| `log_error` set | `SHOW VARIABLES LIKE 'log_error'` → path set |
| SSL enabled | `SHOW VARIABLES LIKE 'have_ssl'` → YES |

---

## See also

- [Mysql — Authentication](../authentication/)
- [Mysql — Access Control](../access-control/)
- [Mysql — Encryption](../encryption/)
