# Linux — Learning Path

<div class="kb-summary">
Recommended reading order for Linux server administration. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌──────────────────────────────────────── Linux — Learning Path ────────────────────────────────────────┐
│                                                                                                       │
│    5 stages in order: Architecture → Deploy → Operations → Security → Troubleshoot                    │
│                                                                                                       │
│   ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│   │  Architecture  │  │     Deploy     │  │    Operations   │  │    Security    │  │  Troubleshoot  │ │
│   │                │  │                │  │                 │  │                │  │                │ │
│   │  How It Works  │  │ Initial Setup  │  │  Health Checks  │  │ Access Control │  │ Common Issues  │ │
│   │Design Standards│  │Install/Upgrade │  │  CLI Reference  │  │ Authentication │  │  Diagnostics   │ │
│   │  Integrations  │  │                │  │    Procedures   │  │   Encryption   │  │   Escalation   │ │
│   │                │  │                │  │ Backup & Restore│  │   Hardening    │  │                │ │
│   │                │  │                │  │     Scripts     │  │                │  │                │ │
│   └────────────────┘  └────────────────┘  └─────────────────┘  └────────────────┘  └────────────────┘ │
│                                                                                                       │
│    Stage 1 (Architecture) builds understanding. Stage 3 (Operations) is daily work. Troubleshoot last.│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```
| Stage | Focus | Time investment |
|-------|-------|----------------|
| 1 — Architecture | Kernel, systemd, storage, networking model | 4–5 h |
| 2 — Deployment | Kickstart/cloud-init, LVM, post-install hardening | 2–3 h |
| 3 — Operations | systemctl, journalctl, LVM ops, daily checks | ongoing |
| 4 — Security | SSH, sudo, SELinux, firewalld, AIDE | 3–4 h |
| 5 — Troubleshooting | journalctl -xe, strace, tcpdump, OOM recovery | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand how the Linux kernel, systemd, and the major subsystems (networking, storage, process management) compose into a running server.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — boot sequence (UEFI → GRUB → kernel → initramfs → systemd target), process hierarchy (PID 1 = systemd, process tree), virtual file systems (`/proc`, `/sys`, `/dev`), and the Unix everything-is-a-file model including block devices and sockets
- [Design Standards](../architecture/design-standards/) — FHS filesystem layout, LVM volume group design (separate `/`, `/var`, `/home`, `/tmp` volumes), network interface naming (`ens`, `eth`, `bond`, `vlan`), and systemd unit organisation conventions
- [Integrations](../architecture/integrations/) — Active Directory integration via SSSD and `realm join`, NFS and SMB storage mounts via `autofs`, and configuration management agent patterns (Ansible agentless, Puppet agent, SaltStack)

**Key concepts before moving on**:

- systemd controls the entire service lifecycle — `systemctl start/stop/enable/disable/status/restart` are the primary operations; `service` and `init.d` are legacy wrappers
- LVM adds a logical abstraction layer between filesystems and physical disks — you can extend volumes online without downtime (increase PV → extend VG → extend LV → resize FS)
- SELinux enforces mandatory access control on top of standard Unix permissions — a process can be blocked by SELinux even if `ls -la` shows the right file permissions
- `journalctl` is the primary log viewer for systemd-managed services; `dmesg` is for kernel ring buffer messages

**Why first**: Linux administration decisions — partition layout, network configuration, systemd unit design — have long-lived consequences. A clear architecture picture prevents choices that are expensive to undo in production.

---

## Stage 2 — Deployment

**Goal**: Build Linux servers consistently with correct partitioning, networking, and baseline configuration from the first boot.

**Read**:

- [Deploy](../deploy/) — kickstart (RHEL/Rocky) or preseed (Debian/Ubuntu) automation, cloud-init for cloud instances, LVM partition layout design, network configuration via `nmcli`, and post-install hardening checklist execution
- [Install & Upgrade](../operations/install-upgrade/) — `dnf`/`apt` package management and subscription management, kernel upgrade procedure (install → set default in GRUB → reboot → verify), and in-place OS major version upgrade paths

**Deployment principles**:

- Always separate `/var` and `/tmp` onto their own LVM logical volumes — a rogue process filling `/var/log` will not crash the OS if `/var` is isolated
- Configure `nmcli` or `NetworkManager` for network settings — avoid editing `/etc/network/interfaces` or `/etc/sysconfig/network-scripts` manually on modern RHEL/Ubuntu
- Enable `kdump` on all production servers to capture kernel crash dumps for post-mortem analysis

---

## Stage 3 — Operations

**Goal**: Monitor and maintain Linux servers — catching resource exhaustion, service failures, and storage issues before they cause outages.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; `systemctl --failed`, `journalctl -p err -n 50`, disk usage (`df -h`), inode usage (`df -i`), load average (`uptime`), and open file descriptor counts (`lsof | wc -l`)
- [CLI Reference](../operations/cli-reference/) — `systemctl`, `journalctl`, `nmcli`, `ip addr`, `ip route`, `lvcreate/lvextend/lvdisplay`, `df`, `du`, `lsof`, `ss -tulpn`, `top`/`htop`, `sar`, `iotop` command patterns
- [Procedures](../operations/procedures/) — LVM volume extension online (no downtime), NIC bonding configuration with `nmcli`, adding a user with restricted `sudo` access, kernel parameter tuning via `sysctl -w` and `/etc/sysctl.d/`
- [Backup & Restore](../operations/backup-restore/) — `rsync`-based incremental file backup, LVM snapshot creation and mount for consistent backup, and bare-metal recovery from backup media using rescue environment
- [Scripts](../operations/scripts/) — disk space alerting with threshold notifications, service restart watchdog with alert on repeated failures, log rotation configuration via `logrotate.d`, and compliance check scripts for CIS benchmark items

**Daily rhythm**: `systemctl --failed` → `journalctl -p err` → disk/inode usage → load average → pending OS updates check.

---

## Stage 4 — Security

**Goal**: Harden the server attack surface, enforce least-privilege access, and maintain audit trails for all privileged actions.

**Read**:

- [Access Control](../security/access-control/) — user and group management (`useradd`, `usermod`, `groupadd`), `sudo` configuration via `/etc/sudoers.d/` (NOPASSWD judiciously), PAM stack customisation, and SSH `AllowUsers`/`AllowGroups` restrictions in `sshd_config`
- [Authentication](../security/authentication/) — SSH key-only login (disable `PasswordAuthentication yes`), SSSD for Active Directory Kerberos authentication and group policy, and PAM `faillock` or `pam_tally2` for brute-force account lockout
- [Encryption](../security/encryption/) — LUKS full-disk encryption (`cryptsetup luksFormat`) with TPM or network-bound decryption (Clevis/Tang), TLS certificate management for locally hosted services, and `gpg` for encrypting sensitive files
- [Hardening](../security/hardening/) — `firewalld` zone-based baseline ruleset, SELinux `enforcing` mode (never `permissive` in production), AIDE file integrity monitoring (baseline + scheduled comparison), and `auditd` rules for privileged command execution and sensitive file access

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose Linux failures — high CPU, disk full, network unreachable, service crash — using the right tool for each subsystem layer.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — service won't start (dependency failure, missing binary, SELinux denial), disk full (`/var/log` bloat, inode exhaustion vs block exhaustion), network unreachable (routing table vs firewall vs NIC), OOM killer event (identify victim process in `dmesg`), and NFS stale mount hang
- [Diagnostics](../troubleshooting/diagnostics/) — `journalctl -xe` for last service failure, `dmesg | tail -50` for kernel events, `strace -p <pid>` for syscall tracing of a stuck process, `perf top` for CPU profiler, `tcpdump -i any port 443` for packet-level network debug, and `lsof +D /path` for open file handles in a directory
- [Escalation](../troubleshooting/escalation/) — Red Hat/SUSE/Canonical support case creation with `sosreport`/`supportconfig`/`ubuntu-bug` output, kernel crash dump (`kdump`) analysis with `crash` utility, and hardware vendor escalation for storage or NIC firmware issues

**Why last**: Troubleshooting makes most sense once you understand the boot sequence, process hierarchy, and systemd dependency model under normal Linux operation.
