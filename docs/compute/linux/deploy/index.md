---
tags:
  - deployment
  - linux
search:
  boost: 1.5
---
# Linux Server — Initial Deployment

<div class="kb-summary">
Linux Server initial deployment: OS install, NTP, syslog forwarding, hardening baseline, optional domain join, and post-install validation.

*Applies to: RHEL 9 / Rocky Linux 9 (Ubuntu equivalents noted)*
</div>

This guide covers deploying a new Linux server from OS install through hardening, NTP, syslog forwarding, and optional domain join. Steps apply to RHEL 9 / Rocky Linux 9; Ubuntu equivalents are noted where commands differ.

---

```d2
direction: right

plan: "Plan" {shape: oval}
install_the_os: "Install the OS" {shape: rectangle}
configure_network_static_ip: "Configure Network (Static IP)" {shape: rectangle}
configure_ntp: "Configure NTP" {shape: rectangle}
register_with_subscription_manager_r: "Register with Subscription Manager (RHEL)" {shape: rectangle}
apply_security_baseline: "Apply Security Baseline" {shape: rectangle}
configure_ssh_hardening: "Configure SSH Hardening" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> install_the_os
install_the_os -> configure_network_static_ip
configure_network_static_ip -> configure_ntp
configure_ntp -> register_with_subscription_manager_r
register_with_subscription_manager_r -> apply_security_baseline
apply_security_baseline -> configure_ssh_hardening
configure_ssh_hardening -> validate
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Install the OS

Boot from the RHEL/Rocky/Ubuntu Server ISO. Select **Minimal Install** (no GUI) to reduce the attack surface.

**Disk partitioning — recommended layout:**

| Mount Point | Minimum Size | Notes |
|-------------|-------------|-------|
| `/boot` | 1 GB | ext4 |
| `/boot/efi` | 600 MB | EFI systems only |
| `/` | 20 GB | xfs (RHEL) or ext4 (Ubuntu) |
| `/var` | 20 GB | Logs and spool; xfs |
| `/var/log` | 10 GB | Separate to prevent log flooding from filling `/` |
| `/home` | 10 GB | User data |
| `swap` | Equal to RAM (up to 8 GB) | |

Configure the network interface at install time if the installer supports it. Otherwise, configure it post-install as shown below.

---

## Configure Network (Static IP)

Use `nmcli` on RHEL/Rocky. On Ubuntu, edit `/etc/netplan/`.

**RHEL / Rocky:**

```bash
nmcli con mod <interface> \
    ipv4.addresses <IP>/<prefix> \
    ipv4.gateway <GW> \
    ipv4.dns "<DNS1> <DNS2>" \
    ipv4.method manual

nmcli con up <interface>
```


```text title="Expected output"
(no output — command completes silently)
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/42)
```

!!! warning "Common errors"
    **`Error: unknown or ambiguous command 'mod'.`** — Use `nmcli connection modify` or ensure NetworkManager version is 1.0+; older versions use `nmcli con modify` syntax differently.
    **`Error: Connection activation failed: No suitable device found for this connection.`** — Verify the interface name is correct with `nmcli device status` and ensure the device exists and is not already managed by another connection.
    **`Error: invalid prefix '24a' in address '<IP>/24a'.`** — Remove extra characters from the prefix value; it must be a number between 0–32 for IPv4 (e.g., `/24` not `/24a`).
Verify:

```bash
ip addr show <interface>
ip route
ping -c 3 <GW>
ping -c 3 8.8.8.8
```


```text title="Expected output"
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 52:54:00:a1:b2:c3 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.45/24 brd 192.168.1.255 scope global eth0
    inet6 fe80::5054:ff:fea1:b2c3/64 scope link
default via 192.168.1.1 dev eth0 proto kernel scope link src 192.168.1.45
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.45
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=1.23 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=1.45 ms
64 bytes from 192.168.1.1: icmp_seq=3 ttl=64 time=1.12 ms
--- 192.168.1.1 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=12.34 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=119 time=11.98 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=119 time=12.11 ms
--- 8.8.8.8 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2005ms
```

!!! warning "Common errors"
    **`Device "eth0" does not exist.`** — Replace `<interface>` with a valid interface name from `ip link show` output.
    **`ping: sendto: Operation not permitted`** — Ensure the user has sufficient privileges or run with `sudo`.
    **`ping: unknown host 8.8.8.8`** — Verify DNS resolution is working with `cat /etc/resolv.conf` and check network connectivity to the gateway first.
**Ubuntu (Netplan):**

Edit `/etc/netplan/00-installer-config.yaml`:

```yaml
network:
  version: 2
  ethernets:
    ens3:
      addresses:
        - <IP>/<prefix>
      routes:
        - to: default
          via: <GW>
      nameservers:
        addresses: [<DNS1>, <DNS2>]
      dhcp4: false
