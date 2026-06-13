---
tags:
  - dell
  - security
---
# PowerStore — Hardening


<div class="kb-summary">
Hardening reference covering Overview, Management Plane Hardening, Host Connectivity Hardening, SupportAssist Hardening, Audit Logging and 2 more sections.

*Applies to: PowerStore 3.x*
</div>
```text
┌──────────────────────────────── Dell PowerStore — Security Hardening ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      PowerStore hardening: disable unused protocols, enforce encryption, restrict access      │   │
│   │         Network: dedicated storage VLAN; restrict management access to jump hosts only        │   │
│   │        Auth: disable default accounts; enforce password complexity and rotation policy        │   │
│   │         Audit: forward syslog to SIEM; alert on privilege escalation and failed logins        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Baseline config → disable unused → enforce MFA → enable logging → audit                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           T-model           │  │          Block only         │  │        iSCSI/FC/NVMe        │   │
│   │           X-model           │  │         Block + File        │  │       Unified protocol      │   │
│   │            Metro            │  │       Sync replication      │  │       Zero-RPO stretch      │   │
│   │          Protection         │  │        Snapshot/Clone       │  │       Immutable snaps       │   │
│   │             Mgmt            │  │          PSM / REST         │  │         Unified pane        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Area       │     Control      │      Standard     │      Verify      │    Frequency     │   │
│   │     Accounts     │ Disable defaults │  No default creds │   Login audit    │      Deploy      │   │
│   │    Protocols     │  Disable unused  │   TLS 1.2+ only   │    Port scan     │     Monthly      │   │
│   │       MFA        │ Enforce all admi │   TOTP/hardware   │    Auth logs     │    Continuous    │   │
│   │     Logging      │ SIEM forwarding  │  All admin events │   SIEM alerts    │      Daily       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerStore T/X appliance · NVMe drives · SAS expansion shelves · 10/25 GbE               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerStore         = Dell mid-range NVMe storage; T-model block-only, X-model unified block+file   │
│    PowerStore Manager = browser GUI and REST API endpoint for all PowerStore operations               │
│    Volume group       = logical collection of volumes sharing snapshot and replication policies       │
│    Protection policy  = assigned to volumes; defines snapshot schedule, retention, and replication    │
│    Metro volume       = synchronously replicated volume across two sites; zero RPO active-active      │
│    Snapshot           = space-efficient point-in-time copy; crash-consistent or app-consistent        │
│    Clone              = full writable copy of a volume or file system; independent lifecycle          │
│    Applied-to         = PowerStore host mapping; volumes are applied-to a host or host group object   │
│    Capacity license   = PowerStore uses usable-capacity licensing; licensed in TiB increments         │
│    Storage container  = PowerStore X-model; unified block and file from the same storage pool         │
│    Appliance          = single PowerStore node pair (dual controllers); scalable to 4 appliances      │
│    NVMe-oF            = NVMe over Fabrics; FC-NVMe or NVMe/TCP host connectivity on PowerStore        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Overview

PowerStore hardening covers four areas: securing the management plane (PowerStore Manager and REST API), securing host connectivity (FC, iSCSI, NFS, SMB), key management configuration, and reducing the operational attack surface through configuration discipline. PowerStoreOS is a closed purpose-built OS — hardening targets the management and connectivity interfaces, not the underlying OS which is not user-accessible.

## Management Plane Hardening

### Authentication Hardening

```bash
# Step 1: Change the default admin password immediately after initial configuration
curl -k -X PATCH "https://<mgmt-ip>/api/rest/user/local/admin" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"current_password": "Password123!", "password": "<strong-new-password>"}'

# Step 2: Configure LDAP/AD authentication before disabling local accounts
# See Authentication page for LDAP configuration commands

# Step 3: Test LDAP authentication with at least two AD admin accounts
# before proceeding

# Step 4: Verify the admin account is the only local account active
curl -k -X GET "https://<mgmt-ip>/api/rest/user/local?select=name,role_name" \
  -H "DELL-EMC-TOKEN: <token>"

