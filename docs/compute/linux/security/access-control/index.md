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

```text title="Expected output"
Enforcing
SELinux status:                 enabled
Current mode:                   enforcing
Mode from config file:          enforcing
Policy version:                 31
Policy MLS status:              enabled
Max kernel policy version:       33

Current mode changed from enforcing to permissive
SELinux status:                 enabled
Current mode:                   permissive
Mode from config file:          enforcing
Policy version:                 31
Policy MLS status:              enabled
Max kernel policy version:       33
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `setenforce: SELinux is disabled` | Enable SELinux in `/etc/selinux/config` and reboot, or verify SELinux is not already disabled. |
    | `getenforce: command not found` | Install the `policycoreutils` package using `yum install policycoreutils` or `apt install selinux-utils`. |
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

```text title="Expected output"
-rw-r--r--. root root system_u:object_r:httpd_sys_content_t:s0 index.html
-rw-r--r--. root root system_u:object_r:httpd_sys_content_t:s0 config.php
drwxr-xr-x. root root system_u:object_r:httpd_sys_rw_content_t:s0 uploads/
-rw-r--r--. root root system_u:object_r:admin_home_t:s0 .htaccess

root     2847 ?  Ss  system_u:system_r:httpd_t:s0        /usr/sbin/httpd -DFOREGROUND
apache   2891 ?  S   system_u:system_r:httpd_t:s0        /usr/sbin/httpd -DFOREGROUND
apache   2892 ?  S   system_u:system_r:httpd_t:s0        /usr/sbin/httpd -DFOREGROUND

uid=0(root) gid=0(root) groups=0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023

Relabeled /opt/webapp/public/
Relabeled /opt/webapp/public/index.html
Relabeled /opt/webapp/public/style.css
Relabeled /opt/webapp/public/script.js
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `chcon: can't apply partial context to unlabeled file` | Ensure SELinux is enabled with `getenforce` and the filesystem is mounted with `context=` option if needed. |
    | `restorecon: No such file or directory` | Verify the path exists and check spelling; use `ls -d /opt/webapp/public/` to confirm the directory is present. |
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

```text title="Expected output"
abrt_anon_write --> off
abrt_handle_event --> off
antivirus_can_scan_system --> off
antivirus_use_jit --> off
...
httpd_can_network_connect --> off
httpd_can_network_connect_db --> off
httpd_can_sendmail --> off
...
httpd_can_network_connect --> off
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `getsebool: command not found` | Install the policycoreutils package with `yum install policycoreutils` or `apt install selinux-utils`. |
    | `Cannot set persistent booleans without SELinux policy loaded` | Ensure SELinux is enabled and a policy is loaded by checking `getenforce` and `sestatus`. |
    | `setsebool: Cannot access policy master file` | Run the command with `sudo` or as root, since SELinux boolean changes require elevated privileges. |
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

```text title="Expected output"
apparmor module is loaded.
29 profiles are loaded.
25 profiles are in enforce mode.
4 profiles are in complain mode.

enforce
  /usr/sbin/man
  /usr/bin/man
complain
  /usr/sbin/nginx
  /usr/sbin/apache2

Setting /etc/apparmor.d/usr.sbin.nginx to enforce mode.
(no output — command completes silently)
(no output — command completes silently)
Reloading /etc/apparmor.d/usr.sbin.nginx.
(no output — command completes silently)

Nov 15 09:42:17 web-prod-01 kernel: apparmor="DENIED" operation="open" profile="nginx" name="/etc/shadow" pid=2847 comm="nginx" requested_mask="r" denied_mask="r" fsuid=33 ouid=0
Nov 15 09:41:53 web-prod-01 kernel: apparmor="DENIED" operation="capable" profile="nginx" pid=2841 comm="nginx" capability=36 capname="block_suspend"
Nov 15 09:40:12 web-prod-01 kernel: apparmor="DENIED" operation="mknod" profile="nginx" name="/var/run/nginx.sock" pid=2839 comm="nginx" requested_mask="c" denied_mask="c"
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `apparmor module is not loaded.` | Load AppArmor with `sudo systemctl start apparmor` and verify with `sudo systemctl enable apparmor`. |
    | `Error: Could not open '/etc/apparmor.d/usr.sbin.nginx' for reading: No such file or directory` | Verify the profile path exists with `ls -la /etc/apparmor.d/` and use the correct filename. |
    | `apparmor_parser: Error while loading application profiles. Skipping /etc/apparmor.d/usr.sbin.nginx` | Check for syntax errors in the profile with `apparmor_parser -d /etc/apparmor.d/usr.sbin.nginx` and fix any rule violations. |
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

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `apparmor_parser: Error in /etc/apparmor.d/usr.local.bin.myapp at line 5: syntax error, unexpected TOK_COMMA` | Remove the trailing comma after `r,` on the `/etc/myapp/** r,` line; AppArmor does not use commas between rules. |
    | `AppArmor parser error: Unknown mode 'rw' in /etc/apparmor.d/usr.local.bin.myapp` | Use separate rules `r,` and `w,` instead of combined `rw,`; AppArmor requires individual mode declarations. |
    | `ERROR: Could not find profile /usr/local/bin/myapp when loading profile` | Ensure the profile filename matches the binary path exactly (e.g., rename file to `usr.local.bin.myapp` without leading slash) and run `sudo apparmor_parser -r /etc/apparmor.d/usr.local.bin.myapp` to load it. |
```bash
visudo   # Always use visudo — validates syntax on save
```

