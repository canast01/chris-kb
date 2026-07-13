---
tags:
  - deployment
  - linux
search:
  boost: 1.5
description: "MySQL initial deployment — installation on RHEL/Ubuntu, post-install hardening, root password setup, firewall rules, and first-connection validation."
---
# MySQL / MariaDB — Initial Deployment

<div class="kb-summary">
MySQL initial deployment — installation on RHEL/Ubuntu, post-install hardening, root password setup, firewall rules, and first-connection validation.

*Applies to: RHEL / Ubuntu LTS*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
install_on_rhel_rocky: "Install on RHEL / Rocky" {shape: rectangle}
install_on_ubuntu_debian: "Install on Ubuntu / Debian" {shape: rectangle}
postinstall_hardening: "Post-Install Hardening" {shape: rectangle}
initial_configuration_etcmysqlmysqlc: "Initial Configuration\n(`/etc/mysql/mysql.conf.d/mysqld.cnf`)" {shape: rectangle}
firewall: "Firewall" {shape: rectangle}
firstconnection_validation: "First-Connection Validation" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> install_on_rhel_rocky
install_on_rhel_rocky -> install_on_ubuntu_debian
install_on_ubuntu_debian -> postinstall_hardening
postinstall_hardening -> initial_configuration_etcmysqlmysqlc
initial_configuration_etcmysqlmysqlc -> firewall
firewall -> firstconnection_validation
firstconnection_validation -> validate
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Install on RHEL / Rocky

```bash
# MySQL 8.0 from official repo
sudo dnf install -y https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm
sudo dnf install -y mysql-community-server
sudo systemctl enable --now mysqld

# Get temporary root password
sudo grep 'temporary password' /var/log/mysqld.log
```


```text title="Expected output"
Last metadata expiration check: 0:00:15 ago on Thu Dec 19 14:32:18 2024.
mysql80-community-release-el9-1.noarch.rpm                                   45 kB/s |  18 kB     00:00
Dependencies resolved.
================================================================================
 Package                    Architecture  Version              Repository  Size
================================================================================
Installing:
 mysql-community-server     x86_64        8.0.35-0.el9         mysql80-c  500 MB

Transaction Summary
================================================================================
Install  1 Package

Total download size: 500 MB
Installed size: 2.2 GB
Downloading Packages:
mysql-community-server-8.0.35-0.el9.x86_64.rpm              2.3 MB/s | 500 MB     03:42
Running transaction
Preparing        :                                                        1/1
Installing       : mysql-community-server-8.0.35-0.el9.x86_64             1/1
Verifying        : mysql-community-server-8.0.35-0.el9.x86_64             1/1

Complete!
Created symlink /etc/systemd/system/multi-user.target.wants/mysqld.service → /usr/lib/systemd/system/mysqld.service.
2024-12-19T14:35:22.847392Z 0 [System] [MY-013169] [Server] /usr/sbin/mysqld (mysqld 8.0.35) initializing of server in progress as process 4521
2024-12-19T14:35:28.392847Z 6 [Note] [MY-000000] [Server] A temporary password is generated for root@localhost: Kx#mP9$vL2wQ
```

!!! warning "Common errors"
    **`Error: Failed to download repository metadata`** — Verify internet connectivity and ensure the MySQL repository URL is accessible from your network.
    **`grep: /var/log/mysqld.log: No such file or directory`** — Wait 10-15 seconds after `systemctl enable --now mysqld` completes for the log file to be created, or check `/var/log/mysql/mysqld.log` if using a custom log path.
## Install on Ubuntu / Debian

```bash
sudo apt update && sudo apt install -y mysql-server
sudo systemctl enable --now mysql
```


```text title="Expected output"
Get:1 http://archive.ubuntu.com/ubuntu focal InRelease [265 kB]
Get:2 http://archive.ubuntu.com/ubuntu focal-updates InRelease [114 kB]
Get:3 http://archive.ubuntu.com/ubuntu focal-security InRelease [114 kB]
Fetched 493 kB in 2s (246 kB/s)
Reading package lists... Done
Reading state information... Done
The following NEW packages will be installed:
  mysql-server mysql-client mysql-common libmysqlclient21
Processing triggers for systemd (245.4-4ubuntu3.6) ...
Setting up mysql-server (8.0.23-0ubuntu0.20.04.1) ...
Created symlink /etc/systemd/system/multi-user.target.wants/mysql.service → /lib/systemd/system/mysql.service.
```

!!! warning "Common errors"
    **`E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)`** — Run the command with `sudo` or ensure your user has passwordless sudo configured.
    **`Unit mysql.service could not be found.`** — Install mysql-server first before enabling the service, or verify the package name matches your distribution (use `apt search mysql-server`).
## Post-Install Hardening

```bash
# Run secure installation wizard
sudo mysql_secure_installation
# Prompts: set root password, remove anonymous users, disallow remote root, remove test DB
```