# Step 5: Store the local admin password in a PAM vault (CyberArk, Thycotic, etc.)
# The local admin account is now the break-glass account — treat it accordingly
```

### TLS Hardening

```bash
# Verify TLS 1.0 and 1.1 are disabled
openssl s_client -connect <mgmt-ip>:443 -tls1   2>&1 | grep -iE "failure|error|alert"
openssl s_client -connect <mgmt-ip>:443 -tls1_1 2>&1 | grep -iE "failure|error|alert"

# Verify TLS 1.2 and 1.3 are operational
openssl s_client -connect <mgmt-ip>:443 -tls1_2 2>&1 | grep "Protocol"
openssl s_client -connect <mgmt-ip>:443 -tls1_3 2>&1 | grep "Protocol"

# Enumerate active cipher suites
nmap --script ssl-enum-ciphers -p 443 <mgmt-ip>
```

PowerStore Manager → **Settings → Security → TLS Configuration**:

| Setting | Required Value |
|---|---|
| Minimum TLS version | TLS 1.2 |
| Disabled protocols | TLS 1.0, TLS 1.1, SSL 3.0 |
| Preferred ciphers | ECDHE-RSA-AES256-GCM-SHA384, ECDHE-RSA-AES128-GCM-SHA256 |
| Disabled ciphers | RC4, 3DES, NULL, EXPORT |

### Certificate Hardening

Replace the factory self-signed certificate before production:

```bash
# Generate CSR (or use your internal PKI to generate the key pair)
openssl req -new -newkey rsa:4096 -nodes \
  -keyout powerstore.key \
  -out powerstore.csr \
  -subj "/C=GB/O=Example Corp/CN=lon01-pstore-001.corp.example.com" \
  -addext "subjectAltName=DNS:lon01-pstore-001.corp.example.com,IP:192.168.10.50"

# Submit CSR to internal CA; receive signed certificate and CA chain

# Import via REST API
curl -k -X POST "https://<mgmt-ip>/api/rest/x509_certificate" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "Manager",
    "certificate": "<base64-PEM-cert+chain>",
    "private_key": "<base64-PEM-key>",
    "passphrase": ""
  }'

# Verify new certificate
echo | openssl s_client -connect <mgmt-ip>:443 2>/dev/null \
  | openssl x509 -noout -issuer -subject -dates
```

Set a calendar reminder to renew the certificate 30 days before expiry. A monitoring script checking certificate expiry should be part of the daily health check.

### Network Access Hardening

Restrict access to the PowerStore management port at the network layer:

```bash
# Firewall rule: limit HTTPS management access to the storage management subnet only
# Example: Linux firewalld on the jump host gateway
firewall-cmd --zone=management --add-rich-rule=\
  'rule family="ipv4" source address="192.168.50.0/24" port protocol="tcp" port="443" accept' --permanent
firewall-cmd --zone=public --add-rich-rule=\
  'rule family="ipv4" port protocol="tcp" port="443" drop' --permanent
firewall-cmd --reload

# Verify that access from outside the management subnet is blocked
nc -zv <untrusted-host> 443   # Should timeout or connection refused
nc -zv <mgmt-workstation> 443 # Should succeed
```

The PowerStore management IP should only be reachable from:

- Storage administrator workstations or jump hosts
- Monitoring systems (with read-only credentials)
- Backup software servers (Veeam, PPDM — with StorageOperator credentials)

### Session Hardening

| Setting | Recommended Value | Configure Via |
|---|---|---|
| Session idle timeout | 15 minutes | PowerStore Manager → Settings → Security → Session Management |
| Maximum session duration | 8 hours | PowerStore Manager → Settings → Security → Session Management |
| Concurrent sessions | Audit if required; no hard limit | Review via `GET /api/rest/session` |

## Host Connectivity Hardening

### Fibre Channel Zoning

Zone discipline is critical — improper zones can expose production volumes to unintended hosts.

```bash
# Principle: one zone per host-to-target-port pair (preferred) or per host initiator
# Never create mega-zones with all initiators and all target ports

