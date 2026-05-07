# Linux Build Standards

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

```
# /etc/sudoers.d/ops-admins
%ops-admins ALL=(ALL) NOPASSWD: ALL

# /etc/sudoers.d/svc-backup
svc-backup ALL=(root) NOPASSWD: /usr/bin/rsync, /usr/bin/tar
```

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

The audit daemon must be running and enabled at boot. Baseline audit rules capture:

- All auth events (watches on `/etc/passwd`, `/etc/shadow`, `/etc/group`)
- `sudo` invocations via PAM
- Privileged command execution
- File opens with write intent on key paths under `/etc`

```bash
systemctl enable --now auditd rsyslog
ausearch -k privileged --start today | head -40
```

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
