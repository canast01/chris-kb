---
tags:
  - ceph
  - security
---
# Ceph — Hardening

<div class="kb-summary">
Ceph security hardening: network isolation, msgr2 encryption, cephx least-privilege, OSD encryption, RGW HTTPS, dashboard TLS, audit logging, and CIS-aligned controls.

*Applies to: Ceph Reef / Squid*
</div>

```d2
direction: right

A: "Network isolation\ncluster / public separation" {shape: rectangle}
B: "msgr2 secure mode\nin-transit encryption" {shape: rectangle}
C: "CephX auth\nper-entity keys + caps" {shape: rectangle}
D: "OSD encryption\ndm-crypt at rest" {shape: rectangle}
E: "RGW HTTPS / TLS\nobject gateway hardening" {shape: rectangle}
F: "Dashboard TLS + MFA\nrestrict admin access" {shape: rectangle}
G: "Audit logging\nauth_debug + ops log" {shape: rectangle}

A -> B
B -> C
C -> D
D -> E
E -> F
F -> G
```

```d2
direction: down

network_isolation: "Network Isolation" {shape: rectangle}
firewall_rules: "Firewall Rules" {shape: rectangle}
disable_insecure_msgr1: "Disable Insecure msgr1" {shape: rectangle}
dashboard_security: "Dashboard Security" {shape: rectangle}
disable_unnecessary_mgr_modules: "Disable Unnecessary MGR Modules" {shape: rectangle}
audit_logging: "Audit Logging" {shape: rectangle}

network_isolation -> firewall_rules: hardens
firewall_rules -> disable_insecure_msgr1: hardens
disable_insecure_msgr1 -> dashboard_security: hardens
dashboard_security -> disable_unnecessary_mgr_modules: hardens
disable_unnecessary_mgr_modules -> audit_logging: hardens
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Network Isolation

```bash
# Verify cluster network is configured (OSD replication stays on dedicated network)
ceph config get osd cluster_network
ceph config get osd public_network

# Set if not configured
ceph config set global cluster_network 10.0.1.0/24
ceph config set global public_network 10.0.0.0/24

# Verify separation took effect on a running OSD
ceph daemon osd.0 config show | grep -E "cluster_network|public_network"
```


```text title="Expected output"
10.0.1.0/24
10.0.0.0/24
(no output — command completes silently)
(no output — command completes silently)
    "cluster_network": "10.0.1.0/24",
    "public_network": "10.0.0.0/24",
```

!!! warning "Common errors"
    **`Error ENOENT: error calling set_config_option`** — Ensure the OSD daemon is running with `ceph osd stat` before applying config changes.
    **`error connecting to the cluster`** — Verify cluster connectivity and that your `ceph.conf` or `CEPH_ARGS` environment variable points to a valid monitor address.
    **`grep: (standard input) is empty`** — The OSD may not have reloaded the config; restart it with `sudo systemctl restart ceph-osd@0` or wait for the next config reload cycle.
## Firewall Rules

| Port | Protocol | From | To | Purpose |
|---|---|---|---|---|
| 6789 | TCP | Client hosts | MON nodes | MON msgr1 (legacy) |
| 3300 | TCP | All Ceph nodes + clients | MON nodes | MON msgr2 |
| 6800–7300 | TCP | Ceph nodes only | OSD nodes | OSD replication + client I/O |
| 8080 | TCP | Admin hosts | MGR node | Dashboard HTTP (disable; use 8443) |
| 8443 | TCP | Admin hosts | MGR node | Dashboard HTTPS |
| 9283 | TCP | Prometheus host | MGR node | Prometheus metrics exporter |
| 7480 | TCP | Client hosts | RGW nodes | RGW HTTP default (prefer 443) |
| 443 | TCP | Client hosts | RGW nodes | RGW HTTPS |

```bash
# firewalld example for OSD nodes (cluster network must be internal-only)
firewall-cmd --permanent --zone=internal --add-source=10.0.1.0/24  # cluster network CIDR
firewall-cmd --permanent --zone=internal --add-port=6800-7300/tcp

