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
