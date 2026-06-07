---
title: NFS
---

# NFS

<div class="kb-summary">
Network File System (NFS) allows hosts to mount remote directories over TCP. Coverage includes version selection (NFSv3/4/4.1), export configuration, UID/GID permission mapping, mount option tuning (hard/soft, sync/async, rsize/wsize), and troubleshooting stale handles and mount failures.
</div>

        NFS ARCHITECTURE
```text
┌─────────────────┐        TCP 2049        ┌──────────────────────┐
│   NFS CLIENT    │                        │    NFS SERVER                                              │
│                 │                        │                                                            │
│  mount -t nfs   │  ─────────────────────►│  /etc/exports                                              │
│  server:/export │                        │  /data 10.0.0.0/24                                         │
│  /mnt/data      │  NFS MOUNT REQUEST     │  (rw,sync,root_squash)                                     │
│                 │ ◄──────────────────────│                                                            │
│  ┌───────────┐  │  mount OK              │  ┌────────────────┐                                        │
│  │ /mnt/data │  │                        │  │  /data         │                                        │
│  │  (remote  │  │  READ / WRITE ops      │  │  (filesystem)  │                                        │
│  │   files)  │◄═╪════════════════════════╪═►│                │                                        │
│  └───────────┘  │                        │  └────────────────┘                                        │
│                 │                        │                                                            │
│  UID/GID check  │  NFSv3: stateless      │  exportfs -ra                                              │
│  (POSIX perms)  │  NFSv4: stateful/Krb5  │  applies changes                                           │
└─────────────────┘                        └──────────────────────┘
```

## NFSv4.1 Session and pNFS Data Path

NFSv4.1 introduces explicit sessions (slot tables replacing per-RPC XIDs) and pNFS, which allows clients to perform I/O directly to data servers without routing data through the metadata server.

```mermaid
sequenceDiagram
    autonumber
    participant C as NFS Client
    participant MS as Metadata Server<br/>(MDS, port 2049)
    participant DS1 as Data Server 1<br/>(pNFS DS)
    participant DS2 as Data Server 2<br/>(pNFS DS)

    Note over C,MS: NFSv4.1 — Session Establishment
    C->>MS: EXCHANGE_ID (client_owner verifier)
    MS-->>C: clientid (64-bit), server_owner, server_scope
    C->>MS: CREATE_SESSION (clientid, fore/back channel attrs, slot table size)
    MS-->>C: sessionid (128-bit), negotiated slot table depth

    Note over C,MS: File Open — Compound Procedure (single RTT)
    C->>MS: COMPOUND [SEQUENCE + PUTROOTFH + LOOKUP("path/file") + OPEN(RW) + GETFH]
    MS-->>C: filehandle, open_stateid, change_info, caching delegation

    Note over C,MS: pNFS — Layout Acquisition
    C->>MS: LAYOUTGET (filehandle, iomode=RW, offset=0, length=EOF, layout_type=files)
    MS-->>C: layout (stripe_unit=1 MiB, DS1 → stripes 0,2,4…  DS2 → stripes 1,3,5…)

    Note over C,DS2: pNFS — Parallel Direct I/O to Data Servers (MDS not in data path)
    C->>DS1: WRITE stripe 0 direct to DS1
    C->>DS2: WRITE stripe 1 direct to DS2 (parallel)
    DS1-->>C: Write response
    DS2-->>C: Write response

    Note over C,MS: Close — Layout Return
    C->>MS: LAYOUTRETURN (filehandle, range, layout stateid)
    C->>MS: CLOSE (open_stateid)
    MS-->>C: new_stateid, layout committed to stable storage
```

| Version | Ports Required | Session Model | Locking | Parallel I/O |
|---|---|---|---|---|
| NFSv3 | 2049 + rpcbind/111 + mountd + NLM | Stateless per RPC | External (NLM daemon) | No |
| NFSv4 | 2049 only | Stateful (lease-based) | Built-in | No |
| NFSv4.1 | 2049 only | Stateful + explicit sessions (slot table) | Built-in | Yes (pNFS) |

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="exports/">
  <strong>Exports</strong>
  <span>Configuring /etc/exports, export rules, squash options, and reloading exports with exportfs.</span>