# Public network (client access to MON and OSD)
firewall-cmd --permanent --zone=public --add-source=10.0.0.0/24
firewall-cmd --permanent --zone=public --add-port=3300/tcp          # MON msgr2
firewall-cmd --permanent --zone=public --add-port=6800-7300/tcp     # OSD client I/O
firewall-cmd --reload
# Block all other inbound on cluster network from outside Ceph nodes
```


```text title="Expected output"
success
success
success
success
success
success
FirewallD is reloading...
```

!!! warning "Common errors"
    **`Error: INVALID_ZONE: public`** — Verify the zone exists with `firewall-cmd --get-zones` and create it if needed with `firewall-cmd --permanent --new-zone=public`.
    **`Error: INVALID_ADDR: '10.0.1.0/24' not usable`** — Ensure the CIDR notation is valid and the source network matches your actual cluster network topology.
    **`Error: COMMAND_FAILED: 'firewall-cmd --reload' failed with exit code 1`** — Check syntax of all previous rules with `firewall-cmd --permanent --list-all` and fix any malformed entries before reloading.
## Disable Insecure msgr1

```bash
# Force all connections to use msgr2 (prevents protocol downgrade attacks)
ceph config set global ms_bind_msgr1 false

# Enable encrypted mode on all connection types
ceph config set global ms_cluster_mode secure    # OSD-to-OSD
ceph config set global ms_service_mode secure    # client-to-OSD / MON
ceph config set global ms_client_mode secure     # outgoing client connections

# Verify
ceph config get mon ms_cluster_mode   # expected: secure
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
secure
```

!!! warning "Common errors"
    **`Error EINVAL: ms_bind_msgr1 = false not supported by this Ceph version`** — Upgrade to Ceph Nautilus or later, as msgr2 enforcement requires a recent cluster version.
    **`Error: set config failed: unknown option 'ms_cluster_mode'`** — Verify the config option name matches your Ceph version (some versions use `ms_mode` instead); check `ceph config help` for available options.
## Dashboard Security

```bash
# Change default admin password
ceph dashboard ac-user-set-password admin --password-policy-check-enabled NewSecurePassword123!

# Enable HTTPS with a signed certificate
ceph dashboard set-ssl-certificate -i /etc/ceph/dashboard.crt
ceph dashboard set-ssl-certificate-key -i /etc/ceph/dashboard.key
ceph config set mgr mgr/dashboard/ssl true

# Create self-signed cert for internal use (testing only)
ceph dashboard create-self-signed-cert

# Verify HTTPS is active
ceph mgr services | grep dashboard   # URL should show https://

# Create read-only monitoring user (never use admin account for monitoring)
ceph dashboard ac-user-create monitoring --roles=read-only

# List available roles
# administrator, read-only, block-manager, rgw-manager, cluster-manager, pool-manager, cephfs-manager

# Disable dashboard entirely if not needed
ceph mgr module disable dashboard
```


```text title="Expected output"
{"password": "NewSecurePassword123!", "username": "admin"}
SSL certificate updated.
SSL certificate key updated.
(no output — command completes silently)
Self-signed certificate created.
dashboard: https://mgr-node-01.ceph.local:8443
User [monitoring] created.
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error EINVAL: invalid password`** — Ensure the password meets complexity requirements (minimum 8 characters, uppercase, lowercase, number, and special character).
    **`Error ENOENT: /etc/ceph/dashboard.crt: No such file or directory`** — Verify the certificate file path is correct and readable by the ceph-mgr process.
    **`Error: User [monitoring] already exists`** — Delete the existing user with `ceph dashboard ac-user-delete monitoring` before recreating it.
## Disable Unnecessary MGR Modules

```bash
# List enabled modules
ceph mgr module ls | grep enabled

# Disable modules not in use
ceph mgr module disable telemetry      # anonymous usage data sent to Ceph project
ceph mgr module disable insights       # workload analytics
ceph mgr module disable rbd_support    # RBD monitoring hooks (if not using)

