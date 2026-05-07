# Linux Build Standards
## Naming Convention

```
<site>-<role>-<nn>
```

Examples:
- `dc1-app-01` — first application server at DC1
- `dc1-db-01` — first database server at DC1
- `dc2-mon-01` — monitoring server at DC2
- `dc1-ansible-01` — Ansible control node

Hostnames are set at provisioning and never changed post-deployment. DNS A and PTR records created before the server is joined to AD.

## OS Build Standards

| Requirement | Standard |
|---|---|
| Supported distributions | RHEL 8/9 (production), Ubuntu 22.04 LTS (monitoring/automation) |
| OS lifecycle | In-support releases only; track EOL in CMDB |
| Kernel | Distribution default; no custom kernel builds |
| Init system | systemd — no legacy SysV init scripts |
| Locale | en_US.UTF-8 |
| Timezone | UTC (application-layer handles local time display) |

## Disk Layout

Standard LVM layout applied at provisioning:

| Mountpoint | Size | Filesystem | Options |
|---|---|---|---|
| `/boot` | 512 MB | xfs | separate partition |
| `/` | 20 GB | xfs | |
| `/var` | 20 GB | xfs | |
| `/tmp` | 5 GB | xfs | `noexec,nosuid,nodev` |
| `/home` | 5 GB | xfs | |
| swap | = RAM (max 16 GB) | swap | |

Application data in a separate VG (`vg_data`) — sized per role.

## Authentication

```bash
# SSH key-based authentication only
# /etc/ssh/sshd_config enforced via Ansible
PasswordAuthentication no
PermitRootLogin no
ChallengeResponseAuthentication no
PubkeyAuthentication yes
```

Sudo access granted via AD group membership:
```bash
# /etc/sudoers.d/infra-admins
%infra_admins ALL=(ALL) ALL
# No NOPASSWD — all privileged operations require password confirmation
```

## NTP Configuration

```bash
# /etc/chrony.conf (RHEL)
server ntp1.corp.local iburst
server ntp2.corp.local iburst
makestep 1.0 3
rtcsync
```

Verify: `chronyc tracking` — `System time` offset should be < 1ms.

## Syslog Forwarding

```bash
# /etc/rsyslog.d/00-forward.conf
*.info @siem.corp.local:514
# Or TLS:
*.info @@siem.corp.local:6514
```

## Package Repository Policy

Production servers point only to approved internal mirrors:
```bash
# RHEL: subscription-manager repos — configure approved repos only
subscription-manager repos --disable="*" --enable=rhel-9-for-x86_64-baseos-rpms --enable=rhel-9-for-x86_64-appstream-rpms

# Ubuntu: /etc/apt/sources.list — point to internal mirror
deb http://mirror.corp.local/ubuntu jammy main restricted universe
```

No direct internet access from production servers — all package traffic via mirror.

## Software Installation Policy

- All packages installed from approved repositories only
- No manual compilation from source in production
- Third-party RPMs/DEBs signed and hosted in the internal repository
- Package additions require a change record
