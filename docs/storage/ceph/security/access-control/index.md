# Ceph — Access Control

<div class="kb-summary">
CephX user accounts, capability syntax for granular permissions, per-pool access control, admin key management, and least-privilege design for application service accounts.
</div>

```text
┌──────────────────────────────────────── Ceph — Access Control ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   CephX: every client authenticates with a shared secret key; no anonymous access            │    │
│   │   Capabilities: per-service (mon, osd, mds); per-pool; least-privilege by default            │    │
│   │   Admin key: client.admin has full access; protect it; use service-specific keys in prod     │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CephX         = Ceph's native shared-secret mutual authentication protocol for all daemon access     │
│  capability    = Permission string granting access: mon, osd, mds per pool or service                 │
│  allow rw      = Read-write capability on a pool; use allow r for read-only service accounts          │
│  allow *       = Full access capability; reserved for client.admin and cephadm keys only              │
│  client.admin  = Superuser key; full cluster access; store securely; rotate on team changes           │
│  profile rbd   = Pre-defined capability set for RBD clients; grants pool-level rbd access             │
│  keyring       = File holding CephX key and capability: /etc/ceph/ceph.client.<name>.keyring          │
│  ceph auth add = Creates a new CephX user with specified capabilities                                 │
│  ceph auth get-or-create = Idempotent user creation; used by cephadm and automation scripts           │
│  caps osd      = OSD capability string; example: allow rw pool=rbd profile rbd                        │
│  least privilege = Grant only required capabilities; separate key per application/workload            │
│  bootstrap-osd = Bootstrap keyring used only during OSD initialization; limited lifespan              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## CephX User Management

```bash
# List all users
ceph auth ls

# Get specific user
ceph auth get client.admin
ceph auth get client.cinder

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

# Delete user
ceph auth del client.oldapp

# Rotate key (delete and recreate)
ceph auth del client.myapp
ceph auth get-or-create client.myapp mon 'allow r' osd 'allow rw pool=myapp-pool'
```

## Capability Syntax Reference

```bash
# MON capabilities
mon 'allow r'         # read-only (status, maps)
mon 'profile rbd'     # preset for RBD clients
mon 'allow *'         # full admin (use only for client.admin)

# OSD capabilities
osd 'allow r'                          # read-only all pools
osd 'allow rw'                         # read-write all pools
osd 'allow rw pool=rbd'                # read-write specific pool
osd 'allow class-read object_prefix rbd_children'  # for clones
osd 'profile rbd pool=rbd'             # preset for RBD on specific pool
osd 'profile rbd-read-only pool=rbd'   # preset for read-only RBD

# Combined: different access per pool
osd 'allow rw pool=volumes, allow r pool=images, allow rw pool=vms'

# MDS capabilities (CephFS)
mds 'allow'    # full filesystem access
mds 'allow rw path=/exports/tenant1'  # directory-level restriction
```

## Keyring File Management

```bash
# Keyring files should be owned by root, mode 600
ls -la /etc/ceph/*.keyring
chmod 600 /etc/ceph/ceph.client.*.keyring
chown root:root /etc/ceph/ceph.client.*.keyring

# Export keyring for distribution to application nodes
ceph auth export client.cinder > /tmp/ceph.client.cinder.keyring
scp /tmp/ceph.client.cinder.keyring app-node:/etc/ceph/

# Verify key on application node
ceph --keyring /etc/ceph/ceph.client.cinder.keyring --id cinder status
```
