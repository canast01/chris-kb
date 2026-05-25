# MDS — Hardening

> Part of the [Cisco MDS](../../index.md) reference.

---

## Overview

Hardening an MDS switch means eliminating unused attack surface, enforcing encrypted management protocols, configuring centralized authentication, restricting management access by source IP, and ensuring all configuration changes are logged with user identity. This page defines the baseline configuration standard for all production MDS switches.

Apply this configuration as part of initial switch commissioning and validate it during periodic security reviews (quarterly recommended).

---

## 1. Disable Unused Services

The default NX-OS installation enables several services that should be disabled in production:

```bash
# Disable Telnet — transmits credentials in cleartext
no feature telnet

# Disable HTTP — use HTTPS only
no feature http-server

# Enable HTTPS for web management and NDFC API
feature https-server

# Disable TFTP server — use SCP for file transfers
no feature tftp-server

# Disable CDP if not needed (optional — CDP is low-risk; disable only if policy requires)
no cdp enable

# Verify only required services are enabled
show feature | include telnet|http|tftp|ftp|snmp|ssh
# Expected: telnet disabled, http-server disabled, tftp-server disabled
#           https-server enabled, ssh enabled, snmp enabled
```

---

## 2. SSH Hardening

```bash
# Confirm SSH v2 only
ssh version 2

# Generate RSA key (minimum 2048-bit)
crypto key generate rsa
# Enter key modulus: 2048

# Verify key
show crypto key mypubkey rsa

# Set SSH session idle timeout (10 minutes)
line vty 0 4
  exec-timeout 10 0

# Restrict VTY lines to SSH only (no Telnet)
line vty 0 4
  transport input ssh

# Verify
show ssh server
```

---

## 3. Management Interface ACL

Restrict SSH and HTTPS access to the management interface to authorised source IP ranges. This prevents brute-force attempts from untrusted networks.

```bash
# Define the authorised management source ranges
ip access-list MGMT-RESTRICT
  10 permit tcp 10.10.0.0/24 any eq 22     # SSH from jump hosts / management subnet
  20 permit tcp 10.10.0.0/24 any eq 443    # HTTPS from management subnet
  30 permit udp 10.10.2.0/24 any eq 161    # SNMP polling from NMS
  40 permit udp any 10.10.3.50/32 eq 514   # Syslog (outbound; for reference)
  50 deny ip any any log

# Apply to management interface (inbound)
interface mgmt0
  ip access-group MGMT-RESTRICT in

# Verify
show ip access-lists MGMT-RESTRICT
show running-config interface mgmt0
```

---

## 4. AAA and Authentication

```bash
# TACACS+ server definitions (encrypted key)
tacacs-server host 10.10.1.10 key 0 <key>
tacacs-server host 10.10.1.11 key 0 <key>

# AAA server group
aaa group server tacacs+ TACACS-SERVERS
  server 10.10.1.10
  server 10.10.1.11

# Authentication: TACACS+ primary, local break-glass fallback
aaa authentication login default group TACACS-SERVERS local

# Authorization: enforce command authorization via TACACS+
aaa authorization commands default group TACACS-SERVERS local

# Accounting: log all exec and configuration commands
aaa accounting default group TACACS-SERVERS

# Break-glass local admin (one per fabric; password in vault)
username admin password 0 <strong-password> role network-admin

# Verify AAA
show aaa
test aaa group TACACS-SERVERS <test-user> <test-password>
```

---

## 5. Role-Based Access Control

```bash
# Confirm built-in roles are appropriate
show role

# Assign read-only role to monitoring accounts
# (Role assignment via TACACS+ AV-pair is preferred — no local role assignment needed)
# username monitoring role network-operator

# Verify no accounts have unnecessary admin rights
show user-account
```

---

## 6. SNMPv3 — Disable v1/v2c

```bash
# Remove default insecure community strings
no snmp-server community public
no snmp-server community private

# Create SNMPv3 authPriv user for NMS polling
snmp-server user nms_poll network-operator v3 auth sha <auth-pass> priv aes-128 <priv-pass>

# Create SNMPv3 authPriv user for trap receiver
snmp-server host 10.10.2.50 traps version 3 priv nms_poll

# Enable relevant trap categories
snmp-server enable traps link
snmp-server enable traps entity
snmp-server enable traps vsan
snmp-server enable traps zone

# Verify
show snmp user
show snmp host
show snmp community
# Expected: no v1/v2c community strings in output
```

---

## 7. NTP Synchronization

