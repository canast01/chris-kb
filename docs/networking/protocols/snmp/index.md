---
title: SNMP
tags:
  - networking
description: "Simple Network Management Protocol (SNMP) polls device metrics and receives asynchronous fault notifications (traps) over UDP — port 161 for polling, 162..."
---

# SNMP

<div class="kb-summary">
Simple Network Management Protocol (SNMP) polls device metrics and receives asynchronous fault notifications (traps) over UDP — port 161 for polling, 162 for traps. SNMPv1/v2c use plaintext community strings; SNMPv3 adds authentication and encryption via the User Security Model (USM). Coverage includes OID polling, trap handling, and monitoring integration.
</div>

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="polling/">
  <strong>Polling</strong>
  <span>OID walks, GET requests, polling intervals, and MIB-based metric collection from network devices.</span>
</a>

<a class="kb-card" href="traps/">
  <strong>Traps</strong>
  <span>Trap vs inform, trap receivers, filtering, and forwarding asynchronous device alerts.</span>
</a>

<a class="kb-card" href="communities/">
  <strong>Communities</strong>
  <span>Community string configuration for SNMPv1/v2c — read-only vs read-write, ACLs, and security risks.</span>
</a>

<a class="kb-card" href="snmpv3/">
  <strong>SNMPv3</strong>
  <span>USM user configuration, authNoPriv vs authPriv, SHA authentication, and AES encryption setup.</span>
</a>

<a class="kb-card" href="monitoring/">
  <strong>Monitoring</strong>
  <span>Integrating SNMP with monitoring platforms (Zabbix, PRTG, Prometheus snmp_exporter), MIB management.</span>
</a>

</div>

## Quick Reference

| Property | SNMPv1 | SNMPv2c | SNMPv3 |
|---|---|---|---|
| Authentication | Community string | Community string | USM (username + auth password) |
| Encryption | None | None | AES-128 / AES-256 (authPriv) |
| Bulk operations | No | Yes (GetBulk) | Yes (GetBulk) |
| Trap acknowledgement | No (fire-and-forget) | Informs (acknowledged) | Informs (acknowledged) |
| Security recommendation | Avoid | Legacy only | Required for production |
| Port (polling) | 161/udp | 161/udp | 161/udp |
| Port (traps) | 162/udp | 162/udp | 162/udp |

**SNMPv3 security levels:**

| Level | Auth | Priv | Use case |
|---|---|---|---|
| `noAuthNoPriv` | No | No | Testing only |
| `authNoPriv` | Yes (MD5/SHA) | No | Low-sensitivity metrics |
| `authPriv` | Yes (SHA) | Yes (AES) | Production — recommended |

## Common Commands / Config

```bash
# Walk all OIDs from a device (SNMPv2c)
snmpwalk -v2c -c <community> <host>

# Get a specific OID (sysDescr)
snmpget -v2c -c <community> <host> 1.3.6.1.2.1.1.1.0

# Walk interface table (SNMPv2c)
snmpwalk -v2c -c <community> <host> 1.3.6.1.2.1.2.2

# Walk with SNMPv3 (authPriv)
snmpwalk -v3 -l authPriv \
  -u <username> \
  -a SHA -A <auth-password> \
  -x AES -X <priv-password> \
  <host> 1.3.6.1.2.1.1

# Send a test trap (SNMPv2c)
snmptrap -v2c -c <community> <trap-receiver> '' 1.3.6.1.6.3.1.1.5.1

# Get system uptime OID
snmpget -v2c -c <community> <host> 1.3.6.1.2.1.1.3.0

# Translate OID to human-readable name (requires MIBs installed)
snmptranslate -Of 1.3.6.1.2.1.1.1.0

# Bulk walk for faster retrieval (SNMPv2c+)
snmpbulkwalk -v2c -c <community> <host> 1.3.6.1.2.1.2
```


