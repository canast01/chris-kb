# NFS Mounts

```
        CLIENT-SIDE MOUNT PROCESS
┌──────────────────────────────────────────────────────────────┐
│  mount -t nfs -o vers=4.1,hard,rsize=1048576 \              │
│         server:/export /mnt/data                            │
│                    │                                        │
│                    ▼                                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  NFS client negotiates version & options with server │   │
│  │  server:/export  ──────────────────►  /mnt/data      │   │
│  │  (remote path)     TCP 2049 mount    (local mountpoint)│  │
│  └──────────────────────────────────────────────────────┘   │
│                    │                                        │
│  Option effects:   │                                        │
│  hard    ──► retry indefinitely if server unreachable       │
│  soft    ──► return error after timeout (risk of corruption)│
│  rsize=  ──► read buffer size (tune for throughput)        │
│  _netdev ──► wait for network at boot (required in fstab)  │
│  vers=   ──► force NFS version (4.1 preferred)             │
└──────────────────────────────────────────────────────────────┘
```

## Overview

NFS mounts attach remote exports to the local filesystem. Mounts can be done manually with `mount`, made persistent via `/etc/fstab`, or managed automatically with autofs. Mount options control reliability, timeout behavior, and NFS version negotiation.

## Manual Mounts

```bash
# Basic NFSv3 mount
mount -t nfs 192.168.10.10:/data/shared /mnt/shared

# Force NFSv4
mount -t nfs4 192.168.10.10:/data/shared /mnt/shared

# Mount with specific options
mount -t nfs -o vers=3,rw,hard,timeo=600,retrans=3 \
  192.168.10.10:/data/shared /mnt/shared

# Mount NFSv4 with Kerberos integrity
mount -t nfs4 -o sec=krb5i,rw 192.168.10.10:/data/secure /mnt/secure

# Unmount
umount /mnt/shared

# Force unmount (use only if server is unreachable)
umount -f -l /mnt/shared
```

## /etc/fstab Options

```bash
# NFSv4 persistent mount
192.168.10.10:/data/shared  /mnt/shared  nfs4  rw,hard,timeo=600,retrans=3,_netdev  0 0

# NFSv3 with soft mount (returns error after timeout instead of hanging)
192.168.10.10:/data/logs  /mnt/logs  nfs  ro,soft,timeo=30,retrans=2,vers=3,_netdev  0 0
```

## Mount Option Reference

| Option | Effect |
|--------|--------|
| `hard` | Retry indefinitely until server responds (default) |
| `soft` | Return error after `retrans` retries (risk of data corruption) |
| `timeo=N` | Timeout in tenths of a second before retry (default 600 = 60s) |
| `retrans=N` | Number of retries before reporting error |
| `_netdev` | Wait for network before mounting at boot |
| `nofail` | Do not fail boot if mount fails |
| `vers=3/4/4.1` | Force NFS version |
| `sec=krb5i` | Use Kerberos with integrity checking |

## Automount with autofs

```bash
# Install autofs
dnf install autofs   # RHEL/CentOS
apt install autofs   # Debian/Ubuntu

# /etc/auto.master — add a map
/mnt/nfs  /etc/auto.nfs  --timeout=300

# /etc/auto.nfs — define mounts
shared  -rw,hard,timeo=600  192.168.10.10:/data/shared
logs    -ro,soft,timeo=30   192.168.10.10:/data/logs

# Enable and start autofs
systemctl enable --now autofs

# Force autofs to re-read maps
systemctl reload autofs
```

## Known Issues

- `hard` mounts can cause processes to hang indefinitely if the NFS server goes offline. For non-critical mounts, use `soft` with a short `timeo` and handle errors in the application layer.
- `_netdev` is required in `/etc/fstab` for NFS mounts — without it, mounts may be attempted before the network is up, causing boot failures.
- NFSv4 mounts require the server to export a pseudo-root (`fsid=0`). If the mount hangs at `Waiting for server…`, verify the NFSv4 pseudo-root export exists with `showmount -e <server>`.