# Review pg_autoscaler (disable for manual PG control in production)
ceph mgr module disable pg_autoscaler

# List currently exposed services
ceph mgr services
```


```text title="Expected output"
enabled_modules:
- balancer
- crash
- diskprediction_local
- insights
- pg_autoscaler
- rbd_support
- telemetry
- volumes

(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)

{
  "ceph mgr": "http://ceph-mgr-01.prod.local:7000/",
  "prometheus": "http://ceph-mgr-01.prod.local:9283/",
  "dashboard": "https://ceph-mgr-01.prod.local:8443/"
}
```

!!! warning "Common errors"
    **`Error ENOENT: mgr module 'telemetry' is not enabled`** — Verify the module name with `ceph mgr module ls` and check if it's already disabled.
    **`Error EINVAL: cannot disable module 'pg_autoscaler': it is required`** — This error occurs on older Ceph versions; skip disabling this module or upgrade to Ceph Quincy or later.
## Audit Logging

```bash
# Enable auth debug logging for incident investigation
# WARNING: verbose — disable after investigation; not for permanent production use
ceph config set global auth_debug true

# Log slow ops (threshold in seconds — log ops slower than this)
ceph config set osd osd_op_log_threshold 5

# Enable cluster-level audit log (records all config changes and auth events)
ceph config set global log_to_file true
ceph config set global log_file /var/log/ceph/ceph.log

# Verify audit log is capturing events
tail -f /var/log/ceph/ceph.log | grep -E "auth|audit"

# Reset debug logging after investigation
ceph config rm global auth_debug
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
2024-01-15T14:32:18.456+0000 7f8a2c1d9e4a -1 auth: client.admin@10.0.1.42 authenticated successfully
2024-01-15T14:32:19.123+0000 7f8a2c1d9e4b -1 audit: config change global/auth_debug=true by client.admin
2024-01-15T14:32:22.789+0000 7f8a2c1d9e4c -1 auth: client.osd.0@10.0.2.15 heartbeat auth check passed
2024-01-15T14:32:45.234+0000 7f8a2c1d9e4d -1 audit: osd_op_log_threshold set to 5 seconds
2024-01-15T14:33:01.567+0000 7f8a2c1d9e4e -1 auth: client.mon.node-02 auth renewal initiated
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: ENOENT: No such file or directory '/var/log/ceph/ceph.log'`** — Create the log directory with `mkdir -p /var/log/ceph && chown ceph:ceph /var/log/ceph` before enabling logging.
    **`Error: permission denied: unable to set config key 'global/auth_debug'`** — Run the command with appropriate Ceph admin privileges or use `sudo ceph` if the user lacks cluster permissions.
    **`tail: cannot open '/var/log/ceph/ceph.log' for reading: Permission denied`** — Change log file permissions with `sudo chmod 644 /var/log/ceph/ceph.log` or run tail with sudo.
## Least Privilege: Key Hygiene

```bash
# Never use client.admin in application configuration
# Create a pool-scoped service account per application
ceph auth get-or-create client.myapp \
  mon 'allow r' \
  osd 'allow rw pool=myapp-pool'

# Check which hosts have the admin keyring (should be admin workstations only)
for host in $(ceph orch host ls -f json | python3 -c \
  "import sys,json; [print(h['hostname']) for h in json.load(sys.stdin)]"); do
  echo -n "$host: "
  ssh "$host" "ls /etc/ceph/ceph.client.admin.keyring 2>/dev/null && echo PRESENT || echo absent"
done

# Rotate keyrings quarterly: create new entity, distribute, verify, delete old
ceph auth del client.myapp        # delete old
ceph auth get-or-create client.myapp mon 'allow r' osd 'allow rw pool=myapp-pool'
```


```text title="Expected output"
[client.myapp]
	key = AQC7vZdnK3p4ExAAr8vL9Z2m8K9vQ1p2K3K4Kw==
	caps mon = "allow r"
	caps osd = "allow rw pool=myapp-pool"

