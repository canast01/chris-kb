---
tags:
  - architecture
  - linux
---
# Linux — Standards

<div class="kb-summary">
Linux architecture standards: kernel version and patch cadence requirements, NTP configuration, disk layout (LVM), network bonding, and SELinux/AppArmor baseline.

*Applies to: RHEL 8.x / 9.x · Ubuntu 22.04 / 24.04*
</div>

```d2
direction: down

naming_convention: "Naming Convention" {shape: rectangle}
ntp_configuration: "NTP Configuration" {shape: rectangle}
syslog_forwarding: "Syslog Forwarding" {shape: rectangle}
package_repository_policy: "Package Repository Policy" {shape: rectangle}
os_component_stack: "OS Component Stack" {shape: rectangle}
software_installation_policy: "Software Installation Policy" {shape: rectangle}

naming_convention -> ntp_configuration: hardens
ntp_configuration -> syslog_forwarding: hardens
syslog_forwarding -> package_repository_policy: hardens
package_repository_policy -> os_component_stack: hardens
os_component_stack -> software_installation_policy: hardens
```

## Naming Convention

Sudo access granted via AD group membership:
```bash
# /etc/sudoers.d/infra-admins
%infra_admins ALL=(ALL) ALL
# No NOPASSWD — all privileged operations require password confirmation
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`sudoers:1 syntax error near line 1`** — Verify the file was edited with `visudo` instead of a standard editor, as direct edits bypass syntax validation.
    **`sudo: parse error in /etc/sudoers.d/infra-admins near line 1`** — Ensure the file has correct permissions (0440) by running `chmod 0440 /etc/sudoers.d/infra-admins`.
## NTP Configuration

```bash
# /etc/chrony.conf (RHEL)
server ntp1.example.local iburst
server ntp2.example.local iburst
makestep 1.0 3
rtcsync
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`command not found: chronyd`** — Install chrony with `sudo yum install chrony` and enable it with `sudo systemctl enable --now chronyd`.
    **`Permission denied: /etc/chrony.conf`** — Edit the file with `sudo vi /etc/chrony.conf` or ensure your user has sudo privileges.
Verify: `chronyc tracking` — `System time` offset should be < 1ms.

## Syslog Forwarding

```bash
# /etc/rsyslog.d/00-forward.conf
*.info @siem.example.local:514
# Or TLS:
*.info @@siem.example.local:6514
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`rsyslogd: action 'action 1' suspended, next retry [timestamp]`** — Verify SIEM server hostname resolves with `nslookup siem.example.local` and confirm port 514/6514 is open with `nc -zv siem.example.local 514`.
    **`error: certificate validation failed`** — For TLS forwarding (@@), ensure the SIEM server certificate is trusted by adding the CA certificate to `/etc/rsyslog.d/ca-certificates.crt` and referencing it in rsyslog.conf with `$DefaultNetstreamDriverCAFile`.
## Package Repository Policy

Production servers point only to approved internal mirrors:
```bash
# RHEL: subscription-manager repos — configure approved repos only
subscription-manager repos --disable="*" --enable=rhel-9-for-x86_64-baseos-rpms --enable=rhel-9-for-x86_64-appstream-rpms

# Ubuntu: /etc/apt/sources.list — point to internal mirror
deb http://mirror.example.local/ubuntu jammy main restricted universe
```


```text title="Expected output"
Removing all repositories.
Repository 'rhel-9-for-x86_64-baseos-rpms' is enabled for this system.
Repository 'rhel-9-for-x86_64-appstream-rpms' is enabled for this system.
```

!!! warning "Common errors"
    **`This system is not registered or the user does not have permission to access Red Hat Network.`** — Register the system first with `subscription-manager register --username=<user> --password=<pass> --auto-attach`.
    **`Error updating certificate used for TLS:`** — Ensure the system's subscription certificate is valid by running `subscription-manager refresh`.
No direct internet access from production servers — all package traffic via mirror.

## OS Component Stack

```d2
direction: right

hwLayer: "Hardware\nCPU · RAM · NIC · Disk" {shape: rectangle}
kernelCore: "Linux Kernel\nsyscall interface · drivers · schedulers" {shape: rectangle}
initSys: "Init System\nsystemd — units · targets" {shape: rectangle}
sysServices: "System Services\nsshd · chronyd · rsyslog · firewalld" {shape: rectangle}
appLayer: "Applications\nweb · database · monitoring agents" {shape: rectangle}

hwLayer -> kernelCore
kernelCore -> initSys
initSys -> sysServices
sysServices -> appLayer
```

## Software Installation Policy

- All packages installed from approved repositories only
- No manual compilation from source in production
- Third-party RPMs/DEBs signed and hosted in the internal repository
- Package additions require a change record

---

## Hostname and DNS Configuration

Hostnames follow the server naming convention `{site}{role}{env}{num}` (see naming-conventions/servers). The hostname must be set persistently and match forward and reverse DNS before a build is marked complete.

```bash
# Set hostname
hostnamectl set-hostname dc1-wapp-prd-01

