# MDS — CLI Reference


<div class="kb-summary">
> Part of the [Cisco MDS](../../index.md) reference. Commonly used NX-OS commands for managing Cisco MDS Fibre Channel switches. MDS runs NX-OS — the same operating system family as Cisco Nexus, so commands follow the `show / configure terminal / interface` pattern.
</div>

> Part of the [Cisco MDS](../../index.md) reference.

Commonly used NX-OS commands for managing Cisco MDS Fibre Channel switches. MDS runs NX-OS — the same operating system family as Cisco Nexus, so commands follow the `show / configure terminal / interface` pattern.

---

## Switch Status & Identity

Start here when connecting to a switch. These commands confirm the software version, check environmental health, and verify which modules are installed and active.

```bash
show version           # NX-OS version, uptime, hardware model
show inventory         # chassis, modules, transceivers with serial numbers
show system uptime
show license usage
show feature           # enabled features (zone, dpvm, fcsp, etc.)
```text
┌─────────────────────────────────── Cisco MDS 9000 — CLI Reference ────────────────────────────────────┐
│                                                                                                       │
│  MDS NX-OS CLI: fabric commands, zone commands, port commands, diagnostics.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Fabric & VSAN Commands            │  │                Zone Commands                │   │
│   │             show flogi database              │  │          show zone active vsan <n>          │   │
│   │            show vsan: all states             │  │           zone name <n> vsan <id>           │   │
│   │           show fcns database vsan            │  │          zoneset name <n> vsan <id>         │   │
│   │          show fcdomain: domain IDs           │  │          zoneset activate name <n>          │   │
│   │            show topology: ISL map            │  │          show device-alias database         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  show flogi and show zone are the two most-used daily operational commands.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Port & Interface Commands           │  │             Diagnostic & Support            │   │
│   │             show interface fc1/1             │  │              show system health             │   │
│   │          show interface trunk: ISLs          │  │               show environment              │   │
│   │          show port-channel summary           │  │               show module all               │   │
│   │             shut / no shut fc1/1             │  │            show tech-support: TAC           │   │
│   │          show interface transceiver          │  │             debug zone basic-er             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS director chassis · supervisor module · line card blades · management Ethernet                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  show flogi database= FC fabric login database; shows all device logins                               │
│  show vsan        = VSAN states; all should show active                                               │
│  show fcns database= FC Name Server database; registered devices in VSAN                              │
│  show fcdomain    = domain ID assignment; shows principal switch                                      │
│  show topology    = ISL map showing connected switches and port numbers                               │
│  show zone active = active zone set members and zone names per VSAN                                   │
│  device-alias     = WWN alias; CFS-distributed across fabric                                          │
│  zoneset activate = activates named zone set in specified VSAN                                        │
│  show interface fc= per-port FC counters: CRC, credit, throughput                                     │
│  show interface trunk= ISL trunk status and allowed VSAN list                                         │
│  show transceiver = SFP optical power level and signal status                                         │
│  show tech-support= full diagnostic bundle for Cisco TAC escalation                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

All modules should show status `ok`. A `failed` or `powered-dn` module requires immediate investigation.

### CPU & Memory

```bash
show system resources   # CPU and memory utilization
show processes cpu      # per-process CPU breakdown
show processes memory
```

### Running Configuration

```bash
show running-config
show startup-config
```

### Logging

```bash
show logging            # recent syslog events
show logging last 50    # last 50 log entries
```

### Quick Health Summary

| Check | Command | Expected |
|---|---|---|
| Version | `show version` | Expected NX-OS release |
| Modules | `show module` | All `ok` |
| Environment | `show environment` | No alerts |
| CPU | `show system resources` | < 70% |
| Recent logs | `show logging last 50` | No error storms |

### Pre-Change Baseline

```bash
show version
show running-config
show interface brief
show flogi database
```

---

## Interfaces & Ports

FC interfaces on MDS are identified as `fc<slot/port>`. Most configuration happens in `interface` config mode. Port modes control how a port behaves — F-port connects to a host/storage, E-port connects to another switch.

### Interface Status

```bash
# Summary of all interfaces
show interface brief

# Detailed single port
show interface fc<slot/port>

# Error counters
show interface fc<slot/port> counters
show interface fc<slot/port> counters errors

# Transceiver / SFP details
show interface fc<slot/port> transceiver
```

### Port Modes

| Mode | Use Case |
|---|---|
| F | Host / initiator (N_Port) |
| E | ISL to another switch (E_Port) |
| TE | Trunking ISL (VSAN-aware) |
| NP | N-Port Virtualization (NPV mode) |
| auto | Auto-detect (default) |
| SD | SPAN destination |

### Configure a Port

```bash
interface fc<slot/port>
  switchport mode F         # force F-port for host connections
  shutdown
  no shutdown
```

### Enable/Disable a Port

```bash
interface fc<slot/port>
  shutdown       # disable
  no shutdown    # enable
```

### Range Operations

```bash
# Apply config to a range of ports
interface fc<slot/port> - fc<slot/port>
  shutdown
```

### FC Domain

