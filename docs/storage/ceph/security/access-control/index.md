---
tags:
  - ceph
  - security
---
# Ceph — Access Control

<div class="kb-summary">
CephX user accounts, capability syntax for granular permissions, per-pool access control, admin key management, and least-privilege design for application service accounts.

*Applies to: Ceph Reef / Squid*
</div>
![Ceph — Access Control](../../../../assets/storage-ceph-security-access-control-index.svg)




```mermaid
graph TD
    classDef client fill:#2563eb,color:#fff
    classDef mon fill:#15803d,color:#fff
    classDef target fill:#7c3aed,color:#fff
    classDef action fill:#1e3a5f,color:#fff

    A([Client presents keyring]):::client --> B[MON validates shared key\nvia CephX challenge]:::mon
    B --> C{Key valid?}:::action
    C -- No --> D([Access denied]):::action
    C -- Yes --> E[MON issues session ticket\nencrypted with target daemon key]:::mon
    E --> F([Client presents ticket\nto OSD / MDS / RGW]):::client
    F --> G[Daemon decrypts ticket\nverifies caps + expiry]:::target
    G --> H{Caps allow op?}:::action
    H -- No --> I([Permission denied]):::action
    H -- Yes --> J([I/O proceeds]):::target
```

```d2
direction: down

root: "Ceph\nAccess Control" {shape: hexagon}
cephx_user_management: "CephX User Management" {shape: rectangle}
capability_syntax_reference: "Capability Syntax Reference" {shape: rectangle}
service_account_patterns: "Service Account Patterns" {shape: rectangle}
keyring_file_management: "Keyring File Management" {shape: rectangle}
rgw_user_layers: "RGW User Layers" {shape: rectangle}
rook_kubernetes_keyring_access: "Rook / Kubernetes Keyring Access" {shape: rectangle}
resources: Protected Resources {shape: cylinder}

root -> cephx_user_management: role
cephx_user_management -> resources: scoped
root -> capability_syntax_reference: role
capability_syntax_reference -> resources: scoped
root -> service_account_patterns: role
service_account_patterns -> resources: scoped
root -> keyring_file_management: role
keyring_file_management -> resources: scoped
root -> rgw_user_layers: role
rgw_user_layers -> resources: scoped
root -> rook_kubernetes_keyring_access: role
rook_kubernetes_keyring_access -> resources: scoped
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

## See also

- [Ceph — Authentication](../authentication/)
- [Ceph — Hardening](../hardening/)
