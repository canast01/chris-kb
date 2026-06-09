# MySQL / MariaDB — Initial Deployment

<div class="kb-summary">
MySQL initial deployment — installation on RHEL/Ubuntu, post-install hardening, root password setup, firewall rules, and first-connection validation.
</div>

```text
┌───────────────────────────────────── MySQL — Deployment Overview ─────────────────────────────────────┐
│                                                                                                       │
│   Install from the official MySQL repo (not distro packages — they lag in version)                    │
│   Post-install hardening is mandatory before the server accepts any application connections           │
│   Validate with: systemctl status mysqld, mysql_secure_installation, and a test connection            │
│                                                                                                       │
│   Installation (RHEL/Rocky)                                                                           │
│   Add MySQL 8.0 repo: dnf install mysql80-community-release RPM                                       │
│   Install: dnf install mysql-community-server; systemctl enable --now mysqld                          │
│   Get temporary root password: grep 'temporary password' /var/log/mysqld.log                          │
│                                                                                                       │
│   Installation (Ubuntu/Debian)                                                                        │
│   Add MySQL apt repo: dpkg -i mysql-apt-config*.deb; apt update                                       │
│   Install: apt install mysql-server; service starts automatically on install                          │
│                                                                                                       │
│   Post-install hardening                                                                              │
│   mysql_secure_installation: change root password, remove anonymous users, disable remote root        │
│   Remove test database; reload privilege tables after changes                                         │
│   Set bind-address = 127.0.0.1 in my.cnf if no remote connections required                            │
│   Firewall: allow TCP 3306 only from app server IPs; deny all other inbound                           │
│                                                                                                       │
│   Validation                                                                                          │
│   systemctl status mysqld: service active and running                                                 │
│   mysql -u root -p -e "SHOW DATABASES;": root login works with new password                           │
│   ss -tlnp | grep 3306: MySQL is listening on the expected interface only                             │
│                                                                                                       │
│   Key terms:                                                                                          │
│   mysql_secure_installation = post-install script; removes unsafe defaults from fresh install         │
│   bind-address  = my.cnf parameter; restricts MySQL to listen on specific network interface           │
│   my.cnf        = MySQL main configuration file; /etc/mysql/my.cnf or /etc/my.cnf                     │
│   tmpdir        = directory for temp tables; ensure sufficient space for large sort operations        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Install on RHEL / Rocky

```bash
# MySQL 8.0 from official repo
sudo dnf install -y https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm
sudo dnf install -y mysql-community-server
sudo systemctl enable --now mysqld

# Get temporary root password
sudo grep 'temporary password' /var/log/mysqld.log
```

## Install on Ubuntu / Debian

```bash
sudo apt update && sudo apt install -y mysql-server
sudo systemctl enable --now mysql
```

## Post-Install Hardening

```bash
# Run secure installation wizard
sudo mysql_secure_installation
# Prompts: set root password, remove anonymous users, disallow remote root, remove test DB
```

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

## First-Connection Validation

```bash
mysql -u root -p -e "SELECT version(); SHOW VARIABLES LIKE 'innodb_buffer_pool_size';"
# Expect: 8.x.x and configured value
```

## Create Application User

```sql
CREATE USER 'appuser'@'10.0.1.%' IDENTIFIED BY '<strong-password>';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_prod.* TO 'appuser'@'10.0.1.%';
FLUSH PRIVILEGES;
```