```bash
show fcdomain               # domain IDs across fabric
show fcdomain domain-list   # all domain IDs in VSAN
```

### Error Counter Reference

| Counter | Cause | Action |
|---|---|---|
| link-failures | Cable/SFP; port resets | Replace SFP; check cable |
| loss-of-sync | Signal quality | Check SFP power levels |
| input-crc | Bad frames | Replace SFP; check cable |
| bb-credit-zero | Buffer-to-buffer credit depleted | Increase BB credits; check ISL design |

### Common Port Issues

| Issue | Check | Action |
|---|---|---|
| Port stays down | SFP, cable, peer | `show interface` — check reason |
| Port mode mismatch | Expected F, got E | Force mode: `switchport mode F` |
| CRC errors | SFP quality | Replace SFP |
| No FLOGI on F-port | Host HBA not sending login | Check host HBA and driver |

---

## FLOGI & Name Server

FLOGI (Fabric Login) is the handshake a device uses to join the SAN fabric. The name server is the fabric's directory — hosts and storage targets register here so they can find each other. If a device's WWN is missing, it hasn't successfully logged in.

### FLOGI Database

```bash
# All logged-in initiators and targets
show flogi database

# Filter to a specific VSAN
show flogi database vsan <id>

# Confirm a specific WWN is logged in
show flogi database | grep <wwn>
```

### FC Name Server

```bash
# All registered devices in the fabric
show fcns database
show fcns database vsan <id>
show fcns database detail         # includes port type, symbolic name

# Name server statistics
show fcns statistics

# Look up a specific WWN
show fcns database | grep <wwn>
```

### Interpreting FLOGI Output

| Field | Meaning |
|---|---|
| Interface | Which MDS port the device logged into |
| VSAN | VSAN the device is in |
| FCID | Fabric-assigned address (N_Port ID) |
| Port Name (PWWN) | Port WWN of the device |
| Node Name (NWWN) | Node WWN of the device |

### Verifying Host-to-Storage Visibility

```bash
# Find the host HBA WWN in FLOGI
show flogi database | grep <host_wwn>

# Confirm storage port is in the name server
show fcns database | grep <storage_wwn>

# Confirm both are in the same VSAN
show vsan membership
```

### Common FLOGI Issues

| Issue | Check | Action |
|---|---|---|
| Host WWN not in FLOGI | HBA link, VSAN membership | Check port state; verify VSAN assignment |
| Storage target not visible | FLOGI and FCNS | Check array port and zoning |
| FCID missing | FLOGI failed | Check port state, VSAN config |
| Duplicate FCID | Fabric merge conflict | Investigate VSAN merges |

---

## Zoning

Zoning controls which initiators (hosts) can see which targets (storage). Without zoning, every device in a VSAN can see every other device — unsafe and unstable. Best practice is single-initiator zoning: one host HBA per zone, paired with its storage target ports.

```bash
# View zoning
show zone
show zone vsan <id>
show zone active vsan <id>
show zoneset
show zoneset active vsan <id>
show zoneset active vsan <id> | grep <wwn>
show zone member vsan <id>

# Create zone and add members
zone name <zone_name> vsan <id>
  member pwwn <wwn>
  member device-alias <alias>

# Device aliases (human-readable names for WWNs)
show device-alias database
device-alias database
  device-alias name <alias> pwwn <wwn>
device-alias commit

# Zoneset (group of zones to activate together)
zoneset name <zoneset_name> vsan <id>
  member <zone_name>

# Activate the zoneset (makes zoning live in the VSAN)
zoneset activate name <zoneset_name> vsan <id>

# Save to startup config (always do this after changes)
copy running-config startup-config
```

---

## VSANs

VSANs (Virtual SANs) partition a physical fabric into multiple logical fabrics. Each VSAN has its own name server, domain IDs, and zoning configuration. VSANs isolate different environments (e.g., Production vs. Dev) on the same physical switch.

### View VSAN Status

```bash
# All VSANs on the switch
show vsan
show vsan <id>

# VSAN port membership
show vsan membership
show vsan membership interface fc<slot/port>
```

### VSAN States

| State | Meaning |
|---|---|
| active | VSAN is running normally |
| suspended | VSAN administratively suspended |

### Create, Assign, Suspend, Delete

```bash
# Create
vsan database
  vsan <id> name "<name>"

# Assign a port to a VSAN
vsan database
  vsan <id> interface fc<slot/port>

# Suspend / resume
vsan database
  vsan <id> suspend
  no vsan <id> suspend

# Delete (disrupts all devices — confirm no active traffic first)
vsan database
  no vsan <id>
```

### VSAN on ISL Trunks

VSANs must be explicitly allowed on trunk ISL ports:

```bash
interface fc<slot/port>
  switchport trunk allowed vsan add <id>
```

### Inter-VSAN Routing (IVR)

IVR allows devices in different VSANs to communicate:

```bash
show ivr
show ivr vsan-topology
ivr enable
```

### Common VSAN Issues

| Issue | Check | Action |
|---|---|---|
| Host not seeing storage | Same VSAN? | `show vsan membership` on both ports |
| VSAN not crossing ISL | Trunk allowed VSANs | Add VSAN to trunk |
| VSAN suspended | Admin state | `no vsan suspend` |

