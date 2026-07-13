---
tags:
  - ceph
  - security
description: "CephX user accounts, capability syntax for granular permissions, per-pool access control, admin key management, and least-privilege design for application..."
---
# Ceph — Access Control

<div class="kb-summary">
CephX user accounts, capability syntax for granular permissions, per-pool access control, admin key management, and least-privilege design for application service accounts.

*Applies to: Ceph Reef / Squid*
</div>

```d2
direction: right

A: "Client presents keyring" {shape: rectangle}
B: "MON validates shared key\nvia CephX challenge" {shape: rectangle}
E: "MON issues session ticket\nencrypted with target daemon key" {shape: rectangle}
F: "Client presents ticket\nto OSD / MDS / RGW" {shape: rectangle}
G: "Daemon decrypts ticket\nverifies caps + expiry" {shape: rectangle}
D: "Access denied" {shape: rectangle}
I: "Permission denied" {shape: rectangle}
J: "I/O proceeds" {shape: rectangle}

A -> B
E -> F
F -> G
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## CephX User Management

```bash
ceph auth ls                          # list all keyring entities
ceph auth get client.<name>           # show caps and key for one entity
ceph auth get-key client.<name>       # just the key (for scripting)

# Create a scoped service account
ceph auth add client.<name> \
  mon 'allow r' \
  osd 'allow rw pool=<pool>'

# Update capabilities on existing entity
ceph auth caps client.<name> \
  osd 'allow rw pool=rbd' \
  mon 'allow r'

# Delete entity
ceph auth del client.<name>

# Export for distribution to application nodes
ceph auth export client.<name> > keyring.conf

# Create service account (Cinder/Nova example)
ceph auth get-or-create client.cinder \
  mon 'profile rbd' \
  osd 'profile rbd pool=volumes, profile rbd pool=vms, profile rbd-read-only pool=images' \
  -o /etc/ceph/ceph.client.cinder.keyring

# Create read-only monitoring user
ceph auth get-or-create client.readonly \
  mon 'allow r' \
  osd 'allow r' \
  -o /etc/ceph/ceph.client.readonly.keyring

# Create user with access to specific pool only
ceph auth get-or-create client.myapp \
  mon 'allow r' \
  osd 'allow rw pool=myapp-pool' \
  -o /etc/ceph/ceph.client.myapp.keyring
```


```text title="Expected output"
client.admin
	key: AQDvF8Zl7x9kLhAAIxK2p8m9Q3vR5sT6uW7xYz==
	caps: [mds] allow *, [mgr] allow *, [mon] allow *, [osd] allow *
client.cinder
	key: AQC4G9Zm8y0mNiBAJyL3q9n0R4wS6tU7vX8yZa==
	caps: [mon] profile rbd, [osd] profile rbd pool=volumes, profile rbd pool=vms, profile rbd-read-only pool=images
client.readonly
	key: AQD5H0an9z1pOjCBKzM4r0o1S5xT7uV8wY9zAb==
	caps: [mon] allow r, [osd] allow r
client.myapp
	key: AQE6I1bo0a2qPkDCLaN5s1p2T6yU8vW9xZ0aBc==
	caps: [mon] allow r, [osd] allow rw pool=myapp-pool

exported client.cinder to keyring.conf
created client.readonly keyring at /etc/ceph/ceph.client.readonly.keyring
created client.myapp keyring at /etc/ceph/ceph.client.myapp.keyring
```

!!! warning "Common errors"
    **`Error EACCES: permission denied`** — Ensure the user running ceph commands has sudo privileges or is in the ceph group with `sudo usermod -a -G ceph $USER`.
    **`Error EINVAL: invalid value for argument`** — Verify pool names exist with `ceph osd pool ls` and use correct capability syntax (e.g., `allow rw pool=poolname` not `allow rw poolname`).
    **`Error ENOENT: No such file or directory`** — Create the target keyring directory with `sudo mkdir -p /etc/ceph` before exporting keyrings with the `-o` flag.
## Capability Syntax Reference

| Capability String | Scope | Effect |
|---|---|---|
| `allow r` | any service | Read-only access |
| `allow rw` | any service | Read-write access |
| `allow rwx` | osd | Read-write plus class method execution |
| `allow *` | any service | Full unrestricted access |
| `allow rw pool=<name>` | osd | Read-write scoped to named pool |
| `allow rw namespace=<ns>` | osd | Read-write scoped to RBD namespace |
| `profile rbd` | mon / osd | Pre-defined RBD client capability set |
| `profile rbd-read-only` | osd | Pre-defined read-only RBD access |
| `allow rw path=/exports/t1` | mds | CephFS directory-level restriction |

```bash
# MON capabilities
mon 'allow r'         # read-only (status, maps)
mon 'profile rbd'     # preset for RBD clients
mon 'allow *'         # full admin (use only for client.admin)