# Confirm FQDN resolves correctly
getent hosts dc1-wapp-prd-01.corp.example.com
dig +short dc1-wapp-prd-01.corp.example.com
dig +short -x 10.10.4.21
```


```text title="Expected output"
10.10.4.21 dc1-wapp-prd-01.corp.example.com
10.10.4.21
dc1-wapp-prd-01.corp.example.com.
```

!!! warning "Common errors"
    **`getent hosts: No such file or directory`** — Ensure `/etc/hosts` contains the hostname entry or DNS is properly configured; add the entry manually if needed.
    **`; <<>> DiG 9.16.1-Ubuntu <<>> +short dc1-wapp-prd-01.corp.example.com`** — Verify DNS resolver is configured in `/etc/resolv.conf` and the nameserver is reachable.
    **`NXDOMAIN`** — Confirm the DNS A record for `dc1-wapp-prd-01.corp.example.com` exists and the reverse DNS PTR record for `10.10.4.21` is properly configured.
DNS resolver configuration is managed by Ansible. `/etc/resolv.conf` must not be edited manually on RHEL/Ubuntu; use `nmcli` or the Ansible `dns_baseline` role.

```ini
# /etc/resolv.conf (managed — do not edit)
search corp.example.com example.com
nameserver 10.10.0.10
nameserver 10.10.0.11
options timeout:2 attempts:3
```

## NTP Configuration

All Linux servers synchronise to internal NTP servers only. External NTP access is blocked at the perimeter firewall.

```ini
# /etc/chrony.conf — managed by Ansible role ntp_baseline
server 10.10.0.5 iburst prefer
server 10.10.0.6 iburst
driftfile /var/lib/chrony/drift
makestep 1.0 3
rtcsync
logdir /var/log/chrony
```

Verify sync:

```bash
chronyc tracking
chronyc sources -v
```


```text title="Expected output"
Reference ID    : 91.189.89.198 (ntp.ubuntu.com)
Stratum         : 2
Ref time (UTC)  : Fri Nov 17 14:32:45 2023
System time     : 0.000000123 seconds fast of NTP time
Latest offset   : +0.000000098 s
RMS offset      : 0.000000156 s
Frequency       : -12.345 ppm fast
Residual freq   : +0.002 ppm
Skew            : 0.015 ppm
Root delay      : 0.045678 seconds
Root dispersion : 0.012345 seconds
Update interval : 64.2 seconds
Leap status     : Normal

MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================
^* 91.189.89.198           1      6   377   32  +123us[ +145us] +/-   15ms
^- 185.125.190.39          2      6   377   33  -234us[ -198us] +/-   22ms
^+ 139.162.238.205         2      6   377   34  +89us [ +112us] +/-   18ms
^- 162.159.200.123         2      6   377   35  -156us[ -134us] +/-   25ms
```

!!! warning "Common errors"
    **`chronyc: Could not get tracking data`** — Verify chronyd daemon is running with `systemctl status chronyd` and listening on localhost.
    **`506 Cannot talk to daemon`** — Ensure chronyd is started with `systemctl start chronyd` and check socket permissions in `/var/run/chrony/`.
Expected: reference time offset under 100 ms, stratum 3 or better. An alert fires if offset exceeds 500 ms for more than 5 minutes.

## SSH and sudo Configuration

SSH daemon configuration is enforced via the `ssh_baseline` Ansible role.

| Parameter | Required Value |
|---|---|
| `PermitRootLogin` | `no` |
| `PasswordAuthentication` | `no` |
| `PubkeyAuthentication` | `yes` |
| `Protocol` | `2` |
| `MaxAuthTries` | `3` |
| `ClientAliveInterval` | `300` |
| `ClientAliveCountMax` | `2` |
| `AllowGroups` | `sshusers` |
| `Banner` | `/etc/ssh/banner` |

sudo is configured via `/etc/sudoers.d/` drop-in files only. The base `/etc/sudoers` must not be modified directly. Engineers receive sudo via AD group membership; service accounts get targeted command whitelists.

```bash
# /etc/sudoers.d/ops-admins
%ops-admins ALL=(ALL) NOPASSWD: ALL

# /etc/sudoers.d/svc-backup
svc-backup ALL=(root) NOPASSWD: /usr/bin/rsync, /usr/bin/tar
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`sudoers:1 syntax error near line 1`** — Run `visudo -c /etc/sudoers.d/ops-admins` to validate syntax before applying, as malformed sudoers files can lock out all sudo access.
    **`>>> /etc/sudoers.d/ops-admins: bad permissions on sudoers file, should be mode 0440`** — Change file permissions with `chmod 0440 /etc/sudoers.d/ops-admins` since sudoers files must be readable only by root.
Run `visudo -c` after any sudoers change to confirm no syntax errors.

## Required Packages and Kernel Parameters

**Mandatory packages installed at build time:**

