---
tags:
  - networking
  - troubleshooting
search:
  boost: 1.5
description: "NFS Troubleshooting reference covering Diagnostic Flow, Quick Diagnostics, Common Issues, Performance Tuning, Export Configuration Reference and 2 more..."
---
# NFS Troubleshooting

<div class="kb-summary">
NFS Troubleshooting reference covering Diagnostic Flow, Quick Diagnostics, Common Issues, Performance Tuning, Export Configuration Reference and 2 more sections.
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
quick_diagnostics: "Quick Diagnostics" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}
performance_tuning: "Performance Tuning" {shape: rectangle}
export_configuration_reference: "Export Configuration Reference" {shape: rectangle}
stale_file_handle_recovery: "Stale File Handle Recovery" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> quick_diagnostics: investigate
symptom -> common_issues: investigate
symptom -> performance_tuning: investigate
symptom -> export_configuration_reference: investigate
symptom -> stale_file_handle_recovery: investigate
diagnostic_flow -> resolution
quick_diagnostics -> resolution
common_issues -> resolution
performance_tuning -> resolution
export_configuration_reference -> resolution
stale_file_handle_recovery -> resolution
```

## Before you begin

- **Access:** Network admin credentials; console or SSH to devices
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Diagnostic Flow

```d2
direction: right

C: "C" {shape: rectangle}
D: "Firewall / routing issue" {shape: rectangle}
E: "E" {shape: rectangle}
F: "Check export on server: showmount / exportfs" {shape: rectangle}
G: "Check permissions: /etc/exports, auth type" {shape: rectangle}
H: "H" {shape: rectangle}
I: "Check rsize/wsize, MTU, server load" {shape: rectangle}
J: "Check UID/GID mapping, export permissions" {shape: rectangle}
K: "Remount — export path changed on server" {shape: rectangle}
L: "Check server health, network, hard/soft mount" {shape: rectangle}
A: "NFS issue reported" {shape: rectangle}
B: "B" {shape: rectangle}

C -> D
E -> F
E -> G
H -> I
H -> J
H -> K
H -> L
```

## Quick Diagnostics

```bash
# Test connectivity to NFS port
nc -zv <nfs-server> 2049

# Show server exports (from client)
showmount -e <nfs-server>

# Check server-side exports
exportfs -v

# Show active NFS mounts on client
mount | grep nfs
nfsstat -m

# NFS client statistics (retransmits, errors)
nfsstat -c

# NFS server statistics
nfsstat -s

# RPC service availability (NFSv3)
rpcinfo -p <nfs-server>
```


```text title="Expected output"
Connection to 192.168.1.50 2049 port [tcp/nfs] succeeded!

Export list for 192.168.1.50:
/export/data                	192.168.1.0/24
/export/backup              	192.168.1.100
/var/nfs/shared             	*

/export/data            	192.168.1.0/24(rw,sync,no_subtree_check)
/export/backup          	192.168.1.100(rw,sync,root_squash)
/var/nfs/shared         	*(ro,sync,no_subtree_check)

192.168.1.50:/export/data on /mnt/data type nfs4 (rw,relatime,vers=4.2,rsize=131072,wsize=131072,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=192.168.1.25,local_lock=none,addr=192.168.1.50)

	Server nfs v4:
	packets	udp	tcp	tcpconn
	1847392	0	1847392	156

Client nfs v4:
	packets	udp	tcp	tcpconn
	1923847	0	1923847	156
	reads	writes	retrans	authtimeo
	847392	523891	12	0

Server nfs v4:
	reads	writes	filehandles	commits	udp	tcp
	847392	523891	2847	12847	0	1923847

   program vers proto   port  service
    100000    4   tcp    111  portmapper
    100000    4   udp    111  portmapper
    100003    3   tcp   2049  nfs
    100003    4   tcp   2049  nfs
    100005    3   tcp   20048 mountd
    100227    3   tcp   2049  nfs_acl
```

!!! warning "Common errors"
    **`nc: connect to 192.168.1.50 port 2049 (tcp) failed: Connection refused`** — Verify the NFS server is running with `systemctl status nfs-server` and firewall allows port 2049.
    **`clnt_create: RPC: Program not registered`** — Ensure the NFS service is started on the server with `systemctl start nfs-server` and wait for RPC registration.
    **`mount.nfs: access denied by server while mounting 192.168.1.50:/export/data`** — Check client IP is in the export list on the server and verify `/etc/exports` permissions with `exportfs -ra`.
## Common Issues

| Symptom | Probable cause | Resolution |
|---|---|---|
| `mount: no route to host` | Firewall blocking 2049 | Open TCP/UDP 2049 (and 111 for NFSv3) |
| `access denied by server` | Client IP not in export ACL | Update `/etc/exports`, run `exportfs -ra` |
| `Stale file handle` | Export path changed or server restarted | Unmount and remount |
| Files owned by `nobody` | NFSv4 idmapd domain mismatch | Match `Domain =` in `/etc/idmapd.conf` on client and server |
| `Permission denied` on read/write | UID mismatch or `root_squash` | Use `no_root_squash` for admin mounts; verify UIDs match |
| Mount hangs indefinitely | `hard` mount + server unreachable | Investigate server; use `intr` option for admin mounts |
| Slow performance | Default rsize/wsize (4K) | Set `rsize=1048576,wsize=1048576` in mount options |
| Kerberos auth fails | Clock drift > 5s | Fix NTP; `klist` to check Kerberos ticket |

## Performance Tuning

```bash
# Recommended mount options for throughput
mount -t nfs -o vers=4.1,hard,timeo=600,rsize=1048576,wsize=1048576,nconnect=8 \
  <server>:/export /mnt

