---
tags:
  - troubleshooting
  - linux
  - known-issues
---
# Linux — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Linux OS bugs, error codes, and workarounds covering boot issues, storage, networking, and systemd service management.

*Applies to: RHEL 8.x / 9.x, Ubuntu 22.04 / 24.04*
</div>

```text
┌──────────────────────────────────── Compute Linux Troubleshooting ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                         Linux: Compute Linux Troubleshooting platform                         │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                  Management: Compute Linux Troubleshooting management console                 │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Compute Linux Troubleshooting infrastructure · management network · monitoring           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Linux              = Compute Linux Troubleshooting platform overview and core concepts             │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- `journalctl -xe` for recent system errors; `dmesg | tail -50` for kernel messages.
- `systemctl status <service>` for service diagnostics.
- Boot failures: boot to rescue mode (`rd.break`) or use `systemctl list-units --state=failed`.

## Boot

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `A start job is running for...` hangs at boot | RHEL 9.x | Systemd service timeout; network mount or service dependency | Boot with `emergency.target`; investigate failing unit; check `/etc/fstab` for non-`nofail` network mounts | N/A |
| `dracut-initqueue timeout` on boot | RHEL 8.x | Root disk not found by dracut; SCSI timeout | Boot from rescue; verify `/etc/fstab` UUID matches actual disk; update initramfs | N/A |

## Storage

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Input/output error` on mounted filesystem | All | Disk failure or filesystem corruption | `fsck` after unmount; if disk failure: replace disk; restore from backup | N/A |
| LVM volume group `inactive` after disk replace | RHEL 8.x/9.x | LVM PV UUID changed after disk replace | Run `pvscan`; if VG still degraded: `vgchange -ay` | N/A |
| `/tmp` full — processes failing | All | Tempfiles not cleaned up; or tmpfs set too small | `df -h /tmp`; clean `/tmp`; increase tmpfs size in `/etc/fstab` | N/A |

## Networking

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `NetworkManager not managing interface` | RHEL 9.x | Interface has `NM_CONTROLLED=no` in ifcfg or is managed by another tool | Remove `NM_CONTROLLED=no`; restart NetworkManager | N/A |
| SSH `Permission denied (publickey)` | All | Wrong key pair, wrong user, or `~/.ssh/authorized_keys` wrong permissions | Check `~/.ssh/authorized_keys` permissions (644); verify correct key; check `sshd_config` | N/A |

## Services

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Failed to start service — timeout` | All | Service ExecStart command hanging or missing dependency | Check service log: `journalctl -u <service>`; verify dependency services running first | N/A |
| Service starts but exits immediately | All | Application crash; missing configuration | Check: `systemctl status <service>` + `journalctl -u <service> --no-pager` | N/A |

## See also

- [Linux — Common Issues](common-issues.md)
- [MySQL — Known Issues](mysql/troubleshooting/known-issues/)
- [PostgreSQL — Known Issues](postgresql/troubleshooting/known-issues/)