ceph-admin-01: PRESENT
ceph-admin-02: PRESENT
ceph-mon-01: absent
ceph-mon-02: absent
ceph-osd-01: absent
ceph-osd-02: absent
ceph-osd-03: absent

updated caps for client.myapp
[client.myapp]
	key = AQC7vZdnK3p4ExAAr8vL9Z2m8K9vQ1p2K3K4Kw==
	caps mon = "allow r"
	caps osd = "allow rw pool=myapp-pool"
```

!!! warning "Common errors"
    **`Error EACCES: permission denied`** — Ensure the user running `ceph auth` commands has sudo access or is part of the ceph group on the admin host.
    **`ssh: Could not resolve hostname <hostname>: Name or service not known`** — Verify all hostnames from `ceph orch host ls` are resolvable via DNS or add entries to `/etc/hosts` on the admin workstation.
    **`entity client.myapp does not exist`** — Run `ceph auth get-or-create` before attempting `ceph auth del`, or use `ceph auth rm` if the entity was already removed.
## CIS Hardening Controls

| Control | Implementation | Command |
|---|---|---|
| Network separation | Dedicated cluster network, firewall OSD ports | `ceph config set global cluster_network 10.0.1.0/24` |
| In-transit encryption | msgr2 secure mode, disable msgr1 | `ceph config set global ms_cluster_mode secure` |
| Authentication | CephX enabled (default); pool-scoped keys | `ceph auth get-or-create client.app ...` |
| At-rest encryption | OSD dm-crypt enabled at creation | `ceph orch apply osd ... --data-encrypt` |
| Dashboard access | HTTPS only, non-admin roles for monitoring | `ceph config set mgr mgr/dashboard/ssl true` |
| Audit logging | Ceph audit log + OS audit (auditd) | `ceph config set global log_to_file true` |
| SSH hardening | Disable password auth; cephadm SSH key only | `/etc/ssh/sshd_config: PasswordAuthentication no` |
| NTP enforced | Clock skew > 50 ms causes MON warnings | `systemctl enable --now chronyd` |
| Prometheus auth | mTLS or basic auth on scrape endpoint | `ceph dashboard set-prometheus-credentials` |
| Unused modules | Disable telemetry, insights, rbd_support | `ceph mgr module disable telemetry` |

## Prometheus Exporter Hardening

The MGR Prometheus exporter (port 9283) exposes detailed cluster metrics. Restrict access and enable authentication to prevent information disclosure.

```bash
# Restrict Prometheus scrape to specific IP (use firewall zone or Prometheus credentials)
firewall-cmd --permanent --zone=internal --add-source=<prometheus-host-ip>
firewall-cmd --permanent --zone=internal --add-port=9283/tcp
firewall-cmd --reload

# Enable basic auth for Prometheus endpoint
ceph dashboard set-prometheus-credentials <username> <password>

# Verify exporter is only listening on expected interface
ss -tlnp | grep 9283
```


```text title="Expected output"
success
success
success
(no output — command completes silently)
LISTEN    0      128        127.0.0.1:9283       0.0.0.0:*       users:(("ceph-mgr",pid=4521,fd=45))
```

!!! warning "Common errors"
    **`Error: INVALID_ZONE: internal`** — Verify the zone exists with `firewall-cmd --get-zones` and use an available zone like `public` or `trusted`.
    **`Error: INVALID_ADDR: <prometheus-host-ip>`** — Replace the placeholder with an actual IP address in CIDR notation (e.g., `192.168.1.50/32`) or remove angle brackets.
## Admin Socket Permissions

Each Ceph daemon creates a Unix domain socket for runtime queries. Restrict these to prevent local privilege escalation.

```bash
# Admin sockets are located at /var/run/ceph/
ls -la /var/run/ceph/

# Verify sockets are owned by ceph user only (no world-readable sockets)
find /var/run/ceph -name "*.asok" -exec ls -la {} \;
# Expected: srwxr-x--- (owner: ceph, group: ceph or cephadm)