# nconnect=N — use N TCP connections (Linux 5.3+, improves parallel throughput)

# Check current I/O sizes in use
nfsstat -m | grep rsize

# Test NFS throughput
dd if=/dev/zero of=/mnt/testfile bs=1M count=1000 oflag=direct
```


```text title="Expected output"
Server.nfs.local:/export on /mnt type nfs4 (rw,relatime,vers=4.1,rsize=1048576,wsize=1048576,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=192.168.1.45,local_lock=none,addr=192.168.1.10)
	rsize=1048576, wsize=1048576
1000+0 records in
1000+0 records out
1048576000 bytes (1.0 GB, 976 MiB) copied, 8.247 s, 127 MB/s
```

!!! warning "Common errors"
    **`mount.nfs: access denied by server while mounting <server>:/export`** — Verify the NFS server's /etc/exports includes the client IP and check firewall rules allow NFS ports (111, 2049, and ephemeral ports).
    **`mount.nfs: No such file or directory`** — Ensure the export path exists on the server and the mount point directory exists locally with `mkdir -p /mnt`.
    **`nfsstat: command not found`** — Install nfs-utils package with `apt-get install nfs-utils` (Debian/Ubuntu) or `yum install nfs-utils` (RHEL/CentOS).
## Export Configuration Reference

```bash
# /etc/exports syntax
/data/exports   10.0.0.0/8(rw,sync,no_subtree_check,no_root_squash)
/data/readonly  *(ro,sync,no_subtree_check)

# Apply changes
exportfs -ra

# Verify active exports
exportfs -v

# Unexport and re-export all
exportfs -ua && exportfs -a
```


```text title="Expected output"
exporting 10.0.0.0/8:/data/exports
exporting *:/data/readonly
/data/exports   	10.0.0.0/8(sync,rw,no_subtree_check,no_root_squash)
/data/readonly  	*(sync,ro,no_subtree_check)
unexporting 10.0.0.0/8:/data/exports
unexporting *:/data/readonly
exporting 10.0.0.0/8:/data/exports
exporting *:/data/readonly
```

!!! warning "Common errors"
    **`exportfs: /etc/exports:1: syntax error - unexpected characters after export path`** — Check for trailing whitespace or missing parentheses in /etc/exports; use `cat -A /etc/exports` to reveal hidden characters.
    **`exportfs: /data/exports does not exist`** — Ensure the export directories exist and are accessible before running exportfs; create them with `mkdir -p /data/exports /data/readonly`.
    **`exportfs: /etc/exports:1: unknown export option 'rw'`** — Verify NFS server is installed (`systemctl status nfs-server`) and use valid options like `rw` only within parentheses without spaces before the opening paren.
## Stale File Handle Recovery

```bash
# Unmount (force if stuck)
umount -l /mnt/data   # lazy unmount — detaches immediately

# Re-establish mount
mount -t nfs -o vers=4.1 <server>:/export /mnt/data

# If mount is hung and blocking
fuser -mk /mnt/data    # kill processes using the mountpoint
umount -f /mnt/data
```


```text title="Expected output"
umount: /mnt/data: not mounted
mount.nfs: mounting 192.168.1.42:/export failed, timed out (retrying)
mount.nfs: mounting 192.168.1.42:/export failed, timed out (retrying)
mount.nfs: mounting 192.168.1.42:/export failed, timed out (retrying)
     PID USERNAME    COMMAND
    2847 root        cat
    3156 appuser     python3
    3201 appuser     rsync
3 processes killed
umount: /mnt/data: mounted by another namespace
```

!!! warning "Common errors"
    **`umount: /mnt/data: not mounted`** — Verify the mountpoint is actually mounted with `mount | grep /mnt/data` before attempting unmount.
    **`mount.nfs: mounting 192.168.1.42:/export failed, timed out`** — Check NFS server connectivity with `showmount -e <server>` and verify firewall rules allow port 2049/111.
    **`umount: /mnt/data: mounted by another namespace`** — Use `mount -l` to identify the namespace and either switch to it or use `umount -l` for lazy unmount instead of `-f`.
## Log Locations

| Platform | Log |
|---|---|
| RHEL/Rocky client | `journalctl -u nfs-client.target` |
| RHEL/Rocky server | `journalctl -u nfs-server` |
| NetApp ONTAP | `event log show -messagename nfs*` |
| Kernel messages | `dmesg | grep -i nfs` |

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Exports](../exports/)
- [Mounts](../mounts/)
- [Permissions](../permissions/)
- [Versions](../versions/)
- [NFS — Overview](../)
