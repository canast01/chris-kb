---
tags:
  - networking
---
# NFS Permissions

<div class="kb-summary">
NFS Permissions reference covering Overview, UID/GID Mapping, NFSv4 ID Mapping (idmapd), Kerberos Security Modes, ACL Interaction and 1 more sections.
</div>

```d2
direction: down

uidgid_mapping: "UID/GID Mapping" {shape: rectangle}
nfsv4_id_mapping_idmapd: "NFSv4 ID Mapping (idmapd)" {shape: rectangle}
kerberos_security_modes: "Kerberos Security Modes" {shape: rectangle}
acl_interaction: "ACL Interaction" {shape: rectangle}
known_issues: "Known Issues" {shape: rectangle}

uidgid_mapping -> nfsv4_id_mapping_idmapd: uses
nfsv4_id_mapping_idmapd -> kerberos_security_modes: uses
kerberos_security_modes -> acl_interaction: uses
acl_interaction -> known_issues: uses
```

## Overview

NFS relies on UID/GID matching between client and server for access control. NFSv3 trusts client-reported UIDs; NFSv4 with Kerberos (`krb5`, `krb5i`, `krb5p`) adds cryptographic authentication. POSIX ACLs are supported over NFS but require the underlying filesystem to support them.

## UID/GID Mapping

```bash
# Check UID/GID of a file on the NFS server
ls -ln /data/shared

# Confirm the same UID exists on the client
id username
getent passwd 1001   # look up by UID

# Create matching user on client (if UIDs differ)
useradd -u 1001 -g 1001 -M -s /sbin/nologin nfsuser

# Use nfsnobody for squashed access
id nfsnobody   # typically UID 65534
```


```text title="Expected output"
total 48
-rw-r--r-- 1 1001 1001 4096 Nov 15 10:23 document.txt
-rw-r--r-- 1 1001 1001 2048 Nov 15 10:24 report.pdf
drwxr-xr-x 2 1001 1001 4096 Nov 15 10:20 archive
-rw-r--r-- 1 1002 1002 1024 Nov 15 09:45 other.log
uid=1000(admin) gid=1000(admin) groups=1000(admin),10(wheel)
nfsuser:x:1001:1001::/home/nfsuser:/sbin/nologin
uid=65534(nfsnobody) gid=65534(nfsnobody) groups=65534(nfsnobody)
```

!!! warning "Common errors"
    **`getent passwd 1001: no such user`** — The UID 1001 does not exist on the client; create it with `useradd -u 1001 -g 1001 -M -s /sbin/nologin nfsuser` to match the server.
    **`useradd: UID 1001 is already in use`** — The UID already exists on the client with a different username; either use a different UID or delete the conflicting user first with `userdel`.
    **`id: nfsnobody: no such user`** — The nfsnobody user does not exist on this system; install the nfs-utils package or create it manually with `useradd -u 65534 -g 65534 -M nfsnobody`.
## NFSv4 ID Mapping (idmapd)

NFSv4 uses `user@domain` strings for identity. The `idmapd` daemon translates between names and UID/GIDs.

```bash
# /etc/idmapd.conf — set the same domain on client and server
[General]
Domain = corp.local

# Restart idmapd after editing
systemctl restart nfs-idmapd   # server
systemctl restart rpc-idmapd   # client (older distros)

# Check idmapd is running
systemctl status nfs-idmapd

# Debug: files showing "nobody" owner on client indicates idmap mismatch
# Force flush of idmap cache
nfsidmap -c
```


```text title="Expected output"
● nfs-idmapd.service - NFSv4 ID Mapper
     Loaded: loaded (/usr/lib/systemd/system/nfs-idmapd.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 14:32:47 UTC; 2s ago
       Docs: man:idmapd(8)
    Process: 8847 ExecStart=/usr/sbin/nfs-idmapd (code=exited, status=0/SUCCESS)
   Main PID: 8848 (nfs-idmapd)
      Tasks: 1 (limit: 4915)
     Memory: 1.2M
        CPU: 12ms
     CGroup: /system.slice/nfs-idmapd.service
             └─8848 /usr/sbin/nfs-idmapd

Jan 18 14:32:47 nfs-server01 systemd[1]: Started NFSv4 ID Mapper.
```

