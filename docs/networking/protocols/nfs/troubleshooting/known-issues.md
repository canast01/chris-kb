---
tags:
  - troubleshooting
  - nfs
  - networking
  - known-issues
---
# NFS — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known NFS issues covering mount failures, permission errors, NFSv4 behavior, and performance problems.

*Applies to: NFSv3 / NFSv4.1 / NFSv4.2*
</div>

```text
┌────────────────────────────────────── Networking Protocols Nfs ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Protocols: Networking Protocols Nfs platform                         │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Networking Protocols Nfs management console                    │   │
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
│    Physical: Networking Protocols Nfs infrastructure · management network · monitoring                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Protocols          = Networking Protocols Nfs platform overview and core concepts                  │
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

- Test NFS: `showmount -e <nfs-server>` for export list; `mount -t nfs <server>:/export /mnt/test` for mount test.
- NFSv4 uses port 2049 only; NFSv3 uses 2049 + portmapper (111) + mountd (typically 635).
- `strace mount ...` or `dmesg` for mount failure diagnostics.

## Mount Failures

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| `mount.nfs: Connection timed out` | NFS server unreachable; TCP 2049 blocked | Verify TCP/UDP 2049 from client to server; check firewall |
| `mount.nfs: access denied by server` | Client IP not in export policy | Add client IP to server's `/etc/exports` or array export ACL |
| `mount.nfs: No route to host` | Network connectivity issue | Check routing from client to NFS server IP |
| NFSv4 mount hangs at `LOOKUP` | NFSv4 domain mismatch between client and server | Set matching `Domain` in `/etc/idmapd.conf` on client and server |

## Permission Errors

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| `Permission denied` on NFSv4 despite correct UNIX permissions | UID/GID not matching between client and server; ID mapping broken | Verify `nfsnobody`/`nobody` mapping; check `rpc.idmapd` running on client and server |
| `Permission denied` on NFSv3 for root user | `root_squash` squashing root to `nobody` | Use `no_root_squash` on export if root access required (use with caution) |

## Performance

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| NFS write latency high | Mount using `sync` option or server write-back disabled | Mount with `async` (accept data loss risk); verify server disk write cache enabled |
| `Stale file handle` after server IP change | NFS client cached old server IP in file handle | Unmount and remount; update `/etc/fstab` to use FQDN rather than IP |

## See also

- [NFS — Common Issues](common-issues.md)
- [NetApp ONTAP — Known Issues](../../../storage/netapp/ontap/troubleshooting/known-issues/)