# OSD capabilities — combined multi-pool
osd 'allow rw pool=volumes, allow r pool=images, allow rw pool=vms'

# Namespace-scoped (RBD namespaces within a pool)
osd 'allow rw pool=rbd namespace=tenant1'

# MDS capabilities (CephFS)
mds 'allow rw path=/exports/tenant1'  # directory-level restriction
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error EINVAL: invalid capability string`** — Verify syntax matches `allow|deny <action> [pool=<name>]` and check for typos in pool or namespace names.
    **`Error EACCES: permission denied`** — Ensure the client key has `mon 'allow r'` capability before attempting OSD or MDS operations; add missing mon capability to the key definition.
## Service Account Patterns

Never use `client.admin` in application configuration files. Create a dedicated keyring per application with the minimum required pool access.

```bash
# Recommended pattern: one keyring per application workload
# App A: read-write on app-a-pool only
ceph auth get-or-create client.app-a \
  mon 'allow r' \
  osd 'allow rw pool=app-a-pool'

# App B: read-only on shared dataset
ceph auth get-or-create client.app-b \
  mon 'allow r' \
  osd 'allow r pool=shared-data'

# Backup agent: needs read from all data pools, write to backup pool
ceph auth get-or-create client.backup \
  mon 'allow r' \
  osd 'allow r pool=volumes, allow r pool=vms, allow rw pool=backups'
```


```text title="Expected output"
[client.app-a]
	key = AQC7vZdnK3p+ExAAZ8mK9vL2pQ4rT5sW6xYzAg==
	caps mon = "allow r"
	caps osd = "allow rw pool=app-a-pool"

[client.app-b]
	key = AQDmwZdnL4q/FxBBa9nL0wM3qR5sU6tX7yZaBh==
	caps mon = "allow r"
	caps osd = "allow r pool=shared-data"

[client.backup]
	key = AQEnxadnM5r+GyCCb0oM1xN4rS6tV7uY8zaBci==
	caps mon = "allow r"
	caps osd = "allow r pool=volumes, allow r pool=vms, allow rw pool=backups"
