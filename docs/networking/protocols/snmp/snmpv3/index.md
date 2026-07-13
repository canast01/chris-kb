---
title: SNMPv3
tags:
  - networking
description: "SNMPv3 adds authentication and encryption to SNMP, replacing the plaintext community strings of v1/v2c."
---

# SNMPv3

<div class="kb-summary">
SNMPv3 adds authentication and encryption to SNMP, replacing the plaintext community strings of v1/v2c.
</div>

        SNMPv3 authPriv SECURITY MODEL (USM)

It is the required version for any environment with compliance requirements.

```d2
direction: down

security_models: "Security Models" {shape: rectangle}
snmpv3_parameters_usm: "SNMPv3 Parameters (USM)" {shape: rectangle}
linux_create_snmpv3_user_snmpd: "Linux — Create SNMPv3 User (snmpd)" {shape: rectangle}
cisco_ios: "Cisco IOS" {shape: rectangle}
arista_eos: "Arista EOS" {shape: rectangle}
snmpv3_trap_inform_cisco: "SNMPv3 Trap / Inform (Cisco)" {shape: rectangle}

security_models -> snmpv3_parameters_usm: uses
snmpv3_parameters_usm -> linux_create_snmpv3_user_snmpd: uses
linux_create_snmpv3_user_snmpd -> cisco_ios: uses
cisco_ios -> arista_eos: uses
arista_eos -> snmpv3_trap_inform_cisco: uses
```

## Security Models

| Level | Authentication | Encryption | Use case |
|---|---|---|---|
| `noAuthNoPriv` | None | None | Same as SNMPv2c — avoid |
| `authNoPriv` | MD5 or SHA | None | Authentication only — still exposes data |
| `authPriv` | SHA (preferred) | AES (preferred) | Full security — use this |

Always use `authPriv` with SHA + AES in production.

## SNMPv3 Parameters (USM)

| Parameter | Description |
|---|---|
| `securityName` | Username (not community string) |
| `authProtocol` | Authentication algorithm: MD5 (deprecated) or SHA, SHA-256, SHA-512 |
| `authKey` | Authentication passphrase (min 8 chars) |
| `privProtocol` | Encryption algorithm: DES (deprecated), AES, AES-128, AES-256 |
| `privKey` | Encryption passphrase (min 8 chars) |
| `securityLevel` | `noAuthNoPriv` / `authNoPriv` / `authPriv` |

## Linux — Create SNMPv3 User (snmpd)

```bash
# Stop snmpd before editing
systemctl stop snmpd

# Create user in /var/lib/snmp/snmpd.conf (not /etc/snmp/snmpd.conf)
net-snmp-create-v3-user -ro -A <authpass> -a SHA -X <privpass> -x AES <username>

# Or manually in /var/lib/snmp/snmpd.conf:
createUser <username> SHA "<authpass>" AES "<privpass>"

# Grant access in /etc/snmp/snmpd.conf
rouser <username> authpriv

systemctl start snmpd

# Test
snmpget -v3 -u <username> -l authPriv \
  -a SHA -A <authpass> \
  -x AES -X <privpass> \
  <device-ip> sysDescr.0
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
SNMPv3 User successfully created.
(no output — command completes silently)
DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (847293) 2:21:33.93
SNMPv3-MIB::usmUserEngineID = Hex: 80:00:1f:88:03:c0:a8:01:64:00:00:00:00
SNMPv3-MIB::usmUserName = STRING: monitor-user
ENTITY-MIB::entityMIB = INTEGER: 1
SNMPv3-MIB::usmUserAuthProtocol = OID: usmHMACwithSHAAuthProtocol
```

!!! warning "Common errors"
    **`Error: cannot open /var/lib/snmp/snmpd.conf: No such file or directory`** — Create the directory with `mkdir -p /var/lib/snmp` before running net-snmp-create-v3-user.
    **`snmpget: Unknown user name "<username>"`** — Verify the username was created in /var/lib/snmp/snmpd.conf and restart snmpd with `systemctl restart snmpd`.
    **`snmpget: Authentication failure (incorrect password, community or key)`** — Ensure the authentication and privacy passwords match exactly between user creation and the snmpget command, including case sensitivity.
## Cisco IOS

```bash
# Create SNMPv3 user
snmp-server group SNMPv3GROUP v3 priv
snmp-server user <username> SNMPv3GROUP v3 auth sha <authpass> priv aes 128 <privpass>

# Restrict to management network
ip access-list standard SNMP-MGMT
 permit 10.10.0.0 0.0.255.255
snmp-server group SNMPv3GROUP v3 priv access SNMP-MGMT

# Verify
show snmp user
show snmp group
```