```text title="Expected output"
SNMPv2-MIB::sysDescr.0 = STRING: Linux router.example.com 5.10.0-8-amd64 #1 SMP Debian 5.10.46-4 (2021-08-03) x86_64
SNMPv2-MIB::sysObjectID.0 = OID: SNMPv2-SMI::enterprises.9.9.46.1
SNMPv2-MIB::sysUpTimeInstance = Timeticks: (847293847) 98 days, 2:09:47.47
SNMPv2-MIB::sysContact.0 = STRING: admin@example.com
SNMPv2-MIB::sysName.0 = STRING: router.example.com
SNMPv2-MIB::sysLocation.0 = STRING: Data Center 1, Rack 42
SNMPv2-MIB::sysServices.0 = INTEGER: 72
SNMPv2-MIB::sysORLastChange.0 = Timeticks: (0) 0:00:00.00
SNMPv2-MIB::sysORIndex.1 = INTEGER: 1
...

SNMPv2-MIB::sysDescr.0 = STRING: Linux router.example.com 5.10.0-8-amd64 #1 SMP Debian 5.10.46-4 (2021-08-03) x86_64

IF-MIB::ifIndex.1 = INTEGER: 1
IF-MIB::ifDescr.1 = STRING: eth0
IF-MIB::ifType.1 = INTEGER: ethernetCsmacd(6)
IF-MIB::ifMtu.1 = INTEGER: 1500
IF-MIB::ifSpeed.1 = Gauge32: 1000000000
IF-MIB::ifPhysAddress.1 = STRING: 08:00:27:a4:2b:c1
IF-MIB::ifAdminStatus.1 = INTEGER: up(1)
IF-MIB::ifOperStatus.1 = INTEGER: up(1)
...

SNMPv2-MIB::sysDescr.0 = STRING: Linux router.example.com 5.10.0-8-amd64 #1 SMP Debian 5.10.46-4 (2021-08-03) x86_64

SNMPv2-MIB::sysUpTimeInstance = Timeticks: (847293847) 98 days, 2:09:47.47

SNMP-COMMUNITY-MIB::snmpTrapAddress.0 = IpAddress: 192.168.1.100
SNMP-COMMUNITY-MIB::snmpTrapCommunity.0 = STRING: public
(no output — trap sent silently)

SNMPv2-MIB::sysUpTimeInstance.0 = Timeticks: (847293847) 98 days, 2:09:47.47

.1.3.6.1.2.1.1.1.0

IF-M
```
**Common OIDs:**

| OID | Name | Description |
|---|---|---|
| `1.3.6.1.2.1.1.1.0` | sysDescr | Device description |
| `1.3.6.1.2.1.1.3.0` | sysUpTime | Uptime in hundredths of a second |
| `1.3.6.1.2.1.1.5.0` | sysName | Hostname |
| `1.3.6.1.2.1.2.2` | ifTable | Interface table |
| `1.3.6.1.4.1.*` | enterprise | Vendor-specific OIDs |

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| `Timeout: No Response` | UDP reachability, ACL on device | Confirm port 161/udp is open; verify community string or USM credentials; check device SNMP ACL |
| `Authentication failure` (v3) | Auth password, auth protocol mismatch | Verify `-a` (SHA/MD5) and `-A` password match device config; check engine ID sync |
| Walk returns no data | Community string wrong; OID not supported | Test with `sysDescr` (1.3.6.1.2.1.1.1.0) first; confirm MIB is loaded on device |
| Traps not received | Trap destination not configured on device; firewall blocking 162/udp | Verify trap receiver IP on device; check firewall for 162/udp inbound on receiver |
| Read-write community exposed | SNMPv2c RW community in use | Restrict to read-only; switch to SNMPv3 authPriv; ACL to monitoring host IPs only |
| MIB not found locally | MIB files not installed | Install net-snmp-mibs or vendor MIB package; set `MIBDIRS` environment variable |
