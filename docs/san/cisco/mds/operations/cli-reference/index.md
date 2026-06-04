# Cisco MDS 9000 — CLI Reference

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
```bash
show system resources   # CPU and memory utilization
show processes cpu      # per-process CPU breakdown
show processes memory
```
```bash
show running-config
show startup-config
```
```bash
show logging            # recent syslog events
show logging last 50    # last 50 log entries
```
```bash
show version
show running-config
show interface brief
show flogi database
```
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
```bash
interface fc<slot/port>
  switchport mode F         # force F-port for host connections
  shutdown
  no shutdown
```
```bash
interface fc<slot/port>
  shutdown       # disable
  no shutdown    # enable
```
```bash
# Apply config to a range of ports
interface fc<slot/port> - fc<slot/port>
  shutdown
```
```bash
show fcdomain               # domain IDs across fabric
show fcdomain domain-list   # all domain IDs in VSAN
```
```bash
# All logged-in initiators and targets
show flogi database

# Filter to a specific VSAN
show flogi database vsan <id>

# Confirm a specific WWN is logged in
show flogi database | grep <wwn>
```
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
```bash
# Find the host HBA WWN in FLOGI
show flogi database | grep <host_wwn>

# Confirm storage port is in the name server
show fcns database | grep <storage_wwn>

# Confirm both are in the same VSAN
show vsan membership
```
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
```bash
# All VSANs on the switch
show vsan
show vsan <id>

# VSAN port membership
show vsan membership
show vsan membership interface fc<slot/port>
```
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
```bash
interface fc<slot/port>
  switchport trunk allowed vsan add <id>
```
```bash
show ivr
show ivr vsan-topology
ivr enable
```
```bash
show topology          # fabric-wide ISL topology
show trunk             # trunk port states and allowed VSANs
show interface trunk   # trunk interface detail

# E-port (ISL) ports only
show interface brief | include E
```
```bash
interface fc<slot/port>
  switchport mode TE
  switchport trunk allowed vsan <vsan_id>
  no shutdown
```
```bash
interface fc<slot/port>
  switchport trunk allowed vsan add <vsan_id>
  switchport trunk allowed vsan remove <vsan_id>
```
```bash
show interface fc<slot/port> counters
show interface fc<slot/port> counters errors
```
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
```bash
show monitor session all
monitor session <n> source interface fc<slot/port>
monitor session <n> destination interface fc<slot/port>
no monitor session <n>
```
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
```bash
# Save a named checkpoint
checkpoint <checkpoint_name>
show checkpoint summary

# Rollback to checkpoint
rollback running-config checkpoint <checkpoint_name>
```
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
```bash
show ssh server
show users

# Generate RSA keys
crypto key generate rsa
show crypto key mypubkey rsa
```
```bash
show snmp user
show snmp community

# Create SNMPv3 user
snmp-server user <user> <group> v3 auth sha <auth_pass> priv aes 128 <priv_pass>
```
