---
title: SNMPv3
tags:
  - networking
---

# SNMPv3


<div class="kb-summary">
SNMPv3 adds authentication and encryption to SNMP, replacing the plaintext community strings of v1/v2c.
</div>

        SNMPv3 authPriv SECURITY MODEL (USM)
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  NMS                              Device agent                                                        │
│  ┌────────────────────┐           ┌──────────────────────┐                                            │
│  │ SNMPv3 GET request │           │ USM validation       │                                            │
│  │                    │           │                      │                                            │
│  │ securityName: monUsr           │ 1. Verify username   │                                            │
│  │ authProtocol: SHA  ├──────────►│ 2. Check SHA HMAC    │                                            │
│  │ authKey: <pass>    │ encrypted │ 3. Decrypt AES       │                                            │
│  │ privProtocol: AES  │  UDP 161  │ 4. Process OID query │                                            │
│  │ privKey: <pass>    │           │                      │                                            │
│  │                    │◄──────────┤ 5. Encrypt response  │                                            │
│  │ OID value returned │           │ 6. Sign with SHA     │                                            │
│  └────────────────────┘           └──────────────────────┘                                            │
│                                                                                                       │
│  Security levels:                                                                                     │
│  noAuthNoPriv ─ no auth, no encryption (avoid)                                                        │
│  authNoPriv   ─ SHA auth, no encryption (metrics only)                                                │
│  authPriv     ─ SHA auth + AES encryption  ◄── use this                                               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
It is the required version for any environment with compliance requirements.

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
