# FabricOS — Hardening

> Part of the [Security](../) reference.

---

## Hardening Sequence — New Switch

```mermaid
flowchart TD
    start([New switch deployed]) --> proto["Disable Telnet + HTTP\nEnable HTTPS only"]
    proto --> snmpHarden["Remove SNMPv1/v2c\nConfigure SNMPv3 SHA+AES"]
    snmpHarden --> aaa["Configure RADIUS / TACACS+\nauthorder RADIUS;LOCAL"]
    aaa --> rbac["Assign RBAC roles\nswitchadmin · zoneadmin · operator"]
    rbac --> ipf["Apply IPfilter policy\nmanagement subnet only"]
    ipf --> ntp["Configure NTP\n2 internal servers"]
    ntp --> syslog["Forward syslog to SIEM\nsyslogadmin --add"]
    syslog --> audit["Enable audit logging\nauditcfg --class 1,2,3,4"]
    audit --> domainId["Set static domain ID\ninsistDomainId=1"]
    domainId --> fabricBinding["Enable fabric binding\nfabricbinding --enable"]
    fabricBinding --> defZone["Disable default zone\ndefzone --noaccess"]
    defZone --> backup["configupload post-hardening\nto backup server"]
    backup --> cmdb["Update CMDB\nhostname · serial · domain ID"]
    cmdb --> done([Switch production-ready])

    style done fill:#15803d,color:#fff
    style start fill:#2563eb,color:#fff
```

## Overview

Hardening a Brocade FabricOS switch closes the attack surface on both the management plane (who can connect and how) and the fabric plane (which devices can join and communicate). Apply hardening immediately after initial switch configuration, before connecting to the production network.

The hardening steps are grouped into three categories:

1. **Management plane** — authentication, protocol restrictions, access control
2. **Fabric plane** — device and switch admission control
3. **Operational** — logging, monitoring, change control

---

## Hardening Checklist

Apply every item on this list to each new switch before it enters production service. Document completion in the CMDB change record.

### Management Plane

- [ ] **Telnet disabled** — SSH only for CLI access (`sshutil --show`)
- [ ] **HTTP disabled, HTTPS enabled** — web management over TLS only (`httpcfg --show`)
- [ ] **RADIUS configured** pointing to Active Directory/LDAP; local accounts as fallback only
- [ ] **Local `admin` password changed** from factory default; stored in enterprise vault
- [ ] **All unused default accounts reviewed** — disable any not required (`userconfig --show`)
- [ ] **RBAC roles assigned** — `switchadmin` for ops, `zoneadmin` for zone-only changes; no shared `admin` accounts for daily use
- [ ] **IPfilter policy applied** — management plane restricted to approved management subnet
- [ ] **SNMP v3 configured** — SHA authentication, AES-128 privacy; default community strings removed
- [ ] **SSH host key generated** — RSA 2048+ or ECDSA (`sshutil --genkey`)
- [ ] **NTP configured and synced** — minimum two NTP servers from internal stratum 2 hierarchy
- [ ] **Syslog forwarded to SIEM** — all facility levels forwarded (`syslogadmin --show`)
- [ ] **Audit logging enabled** — zone changes, logins, firmware events logged

### Fabric Plane

- [ ] **Static domain ID set** — `insistDomainId = 1` in `configure`; domain ID recorded in SAN design register
- [ ] **Fabric binding enabled** — only known switches permitted to form ISLs
- [ ] **Zoning configured** — single-initiator, WWN-based zones only; no default zone (open fabric)
- [ ] **Default zone disabled** — verify `defzone --show` returns `off` (all devices not in a zone are isolated)

### Operational

- [ ] **Configuration backup taken** — post-hardening config uploaded to backup server
- [ ] **CMDB updated** — switch hostname, serial number, domain ID, port map, support contract
- [ ] **SANnav discovery completed** — switch visible in SANnav with no unresolved alerts
- [ ] **MAPS policy applied** — `dflt_conservative_policy` or equivalent as baseline

---

## Management Protocol Hardening

### Disable Telnet

```bash
configure
# Navigate: Fabric parameters → System Services → Telnet
# Enter: 0 (disable)
# Complete the configure wizard

# Verify
sshutil --show    # Confirm telnetd = disabled
```

### Disable HTTP

```bash
# Disable HTTP, enable HTTPS only
httpcfg --set -http 0
httpcfg --set -https 1

# Verify
httpcfg --show    # HTTP: disabled; HTTPS: enabled
```

### Remove Default SNMP Community Strings

```bash
# Show existing community strings
snmpconfig --show snmpv1

# Remove each community string found
snmpconfig --delete snmpv1 -user public
snmpconfig --delete snmpv1 -user private

# Configure SNMP v3
snmpconfig --set mibCapability
# Follow interactive prompts: user, SHA auth password, AES-128 priv password

# Verify
snmpconfig --show
```