# Audit: check for any zoning misconfigurations
# On Brocade switch:
# switch:admin> zoneshow   # List all zones
# switch:admin> cfgshow    # Show active zone configuration

# Verify each host zone contains:
# - The host's initiator WWN(s)
# - Only the PowerStore target port WWNs for that host's fabric
# - No other hosts' initiators

# PowerStore FC port WWNs
curl -k -X GET "https://<mgmt-ip>/api/rest/fc_port?select=name,wwn,node_id" \
  -H "DELL-EMC-TOKEN: <token>"
```

### iSCSI Security

```bash
# Enforce CHAP on all iSCSI hosts
# 1. Configure CHAP credentials in PowerStore for each iSCSI initiator
curl -k -X PATCH "https://<mgmt-ip>/api/rest/host_initiator/<initiator-id>" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "chap_mutual_username": "<host-chap-user>",
    "chap_mutual_password": "<chap-password-min-12>"
  }'

# 2. Isolate iSCSI traffic on dedicated VLANs
# - Never allow iSCSI traffic on the general data or management VLANs
# - Use separate VLANs for iSCSI-A and iSCSI-B paths
# - Enable jumbo frames (MTU 9000) end-to-end on iSCSI VLANs
```

### NFS Security

```bash
# Harden NFS exports: restrict access to specific subnets
curl -k -X PATCH "https://<mgmt-ip>/api/rest/nfs_export/<export-id>" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rw_hosts": [{"ip": "192.168.20.0", "prefix_length": 24}],
    "no_access_hosts": [],
    "min_security": "sys",
    "no_suid": true
  }'

# Audit all NFS exports for overly permissive access
curl -k -X GET "https://<mgmt-ip>/api/rest/nfs_export?select=name,rw_hosts,ro_hosts,min_security" \
  -H "DELL-EMC-TOKEN: <token>" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for e in data:
    rw = e.get('rw_hosts', [])
    for h in rw:
        ip = h.get('ip', '')
        prefix = h.get('prefix_length', 32)
        # Flag any /8 or broader subnet
        if prefix <= 8:
            print(f'WARNING: Export {e[\"name\"]} has broad RW access: {ip}/{prefix}')
"
```

## SupportAssist Hardening

SupportAssist enables Dell to proactively monitor the array and create automated service requests.

```text
PowerStore → SupportAssist (ESRS) → Dell SRS Cloud → Dell Support
```

| SupportAssist Setting | Recommended Value | Notes |
|---|---|---|
| Connect Home | Enabled | Required for proactive monitoring |
| Direct internet | Disabled | Route through authenticated corporate proxy |
| Proxy server | `proxy.corp.example.com:8080` | Proxy must allow HTTPS to `esrs3.emc.com:443` |
| Remote Support | Enabled (Dell Support only) | Allows Dell engineers to initiate remote sessions |

Configure: PowerStore Manager → **Settings → Support → SupportAssist**.

## Audit Logging

PowerStore logs all management operations (user logins, provisioning actions, configuration changes) to an internal audit log. Forward these to a SIEM:

```bash
# Configure syslog forwarding for audit events
curl -k -X POST "https://<mgmt-ip>/api/rest/remote_syslog" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "192.168.10.200",
    "port": 514,
    "transport": "UDP",
    "enabled": true
  }'

# Verify syslog is forwarding (check the SIEM for incoming events)
curl -k -X GET "https://<mgmt-ip>/api/rest/remote_syslog" \
  -H "DELL-EMC-TOKEN: <token>"
