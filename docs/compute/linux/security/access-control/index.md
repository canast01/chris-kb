---
tags:
  - linux
  - security
---
# Linux — Access Control

```bash
# View permissions
ls -l /path/to/file

# Set owner and group
chown jsmith:developers /opt/app/config.cfg

# Set permissions — owner rw, group r, others none
chmod 640 /opt/app/config.cfg

# Set permissions recursively (files and directories)
find /opt/app -type f -exec chmod 640 {} \;
find /opt/app -type d -exec chmod 750 {} \;

# Sticky bit on shared directories — only owner can delete their files
chmod 1777 /tmp
chmod 1775 /opt/shared

# SGID on a directory — new files inherit group
chmod 2775 /opt/projects
```

```d2
direction: right

subject: "Subject\nProcess with SELinux label\ne.g. httpd_t" {shape: rectangle}
dacCheck: "dacCheck" {shape: rectangle}
audit: "AVC Denial logged\n/var/log/audit/audit.log" {shape: rectangle}
dacDeny: "DENY\n(DAC blocks" {shape: rectangle}
allow: "ALLOW\nAccess granted to object" {shape: rectangle}
object: "Object\nFile / Socket / Port\ne.g. httpd_sys_content_t" {shape: rectangle}
selinuxCheck: "selinuxCheck" {shape: rectangle}

subject -> dacCheck
audit -> dacDeny
allow -> object
```
```bash
# Check current mode
getenforce        # Enforcing / Permissive / Disabled
sestatus          # Detailed status including policy type

# Temporarily set to permissive (survives until reboot)
setenforce 0

# Permanently set mode in /etc/selinux/config
# SELINUX=enforcing   (enforcing | permissive | disabled)
# Requires reboot to take effect when changing disabled <-> enforcing
```
```bash
# View file context
ls -Z /var/www/html/

# View process context
ps -eZ | grep httpd

# View user context
id -Z

# Change file context
chcon -t httpd_sys_content_t /opt/webapp/public/
# Restore to policy default
restorecon -Rv /opt/webapp/public/

# Make a context change permanent (survives restorecon)
semanage fcontext -a -t httpd_sys_content_t "/opt/webapp/public(/.*)?"
restorecon -Rv /opt/webapp/public/
```
```bash
# List all booleans
getsebool -a

# Common web server booleans
getsebool httpd_can_network_connect
setsebool -P httpd_can_network_connect on   # -P = persistent

# Allow services to use NFS home directories
setsebool -P use_nfs_home_dirs on

# Allow SSSD to use LDAP
setsebool -P sssd_use_ldap on
```
```bash
# View recent AVC denials
ausearch -m avc --start recent | audit2why

# Generate a permissive policy module from denials (for testing)
ausearch -m avc --start recent | audit2allow -M mypolicy
semodule -i mypolicy.pp

# Check SELinux denials in journal
journalctl | grep "SELinux is preventing"

# sealert (setroubleshoot-server package) — human-readable denial explanations
sealert -a /var/log/audit/audit.log
```
```d2
direction: right

proc: "Process\ne.g. nginx" {shape: rectangle}
profileLoaded: "profileLoaded" {shape: rectangle}
complain: "Complain mode\nLog but allow" {shape: rectangle}
policyCheck: "policyCheck" {shape: rectangle}
allowed: "ALLOW\nOperation proceeds" {shape: rectangle}
denied: "DENY\nOperation blocked + logged" {shape: rectangle}
noProfile: "Unconfined\nNo restrictions" {shape: rectangle}
enforce: "enforce" {shape: rectangle}

proc -> profileLoaded
complain -> policyCheck
```
```bash
# Check status
aa-status

# List loaded profiles and their modes
aa-status 2>/dev/null | grep -E "enforce|complain"

# Set a profile to enforce mode
aa-enforce /etc/apparmor.d/usr.sbin.nginx

# Set a profile to complain (audit only, no blocking)
aa-complain /etc/apparmor.d/usr.sbin.nginx

# Reload a profile after editing
apparmor_parser -r /etc/apparmor.d/usr.sbin.nginx

# View denials
journalctl | grep "apparmor" | grep "DENIED" | tail -20
dmesg | grep "apparmor=\"DENIED\""
```
```bash
# /etc/apparmor.d/usr.local.bin.myapp
/usr/local/bin/myapp {
  # Allow read on config directory
  /etc/myapp/** r,
  # Allow read/write on data directory
  /var/lib/myapp/** rw,
  # Allow write on log file
  /var/log/myapp.log w,
  # Allow network (TCP)
  network tcp,
  # Deny everything else implicitly
}
```
```bash
visudo   # Always use visudo — validates syntax on save
```
```bash
# Separate duty: backup operator — only rsync and tar
%backupops  ALL=(root) /usr/bin/rsync, /usr/bin/tar

# Developers — restart application services only
%developers  ALL=(root) /usr/bin/systemctl restart app-*, /usr/bin/systemctl status app-*

# Network team — only network-related commands
%netops  ALL=(root) /usr/sbin/ip, /usr/sbin/ss, /usr/sbin/tcpdump

# Deny a specific command even within a permitted group
jsmith  ALL=(ALL) ALL, !/bin/su, !/usr/bin/passwd root
```
```bash
# Audit who has sudo access
grep -E "^[^#]" /etc/sudoers /etc/sudoers.d/* | grep -v "^Defaults"

# Check a specific user's sudo permissions
sudo -l -U jsmith
```
```bash
# /etc/security/access.conf format:
# permission : users/groups : origins
# + = allow, - = deny

# Allow root only from console and specific management host
+ : root : LOCAL 10.10.10.5
- : root : ALL

# Allow domain admin group from anywhere on the corporate network
+ : @linuxadmins : 10.0.0.0/8 .example.local
+ : @linuxadmins : LOCAL

# Allow all users from internal networks
+ : ALL : 10.0.0.0/8 192.168.0.0/16

# Deny all others
- : ALL : ALL
```
```bash
# /etc/pam.d/system-auth — enable pam_access
account     required      pam_access.so
```
```bash
# Make a file immutable
chattr +i /etc/resolv.conf

# Remove immutable flag
chattr -i /etc/resolv.conf

# Make a file append-only (useful for log files)
chattr +a /var/log/secure

# View attributes
lsattr /etc/resolv.conf
lsattr /var/log/
```
```bash
# View capabilities on a binary
getcap /usr/bin/ping
getcap /usr/sbin/tcpdump

# Grant a capability (instead of setuid root)
setcap cap_net_raw+ep /usr/sbin/tcpdump

# Remove all capabilities
setcap -r /usr/sbin/tcpdump

# View all binaries with capabilities
find / -xdev -type f -exec getcap {} \; 2>/dev/null

# View capabilities of a running process
cat /proc/<pid>/status | grep Cap
capsh --decode=<hex-value>
```
```bash
# Find world-writable files outside /tmp (should be none)
find / -xdev -type f -perm -0002 -not -path "/tmp/*" -not -path "/proc/*" 2>/dev/null

# Find setuid binaries
find / -xdev -type f -perm -4000 2>/dev/null

# Find setgid binaries
find / -xdev -type f -perm -2000 2>/dev/null

# Find files with no owner (orphaned)
find / -xdev -nouser -o -nogroup 2>/dev/null

# Check /etc/passwd for accounts with UID 0 (should only be root)
awk -F: '$3 == 0 { print $1 }' /etc/passwd

# Check for accounts with empty passwords
awk -F: '$2 == "" { print $1 }' /etc/shadow
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Linux — Authentication](../authentication/)
- [Linux — Hardening](../hardening/)
- [Linux — Encryption](../encryption/)
