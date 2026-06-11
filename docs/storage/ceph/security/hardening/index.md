# Ceph — Hardening

<div class="kb-summary">
Ceph security hardening: network firewall rules for cluster isolation, disabling unused mgr modules, alert configuration, dashboard access control, and CIS-aligned controls.
</div>

```text
┌────────────────────────────────────────── Ceph — Hardening ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Network: firewall the cluster network; only Ceph nodes should reach OSD ports              │    │
│   │   Dashboard: change default admin password; enable TLS; restrict source IPs                  │    │
│   │   Modules: disable pg_autoscaler, telemetry, crash if not needed to reduce attack surface    │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cluster network = Separate network for OSD-to-OSD replication; block from client-facing hosts        │
│  Public network  = Client-facing network; OSDs listen here for client I/O requests                    │
│  firewalld      = Linux firewall service; restrict cluster network ports to Ceph OSD nodes only       │
│  Dashboard TLS  = Ceph Dashboard HTTPS cert; ceph dashboard create-self-signed-cert for internal use  │
│  telemetry module = MGR module sending anonymous usage data to Ceph project; disable if not desired   │
│  pg_autoscaler  = MGR module auto-adjusting PG counts; disable for production cluster stability       │
│  crash module   = Captures daemon crash dumps; keep enabled for diagnostic visibility                 │
│  admin socket   = Unix socket for per-daemon runtime info; restrict file permissions on all hosts     │
│  msgr2 secure   = Ceph messenger v2 encryption mode; encrypts all OSD-to-OSD and client traffic       │
│  ceph config    = Central config database; use to set security options without editing ceph.conf      │
│  nomonmap       = Prevents unauthenticated MON map enumeration; enforced by CephX by default          │
│  CIS benchmark  = Center for Internet Security hardening guide; reference for Ceph compliance audits  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Network Firewall Rules

```bash
# Ports used by Ceph daemons:
# MON:      6789 (msgr1), 3300 (msgr2)
# OSD:      6800-7568 (each OSD uses 2 ports)
# MGR:      8443 (dashboard), 9283 (Prometheus metrics)
# RGW:      7480 (HTTP), 443 (HTTPS)
# MDS:      6800+ (communication with MON + clients)

# firewalld example for OSD nodes (cluster network must be internal-only)
firewall-cmd --permanent --zone=internal --add-source=10.0.2.0/24  # cluster network CIDR
firewall-cmd --permanent --zone=internal --add-port=6800-7568/tcp

# Public network (client access)
firewall-cmd --permanent --zone=public --add-source=10.0.1.0/24   # public network CIDR
firewall-cmd --permanent --zone=public --add-port=6789/tcp          # MON
firewall-cmd --permanent --zone=public --add-port=3300/tcp          # MON msgr2
firewall-cmd --permanent --zone=public --add-port=6800-7568/tcp     # OSD
firewall-cmd --reload

# Block all other inbound on cluster network
# (cluster network should not be reachable from outside Ceph nodes)
```

## Dashboard Hardening

```bash
# Change default admin password
ceph dashboard ac-user-set-password admin --password-policy-check-enabled NewSecurePassword123!

# Enable TLS (use custom cert)
ceph config set mgr mgr/dashboard/ssl true
ceph dashboard set-ssl-certificate -i /etc/ceph/dashboard.crt
ceph dashboard set-ssl-certificate-key -i /etc/ceph/dashboard.key

# Create read-only monitoring user (instead of using admin)
ceph dashboard ac-user-create monitoring viewer viewer
# Roles: administrator, read-only, block-manager, rgw-manager, cluster-manager, pool-manager, cephfs-manager

# Disable dashboard if not needed
ceph mgr module disable dashboard
```

## Disable Unnecessary MGR Modules

```bash
# List enabled modules
ceph mgr module ls | grep enabled

# Disable modules not in use
ceph mgr module disable telemetry      # disables opt-in telemetry
ceph mgr module disable insights       # workload analytics (if not using)
ceph mgr module disable rbd_support    # if not using RBD monitoring hooks

# pg_autoscaler: useful but review if you want manual PG control
ceph mgr module disable pg_autoscaler  # if you manage PGs manually

# List currently active module plugins
ceph mgr services
```

## CIS Hardening Checklist

| Control | Action |
|---|---|
| Change default admin keyring location | Move client.admin keyring out of /etc/ceph/ on non-admin nodes |
| Disable SSH root login on Ceph nodes | Use cephadm SSH key only; disable PasswordAuthentication |
| Enable NTP on all nodes | Clock skew > 500ms causes MON election failures |
| Enable msgr2 secure mode | Encrypt client and inter-daemon traffic |
| Enable OSD encryption | Configure dmcrypt at OSD creation time |
| Restrict dashboard access | Use TLS; non-admin roles for monitoring users |
| Enable Prometheus auth | Configure basic auth or mTLS for Prometheus scrape endpoint |
| Disable unused mgr modules | Reduce attack surface; disable telemetry, insights if unused |
| Log audit trail | Enable Ceph audit log: `ceph config set global log_to_file true` |
| Firewall cluster network | Only Ceph nodes should reach OSD replication ports |
