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
┌───────────────────────────────────────────────── NFS ─────────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     Network file sharing — NFSv3/v4.1, exports, ID mapping                    │   │
│   │             Protocols: NFS (TCP/UDP 2049) · NFSv3 also uses portmapper(111)/mountd            │   │
│   │                  Management: /etc/exports (server) · mount/showmount (client)                 │   │
│   │          Client mount -> portmapper/mountd (v3) or direct (v4) -> Export check -> I/O         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Server           │  │      NFS server daemon      │  │     Exports filesystems     │   │
│   │            Export           │  │      /etc/exports entry     │  │     Client IP/subnet ACL    │   │
│   │           Mapping           │  │      UID/GID or idmapd      │  │     NFSv4 domain mapping    │   │
│   │           Locking           │  │     NLM (v3) / built-in     │  │     Diff. lock managers     │   │
│   │           Caching           │  │      Client attr cache      │  │     actimeo controls it     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │       nfsd       │  Serves exports  │    TCP/UDP 2049   │    Export ACL    │   Kernel-based   │   │
│   │      mountd      │  Mount handler   │    TCP/UDP (v3)   │    Export ACL    │Unused if v4-only │   │
│   │    rpc.idmapd    │ UID/GID mapping  │      Internal     │       N/A        │Domain must match │   │
│   │    showmount     │  Lists exports   │    TCP/UDP 2049   │       N/A        │   showmount -e   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: NFS server (array or Linux host) - client hosts - IP network                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Export         = a server-side directory made available to clients                                   │
│  NFSv3          = stateless; needs portmapper + mountd alongside nfsd                                 │
│  NFSv4.1        = stateful; only port 2049, built-in locking                                          │
│  root_squash    = maps remote root to a non-privileged server user                                    │
│  no_root_squash = disables root squashing; security risk if misused                                   │
│  Stale handle   = client cached handle no longer matches server state                                 │
│  idmapd         = maps NFSv4 numeric IDs to/from names via a domain                                   │
│  NFS domain     = string client and server idmapd must agree on                                       │
│  async export   = server acks writes before disk; faster, riskier                                     │
│  NLM            = Network Lock Manager; file locking for NFSv3                                        │
│  Hard vs soft   = hard retries forever, soft can return I/O errors                                    │
│  showmount      = client tool listing the exported paths on a server                                  │
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
