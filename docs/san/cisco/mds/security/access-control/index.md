# MDS — Access Control

> Part of the [Cisco MDS](../../) reference.

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

## Checklist

- [ ] RBAC roles assigned: `network-admin` for ops, `network-operator` for monitoring
- [ ] VSAN isolation in place — production and replication VSANs separated
- [ ] Management interface IP ACL restricts access to management subnet only
- [ ] All config changes logged via `aaa accounting` to TACACS+ or syslog