</a>

<a class="kb-card" href="mounts/">
  <strong>Mounts</strong>
  <span>Mount options (hard/soft, sync/async, noatime, rsize/wsize), /etc/fstab entries, and autofs.</span>
</a>

<a class="kb-card" href="permissions/">
  <strong>Permissions</strong>
  <span>UID/GID mapping, root squash, no_root_squash, and Kerberos-based identity with NFSv4.</span>
</a>

<a class="kb-card" href="versions/">
  <strong>Versions</strong>
  <span>NFSv3 vs NFSv4 vs NFSv4.1 feature comparison, stateful sessions, pNFS, and protocol negotiation.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Stale file handles, mount timeouts, permission denied errors, rpcbind failures, and nfsstat analysis.</span>
</a>

</div>

## Quick Reference

| Property | NFSv3 | NFSv4 | NFSv4.1 |
|---|---|---|---|
| Transport | TCP / UDP | TCP only | TCP only |
| Port | 2049 + rpcbind (111) | 2049 only | 2049 only |
| Stateful | No | Yes | Yes |
| Locking | NLM (separate daemon) | Built-in | Built-in |
| Kerberos auth | Optional | Supported | Supported |
| pNFS (parallel) | No | No | Yes |
| Recommended use | Legacy / simple | General | High-performance / modern |

**Common mount options:**

| Option | Effect |
|---|---|
| `hard` | Retries indefinitely on server failure — recommended for data integrity |
| `soft` | Returns error after timeout — use only for non-critical mounts |
| `sync` | Writes confirmed before returning — safer, slower |
| `async` | Writes buffered — faster, risk of data loss on crash |
| `noatime` | Disables access time updates — reduces write traffic |
| `rsize=1048576` | Read buffer size (1 MiB) — tune for throughput |
| `wsize=1048576` | Write buffer size (1 MiB) — tune for throughput |
| `nfsvers=4.1` | Force specific NFS version |

## Common Commands / Config

```bash
# Show exports from a remote NFS server
showmount -e <nfs-server>

# Mount an NFS share manually (NFSv4.1, hard mount)
mount -t nfs -o vers=4.1,hard,noatime,rsize=1048576,wsize=1048576 \
  <nfs-server>:/export/path /mnt/nfs

# /etc/fstab entry for persistent NFSv4 mount
# <nfs-server>:/export/path  /mnt/nfs  nfs  vers=4,hard,noatime,_netdev  0 0

# Reload exports after editing /etc/exports (no restart needed)
exportfs -ra

# Show currently active exports
exportfs -v

# Display NFS client and server statistics
nfsstat -c   # client stats
nfsstat -s   # server stats
nfsstat -m   # mounted filesystems and options

# Check RPC services (needed for NFSv3 portmapper)
rpcinfo -p <nfs-server>

# Unmount a stuck NFS mount (lazy unmount)
umount -l /mnt/nfs

# Check NFS mount details including negotiated version
mount | grep nfs
```

**Example /etc/exports entry:**
```bash
# /etc/exports
/data/shared  192.168.1.0/24(rw,sync,no_subtree_check,root_squash)
/data/readonly  10.0.0.0/8(ro,sync,no_subtree_check,all_squash)
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| `mount.nfs: Connection timed out` | Firewall on port 2049; rpcbind (111) for v3 | Open port 2049/tcp; for NFSv3 also open 111/tcp+udp and ensure rpcbind is running |
| `Stale file handle` | Server-side export was removed or path changed | Unmount (`umount -l`) and remount; verify export still exists with `showmount -e` |
| `Permission denied` on client | UID/GID mismatch between client and server | Confirm UIDs match or configure `all_squash` + `anonuid`/`anongid` in exports |
| Mount hangs indefinitely | Hard mount + server unreachable | Use `umount -l` (lazy); consider `soft,timeo=30` for non-critical mounts |
| `rpc.statd: unable to register` | rpcbind not running | Start rpcbind: `systemctl start rpcbind` |
| High NFS latency | rsize/wsize too small; async disabled | Increase rsize/wsize to 1 MiB; consider `async` if data loss risk is acceptable |
