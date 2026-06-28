---
tags:
  - san
  - security
---
# Cisco MDS — Security Hardening
![Cisco MDS — Security Hardening](../../../../assets/san-cisco-mds-security-hardening.svg)


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
```bash
# Confirm built-in roles are appropriate
show role

# Assign read-only role to monitoring accounts
# (Role assignment via TACACS+ AV-pair is preferred — no local role assignment needed)
# username monitoring role network-operator

# Verify no accounts have unnecessary admin rights
show user-account
```
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
```bash
# Configure NTP servers
ntp server 10.10.0.10 prefer
ntp server 10.10.0.11

# Verify sync
show ntp status
# Expected: "Clock is synchronized" with stratum <= 5

show ntp peer-status
```
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
```bash
banner motd #
WARNING: This system is for authorized use only.
All connections are monitored and recorded.
Unauthorized access or use is prohibited and may result in legal action.
#
```
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

```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "Cisco MDS Core" {shape: hexagon}

external -> perimeter_controls: traffic in
perimeter_controls -> identity_access
identity_access -> audit_logging
audit_logging -> core: secured path
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Mds — Authentication](authentication/)
- [Mds — Access Control](access-control/)
- [Mds — Encryption](encryption/)