```

!!! warning "Common errors"
    **`Error EACCES: permission denied`** — Ensure the user running the command has sudo privileges or is part of the ceph group; run `sudo ceph auth get-or-create` if needed.
    **`Error: pool 'app-a-pool' does not exist`** — Create the pool first with `ceph osd pool create app-a-pool <pg_num>` before assigning capabilities to it.
    **`Error EINVAL: invalid caps`** — Verify the OSD capability syntax uses commas without spaces between pool rules (e.g., `allow r pool=volumes, allow r pool=vms` is correct).
Quarterly rotation procedure: create new entity with `-new` suffix, distribute, verify, then delete old.

## Keyring File Management

```bash
# Keyring files must be owned by root, mode 600
ls -la /etc/ceph/*.keyring
chmod 600 /etc/ceph/ceph.client.*.keyring
chown root:root /etc/ceph/ceph.client.*.keyring

# Export keyring for distribution to application nodes
ceph auth export client.cinder > /tmp/ceph.client.cinder.keyring
scp /tmp/ceph.client.cinder.keyring app-node:/etc/ceph/

# Verify key on application node
ceph --keyring /etc/ceph/ceph.client.cinder.keyring --id cinder status
```


```text title="Expected output"
-rw------- 1 root root 129 Nov 14 10:23 /etc/ceph/ceph.client.admin.keyring
-rw------- 1 root root 115 Nov 14 10:23 /etc/ceph/ceph.client.cinder.keyring
-rw------- 1 root root 108 Nov 14 10:23 /etc/ceph/ceph.client.glance.keyring
ceph.client.cinder.keyring                                    100%  115     45.2KB/s   00:00
  cluster:
    mon: allow profile rbd
    osd: allow class-read object_prefix rbd_children, allow rwx pool=cinder-volumes
  mds: allow rw
  fsid: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  released: squid
  status: HEALTH_OK
  monmap e3: 3 mons at {mon-01=10.0.1.10:6789/0,mon-02=10.0.1.11:6789/0,mon-03=10.0.1.12:6789/0}
  election epoch 24, quorum 0,1,2
  fsid a1b2c3d4-e5f6-7890-abcd-ef1234567890
  health HEALTH_OK
```

!!! warning "Common errors"
    **`scp: /etc/ceph/ceph.client.cinder.keyring: Permission denied`** — Ensure the destination directory exists and the app-node user has write permissions, or use `sudo scp` with passwordless SSH key authentication configured.
    **`Error connecting to the cluster: (13) Permission denied`** — Verify the keyring file exists at the specified path and is readable by the cinder user; check that the key has appropriate Ceph capabilities assigned via `ceph auth get client.cinder`.
## RGW User Layers

RGW authentication operates at two independent layers. Confusion between them is a common misconfiguration.

| Layer | Entity type | Managed by | Purpose |
|---|---|---|---|
| CephX (daemon auth) | `client.rgw.<id>` | `ceph auth` | RGW daemon authenticates to MON/OSD |
| RGW user (S3/Swift) | S3 access key / Swift user | `radosgw-admin` | End-user or application S3/Swift access |

```bash
# CephX entity for the RGW daemon itself (created by cephadm automatically)
ceph auth get client.rgw.myorg

# RGW S3/Swift user management — completely separate from cephx
radosgw-admin user create --uid=app-user --display-name="App Service Account" \
  --access-key=AKID1234 --secret=secretkey

radosgw-admin user info --uid=app-user
radosgw-admin caps add --uid=app-user --caps="buckets=read"
```


```text title="Expected output"
[client.rgw.myorg]
	key = AQDvZ8Zl9xK3FRAAp7vQ8m2K9L0pQ1R2S3T4U5==
	caps mon = "allow rwx"
	caps osd = "allow rwx pool=default.rgw.buckets.data,default.rgw.buckets.index"

{
    "user_id": "app-user",
    "display_name": "App Service Account",
    "email": "",
    "suspended": 0,
    "max_buckets": 1000,
    "auid": 0,
    "subusers": [],
    "keys": [
        {
            "user": "app-user",
            "access_key": "AKID1234",
            "secret_key": "secretkey"
        }
    ],
    "swift_keys": [],
    "caps": [
        {
            "type": "buckets",
            "perm": "read"
        }
    ],
    "op_mask": "read",
    "default_placement": "",
    "placement_tags": [],
    "bucket_quota": {
        "enabled": false,
        "check_on_list": false,
        "max_size": -1,
        "max_objects": -1
    },
    "user_quota": {
        "enabled": false,
        "check_on_list": false,
        "max_size": -1,
        "max_objects": -1
    },
    "temp_url_keys": [],
    "type": "rgw",
    "mfa_ids": []
}
```

!!! warning "Common errors"
    **`error: ENOENT: couldn't find user app-user`** — Run `radosgw-admin user create` before attempting `radosgw-admin user info` or `radosgw-admin caps add`.
    **`error: invalid access key format`** — Use a valid AWS-style access key (20+ alphanumeric characters) or omit `--access-key` to auto-generate one.
## Rook / Kubernetes Keyring Access

Rook stores all cephx keyrings as Kubernetes Secrets in the `rook-ceph` namespace. Never copy them manually; retrieve via `oc get secret`.

```bash
# List cephx-related secrets
oc get secret -n rook-ceph | grep keyring

# Retrieve admin keyring (base64-encoded)
oc get secret -n rook-ceph rook-ceph-admin-keyring -o jsonpath='{.data.keyring}' | base64 -d

# Retrieve OSD keyring for a specific OSD
oc get secret -n rook-ceph rook-ceph-osd-<id>-keyring -o jsonpath='{.data.keyring}' | base64 -d

# Create a custom keyring secret for an application
oc create secret generic ceph-app-keyring \
  --from-file=keyring=/etc/ceph/ceph.client.myapp.keyring \
  -n rook-ceph
```


```text title="Expected output"
rook-ceph-admin-keyring                          Opaque                                1      45d
rook-ceph-mon-keyring                            Opaque                                1      45d
rook-ceph-osd-0-keyring                          Opaque                                1      45d
rook-ceph-osd-1-keyring                          Opaque                                1      45d
rook-ceph-rgw-keyring                            Opaque                                1      45d

[client.admin]
	key = AQC7vOdlK3+PHRAAj8Z1Z2K5vZ8K9mL3Z5K8Zg==
	caps mon = "allow *"
	caps osd = "allow *"
	caps mds = "allow *"

[client.osd.0]
	key = AQDvwOdlL4+QIRAAk9a2a3L6wa9L0nM4a6L9ah==
	caps mon = "allow profile osd"
	caps osd = "allow *"

secret/ceph-app-keyring created
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "secret" in group "" in the namespace "rook-ceph"`** — Verify the rook-ceph namespace exists with `oc get ns rook-ceph` and that the Rook operator is deployed.
    **`error: resource name may not be empty`** — Replace `<id>` with the actual OSD number (e.g., `rook-ceph-osd-0-keyring`) in the OSD keyring retrieval command.
    **`error: no such file or directory`** — Ensure the keyring file exists at `/etc/ceph/ceph.client.myapp.keyring` before creating the secret, or use `--from-literal=keyring=<key-content>` instead.
## Capability Audit

Regularly audit which entities exist and what capabilities they hold. Remove unused entities; tighten capabilities that are wider than needed.

```bash
# Show all entities with capabilities (review for over-privileged accounts)
ceph auth ls

# Find any entity with allow * (should only be client.admin and bootstrap keys)
ceph auth ls | grep -B1 "allow \*"

# Export full auth state for offline review
ceph auth export > /tmp/ceph-auth-audit-$(date +%F).txt

# Check for entities with rw on all pools (should be pool-scoped)
ceph auth ls | grep "allow rw$"   # flag: no pool restriction
```


```text title="Expected output"
entity auid cap mon cap osd cap mds cap mgr
client.admin 0 allow * allow * allow * allow *
client.rbd-pool-user 1 allow r pool=rbd allow rwx pool=rbd
client.cephfs-user 2 allow r pool=cephfs_data,cephfs_metadata allow rwx pool=cephfs_data,cephfs_metadata
client.backup 3 allow profile rbd pool=backups allow rwx pool=backups
mgr.ceph-node1 4 allow profile mgr allow rwx
osd.0 5 allow rwx allow rwx
osd.1 5 allow rwx allow rwx

entity auid cap mon cap osd cap mds cap mgr
client.admin 0 allow * allow * allow * allow *

Exported auth state to /tmp/ceph-auth-audit-2024-01-15.txt

(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error connecting to cluster: [Errno 2] No such file or directory`** — Ensure the Ceph cluster is running and `/etc/ceph/ceph.conf` exists on the local system.
    **`permission denied: user does not have caps: mon ['allow r']`** — Run these commands as root or with sudo, or use a client key with sufficient mon and auth capabilities.
    **`grep: (standard input): No such file or directory`** — Verify the Ceph cluster is healthy with `ceph status` before running auth queries.
## Access Control Checklist

| Check | Expected state | Command |
|---|---|---|
| No app uses client.admin | client.admin absent from all app configs | `grep -r client.admin /etc/` |
| All keyring files mode 600 | `-rw-------` on all keyring files | `ls -la /etc/ceph/*.keyring` |
| Per-pool scoping | All app accounts have `pool=` in osd caps | `ceph auth ls \| grep osd` |
| Unused entities removed | No orphaned service accounts | `ceph auth ls` |
| Bootstrap keys restricted | No bootstrap key with `allow *` | `ceph auth get client.bootstrap-osd` |
| Keyring rotation log | All rotations logged with date and owner | Maintain a rotation register |

## Profile-Based Capabilities (Pre-Defined)

Ceph ships with pre-defined capability profiles that bundle common permissions. Prefer profiles over raw capability strings to reduce misconfiguration risk.

| Profile | Target service | What it grants |
|---|---|---|
| `profile rbd` | mon + osd | RBD client: pool access, class methods |
| `profile rbd-read-only` | osd | RBD read-only access to a named pool |
| `profile osd` | mon | OSD daemon identity (used by OSD daemons) |
| `profile mds` | mon | MDS daemon identity |
| `profile bootstrap-osd` | mon | Provision new OSD keyrings; limited scope |

```bash
# Use profile rbd for OpenStack Cinder/Nova/Glance
ceph auth get-or-create client.cinder \
  mon 'profile rbd' \
  osd 'profile rbd pool=volumes, profile rbd pool=vms, profile rbd-read-only pool=images'
```


```text title="Expected output"
[client.cinder]
	key = AQC7vZdnF8K3ExAA7vK9mZ4pQ2R8sT9uV0wXyZ==
	caps mon = "profile rbd"
	caps osd = "profile rbd pool=volumes, profile rbd pool=vms, profile rbd-read-only pool=images"
```

!!! warning "Common errors"
    **`Error EINVAL: invalid command`** — Verify the mon and osd capability strings are enclosed in single quotes and contain valid pool names that exist in your cluster.
    **`Error EACCES: permission denied`** — Run the command with appropriate Ceph cluster permissions (typically as root or with `sudo ceph` on a monitor node).
## See also

- [Ceph — Authentication](../authentication/)
- [Ceph — Hardening](../hardening/)
