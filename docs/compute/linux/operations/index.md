# Linux — Operations



<div class="kb-summary">
Linux — Operations reference: Health Checks, Procedures, Common Issues, CLI Reference, and 3 more.
</div>

```
┌────────────────────────────────────────── Linux Operations ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  Day-to-Day Linux Operations                                  │   │
│   │       Patching: dnf update / apt upgrade → test → prod ring; kernel updates need reboot       │   │
│   │        Monitoring: node_exporter metrics · journalctl · top/htop/sar · iostat · vmstat        │   │
│   │       Automation: Ansible playbooks, Bash cron jobs, systemd timers for recurring tasks       │   │
│   │       Access: SSH key auth; sudo with NOPASSWD for automation; MFA for privileged users       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Operations tasks span patching, monitoring, automation, and user/service management                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Service Management              │  │              Package & Updates              │   │
│   │         systemctl start/stop/restart         │  │            dnf update --security            │   │
│   │           systemctl enable/disable           │  │             apt-get dist-upgrade            │   │
│   │          journalctl -u svc --since           │  │           rpm -qa / dpkg -l: audit          │   │
│   │           systemctl daemon-reload            │  │            dnf history / apt log            │   │
│   │         systemd-analyze blame: slow          │  │            needs-restarting check           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 servers · SSD/NVMe · NIC · iDRAC/iLO BMC · UPS · Power & Cooling                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  dnf         = Dandified YUM; package manager for RHEL/Rocky/Fedora; supports modules                 │
│  apt         = Advanced Package Tool; package manager for Debian/Ubuntu systems                       │
│  systemctl   = CLI for systemd; start/stop/enable/disable/status service units                        │
│  journalctl  = Query systemd journal; filter by unit, time, priority, or boot                         │
│  node_exporter= Prometheus exporter; exposes Linux host metrics on TCP port 9100                      │
│  sar         = System Activity Reporter; collects CPU, memory, I/O stats over time                    │
│  iostat      = I/O statistics; shows disk utilisation, throughput, and await times                    │
│  vmstat      = Virtual memory stats; reports procs, memory, swap, I/O, CPU                            │
│  needs-restarting= dnf plugin that identifies services needing restart after update                   │
│  Ansible     = Agentless SSH automation; idempotent YAML playbooks for Linux config                   │
│  cron        = Classic job scheduler; reads /etc/crontab and user crontabs                            │
│  systemd timer= Modern cron replacement; accurate scheduling with dependency support                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Routine checks, service validation, and status verification.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Day-to-day operational tasks and how-to guides.</span></a>
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Commands, syntax, and quick reference.</span></a>
<a class="kb-card" href="install-upgrade/"><strong>Install & Upgrade</strong><span>Installation, upgrade, patching, and decommission.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts and reusable code.</span></a>
<a class="kb-card" href="backup-restore/"><strong>Backup & Restore</strong><span>Backup configuration, restore procedures, and validation.</span></a>
</div>