---

## ISLs & Trunking

ISLs (Inter-Switch Links) connect MDS switches together to form a fabric. TE ports are trunking ISLs — they carry multiple VSANs over a single physical link. Port channels bond multiple ISLs for higher bandwidth and redundancy.

### ISL Status

```bash
show topology          # fabric-wide ISL topology
show trunk             # trunk port states and allowed VSANs
show interface trunk   # trunk interface detail

# E-port (ISL) ports only
show interface brief | include E
```

### Configure a TE Port (Trunking ISL)

```bash
interface fc<slot/port>
  switchport mode TE
  switchport trunk allowed vsan <vsan_id>
  no shutdown
```

### Restrict VSANs on an ISL

```bash
interface fc<slot/port>
  switchport trunk allowed vsan add <vsan_id>
  switchport trunk allowed vsan remove <vsan_id>
```

### ISL Error Counters

```bash
show interface fc<slot/port> counters
show interface fc<slot/port> counters errors
```

Watch for: `link-failures`, `loss-of-sync`, `input-crc`

### Port Channel (LAG for ISLs)

```bash
interface port-channel <id>
  switchport mode E
  no shutdown

interface fc<slot/port>
  channel-group <id>
  no shutdown

show port-channel summary
show interface port-channel <id>
```

### Common ISL Issues

| Issue | Check | Action |
|---|---|---|
| ISL down | Port mode and status | Verify `switchport mode TE/E` |
| VSAN not crossing ISL | Trunk allowed VSANs | Add VSAN to trunk |
| CRC errors | SFP and cable | Replace SFP; check cable quality |
| Port channel member not up | Channel-group config | Verify all members in same channel |

---

## Diagnostics, Counters & SPAN

Tools for troubleshooting port errors, running hardware tests, and capturing SAN traffic for analysis.

### Port Errors and Counters

```bash
# Port errors
show interface fc<slot/port> counters
show interface fc<slot/port> counters errors
clear counters interface fc<slot/port>

# CRC / link reset errors
show interface fc<slot/port> | include CRC

# Hardware diagnostics
show diagnostics result module <slot>

# Event log
show logging onboard
show logging last <n>

# Core health
show system internal sysmgr status
```

### SPAN (Traffic Capture)

SPAN mirrors traffic from one port to another, letting you capture FC frames for analysis:

```bash
show monitor session all
monitor session <n> source interface fc<slot/port>
monitor session <n> destination interface fc<slot/port>
no monitor session <n>
```

---

## Firmware & Configuration

Keeping NX-OS up to date ensures security fixes and feature improvements. MDS supports ISSU (In-Service Software Upgrade) for non-disruptive upgrades. Always save configuration before and after changes.

### Version & Upgrade

```bash
# Current version
show version
show install all status         # result of last install operation

# Stage and install from URL (TFTP/SCP/HTTP)
install all kickstart <kickstart_url> system <system_url>

# Non-disruptive upgrade check (ISSU)
install all nxos <url> non-disruptive

# Preview impact before committing
install all kickstart <url> system <url> status
```

### Configuration Backup

```bash
# Save running to startup (before any change)
copy running-config startup-config

# Copy config off-switch via TFTP
copy running-config tftp://<server>/<filename>

# Copy config off-switch via SCP
copy running-config scp://<user>@<server>/<path>/<filename>

# Restore from TFTP
copy tftp://<server>/<filename> running-config

# Show full config
show running-config
show startup-config
```

### Configuration Checkpoint & Rollback

```bash
# Save a named checkpoint
checkpoint <checkpoint_name>
show checkpoint summary

# Rollback to checkpoint
rollback running-config checkpoint <checkpoint_name>
```

---

## Security & Users

User management and authentication for MDS switches. TACACS+/RADIUS integration is recommended for enterprise deployments to enforce consistent access policies and audit trails.

### Local Users

```bash
# Show all local users
show users

# Show defined roles
show role

# Create a local user
username <user> password <pass> role <role>

# Delete a user
no username <user>

# Assign admin role
username <user> role network-admin
```

### TACACS+ / RADIUS

```bash
# Show AAA config
show aaa

# Show TACACS+ servers
show tacacs-server

# Show RADIUS servers
show radius-server

# Configure TACACS+ server
tacacs-server host <ip> key <key>
aaa group server tacacs+ <group_name>
  server <ip>
aaa authentication login default group <group_name>
```

### SSH

```bash
show ssh server
show users

# Generate RSA keys
crypto key generate rsa
show crypto key mypubkey rsa
```

### SNMPv3

```bash
show snmp user
show snmp community

# Create SNMPv3 user
snmp-server user <user> <group> v3 auth sha <auth_pass> priv aes 128 <priv_pass>
```

### Common Security Issues

| Issue | Check | Action |
|---|---|---|
| Login fails | Local account or TACACS reachability | Check `show tacacs-server`; test locally |
| SSH key error | Key mismatch | Regenerate: `crypto key generate rsa` |
| AAA lockout | TACACS down | Ensure local fallback configured |
