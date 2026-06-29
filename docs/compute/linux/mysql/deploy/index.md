---
tags:
  - deployment
  - linux
search:
  boost: 1.5
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
initial_configuration_etcmysqlmysqlc: "Initial Configuration (`/etc/mysql/mysql.conf.d/mysqld.cnf`)" {shape: rectangle}
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

---

## Verify

```bash
systemctl status <service-name>   # Active: running
journalctl -u <service-name> -n 20 --no-pager  # no ERROR lines
ss -tlnp | grep <port>            # service listening on expected port
```

---

## See also

- [Mysql — Procedures](../operations/procedures/)
- [Mysql — Common Issues](../troubleshooting/common-issues/)
- [Mysql — How It Works](../architecture/how-it-works/)