---

## Audit Logging

Audit logging captures all login events, configuration changes, zone modifications, and firmware operations. These logs must be forwarded to the SIEM in real time.

### Enable Audit Logging

```bash
# Enable audit logging — classes:
# 1 = Fabric events (topology changes, domain changes)
# 2 = Security events (logins, policy changes)
# 3 = Configuration events (zone changes, port config)
# 4 = Firmware events (firmware download, HA failover)
auditcfg --class 1,2,3,4

# Verify audit logging is active
auditcfg --show

# View recent audit log entries
auditlog --show

# View last 100 audit entries
auditlog --show -n 100
```

### Configure Syslog Forwarding

```bash
# Add SIEM syslog destination
syslogadmin --add -ip <siem-ip>

# Verify syslog destinations
syslogadmin --show

# Test by running a command that generates an audit event
# e.g., cfgsave (triggers a zone config save audit event)
# Then check the SIEM for the forwarded log entry
```

### Syslog Facility and Severity

Brocade FabricOS sends syslog at facility `LOCAL1` (by default). Configure the SIEM to accept and parse this facility. Log format includes:

```
<timestamp> <switch-hostname> RASLOG: <severity> [<module>/<id>] <message>
```

Severity levels map to standard syslog levels: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`.

---

## Default Zone Enforcement

The default zone controls what happens to devices that are not in any active zone. It must be disabled (set to `off`) in all production fabrics. If the default zone is `on`, devices not in any zone can see all other unzoned devices — a significant security risk.

```bash
# Check default zone state
defzone --show

# Disable the default zone (recommended for all production fabrics)
defzone --noaccess

# Activate and save
cfgenable <active-zoneset>
cfgsave

# Verify
defzone --show    # Expected: Default Zone: OFF (no access)
```

---

## Security Baselines Summary

| Control | Standard | Command |
|---|---|---|
| Management CLI | SSH only; Telnet disabled | `sshutil --show` |
| Web management | HTTPS only; HTTP disabled | `httpcfg --show` |
| SNMP | SNMPv3 (SHA + AES-128); no v1/v2c | `snmpconfig --show` |
| RADIUS/TACACS+ | Primary auth; local as fallback only | `aaaconfig --show` |
| Local admin | Unique password in vault; break-glass only | Vault policy |
| IPfilter | Management subnet restriction | `ipfilter --show` |
| Audit logging | Classes 1–4 enabled; forwarded to SIEM | `auditcfg --show` |
| Syslog | Forwarded to SIEM | `syslogadmin --show` |
| NTP | Two internal servers; synced | `tsclockserver` |
| Default zone | Disabled (`off`) | `defzone --show` |
| Fabric binding | Enabled | `fabricbinding --show` |
| Static domain ID | Set and documented | `switchshow \| grep Domain` |

---

## Post-Hardening Verification

Run this sequence after completing hardening to verify all controls are applied:

```bash
# 1. Management protocols
sshutil --show        # telnetd disabled
httpcfg --show        # HTTP disabled; HTTPS enabled
snmpconfig --show     # SNMPv3 configured; no community strings

# 2. Authentication
aaaconfig --show      # RADIUS configured; auth order includes LOCAL fallback

# 3. Network access control
ipfilter --show       # Active policy restricting management plane

# 4. Fabric security
defzone --show        # Default zone off (no access)
fabricbinding --show  # Fabric binding enabled

# 5. Audit and logging
auditcfg --show       # Audit classes 1,2,3,4 enabled
syslogadmin --show    # SIEM syslog destination configured

# 6. NTP
tsclockserver         # NTP servers configured
date                  # Clock is synced (matches expected time)

# 7. Domain ID
switchshow | grep Domain    # Static domain ID matches SAN design register
```

Take a configuration backup after completing verification:

```bash
cfgsave
configupload -all -scp -host <backup-server> -u <user> -f /backups/brocade/<switch>_post-hardening.cfg
```

---

## Periodic Review

Hardening is not a one-time task. Schedule these reviews:

| Review | Frequency | Action |
|---|---|---|
| SNMP password rotation | Quarterly | Rotate auth and priv passwords; update monitoring platform |
| Break-glass password rotation | Quarterly | Rotate local `admin` password; update vault |
| IPfilter policy review | After network changes | Confirm management subnet is still correct |
| Audit log review | Monthly | Review SIEM for unusual login patterns or config changes |
| Firmware currency | Quarterly | Compare installed FOS version against Broadcom release notes |
| CMDB accuracy | After any change | Update switch serial, firmware, port map in CMDB |