# Set socket permissions explicitly if incorrect
ceph config set global admin_socket_mode 0660
```


```text title="Expected output"
total 48
drwxr-x--- 3 ceph ceph 4096 Nov 14 10:23 .
drwxr-xr-x 13 root root 4096 Nov 14 09:15 ..
srwxr-x--- 1 ceph ceph    0 Nov 14 10:23 ceph.client.admin.asok
srwxr-x--- 1 ceph ceph    0 Nov 14 10:23 ceph.mon.ceph-mon01.asok
srwxr-x--- 1 ceph ceph    0 Nov 14 10:23 ceph.osd.0.asok
srwxr-x--- 1 ceph ceph    0 Nov 14 10:23 ceph.osd.1.asok
srwxr-x--- 1 ceph ceph    0 Nov 14 10:23 ceph.mgr.ceph-mgr01.asok
srwxr-x--- 1 ceph ceph    0 Nov 14 10:23 ceph.mds.ceph-mds01.asok
(no output — command completes silently)
```

!!! warning "Common errors"
    **`find: '/var/run/ceph': Permission denied`** — Run the command with `sudo` to access the ceph runtime directory.
    **`Error EINVAL: invalid admin_socket_mode value`** — Use octal notation without leading zero (e.g., `ceph config set global admin_socket_mode 432` for 0660 in decimal) or verify the parameter name with `ceph config help admin_socket_mode`.
## Hardening Verification Commands

Run these after applying hardening controls to confirm the state matches intent.

```bash
# Verify msgr2 secure mode
ceph config get mon ms_cluster_mode    # expect: secure
ceph config get osd ms_service_mode    # expect: secure
ceph config get global ms_bind_msgr1   # expect: false

# Verify network config
ceph config get osd public_network
ceph config get osd cluster_network

# Verify dashboard TLS
ceph mgr services | grep dashboard     # URL must be https://

# Verify OSD encryption in spec
ceph orch ls --service-type osd -f yaml | grep -i encrypt

# Verify no over-privileged entities
ceph auth ls | grep "allow \*"         # should show only client.admin and bootstrap keys

# Verify NTP on all nodes
for host in $(ceph orch host ls -f json | python3 -c \
  "import sys,json; [print(h['hostname']) for h in json.load(sys.stdin)]"); do
  echo -n "$host: "; ssh "$host" chronyc tracking | grep "System time"
done
```


```text title="Expected output"
secure
secure
false
10.0.1.0/24
10.0.2.0/24
dashboard https://ceph-mgr-01.example.com:8443
    encryption: true
    encryption_type: block
client.admin
	key: AQDvB8Zl7x9kLhAAixN3pK8q9mN2oP5rQ6sT7u==
	caps: [mds] allow *
	caps: [mon] allow *
	caps: [osd] allow *
client.bootstrap-osd
	key: AQEvB8Zl8y0lMiBbjxO4qL9r0nO3pQ6rR7tU8v==
	caps: [mon] allow profile bootstrap-osd
ceph-mon-01: System time offset: 0.000123456 seconds
ceph-osd-01: System time offset: -0.000087654 seconds
ceph-osd-02: System time offset: 0.000045678 seconds
```

!!! warning "Common errors"
    **`error: entity name 'client.admin' does not have caps`** — Ensure the admin keyring exists by running `ceph auth get client.admin` or reinitialize with `ceph-authtool`.
    **`ssh: Could not resolve hostname ceph-osd-01: Name or service not known`** — Verify hostname resolution by checking `/etc/hosts` or DNS, or use IP addresses directly in the `ceph orch host ls` output.
    **`ModuleNotFoundError: No module named 'json'`** — Install Python3 json module or simplify the hostname extraction using `ceph orch host ls | awk '{print $1}'` instead.
## See also

- [Ceph — Access Control](../access-control/)
- [Ceph — Authentication](../authentication/)
- [Ceph — Health Checks](../../operations/health-checks/)
