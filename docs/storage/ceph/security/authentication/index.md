# Ceph — Authentication

<div class="kb-summary">
CephX shared-secret authentication protocol, how clients authenticate to MONs and OSDs, key distribution, session tickets, and secure bootstrap of new nodes.
</div>

## CephX Protocol Overview

```text
CephX uses a shared-secret (pre-shared key) mutual authentication scheme:

  1. Client requests a session ticket from MON
     Client presents: username + timestamp + encrypted nonce
     MON verifies: username in auth DB + decrypts nonce with stored key

  2. MON returns a session ticket
     Ticket is encrypted with the OSD's key
     Client cannot read the ticket content

  3. Client presents ticket to OSD
     OSD decrypts ticket using its own key
     OSD verifies: client name + capabilities + expiry timestamp

  4. Established session: normal I/O proceeds
     Sessions are time-limited (default: 12 hours)

Key properties:
  - No passwords over the wire; all challenges use HMAC
  - Compromise of one key doesn't expose others
  - Keys stored at: /etc/ceph/ceph.client.<name>.keyring (clients)
                     /var/lib/ceph/osd/ceph-N/keyring (OSDs)
                     /var/lib/ceph/mon/ceph-<host>/keyring (MONs)
```

## Key Distribution

```bash
# On a new client node that needs to access Ceph:
# 1. Install ceph-common package (provides ceph-fuse, rbd, rados commands)
dnf install -y ceph-common   # RHEL/Rocky
apt-get install -y ceph-common  # Ubuntu

# 2. Copy ceph.conf and keyring from admin node
scp admin-node:/etc/ceph/ceph.conf /etc/ceph/
scp admin-node:/etc/ceph/ceph.client.myapp.keyring /etc/ceph/

# 3. Set correct permissions
chmod 644 /etc/ceph/ceph.conf
chmod 600 /etc/ceph/ceph.client.myapp.keyring

# 4. Test connectivity
ceph --id myapp health
rbd --id myapp ls rbd
```

## Cluster Bootstrap Auth (New Node)

```bash
# When cephadm adds a new node, it:
# 1. Creates bootstrap keyrings for each daemon type
# 2. Generates unique OSD/MON keyrings per daemon
# 3. Distributes them via SSH (key already copied in advance)

# Verify keyrings exist on a new OSD node
ls /var/lib/ceph/osd/ceph-*/keyring

# Check MON keyring
cat /var/lib/ceph/mon/ceph-$(hostname -s)/keyring

# Verify daemon is authenticating correctly
ceph auth get osd.5   # should show capabilities
```

## Session Timeouts and Rotation

```bash
# Check current auth timeout settings
ceph config show-with-defaults global | grep -i auth_mon

# Adjust session timeout (default 12h for clients, 86400s)
ceph config set global auth_service_ticket_ttl 3600  # 1 hour sessions

# There is no automatic key rotation in Ceph — rotate manually
# Process:
# 1. Create new key with same capabilities
# 2. Distribute new keyring to all application nodes
# 3. Restart application services to pick up new key
# 4. Delete old key after confirming new key works
ceph auth del client.oldkey
```