!!! warning "Common errors"
    **`systemctl: command not found`** — Verify the system uses systemd (RHEL/CentOS 7+, Ubuntu 15.04+); older distros use `service nfs-idmapd restart` instead.
    **`nfsidmap: command not found`** — Install the nfs-utils package with `apt-get install nfs-utils` (Debian/Ubuntu) or `yum install nfs-utils` (RHEL/CentOS).
    **`Domain = corp.local` not taking effect (files still show "nobody")`** — Ensure `/etc/idmapd.conf` has identical `Domain` values on both client and server, then run `nfsidmap -c` and remount the NFS share.
## Kerberos Security Modes

| Mode | Authentication | Integrity | Encryption |
|------|----------------|-----------|------------|
| `sec=sys` | UID/GID (trust client) | No | No |
| `sec=krb5` | Kerberos ticket | No | No |
| `sec=krb5i` | Kerberos ticket | Yes | No |
| `sec=krb5p` | Kerberos ticket | Yes | Yes |

```bash
# Export with Kerberos (server /etc/exports)
/data/secure  192.168.10.0/24(rw,sync,sec=krb5i,no_subtree_check)

# Mount with Kerberos (client)
mount -t nfs4 -o sec=krb5i 192.168.10.10:/data/secure /mnt/secure

# Verify Kerberos keytab includes nfs/ principal
klist -k /etc/krb5.keytab | grep nfs
```


```text title="Expected output"
Keytab name: FILE:/etc/krb5.keytab
KVNO Timestamp           Principal
---- ------------------- ------
   3 01/15/2025 09:22:14 nfs/nfsserver.example.com@EXAMPLE.COM (des3-cbc-sha1)
   3 01/15/2025 09:22:14 nfs/nfsserver.example.com@EXAMPLE.COM (aes256-cts-hmac-sha1-96)
   2 01/15/2025 08:45:02 host/nfsserver.example.com@EXAMPLE.COM (aes256-cts-hmac-sha1-96)
```

!!! warning "Common errors"
    **`mount.nfs4: access denied by server while mounting 192.168.10.10:/data/secure`** — Verify the client IP is within the 192.168.10.0/24 range in /etc/exports and reload exports with `exportfs -ra`.
    **`klist: No such file or directory while opening keytab /etc/krb5.keytab`** — Generate the keytab on the NFS server using `kadmin.local -q "ktadd -k /etc/krb5.keytab nfs/nfsserver.example.com@REALM"`.
    **`mount.nfs4: No security policy found for sec=krb5i`** — Install nfs-utils with Kerberos support (`yum install nfs-utils` on RHEL/CentOS or `apt install nfs-common` on Debian) and restart the NFS service.
## ACL Interaction

```bash
# Check if ACLs are supported on the NFS mount
getfacl /mnt/shared/testfile

# Set an ACL on the NFS server (must be done server-side for persistence)
setfacl -m u:devuser:rwx /data/shared/project

# Verify ACL is visible from client
getfacl /mnt/shared/project

# Mount with ACL support explicitly
mount -t nfs4 -o acl 192.168.10.10:/data/shared /mnt/shared
```


```text title="Expected output"
# file: /mnt/shared/testfile
# owner: root
# group: nfsgroup
user::rw-
user:appuser:r--
group::r--
mask::rwx
other::---

# file: /data/shared/project
# owner: sysadmin
# group: developers
user::rwx
user:devuser:rwx
group::r-x
mask::rwx
other::---

# file: /mnt/shared/project
# owner: sysadmin
# group: developers
user::rwx
user:devuser:rwx
group::r-x
mask::rwx
other::---
```

!!! warning "Common errors"
    **`setfacl: /data/shared/project: Operation not supported`** — Verify ACLs are enabled on the NFS server filesystem with `tune2fs -l /dev/sda1 | grep acl` and remount with `mount -o remount,acl /data` if needed.
    **`getfacl: /mnt/shared/project: No such file or directory`** — Ensure the NFS mount is active with `mount | grep nfs` and the export path exists on the server with `exportfs -v`.
    **`mount.nfs4: access denied by server while mounting 192.168.10.10:/data/shared`** — Verify the export is configured in `/etc/exports` on the server and run `exportfs -ra` to apply changes.
## Known Issues

- If files appear owned by `nobody` on the NFSv4 client, the `idmapd` domain setting does not match between client and server. Set `Domain =` to the same value in `/etc/idmapd.conf` on both sides.
- `no_root_squash` is required for backup agents or configuration management tools running as root on the client. Use it only for trusted management hosts, never for general user access exports.
- POSIX ACLs set on the server are visible over NFSv4 but not over NFSv3. If ACLs are critical, use NFSv4 and verify the underlying server filesystem (ext4, XFS) has ACL support mounted.