```

Audit events to monitor in the SIEM:

| Event | Alert Threshold | Priority |
|---|---|---|
| Failed login attempts | 5+ failures within 10 minutes | High |
| Successful login from unexpected IP | Any IP outside management subnet | High |
| Volume deletion | Any deletion of production volumes | Medium |
| User or role changes | Any change outside a change management window | High |
| LDAP configuration changes | Any change | High |
| Certificate changes | Any change | Medium |
| Replication session modification | Any outside a maintenance window | Medium |

## Hardening Checklist

### Critical — Complete Before Production

- [ ] Default `admin` password changed; new password stored in PAM vault
- [ ] LDAP/AD authentication configured and tested with at least two admin accounts
- [ ] Break-glass local admin account confirmed in PAM vault; password known only to the vault
- [ ] Self-signed certificate replaced with CA-signed certificate
- [ ] TLS 1.0 and 1.1 disabled; TLS 1.2 minimum enforced
- [ ] Session idle timeout set to 15 minutes
- [ ] Management network access restricted to management VLAN at firewall/switch level
- [ ] SupportAssist configured with proxy; no direct internet access
- [ ] D@RE confirmed enabled (`is_encryption_enabled: true` in appliance API response)
- [ ] Service accounts created with minimum required roles (StorageOperator, not Administrator)
- [ ] Syslog forwarding configured to SIEM; test event received

### Important — Complete Within 30 Days

- [ ] KMIP key management configured if required by security policy
- [ ] CHAP enabled on all iSCSI hosts (if using iSCSI)
- [ ] NFS exports restricted to specific subnets (no wildcard access)
- [ ] SMB shares: confirm no `Everyone` or `Authenticated Users` with write access
- [ ] FC zoning audited — no mega-zones; each host zone contains only that host's initiators
- [ ] Alert notification destinations configured (email + ITSM webhook for CRITICAL)
- [ ] CloudIQ registered and showing healthy status
- [ ] Certificate expiry monitoring configured (alert 30 days before expiry)
- [ ] Ansible/Terraform service accounts created with minimum required roles

### Periodic — Quarterly and Annually

- [ ] Quarterly: access review — all local and LDAP-mapped accounts reviewed; stale accounts removed
- [ ] Quarterly: host object review — stale initiators removed from decommissioned hosts
- [ ] Quarterly: NFS export audit — access lists still correct
- [ ] Annually: KMIP key rotation (if using external key management)
- [ ] Annually: certificate renewal (before expiry)
- [ ] Annually: DR test — replication failover and failback; validate RTO/RPO
- [ ] Annually: rotate all service account passwords; update automation scripts
- [ ] Monthly: review Dell Security Advisories for PowerStoreOS; apply patches per risk timeline

## Compliance Mapping

| Framework | Control | PowerStore Hardening Action |
|---|---|---|
| PCI-DSS v4.0 Req 2.2 | System configured to prevent known security vulnerabilities | Disable TLS 1.0/1.1; replace self-signed cert; enforce CHAP on iSCSI |
| PCI-DSS v4.0 Req 7 | Restrict access by business need to know | RBAC roles; host-level access control; NFS export restrictions |
| PCI-DSS v4.0 Req 8 | Identify users and authenticate access | LDAP/AD authentication; named accounts; no shared credentials |
| PCI-DSS v4.0 Req 10 | Log and monitor all access | Syslog to SIEM; retain 12 months |
| NIST 800-53 AC-2 | Account Management | Quarterly access review; disable unused accounts; rotate service account credentials |
| NIST 800-53 AC-3 | Access Enforcement | RBAC; host-level access; SAN zoning; NFS subnet restrictions |
| NIST 800-53 AU-2 | Event Logging | Audit log to SIEM; forward PowerStore syslog events |
| NIST 800-53 CM-7 | Least Functionality | Remove unused host objects; restrict management access by IP |
| NIST 800-53 IA-5 | Authenticator Management | Rotate passwords; enforce complexity via AD policy; CHAP on iSCSI |
| ISO 27001 A.8.2 | Privileged access rights | StorageOperator for day-to-day; Administrator for changes only; quarterly review |
| ISO 27001 A.8.5 | Secure authentication | LDAP/AD; MFA via jump host; session timeout 15 minutes |
| CIS Controls v8 CIS 4 | Secure Configuration | Hardening checklist above; periodic review |
| CIS Controls v8 CIS 5 | Account Management | Named accounts; quarterly review; disable stale accounts |

---

## See also

- [Powerstore — Authentication](authentication/)
- [Powerstore — Access Control](access-control/)
- [Powerstore — Encryption](encryption/)
