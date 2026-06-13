---
tags:
  - networking
---
# SNMP Communities


<div class="kb-summary">
An SNMP community string is a plaintext password used in SNMPv1 and SNMPv2c to authenticate read or write access to a device's management information base (MIB).
</div>

        COMMUNITY STRING FLOW (SNMPv1/v2c)
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  NMS (monitoring server)        Device (switch/router)                                                │
│  ┌─────────────────────┐        ┌────────────────────────┐                                            │
│  │ GET request         │        │ community ACL check    │                                            │
│  │ community: "mon-ro" ├──────►│ "mon-ro" matches RO    │                                             │
│  │ OID: sysDescr.0     │        │ NMS IP in access-list  │                                            │
│  └─────────────────────┘        └──────────┬─────────────┘                                            │
│                                            │ OK                                                       │
│  ┌─────────────────────┐        ┌──────────▼─────────────┐                                            │
│  │ OID value returned  │◄───────│ MIB lookup             │                                            │
│  │ "Cisco IOS 17.3"    │        │ returns OID value      │                                            │
│  └─────────────────────┘        └────────────────────────┘                                            │
│                                                                                                       │
│  RO community: GET/GETNEXT/GETBULK only                                                               │
│  RW community: all ops + SET (device config change) — risk!                                           │
│  All traffic is PLAINTEXT — use SNMPv3 for production                                                 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Community strings provide no encryption.

!!! warning "SNMPv2c security"
    Community strings are transmitted in plaintext and are visible in packet captures. Treat them as secrets and use SNMPv3 for any environment with compliance requirements or sensitive data. SNMPv2c is acceptable only on isolated management VLANs with strict ACLs.

## Community Types

| Community | Access | Typical name | Risk |
|---|---|---|---|
| **Read-only (RO)** | GET, GETNEXT, GETBULK | `public`, `ro-community` | Data exposure |
| **Read-write (RW)** | All RO + SET | `private`, `rw-community` | Device misconfiguration |

Never use default community strings (`public` / `private`) in production.

## Configuring Communities — Linux (snmpd)

```bash
# /etc/snmp/snmpd.conf
rocommunity  monitoring-ro  10.0.0.0/8    # read-only, restricted to management network
rocommunity6 monitoring-ro  ::1/128

# Remove default "public" if present
# Comment out: rocommunity public default

systemctl restart snmpd

# Test locally
snmpwalk -v2c -c monitoring-ro localhost system
```

## Cisco IOS

```bash
# Read-only community with ACL restriction
ip access-list standard SNMP-MGMT
 permit 10.10.0.0 0.0.255.255

snmp-server community <community-string> RO SNMP-MGMT
snmp-server community <rw-string> RW SNMP-MGMT

# Remove defaults
no snmp-server community public
no snmp-server community private

# Verify
show snmp community
```

## Arista EOS

```text
snmp-server community <community-string> ro
snmp-server community <community-string> view system-view ro
show snmp community
```

## Brocade FOS

```bash
snmpconfig --set snmpv1
# Follow prompts to set community strings and access list
snmpconfig --show snmpv1
```

## Testing Community Access

```bash
# Test from NMS / monitoring server
snmpget  -v2c -c <community> <device-ip> sysDescr.0
snmpwalk -v2c -c <community> <device-ip> system

# If no response — check:
# 1. Community string correct
# 2. NMS IP in ACL on device
# 3. UDP 161 not blocked by firewall
```

## Community String Standards

- Minimum 16 characters, mixed alphanumeric
- Different strings for RO and RW
- Store in CyberArk or secrets manager — never in plaintext config files
- Rotate annually or when staff leave
- Scope with ACLs to management network ONLY

## Common Issues

| Symptom | Cause | Check |
|---|---|---|
| `Timeout: No Response` | Wrong community or UDP 161 blocked | Test with `snmpget`; check firewall |
| No response from new device | Community not configured | Verify `show snmp community` on device |
| NMS sees wrong data | RW community accidentally used for RO polling | Use separate strings for read and write |
| Community string visible in Wireshark | SNMPv2c by design | Migrate to SNMPv3 for sensitive environments |
