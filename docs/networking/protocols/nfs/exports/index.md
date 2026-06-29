---
tags:
  - networking
---
# NFS Exports

<div class="kb-summary">
NFS Exports reference covering Overview, /etc/exports Syntax, Key Export Options, Applying Export Changes, Verifying Exports from Client Side and 1 more sections.
</div>

```d2
direction: down

etcexports_syntax: "/etc/exports Syntax" {shape: rectangle}
key_export_options: "Key Export Options" {shape: rectangle}
applying_export_changes: "Applying Export Changes" {shape: rectangle}
verifying_exports_from_client_side: "Verifying Exports from Client Side" {shape: rectangle}
known_issues: "Known Issues" {shape: rectangle}

etcexports_syntax -> key_export_options: uses
key_export_options -> applying_export_changes: uses
applying_export_changes -> verifying_exports_from_client_side: uses
verifying_exports_from_client_side -> known_issues: uses
```

## Overview

NFS exports are defined in `/etc/exports` on Linux servers. Each line specifies a directory, the clients allowed to mount it, and a set of options controlling access, security, and behavior. Changes take effect with `exportfs -ra` — no service restart required.

## /etc/exports Syntax

```text
/path/to/export  client_spec(options)
```

```bash
# Examples
/data/shared     192.168.10.0/24(rw,sync,no_subtree_check)
/data/readonly   *(ro,sync,no_root_squash)
/home            10.0.0.0/8(rw,sync,root_squash,anonuid=65534,anongid=65534)
/srv/nfs4        *(rw,sync,fsid=0,no_subtree_check)           # NFSv4 pseudo-root
/srv/nfs4/data   *(rw,sync,bind=/data/shared,no_subtree_check) # NFSv4 bind mount
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`exportfs: /data/shared: No such file or directory`** — Verify the export path exists on the NFS server with `ls -ld /data/shared` before adding it to /etc/exports.
    **`exportfs: /etc/exports:1: syntax error - unexpected character after line`** — Check for trailing whitespace, missing parentheses, or invalid characters; use `exportfs -v` to validate syntax after editing.
    **`mount.nfs: access denied by server while mounting 192.168.10.5:/data/shared`** — Run `exportfs -ra` on the server to reload /etc/exports after making changes, then retry the client mount.
## Key Export Options

| Option | Meaning |
|--------|---------|
| `rw` | Read-write access |
| `ro` | Read-only access |
| `sync` | Write to disk before replying (safer) |
| `async` | Reply before write completes (faster, risk of data loss) |
| `no_root_squash` | Root on client retains root privileges |
| `root_squash` | Root on client mapped to anonymous UID (default) |
| `all_squash` | All users mapped to anonymous UID |
| `no_subtree_check` | Disable subtree checking (recommended for most cases) |
| `fsid=0` | Marks the NFSv4 pseudo-root |

## Applying Export Changes

```bash
# Reload exports without restarting NFS
exportfs -ra

# List currently active exports
exportfs -v

# Export a directory immediately (without editing /etc/exports)
exportfs -o rw,sync,no_subtree_check 192.168.10.50:/data/tmp

# Unexport a directory
exportfs -u 192.168.10.50:/data/tmp

# Restart NFS server (last resort)
systemctl restart nfs-server
```


```text title="Expected output"
exporting 192.168.1.100:/srv/nfs
exporting 192.168.1.101:/srv/nfs
exporting 192.168.1.102:/srv/nfs

/srv/nfs       	192.168.1.100(rw,sync,wdelay,hide,nocrossmnt,secure,root_squash,no_all_squash)
/srv/nfs       	192.168.1.101(rw,sync,wdelay,hide,nocrossmnt,secure,root_squash,no_all_squash)
/srv/nfs       	192.168.1.102(rw,sync,wdelay,hide,nocrossmnt,secure,root_squash,no_all_squash)
/data/tmp      	192.168.10.50(rw,sync,no_subtree_check)

unexporting 192.168.10.50:/data/tmp

Redirecting to /bin/systemctl restart nfs-server
```

!!! warning "Common errors"
    **`exportfs: /data/tmp does not exist or access denied`** — Verify the directory exists and the nfs-server process has read permissions on the parent path.
    **`exportfs: No such file or directory`** — Ensure /etc/exports exists and contains valid export entries before running `exportfs -ra`.
    **`Job for nfs-server.service failed because the control process exited with error code`** — Check `/var/log/messages` or `journalctl -xe` for NFS daemon startup errors, often caused by invalid /etc/exports syntax.
## Verifying Exports from Client Side

```bash
# List exports available from a server
showmount -e 192.168.10.10

# Check which clients have mounted each export
showmount -a 192.168.10.10

# Verify NFS service is listening
rpcinfo -p 192.168.10.10 | grep nfs
```


```text title="Expected output"
Export list for 192.168.10.10:
/export/home           192.168.1.0/24
/export/data           10.0.0.0/8
/export/backups        192.168.10.5
/var/nfs/shared        (everyone)

192.168.10.10:
  192.168.1.15:/export/home
  192.168.1.22:/export/data
  10.5.3.8:/export/backups

    100003  3   tcp                  2049  nfs
    100003  4   tcp                  2049  nfs
    100003  3   udp                  2049  nfs
    100003  4   udp                  2049  nfs
```

!!! warning "Common errors"
    **`clnt_create: RPC: Port mapper failure - Unable to receive`** — Verify the NFS server is running with `systemctl status nfs-server` and that port 111 (portmapper) is accessible.
    **`showmount: clnt_create error: RPC: Authentication error; why = Client authentication has failed`** — Check firewall rules allow NFS traffic (ports 111, 2049) from your client to the server using `sudo ufw allow from 192.168.1.0/24 to any port 2049`.
## Known Issues

- `exportfs -ra` silently ignores malformed lines in `/etc/exports`. Check `journalctl -u nfs-server` or `exportfs -v` output to confirm an export actually loaded.
- Overlapping export paths (e.g. exporting both `/data` and `/data/sub` to the same client with different options) can produce unexpected option inheritance. Test with `exportfs -v` and verify the options shown for each path.
- `no_subtree_check` is recommended for directories that are entire filesystems; omitting it causes extra kernel overhead and occasional permission errors when files are opened by handle across export boundaries.
