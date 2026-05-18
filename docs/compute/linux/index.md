# Linux Server

<div class="kb-summary">
Linux server infrastructure running RHEL and Ubuntu — systemd service management, LVM2 storage, LACP bonded networking, SELinux/AppArmor security, and Ansible-driven automation for enterprise workloads.
</div>

```
┌──────────────────────────────────────────────────────┐
│                  Linux Server Stack                  │
├──────────────────────────────────────────────────────┤
│  Applications / Services  (nginx, postgres, custom)  │
├──────────────────────────────────────────────────────┤
│           systemd (PID 1 — unit management)          │
│   ┌──────────┬──────────┬──────────┬──────────────┐  │
│   │ services │ sockets  │ timers   │ mounts       │  │
│   └──────────┴──────────┴──────────┴──────────────┘  │
├──────────────────────────────────────────────────────┤
│                 Linux Kernel                         │
│   ┌──────────┬──────────┬──────────────────────────┐  │
│   │ SELinux/ │ netfilter│   LVM2 / block devices   │  │
│   │ AppArmor │ (fw)     │   /dev/sd*  /dev/dm-*    │  │
│   └──────────┴──────────┴──────────────────────────┘  │
├─────────────────┬────────────────────────────────────┤
│  Storage        │  Network                           │
│  SAN/NAS/LVM    │  LACP bond → VLAN → switch        │
├─────────────────┴────────────────────────────────────┤
│  Users & Auth: PAM → SSSD → Active Directory         │
└──────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