```text title="Expected output"
User name: admin-snmp
Engine ID: 800007E5-03-A1B2C3D4E5F6
Storage type: nonvolatile
Status: active
Authentication Protocol: SHA
Privacy Protocol: AES128

Group Name: SNMPv3GROUP
Security Model: v3
Read View: v1default
Write View: v1default
Notify View: v1default
Row Status: active
Access List: SNMP-MGMT

Standard IP access list SNMP-MGMT
    10 permit 10.10.0.0 0.0.255.255
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the device is in global configuration mode and supports SNMPv3 (use `configure terminal` first).
    **`% Incomplete command`** — Ensure all parameters including `<authpass>` and `<privpass>` are provided without angle brackets.
    **`% Access denied: SNMP-MGMT not found`** — Create the access list before applying it to the group with `ip access-list standard SNMP-MGMT` first.
## Arista EOS

```text
snmp-server group SNMPv3GROUP v3 priv
snmp-server user <username> SNMPv3GROUP v3 auth sha <authpass> priv aes <privpass>
show snmp user
show snmp group
```

## SNMPv3 Trap / Inform (Cisco)

```bash
# Send v3 traps to NMS
snmp-server host <nms-ip> version 3 priv <username>
snmp-server enable traps
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`% Invalid command.`** — Verify you are in the correct configuration mode (use `configure terminal` on Cisco devices or equivalent for your platform).
    **`% Incomplete command.`** — Add the required security level parameter; use `snmp-server host <nms-ip> version 3 priv <username>` with a valid username configured via `snmp-server user`.
## Polling with SNMPv3

```bash
# snmpwalk
snmpwalk -v3 -u <username> -l authPriv \
  -a SHA -A <authpass> \
  -x AES -X <privpass> \
  <device-ip> system

# snmpbulkwalk
snmpbulkwalk -v3 -u <username> -l authPriv \
  -a SHA -A <authpass> \
  -x AES -X <privpass> \
  <device-ip> ifTable
```


```text title="Expected output"
DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (487293847) 56 days, 8:01:28.47
SNMPv2-MIB::sysDescr.0 = STRING: Cisco IOS Software, C2960X Software, Version 15.2(4)E10
SNMPv2-MIB::sysObjectID.0 = OID: SNMPv2-SMI::enterprises.9.9.46.1
SNMPv2-MIB::sysUpTime.0 = Timeticks: (487293847) 56 days, 8:01:28.47
SNMPv2-MIB::sysContact.0 = STRING: network-ops@example.com
SNMPv2-MIB::sysName.0 = STRING: switch-core-01.prod.local
SNMPv2-MIB::sysLocation.0 = STRING: DataCenter-2, Rack-42
IF-MIB::ifNumber.0 = INTEGER: 52
IF-MIB::ifIndex.1 = INTEGER: 1
IF-MIB::ifDescr.1 = STRING: GigabitEthernet0/1
IF-MIB::ifType.1 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifMtu.1 = INTEGER: 1500
...
```

!!! warning "Common errors"
    **`snmpwalk: Unknown user name "<username>"`** — Replace `<username>` with an actual SNMPv3 user configured on the target device.
    **`snmpwalk: Authentication failure (incorrect password, community or engine ID)`** — Verify the authentication password (`-A`) and privacy password (`-X`) match the device configuration exactly.
    **`snmpwalk: No response from <device-ip>`** — Confirm the device IP is reachable, SNMPv3 is enabled on port 161, and the firewall allows SNMP traffic.
## Prometheus SNMP Exporter — SNMPv3 Config

```yaml
# snmp.yml
modules:
  cisco_v3:
    version: 3
    auth:
      username: <username>
      security_level: authPriv
      auth_protocol: SHA
      auth_password: <authpass>
      priv_protocol: AES
      priv_password: <privpass>
```

## Common Issues

| Symptom | Cause | Check |
|---|---|---|
| `Authentication failure` | Wrong auth password or protocol | Verify `-a SHA -A <pass>` matches device config |
| `Unknown security name` | Username not created on device | `show snmp user` on device |
| `Timeout: No Response` | User created but no group access | Check `show snmp group` — user must be in a group |
| Engine ID mismatch | Trap engine ID mismatch | Use `snmpwalk` to get remote engine ID |