- `chrony` — time sync
- `rsyslog` — system logging
- `audit` / `auditd` — kernel audit framework
- `aide` — file integrity monitoring
- `nmap-ncat` — connectivity testing
- `open-vm-tools` — VMware guest tools (VM builds only)
- `cloud-init` — cloud builds only

**Kernel parameters (`/etc/sysctl.d/99-baseline.conf`):**

```ini
net.ipv4.ip_forward = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.tcp_syncookies = 1
fs.suid_dumpable = 0
kernel.core_pattern = |/bin/false
```

Apply without reboot: `sysctl --system`

## Syslog and Audit Configuration

Remote syslog forwarding to the central SIEM is mandatory. The `rsyslog_baseline` Ansible role deploys:

```bash
# /etc/rsyslog.d/50-remote.conf
*.* @@siem.corp.example.com:514;RSYSLOG_ForwardFormat
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`error: unexpected character '@' [/etc/rsyslog.d/50-remote.conf:1]`** — Verify the rsyslog configuration syntax; the double `@@` is correct for TCP forwarding, but check for typos or encoding issues in the file.
    **`rsyslogd: action 'omfwd' suspended, next retry [timestamp] [/etc/rsyslog.d/50-remote.conf:1]`** — Confirm that siem.corp.example.com is resolvable and that port 514/TCP is open and the remote syslog server is listening.
The audit daemon must be running and enabled at boot. Baseline audit rules capture:

- All auth events (watches on `/etc/passwd`, `/etc/shadow`, `/etc/group`)
- `sudo` invocations via PAM
- Privileged command execution
- File opens with write intent on key paths under `/etc`

```bash
systemctl enable --now auditd rsyslog
ausearch -k privileged --start today | head -40
```


```text title="Expected output"
Created symlink /etc/systemd/system/multi-user.target.wants/auditd.service → /usr/lib/systemd/system/auditd.service.
Created symlink /etc/systemd/system/multi-user.target.wants/rsyslog.service → /usr/lib/systemd/system/rsyslog.service.
----
time->Thu Nov 14 09:23:15 2024
type=EXECVE msg=audit(1731588195.847:2156): argc=3 argv[0]="/usr/bin/sudo" argv[1]="useradd" argv[2]="newuser"
type=SYSCALL msg=audit(1731588195.847:2156): arch=c000003e syscall=59 success=yes exit=0 a0=0x7ffd4a2b1e20 a1=0x7ffd4a2b1e40 a2=0x7ffd4a2b1e60 a3=0x0 items=2 ppid=4521 pid=4522 auid=1000 uid=0 gid=0 euid=0 egid=0 fsuid=0 fsgid=0 tty=pts/0 ses=42 comm="sudo" exe="/usr/bin/sudo" key="privileged"
time->Thu Nov 14 09:45:32 2024
type=EXECVE msg=audit(1731589532.921:2287): argc=2 argv[0]="/usr/sbin/usermod" argv[1]="-G"
type=SYSCALL msg=audit(1731589532.921:2287): arch=c000003e syscall=59 success=yes exit=0 a0=0x55d8c4a2e1f0 a1=0x55d8c4a2e210 a2=0x55d8c4a2e230 a3=0x100 items=1 ppid=3891 pid=3892 auid=1000 uid=0 gid=0 euid=0 egid=0 fsuid=0 fsgid=0 tty=pts/1 ses=43 comm="usermod" exe="/usr/sbin/usermod" key="privileged"
time->Thu Nov 14 10:12:47 2024
type=EXECVE msg=audit(1731591167.445:2398): argc=1 argv[0]="/usr/bin/passwd"
type=SYSCALL msg=audit(1731591167.445:2398): arch=c000003e syscall=59 success=yes exit=0 a0=0x7fff9a1c2d40 a1=0x7fff9a1c2d60 a2=0x7fff9a1c2d80 a3=0x0 items=0 ppid=2156 pid=2157 auid=1000 uid=0 gid=0 euid=0 egid=0 fsuid=0 fsgid=0 tty=pts/0 ses=42 comm="passwd" exe="/usr/bin/passwd" key="privileged"
...
```

!!! warning "Common errors"
    **`ausearch: command not found`
Log retention on the host: 30 days rolling via `logrotate`. Long-term retention is handled by the SIEM (90 days hot, 1 year cold).

## Build Completion Checklist

Before a Linux build is marked complete, confirm all items below:

- [ ] Hostname set; DNS forward and reverse resolve correctly
- [ ] NTP synced; `chronyc tracking` shows offset under 100 ms
- [ ] SSH key-auth only; root login disabled; `sshd_config` matches baseline
- [ ] All mandatory packages installed and services enabled at boot
- [ ] `sysctl` baseline applied and survives reboot
- [ ] `rsyslog` forwarding confirmed (test event visible in SIEM)
- [ ] `auditd` running; baseline rules loaded (`auditctl -l`)
- [ ] No pending security patches (`yum/dnf/apt` security update count = 0)
- [ ] Server visible in monitoring platform within 15 minutes of first boot
- [ ] AIDE database initialised (`aide --init`)

---

## See also

- [Linux — Deploy](../../deploy/)
