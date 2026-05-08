# Cisco MDS — Security

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Local accounts, directory integration, MFA, and certificate-based auth.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC, roles, permissions, and service accounts.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data-at-rest, data-in-transit, and key management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines, hardening guides, and compliance controls.</span>
</a>

</div>

> Part of the [Cisco MDS](../) reference.

---
## Hardening Checklist

- [ ] Telnet, HTTP, and TFTP disabled; SSH and HTTPS only
- [ ] AAA configured (TACACS+ primary, RADIUS fallback) pointing to Active Directory
- [ ] Local `admin` account password stored in vault; used for break-glass only
- [ ] RBAC roles assigned: `network-admin` for ops, `network-operator` for monitoring
- [ ] VSAN isolation in place — production and replication VSANs separated
- [ ] Management interface IP ACL restricts access to management subnet only
- [ ] NTP configured and synced (required for certificate-based auth and log correlation)
- [ ] SNMP v3 configured; v1/v2c community strings disabled or restricted
- [ ] All config changes logged via `aaa accounting` to TACACS+ or syslog

---

## Disable Unused Services

```
# Disable Telnet
no feature telnet

# Disable HTTP (HTTPS only)
no feature http-server
feature https-server

# Disable TFTP server if not required
no feature tftp-server

# Verify only SSH and HTTPS are active
show feature | include telnet\|http\|tftp\|ssh
```

---

## AAA Configuration (TACACS+)

```
# Add TACACS+ server
tacacs-server host <tacacs-server-ip> key <shared-secret>

# Configure AAA to use TACACS+ for authentication, authorisation, and accounting
aaa authentication login default group tacacs+ local
aaa authorization commands default group tacacs+ local
aaa accounting default group tacacs+

# Keep local fallback in case TACACS+ is unreachable
username admin password <strong-password> role network-admin
```

**Verify AAA is working:**

```
test aaa group tacacs+ <test-username> <test-password>
```

---

## Role-Based Access Control

```
# Built-in NX-OS roles
# network-admin  — full config access
# network-operator — read-only (show commands only)
# san-admin — SAN-specific (zoning, VSANs, FC services)

# Assign a TACACS+-authenticated user to a role
# (Role assignment comes from TACACS+ AV-pairs or local role mapping)

# Verify current user roles
show role
show user-account
```

---

## VSAN Isolation

VSAN isolation provides logical fabric separation. Hosts in different VSANs cannot communicate across VSAN boundaries without explicit VSAN routing policy.

```
# Verify VSAN membership per port
show vsan membership

# Verify VSAN database
show vsan

# Ensure no production host ports are in the default VSAN 1
show vsan 1 membership
# Any F_Ports listed in VSAN 1 are a configuration error
```

---

## Management Interface IP ACL

```
# Create an IP access list restricting management access
ip access-list MGMT-RESTRICT
  permit ip <mgmt-subnet>/<prefix> any
  deny ip any any log

# Apply to the management (mgmt0) interface
interface mgmt0
  ip access-group MGMT-RESTRICT in
```

---

## SNMP Hardening

```
# Disable default SNMPv1/v2c community strings
no snmp-server community public
no snmp-server community private

# Configure SNMPv3 with auth + priv
snmp-server user nms_user network-operator auth sha <auth-password> priv aes-128 <priv-password>
snmp-server host <nms-ip> traps version 3 priv nms_user

# Restrict SNMP to monitoring subnet
snmp-server host <nms-ip> traps version 3 priv nms_user
ip access-list SNMP-RESTRICT
  permit udp <nms-subnet>/<prefix> any eq 162
  deny udp any any eq 162 log
```

---

## Audit Logging

```
# Enable accounting for all exec and config commands
aaa accounting default group tacacs+

# Configure local syslog with accounting detail
logging level aaa 6
logging server <siem-ip> 5 facility local7

# Verify accounting is capturing config changes
show accounting log
```