```text title="Expected output"
(no output — command opens /etc/sudoers in your default editor for safe editing)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `visudo: /etc/sudoers.d/50-cloud-init: syntax error near line 3` | Fix the syntax error in the specified file (check for missing colons, invalid usernames, or malformed rules) and save again. |
    | `visudo: no changes made to /etc/sudoers` | This is informational when you exit the editor without making changes; no action needed unless you intended to modify sudoers. |
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

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sudo: command not allowed` | Verify the command path matches exactly in sudoers (e.g., `/usr/bin/systemctl` not `systemctl`), and check for negation rules that may block it. |
    | `sudoers: syntax error near line X` | Run `sudo visudo` to validate sudoers syntax before applying changes, as invalid entries will lock out sudo access. |
```bash
# Audit who has sudo access
grep -E "^[^#]" /etc/sudoers /etc/sudoers.d/* | grep -v "^Defaults"

# Check a specific user's sudo permissions
sudo -l -U jsmith
```

```text title="Expected output"
/etc/sudoers:root	ALL=(ALL)	ALL
/etc/sudoers:jsmith	ALL=(ALL)	NOPASSWD: /usr/bin/systemctl
/etc/sudoers.d/admins:%wheel	ALL=(ALL)	ALL
/etc/sudoers.d/admins:%sudo	ALL=(ALL)	ALL
/etc/sudoers.d/webops:webadmin	ALL=(ALL)	/usr/bin/nginx, /usr/bin/systemctl restart nginx

Matching Defaults entries for jsmith on ip-172-31-45-12:
	env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin

User jsmith may run the following commands on ip-172-31-45-12:
	(ALL) NOPASSWD: /usr/bin/systemctl
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `sudo: /etc/sudoers is world writable` | Fix file permissions with `chmod 0440 /etc/sudoers`. |
    | `sudo: parse error in /etc/sudoers.d/admins near line 3` | Validate sudoers syntax with `visudo -c -f /etc/sudoers.d/admins` before applying changes. |
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

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `access.conf: line 5: unknown user 'root'` | Ensure the root user exists in /etc/passwd and PAM is properly configured to read access.conf via pam_access.so. |
    | `access.conf: syntax error at line 8: invalid CIDR notation` | Correct malformed network ranges (e.g., change `10.0.0.0/8` to valid CIDR like `10.0.0.0/8`) and verify no trailing spaces exist. |
    | `Login denied by access.conf` | Verify the rule order is correct (first matching rule wins) and that the user/group name and origin match the connecting source exactly using `who` or `last` to confirm the actual origin string. |
```bash
# /etc/pam.d/system-auth — enable pam_access
account     required      pam_access.so
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `pam_access.so: cannot open shared object file: No such file or directory` | Install the libpam-modules package with `apt-get install libpam-modules` or `yum install pam`. |
    | `PAM-1.1.8 (Linux-PAM 1.1.8) 29-Apr-2014 (Red Hat 6.5)` | This indicates pam_access.so exists but may not be properly compiled; verify with `ldd /lib64/security/pam_access.so` and reinstall if broken. |
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

```text title="Expected output"
----i--------e-- /etc/resolv.conf
(no output — command completes silently)
(no output — command completes silently)
-----a-------e-- /var/log/secure
----i--------e-- /etc/resolv.conf
----i--------e-- /var/log/audit
-----a-------e-- /var/log/secure
----i--------e-- /var/log/messages
-----a-------e-- /var/log/cron
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `chattr: Operation not permitted` | Ensure you are running as root (use `sudo chattr`) and the filesystem supports extended attributes (ext4, ext3, btrfs). |
    | `lsattr: No such file or directory` | Verify the file or directory path exists and you have read permissions on the parent directory. |
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

```text title="Expected output"
/usr/bin/ping = cap_net_raw+ep
/usr/sbin/tcpdump = cap_net_raw,cap_net_admin+ep

(no output — command completes silently)

(no output — command completes silently)

/usr/bin/ping = cap_net_raw+ep
/usr/sbin/tcpdump = cap_net_raw,cap_net_admin+ep
/usr/bin/mtr = cap_net_raw+ep
/usr/bin/arping = cap_net_raw+ep
/usr/sbin/arpwatch = cap_net_raw+ep
...

CapInh:	0000000000000000
CapPrm:	0000000100000000
CapEff:	0000000100000000
CapBnd:	0000003fffffffff
CapAmb:	0000000000000000

 cap_net_raw+ep
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `getcap: /usr/sbin/tcpdump: No such file or directory` | Verify the binary exists with `which tcpdump` or install the package (e.g., `apt-get install tcpdump`). |
    | `Operation not permitted` | Run `setcap` and `getcap` commands with `sudo` or as root, as capability manipulation requires CAP_SETFCAP. |
    | `Invalid argument` | Ensure the capability name is valid (e.g., `cap_net_raw`, not `CAP_NET_RAW`) and the syntax uses `+ep` or `+i` for the flags. |
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


```text title="Expected output"
/usr/local/bin/backup.sh
/opt/scripts/deploy.sh

/usr/bin/sudo
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/newgrp
/usr/sbin/unix_chkpwd
/usr/sbin/usernetctl
...

/usr/bin/locate
/usr/bin/ssh-keysign
/usr/sbin/netreport
/usr/sbin/usernetctl

root
admin

(no output — no accounts with empty passwords detected)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `find: '/root': Permission denied` | Run the command with `sudo` to access all directories, or redirect stderr to /dev/null (already done in the example). |
    | `awk: can't open file /etc/shadow: Permission denied` | Execute the awk command with `sudo` since /etc/shadow is readable only by root. |
    | `find: '/proc/[pid]/fd/[num]': No such file or directory` | Add `-xdev` flag (already present) and increase the timeout or run during low system activity to avoid race conditions. |
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