```

Apply:

```bash
netplan apply
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: invalid YAML in /etc/netplan/*.yaml`** — Validate YAML syntax with `netplan validate` before applying, or check for tabs instead of spaces in the configuration file.
    **`Error: Failed to apply network config: Permission denied`** — Run the command with `sudo netplan apply` as root or a user with sudo privileges.
    **`Error: Cannot find netplan executable`** — Install netplan with `apt install netplan.io` on Debian/Ubuntu systems where it may not be pre-installed.
---

## Configure NTP

Accurate time is required for Kerberos (domain join), log correlation, and certificate validity.

**RHEL / Rocky:**

```bash
dnf install chrony -y
systemctl enable --now chronyd
```


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 07 Dec 2024 14:22:18 UTC.
Dependencies resolved.
================================================================================
 Package             Arch         Version              Repository        Size
================================================================================
Installing:
 chrony              x86_64       4.3-1.fc39           fedora           566 kB

Transaction Summary
================================================================================
Install  1 Package

Total download size: 566 kB
Installed size: 1.3 MiB
Downloading Packages:
chrony-4.3-1.fc39.x86_64.rpm                       100% |████████| 566 kB
Running transaction
Preparing        :                                                        1/1
Installing       : chrony-4.3-1.fc39.x86_64.rpm                          1/1
Running scriptlet: chrony-4.3-1.fc39.x86_64.rpm                          1/1
Verifying        : chrony-4.3-1.fc39.x86_64.rpm                          1/1

Installed:
  chrony-4.3-1.fc39.x86_64

Complete!
Created symlink /etc/systemd/system/multi-user.target.wants/chronyd.service → /usr/lib/systemd/system/chronyd.service.
```

!!! warning "Common errors"
    **`Error: Unable to find a match: chrony`** — Ensure the system repositories are enabled with `dnf repolist` and run `dnf makecache` to refresh metadata.
    **`Error: Failed to enable unit: Unit file /usr/lib/systemd/system/chronyd.service not found.`** — Verify the chrony package installed successfully and check `/usr/lib/systemd/system/` for the chronyd.service file.
Edit `/etc/chrony.conf` — replace the default pool with your NTP server:

```text
server <NTP-server> iburst
```

Restart and verify:

```bash
systemctl restart chronyd
chronyc sources -v
chronyc tracking
```


```text title="Expected output"
(no output — command completes silently)
210 Number of sources = 4
  .-- Source mode  '^' = server, '=' = peer, '#' = local clock.
 / .- Sample mode  '+' = combined, '-' = not combined, '?' = not combined.
| /  .- Poll adjustment. '+' = adj. larger, '-' = adj. smaller.
|| /   - Leap status.  '+' = leap second pending, '-' = no leap second.
|| |
MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================================
^+ ntp1.example.com              2  10   377    42  -1.234ms[-1.456ms] +/-   12ms
^+ 91.189.89.199                 2  10   377    51  +2.341ms[+2.123ms] +/-   18ms
^- 162.159.200.123               3  10   377    38  +8.234ms[+8.012ms] +/-   45ms
^? 203.0.113.45                  0  10     0     -     +0ns[   +0ns] +/-    0ns

Reference ID    : C0A80101 (192.168.1.1)
Leap status     : Normal
RMS offset      : 1.234 ms
Frequency       : -2.341 ppm
Residual freq   : +0.012 ppm
Skew            : 1.456 ppm
Root delay      : 28.456 ms
Root dispersion : 34.123 ms
Update interval : 1024.5 s
Estimated error : 2.341 ms
```

!!! warning "Common errors"
    **`chronyd: command not found`** — Install chrony with `apt install chrony` (Debian/Ubuntu) or `yum install chrony` (RHEL/CentOS).
    **`Failed to restart chronyd.service: Unit chronyd.service not found.`** — Enable and start the service with `systemctl enable chronyd && systemctl start chronyd`.
    **`Permission denied`** — Run the commands with `sudo` or as the root user.
`Reference ID` should show your NTP server, and `System time` offset should be under 100ms.

**Ubuntu:**

```bash
timedatectl set-ntp true
timedatectl show-timesync
```


```text title="Expected output"
System clock synchronized: yes
              RTC adjusted: yes
       RTC time now: Wed 2024-01-17 14:32:18
       Time zone: UTC (UTC, +0000)
 Network time on: yes
NTP synchronized: yes
 RTC in local TZ: no
      DST active: n/a
       Leap sec: normal
Human time adjustment: 0
       Leap second: 0
       Poll interval: 34min 8s
      Frequency adjustment: +12.345ppm
```

!!! warning "Common errors"
    **`System has not been booted with systemd as init system (PID 1). Cannot operate.`** — Ensure the system is running systemd; this command is not compatible with other init systems like SysVinit.
    **`Failed to set ntp: Unit systemd-timesyncd.service not found.`** — Install or enable the systemd-timesyncd service with `systemctl enable systemd-timesyncd`.
---

## Register with Subscription Manager (RHEL)

If deploying RHEL (not Rocky/AlmaLinux), register with Red Hat Subscription Manager to enable package repos.

```bash
subscription-manager register \
    --username <redhat-user> \
    --password <redhat-password> \
    --auto-attach
```


```text title="Expected output"
Registering to: subscription.rhsm.redhat.com:443/subscription
The system has been registered with ID: 12a3b4c5-6d7e-8f9g-0h1i-2j3k4l5m6n7o
Installed Product Current Version Status:
Red Hat Enterprise Linux Server 8.6 (Ootpa) RHEL for x86_64 Subscribed
Installed Product Current Version Status:
Red Hat Enterprise Linux for SAP Applications 8.6 (Ootpa) Not Subscribed
Installed Product Current Version Status:
Red Hat Enterprise Linux (for High Availability) 8.6 (Ootpa) Not Subscribed
Installed Product Current Version Status:
Red Hat Enterprise Linux (for Resilient Storage) 8.6 (Ootpa) Not Subscribed
Installed Product Current Version Status:
Red Hat Enterprise Linux (for SAP) 8.6 (Ootpa) Not Subscribed
...
Installed Product Current Version Status:
Red Hat Enterprise Linux (for Real Time) 8.6 (Ootpa) Not Subscribed
Installed Product Current Version Status:
Red Hat Enterprise Linux (for NFV) 8.6 (Ootpa) Not Subscribed

Installed Product Current Version Status:
Red Hat Enterprise Linux Server 8.6 (Ootpa) Subscribed
```

!!! warning "Common errors"
    **`Error: Invalid username or password`** — Verify credentials are correct and the Red Hat account has active subscriptions.
    **`Error: This system is already registered`** — Run `subscription-manager unregister` first to clear the existing registration.
    **`Error: Unable to reach subscription.rhsm.redhat.com`** — Ensure the system has network connectivity and firewall rules allow HTTPS traffic to Red Hat's subscription servers.
Verify attached subscriptions:

```bash
subscription-manager status
subscription-manager list --consumed
```


```text title="Expected output"
+-------------------------------------------+
   System Status Details
+-------------------------------------------+
Overall Status: Current

System Purpose Status
Purpose Level: Self Support

Content Status
Red Hat Enterprise Linux Server (release 8.9)
Subscription Name: Red Hat Enterprise Linux Server, Standard (Physical or Virtual Nodes)
SKU: RH00604F5
Contract: 12345678
Serial: a1b2c3d4e5f6g7h8
Active: True
Quantity: 1
Starts: 06/15/2024
Ends: 06/14/2025
System Type: Physical

Subscription Name: Red Hat Satellite Infrastructure Subscription
SKU: RH00888ABC
Serial: x9y8z7w6v5u4t3s2
Active: True
Quantity: 1
Starts: 06/15/2024
Ends: 06/14/2025
```

!!! warning "Common errors"
    **`This system is not registered with an entitlement server. See your system administrator for more information.`** — Register the system using `subscription-manager register --username <user> --password <pass>` and attach a subscription with `subscription-manager attach --auto`.
    **`Traceback (most recent call last): ... dbus.exceptions.DBusException: org.freedesktop.DBus.Error.ServiceUnknown`** — Start the subscription manager daemon with `sudo systemctl start rhsmcertd` and ensure it is enabled.
For Rocky or AlmaLinux, repos are enabled by default — skip this step.

---

## Apply Security Baseline

Update all packages and install baseline security tooling.

```bash
# Full system update
dnf update -y

# Core security packages
dnf install -y aide firewalld

# Enable firewall
systemctl enable --now firewalld

# Verify SELinux is enforcing
sestatus
```


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 19 Dec 2024 14:22:18 UTC.
Dependencies resolved.
================================================================================
 Package                    Arch       Version              Repository   Size
================================================================================
Installing:
 kernel                     x86_64     6.8.2-1.fc40         updates     65 M
 systemd                    x86_64     255.4-1.fc40         updates     4.2 M
 glibc                      x86_64     2.39-4.fc40          updates     2.1 M

Complete! 47 packages upgraded, 8 newly installed.
Dependencies resolved.
================================================================================
 Package                    Arch       Version              Repository   Size
================================================================================
Installing:
 aide                       x86_64     0.18.5-1.fc40        fedora      456 k
 firewalld                  noarch     1.3.0-1.fc40         fedora      2.1 M

Complete! 2 packages installed.
Created symlink /etc/systemd/system/dbus-org.fedoraproject.FirewallD1.service → /usr/lib/systemd/unit/firewalld.service.
Created symlink /etc/systemd/system/multi-user.target.wants/firewalld.service → /usr/lib/systemd/unit/firewalld.service.
 firewalld.service - firewalld - dynamic firewall daemon
   Loaded: loaded (/usr/lib/systemd/unit/firewalld.service; enabled; preset: enabled)
   Active: active (running) since Thu 2024-12-19 14:23:45 UTC; 2s ago
     Docs: man:firewalld(1)
  Process: 8742 ExecStart=/usr/sbin/firewalld --nofork --nopid $FIREWALLD_ARGS (code=0/exited)
 Main PID: 8743 (firewalld)
    Tasks: 3 (limit: 4915)
   Memory: 42.3M
      CPU: 187ms
   CGroup: /system.slice/firewalld.service
           └─8743 /usr/sbin/firewalld --nofork --nopid

 SELinux status:                 enabled
 Current mode:                   enforcing
 Mode from config file:          enforcing
 Policy version:                 33
 Policy MLS status:              enabled
 Max logins before policy reload: 2147483647
 Process count:                  287
```

!!! warning "Common errors"
    **`Error: Unable to find a match: aide`** — Verify the EPEL or appropriate repository is enabled with `dnf repolist` and enable it if needed.
    **`Error: firewalld.service is masked`** — Unmask the service first with `systemctl unmask firewalld` before enabling it.
If SELinux is in permissive mode, set it to enforcing:

```bash
setenforce 1
sed -i 's/^SELINUX=permissive/SELINUX=enforcing/' /etc/selinux/config
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`setenforce: command not found`** — Install SELinux tools with `yum install policycoreutils-python-utils` or `apt install selinux-utils` depending on your distribution.
    **`sed: can't read /etc/selinux/config: No such file or directory`** — SELinux is not installed on this system; install it first with your package manager before attempting to configure it.
Initialise AIDE (file integrity baseline) — this takes several minutes:

```bash
aide --init
mv /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz
```


```text title="Expected output"
AIDE initialized.
Database has been successfully initialized.
(no output — command completes silently)
```

!!! warning "Common errors"
    **`aide: error while loading shared libraries: libmhash.so.2: cannot open shared object file`** — Install the libmhash library with `apt-get install libmhash2` (Debian/Ubuntu) or `yum install mhash` (RHEL/CentOS).
    **`mv: cannot stat '/var/lib/aide/aide.db.new.gz': No such file or directory`** — Verify the aide --init command completed successfully and check that /var/lib/aide/ directory exists with `ls -la /var/lib/aide/`.
Schedule a daily integrity check:

```bash
echo "0 3 * * * root /usr/sbin/aide --check" >> /etc/cron.d/aide
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`bash: /etc/cron.d/aide: Permission denied`** — Run the command with `sudo` to gain write access to the cron.d directory.
    **`bash: /etc/cron.d/aide: No such file or directory`** — Create the file first with `sudo touch /etc/cron.d/aide` or use `sudo tee` instead of `>>`.
---

## Configure SSH Hardening

Edit `/etc/ssh/sshd_config` to restrict SSH access:

```bash
# Disable root login
PermitRootLogin no

# Disable password authentication (key-based only)
PasswordAuthentication no

# Restrict to specific users or groups
AllowGroups sshusers wheel

# Use only strong ciphers
Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr
MACs hmac-sha2-512,hmac-sha2-256

# Reduce idle timeout
ClientAliveInterval 300
ClientAliveCountMax 2

# Disable X11 forwarding
X11Forwarding no
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`sshd: no hostkeys available -- exiting.`** — Ensure SSH host keys exist in `/etc/ssh/` before applying these settings; regenerate with `ssh-keygen -A` if missing.
    **`sshd_config: line X: Bad cipher type 'aes256-gcm@openssh.com'`** — Verify your OpenSSH version supports the specified ciphers; use `ssh -Q cipher` to list available options and adjust accordingly.
    **`AllowGroups: no such group 'sshusers'`** — Create the required groups with `groupadd sshusers` and `groupadd wheel` before applying the configuration, or use existing groups.
Validate the configuration and restart:

```bash
sshd -t
systemctl restart sshd
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`sshd: no hostkeys available -- exiting.`** — Generate SSH host keys with `ssh-keygen -A` before starting sshd.
    **`Job for ssh.service failed because the control process exited with error code.`** — Check `/etc/ssh/sshd_config` for syntax errors using `sshd -t` and review `/var/log/auth.log` for details.
Open the SSH port in the firewall:

```bash
firewall-cmd --permanent --add-service=ssh
firewall-cmd --reload
```


```text title="Expected output"
success
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: INVALID_SERVICE: ssh not available`** — Verify the service is defined in `/etc/firewalld/services/ssh.xml` or use `firewall-cmd --get-services` to list available services.
    **`Error: COMMAND_FAILED: '/usr/sbin/iptables -t filter -I INPUT_direct -p tcp -m tcp --dport 22 -j ACCEPT' failed`** — Ensure firewalld is running with `systemctl start firewalld` and iptables/nftables backend is properly configured.
---

## Configure Syslog Forwarding

Forward logs to a central syslog server (e.g., a SIEM or syslog aggregator).

```bash
dnf install rsyslog -y
systemctl enable --now rsyslog
```


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 19 Dec 2024 14:22:18 UTC.
Dependencies resolved.
================================================================================
 Package             Arch         Version              Repository        Size
================================================================================
Installing:
 rsyslog             x86_64       8.2102.0-109.el9     appstream        664 k

Transaction Summary
================================================================================
Install  1 Package

Total download size: 664 k
Installed size: 1.8 M
Downloading Packages:
rsyslog-8.2102.0-109.el9.x86_64.rpm                    892 kB/s | 664 kB     00:01
Running transaction
Preparing        :                                                        1/1
Installing       : rsyslog-8.2102.0-109.el9.x86_64                       1/1
Running scriptlets: rsyslog-8.2102.0-109.el9.x86_64                       1/1
Verifying        : rsyslog-8.2102.0-109.el9.x86_64                       1/1

Complete!
Created symlink /etc/systemd/system/syslog.target.wants/rsyslog.service → /usr/lib/systemd/system/rsyslog.service.
```

!!! warning "Common errors"
    **`Error: Unable to find a match: rsyslog`** — Verify repository access with `dnf repolist` and ensure appstream repository is enabled.
    **`Failed to enable unit: Unit file /usr/lib/systemd/system/rsyslog.service not found.`** — Confirm the package installed successfully with `rpm -q rsyslog` before enabling the service.
Add a remote target to `/etc/rsyslog.conf`:

```text
# Forward all logs to central syslog server (TCP)
*.* @@<syslog-server>:514
```

Restart and verify forwarding:

```bash
systemctl restart rsyslog
logger -p local0.info "Test message from $(hostname)"
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Failed to restart rsyslog.service: Unit rsyslog.service not found.`** — Install rsyslog with `apt-get install rsyslog` (Debian/Ubuntu) or `yum install rsyslog` (RHEL/CentOS), then retry the restart.
    **`sudo: systemctl: command not found`** — Run the command with `sudo systemctl restart rsyslog` or as the root user, as systemctl requires elevated privileges.
Confirm the test message appears on the syslog server.

---

## Domain Join (if required)

Join the server to Active Directory using `realmd` and `sssd`.

```bash
dnf install -y sssd realmd oddjob oddjob-mkhomedir adcli samba-common-tools

# Discover the domain
realm discover corp.local

# Join the domain
realm join --user=<domain-admin> corp.local
```


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 19 Dec 2024 14:22:18 UTC.
Dependencies resolved.
================================================================================
 Package                      Arch       Version              Repository   Size
================================================================================
Installing:
 sssd                         x86_64     2.9.1-4.el9          baseos      1.2 M
 realmd                       x86_64     0.17.10-1.el9        baseos      412 k
 oddjob                       x86_64     0.34.7-2.el9         baseos      98 k
 oddjob-mkhomedir            x86_64     0.34.7-2.el9         baseos      52 k
 adcli                        x86_64     0.9.2-2.el9          baseos      156 k
 samba-common-tools          x86_64     4.18.5-2.el9         baseos      2.1 M
...
Complete! 

 realm-name: CORP.LOCAL
 kerberos-realm: CORP.LOCAL
 configured: kerberos-password
 server-software: active-directory
 client-software: sssd
 required-package: sssd
 required-package: adcli
 required-package: samba-common-tools

Password for corp-admin@CORP.LOCAL:
 * Successfully enrolled machine in realm
```

!!! warning "Common errors"
    **`realm: Couldn't resolve host: corp.local`** — Verify DNS resolution with `nslookup corp.local` and ensure the domain controller is reachable on port 389/636.
    **`adcli: couldn't connect to corp.local: SASL(-1): generic failure`** — Confirm the domain admin credentials are correct and the user account has permission to join computers to the domain.
    **`Error: Failed to start sssd.service`** — Run `systemctl status sssd` to check logs, then verify `/etc/sssd/sssd.conf` has correct domain and server settings.
Verify join status:

```bash
realm list
id <domain-user>@corp.local
```


```text title="Expected output"
corp.local
  type: kerberos
  realm-name: CORP.LOCAL
  domain-name: corp.local
  configured: kerberos-member
  server-software: active-directory
  client-software: sssd
  uid=1234601106(domain-user@corp.local) gid=1234600513(domain users@corp.local) groups=1234600513(domain users@corp.local),1234600512(domain admins@corp.local)
```

!!! warning "Common errors"
    **`realm: command not found`** — Install the realmd package with `sudo apt-get install realmd` or `sudo yum install realmd`.
    **`id: domain-user@corp.local: no such user`** — Ensure the domain user is enrolled in the realm with `sudo realm join corp.local` and SSSD is running via `sudo systemctl restart sssd`.
Configure home directory creation on first login:

```bash
authselect select sssd with-mkhomedir --force
systemctl enable --now oddjobd
```


```text title="Expected output"
Selecting sssd with-mkhomedir...
Backup stored at /etc/authselect/backups/2024-01-15-14-32-45-user
Profile installed successfully.
Created symlink /etc/systemd/system/multi-user.target.wants/oddjobd.service → /etc/systemd/system/oddjobd.service.
oddjobd.service is being started.
```

!!! warning "Common errors"
    **`Error: Profile 'sssd with-mkhomedir' was not found.`** — Verify the profile name is correct and run `authselect list-profiles` to see available options.
    **`Unit oddjobd.service could not be found.`** — Install the oddjob package first with `yum install oddjob` or `apt install oddjob`.
Restrict SSH access to specific AD groups:

```bash
realm permit -g "Linux Admins"
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`realm: command not found`** — Install the realmd package with `sudo apt-get install realmd` (Debian/Ubuntu) or `sudo yum install realmd` (RHEL/CentOS).
    **`Error: Couldn't find realm configuration for domain`** — Ensure the system is already joined to an Active Directory domain with `realm join domain.com` before granting permissions.
---

## Validate the Deployment

Run the following checks and confirm all pass before handing off the server.

```bash
# No failed services
systemctl --failed

# Network connectivity
ping -c 3 <gateway>
ping -c 3 <DNS-server>
nslookup corp.local

# NTP sync status
timedatectl status
chronyc tracking

# SELinux enforcing
sestatus

# Firewall active
firewall-cmd --state
firewall-cmd --list-all

# SSH hardening confirmed
sshd -T | grep -E 'permitrootlogin|passwordauthentication'
```


```text title="Expected output"
(no output — command completes silently)

PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.
64 bytes from 10.0.0.1: icmp_seq=1 ttl=64 time=2.14 ms
64 bytes from 10.0.0.1: icmp_seq=2 ttl=64 time=1.98 ms
64 bytes from 10.0.0.1: icmp_seq=3 ttl=64 time=2.05 ms

PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=18.42 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=119 time=17.89 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=119 time=18.21 ms

Server:		10.0.0.2
Address:	10.0.0.2#53

Name:	corp.local
Address: 10.20.30.40

               Local time: Wed 2024-01-17 14:32:18 UTC
           Universal time: Wed 2024-01-17 14:32:18 UTC
                 RTC time: Wed 2024-01-17 14:32:18
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
                 RTC in UTC: yes

Reference ID    : 91F2A8C1 (ntp.ubuntu.com)
Stratum         : 2
Root distance   : 0.038472 seconds
Update interval : 1024.0 seconds
Leap status     : Normal

SELinux status:                 enabled
Current mode:                   enforcing
Mode from config file:          enforcing

active

public
  target: default
  icmp-block-inversion: no
  interfaces: eth0
  sources: 
  services: ssh
  ports: 
  protocols: 
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 

permitrootlogin no
passwordauthentication no
```

!!! warning "Common errors"
    **`ping: <gateway>: Name or service not known`** — Replace `<gateway>` and `<DNS-server>` placeholders with actual IP addresses (e.g., `10.0.0.1` and `8.8.8.8`).
    **`nslookup: command not found`** — Install `bind-utils` (RHEL/CentOS) or `dnsutils` (Debian/Ubuntu) package.
    **`Unit chrony.service could not be found`** — Verify NTP daemon is installed and running with `systemctl status chrony` or `systemctl status ntpd`.
Expected results: `systemctl --failed` returns empty, `sestatus` shows `SELinux status: enabled` and `Current mode: enforcing`, and SSH hardening settings match what was configured.

---

## Verify

```bash
systemctl status <service-name>   # Active: running
journalctl -u <service-name> -n 20 --no-pager  # no ERROR lines
ss -tlnp | grep <port>            # service listening on expected port
```


```text title="Expected output"
● nginx.service - The NGINX HTTP and reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2h 45min ago
       Docs: man:nginx(1)
    Process: 2847 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
   Main PID: 2851 (nginx)
      Tasks: 3 (limit: 4915)
     Memory: 12.4M
        CPU: 2.3s
     CGroup: /system.slice/nginx.service
             ├─2851 nginx: master process /usr/sbin/nginx
             ├─2852 nginx: worker process
             └─2853 nginx: worker process

Jan 15 14:32:18 prod-web-01 systemd[1]: Starting The NGINX HTTP and reverse proxy server...
Jan 15 14:32:18 prod-web-01 systemd[1]: Started The NGINX HTTP and reverse proxy server.
Jan 15 14:32:45 prod-web-01 nginx[2851]: 192.168.1.100 - - [15/Jan/2024:14:32:45 +0000] "GET / HTTP/1.1" 200 612
Jan 15 14:35:12 prod-web-01 nginx[2851]: 192.168.1.105 - - [15/Jan/2024:14:35:12 +0000] "GET /api/health HTTP/1.1" 200 45

LISTEN  0  511  0.0.0.0:80   0.0.0.0:*  users:(("nginx",pid=2851,fd=6),("nginx",pid=2852,fd=6),("nginx",pid=2853,fd=6))
LISTEN  0  511  0.0.0.0:443  0.0.0.0:*  users:(("nginx",pid=2851,fd=7),("nginx",pid=2852,fd=7),("nginx",pid=2853,fd=7))
```

!!! warning "Common errors"
    **`Unit <service-name>.service could not be found.`** — Verify the correct service name with `systemctl list-units --type=service` and check for typos.
    **`Permission denied`** — Run the commands with `sudo` or as root to access systemd and socket information.
    **`(no output from ss command)`** — Confirm the service is actually listening on the expected port and that the port number in the grep filter matches the service configuration.
---

## See also

- [Linux — Procedures](../operations/procedures/)
- [Linux — Common Issues](../troubleshooting/common-issues/)
- [Linux — How It Works](../architecture/how-it-works/)