```text title="Expected output"
Securing the MySQL server deployment.

Enter password for user root: 
The 'validate_password' component is installed on the server.
The subsequent steps will run with the default Low Level of checks.
Please set the password for root here.

New password: 
Re-enter new password: 
By default, a MySQL installation has an anonymous user, allowing anyone
to log into MySQL without having to have a user account. This is intended
only for testing, and to make the installation go a bit smoother
you should remove them before moving into a production environment.

Remove anonymous users? (Press y|Y for Yes, any other key for No) : y
 ... Success!

Normally, root should only be allowed to connect from 'localhost'. This
ensures that someone cannot guess at the root password over the network.

Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y
 ... Success!

By default, MySQL comes with a database named 'test' that anyone can
access. This should be removed before moving into a production environment.

Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y
 ... Success!

Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.

Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y
 ... Success!

All done!
```

!!! warning "Common errors"
    **`ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)`** — Verify the root password you entered matches what you typed in the confirmation prompt, or reset it with `sudo mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword';"`
    **`Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)`** — Ensure the MySQL service is running with `sudo systemctl start mysql` before running the secure installation wizard.
## Initial Configuration (`/etc/mysql/mysql.conf.d/mysqld.cnf`)

```ini
[mysqld]
bind-address            = 127.0.0.1   # or specific IP; never 0.0.0.0 without firewall
max_connections         = 200
innodb_buffer_pool_size = 2G          # adjust to 70% of RAM
innodb_log_file_size    = 512M
slow_query_log          = 1
slow_query_log_file     = /var/log/mysql/slow.log
long_query_time         = 2
```

## Firewall

```bash
# Allow MySQL only from app server subnet
sudo firewall-cmd --add-rich-rule='rule family=ipv4 source address=10.0.1.0/24 port port=3306 protocol=tcp accept' --permanent
sudo firewall-cmd --reload
```


```text title="Expected output"
success
success
```

!!! warning "Common errors"
    **`Error: INVALID_RULE: rule family=ipv4 source address=10.0.1.0/24 port port=3306 protocol=tcp accept: bad attribute`** — Remove the duplicate "port" keyword; the correct syntax is `source address=10.0.1.0/24 port protocol=tcp port=3306 accept`.
    **`Error: COMMAND_FAILED: '/usr/sbin/firewall-cmd --add-rich-rule=...' exited with status 1: org.fedoraproject.FirewallD1.Exception: INVALID_RULE`** — Ensure firewalld is running with `sudo systemctl start firewalld` before adding rules.
## First-Connection Validation

```bash
mysql -u root -p -e "SELECT version(); SHOW VARIABLES LIKE 'innodb_buffer_pool_size';"
# Expect: 8.x.x and configured value
```


```text title="Expected output"
mysql: [Warning] Using a password on the command line interface can be insecure.
+-----------+
| version() |
+-----------+
| 8.0.35-0ubuntu0.20.04.1 |
+-----------+
+---------------------------+----------------------+
| Variable_name             | Value                |
+---------------------------+----------------------+
| innodb_buffer_pool_size   | 1073741824           |
+---------------------------+----------------------+
```

!!! warning "Common errors"
    **`Access denied for user 'root'@'localhost' (using password: YES)`** — Verify the root password is correct and the MySQL service is running with `systemctl status mysql`.
    **`ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock'`** — Start the MySQL service with `systemctl start mysql` and confirm the socket file exists.
## Create Application User

```sql
CREATE USER 'appuser'@'10.0.1.%' IDENTIFIED BY '<strong-password>';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_prod.* TO 'appuser'@'10.0.1.%';
FLUSH PRIVILEGES;
```

---

## Verify

```bash
systemctl status <service-name>   # Active: running
journalctl -u <service-name> -n 20 --no-pager  # no ERROR lines
ss -tlnp | grep <port>            # service listening on expected port
```


```text title="Expected output"
● mysql.service - MySQL Community Server
     Loaded: loaded (/usr/lib/systemd/system/mysql.service; enabled; vendor preset: disabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2h 45min ago
       Docs: man:mysqld(8)
   Main PID: 3847 (mysqld)
      Tasks: 27 (limit: 4915)
     Memory: 287.4M
        CPU: 2min 34.821s
     CGroup: /system.slice/mysql.service
             └─3847 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysql/mysql.pid

Jan 15 14:32:18 db-prod-01 systemd[1]: Started MySQL Community Server.
Jan 15 14:32:19 db-prod-01 mysqld[3847]: 2024-01-15T14:32:19.234567Z 0 [System] [MY-013169] [Server] /usr/sbin/mysqld: ready for connections.
Jan 15 14:32:20 db-prod-01 mysqld[3847]: 2024-01-15T14:32:20.456789Z 2 [Note] [MY-000000] [Server] Event Scheduler: Loaded 3 events

LISTEN     0      80                 127.0.0.1:3306            0.0.0.0:*      users:(("mysqld",pid=3847,fd=42))
```

!!! warning "Common errors"
    **`Active: inactive (dead)`** — Run `systemctl start mysql` to start the service, then verify with `systemctl status mysql`.
    **`Job for mysql.service failed because the control process exited with error code`** — Check `/var/log/mysql/error.log` for startup errors and ensure `/var/lib/mysql` has correct permissions (`chown -R mysql:mysql /var/lib/mysql`).
    **`Address already in use`** — Verify no other MySQL instance is running on port 3306 with `lsof -i :3306` and kill conflicting processes if needed.
---

## See also

- [Mysql — Procedures](../operations/procedures/)
- [Mysql — Common Issues](../troubleshooting/common-issues/)
- [Mysql — How It Works](../architecture/how-it-works/)
