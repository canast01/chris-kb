# NFS Versions


<div class="kb-summary">
NFS Versions reference covering Version Comparison, Recommended Version, Checking NFS Version in Use, Configuring NFS Version, NFSv4 ID Mapping and 1 more sections.
</div>

        NFSv3 vs NFSv4 vs NFSv4.1 COMPARISON
```text
┌─────────────────────┬──────────────┬──────────────┬──────────────┐
│ Feature             │   NFSv3      │   NFSv4      │  NFSv4.1     │
├─────────────────────┼──────────────┼──────────────┼──────────────┤
│ Transport           │ UDP or TCP   │ TCP only     │ TCP only     │
│ Port                │ 2049+111     │ 2049 only    │ 2049 only    │
│ Stateful            │ No           │ Yes          │ Yes          │
│ Locking             │ NLM (extra)  │ Built-in     │ Built-in     │
│ Kerberos auth       │ Optional     │ Supported    │ Supported    │
│ pNFS (parallel)     │ No           │ No           │ Yes          │
│ ACLs                │ No native    │ NFSv4 ACLs   │ NFSv4 ACLs  │
│ ID mapping          │ UID/GID nums │ user@domain  │ user@domain  │
├─────────────────────┼──────────────┼──────────────┼──────────────┤
│ Recommended for     │ Legacy only  │ General use  │ Modern/perf  │
└─────────────────────┴──────────────┴──────────────┴──────────────┘
```

## Version Comparison

| Feature | NFSv3 | NFSv4 | NFSv4.1 |
|---|---|---|---|
| Transport | UDP or TCP | TCP only | TCP only |
| Stateful | No | Yes | Yes |
| Security | AUTH_SYS (UID/GID) | Kerberos, RPCSEC_GSS | Kerberos, RPCSEC_GSS |
| ACLs | No native ACLs | NFSv4 ACLs | NFSv4 ACLs |
| Locking | NLM (separate protocol) | Built-in | Built-in |
| Multipath (pNFS) | No | No | Yes (pNFS) |
| Port | 2049 + portmapper (111) | 2049 fixed | 2049 fixed |
| ID mapping | UID/GID numbers | user@domain strings | user@domain strings |

## Recommended Version

- **NFSv4.1** — preferred for new deployments. Stateful, single port (2049), pNFS capable, strongest security options.
- **NFSv3** — legacy compatibility only. Required for some storage arrays and older clients.
- **NFSv4.0** — functional but superseded; prefer 4.1.

## Checking NFS Version in Use

```bash
# Linux client — show mount options including NFS version
mount | grep nfs
# or
cat /proc/mounts | grep nfs

# Verbose mount info including vers=
nfsstat -m

# Server-side — which versions are enabled
cat /proc/fs/nfsd/versions

# Show active NFS connections and versions
ss -tnp | grep :2049
```

## Configuring NFS Version

### Mount — Client Side

```bash
# Force NFSv4.1
mount -t nfs -o vers=4.1,rw <server>:<export> /mnt/data

# Force NFSv3
mount -t nfs -o vers=3,tcp <server>:<export> /mnt/data

# Persistent in /etc/fstab
<server>:/export  /mnt/data  nfs  vers=4.1,hard,timeo=600,rsize=1048576,wsize=1048576  0 0
```

### NFS Server — Enable/Disable Versions (RHEL/Rocky)

```bash
# /etc/nfs.conf — set which versions the server offers
[nfsd]
vers3=n       # disable NFSv3
vers4=y
vers4.0=n     # disable NFSv4.0
vers4.1=y
vers4.2=y

systemctl restart nfs-server
cat /proc/fs/nfsd/versions
```

## NFSv4 ID Mapping

NFSv4 maps file ownership using `user@domain` strings instead of raw UID/GID. Misconfigured ID mapping causes files to appear as `nobody`.

```bash
# Check idmapd is running
systemctl status rpcidmapd

# /etc/idmapd.conf
[General]
Domain = example.com   # must match on client and server

# Flush ID mapping cache
nfsidmap -c
```

## Common Version-Related Issues

| Symptom | Cause | Check |
|---|---|---|
| Files owned by `nobody` | NFSv4 ID mapping mismatch | Verify `Domain =` in `/etc/idmapd.conf` matches on both sides |
| Mount hangs / slow | NFSv4 state recovery after server restart | Use `hard` mount option; check `nfsstat` for retries |
| Kerberos auth fails | Clock skew > 5 minutes | Verify NTP sync on client and server |
| NFSv3 locks not released | Stale NLM lock | `sm-notify` restart or server-side lock clear |
| Client defaults to NFSv3 | Default mount type | Explicitly specify `vers=4.1` in mount options |