NTP is required for log correlation, certificate validity, and TACACS+ accounting timestamp accuracy.

```bash
# Configure NTP servers
ntp server 10.10.0.10 prefer
ntp server 10.10.0.11

# Verify sync
show ntp status
# Expected: "Clock is synchronized" with stratum <= 5

show ntp peer-status
```

---

## 8. Syslog Forwarding

All log events must be forwarded to a SIEM or log aggregator for correlation and alerting.

```bash
# Forward notifications and above to SIEM
logging server 10.10.3.50 5 facility local7
logging server 10.10.3.51 5 facility local7   # secondary/redundant

# Set local buffer size and level
logging logfile messages 6 size 4194304

# Verify
show logging server
show logging
```

---

## 9. VSAN Security

```bash
# Confirm no production ports in VSAN 1 (insecure default)
show vsan 1 membership
# Should show no F_Ports (host or storage ports)

# Enable enhanced zoning on all production VSANs
zone mode enhanced vsan 10
zone mode enhanced vsan 20

# Verify
show zone status vsan 10
# Mode: Enhanced   (default-deny)

# Restrict ISL trunks to only required VSANs — remove VSAN 1
interface fc2/1
  switchport trunk allowed vsan 10,20,99
  no switchport trunk allowed vsan 1
```

---

## 10. Login Banner

```bash
banner motd #
WARNING: This system is for authorized use only.
All connections are monitored and recorded.
Unauthorized access or use is prohibited and may result in legal action.
#
```

---

## 11. CFS (Cisco Fabric Services) Security

CFS distributes device alias and zone changes across the fabric. Restrict CFS to prevent unauthorized switches from joining CFS distribution.

```bash
# Restrict CFS to specific IP addresses (MDS management IPs)
cfs ipv4 distribute
cfs ipv4 mcast-address 239.255.70.83   # default multicast; adjust if needed

# If using IP distribution, restrict CFS peers
cfs eth distribute   # or cfs ipv4 distribute — depending on transport

# Verify CFS status
show cfs status
show cfs peers
```

---

## Hardening Checklist

### Network Services

- [ ] Telnet disabled: `show feature | include telnet` = disabled
- [ ] HTTP disabled; HTTPS enabled: `show feature | include http-server` = disabled
- [ ] TFTP server disabled: `show feature | include tftp-server` = disabled
- [ ] SSH v2 only: `show ssh server | include version` = v2
- [ ] SSH RSA key generated (2048-bit minimum): `show crypto key mypubkey rsa`
- [ ] VTY lines accept SSH only: `show running-config | include transport input`

### Authentication and Authorization

- [ ] TACACS+ configured with at least two servers and encrypted key
- [ ] AAA authentication, authorization, and accounting all enabled and pointing to TACACS-SERVERS
- [ ] Local break-glass admin exists; password in vault; used break-glass only
- [ ] No other local accounts with admin roles
- [ ] TACACS+ test passes: `test aaa group TACACS-SERVERS <user> <pass>`
- [ ] NTP synchronized: `show ntp status` = synchronized

### Access Restriction

- [ ] Management interface (mgmt0) has inbound ACL restricting to management subnet
- [ ] SNMP access restricted by ACL or SNMPv3 user scoping
- [ ] Login banner configured

### Encryption

- [ ] SNMPv1/v2c community strings removed
- [ ] SNMPv3 authPriv configured (SHA + AES-128 minimum)
- [ ] HTTPS certificate is current

### Data Plane

- [ ] No production ports in VSAN 1: `show vsan 1 membership`
- [ ] Enhanced zoning on all production VSANs: `show zone status vsan <id>`
- [ ] Single-initiator zoning enforced: `show zone vsan <id>` — no multi-initiator zones
- [ ] ISL trunks do not carry VSAN 1 on production links

### Logging

- [ ] Syslog forwarding to SIEM configured: `show logging server`
- [ ] AAA accounting to TACACS+ enabled: `show accounting log`
- [ ] Local logging buffer adequate: `show logging info`

---

## Periodic Review Schedule

| Review | Frequency | Owner |
|---|---|---|
| Full hardening checklist audit | Quarterly | SAN infrastructure team |
| Local account password rotation | Quarterly | SAN infrastructure team + vault admin |
| NX-OS version vs. Cisco recommended | Quarterly | SAN infrastructure team |
| SmartNet / maintenance contract expiry | Semi-annually | Asset management |
| SNMP community string review | Quarterly (if v2c in use) | SAN infrastructure team |
| Syslog receiver health check | Monthly | SIEM / security team |
