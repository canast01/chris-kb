# NFS Permissions


<div class="kb-summary">
NFS Permissions reference covering Overview, UID/GID Mapping, NFSv4 ID Mapping (idmapd), Kerberos Security Modes, ACL Interaction and 1 more sections.
</div>

        NFS PERMISSION LAYERS
```text
┌──────────────────────────────────────────────────────────────┐
│  Layer 1 — EXPORT OPTIONS (server /etc/exports)                                                       │
│  ┌────────────────────────────────────────────────────────┐                                           │
│  │  IP restriction: only 192.168.10.0/24 can mount        │                                           │
│  │  root_squash: root on client → UID 65534 (nfsnobody)   │                                           │
│  │  ro / rw: read-only or read-write at mount level        │                                          │
│  └────────────────────────────────────────────────────────┘                                           │
│                         │ mount permitted                                                             │
│                         ▼                                                                             │
│  Layer 2 — POSIX UID/GID on files (server filesystem)                                                 │
│  ┌────────────────────────────────────────────────────────┐                                           │
│  │  File owner: UID 1001 (must match client UID 1001)      │                                          │
│  │  Permissions: rwxr-xr-x                                │                                           │
│  │  NFSv4: user@domain mapping via idmapd                 │                                           │
│  └────────────────────────────────────────────────────────┘                                           │
│                         │                                                                             │
│  Effective access = export options AND POSIX permissions                                              │
└──────────────────────────────────────────────────────────────┘
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

## Known Issues

- If files appear owned by `nobody` on the NFSv4 client, the `idmapd` domain setting does not match between client and server. Set `Domain =` to the same value in `/etc/idmapd.conf` on both sides.
- `no_root_squash` is required for backup agents or configuration management tools running as root on the client. Use it only for trusted management hosts, never for general user access exports.
- POSIX ACLs set on the server are visible over NFSv4 but not over NFSv3. If ACLs are critical, use NFSv4 and verify the underlying server filesystem (ext4, XFS) has ACL support mounted.
