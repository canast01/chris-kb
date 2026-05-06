# Cisco MDS NX-OS CLI Reference

Commonly used NX-OS commands for managing Cisco MDS Fibre Channel switches.

---

## Switch Status & Identity

```bash
# Switch info
show version
show inventory
show environment
show system uptime
show license usage
show feature
```

---

## Interfaces & Ports

```bash
# Interface status
show interface brief
show interface fc<slot/port>
show interface fc<slot/port> counters
show interface fc<slot/port> transceiver

# Port configuration
interface fc<slot/port>
  switchport mode {auto | E | F | Fx | NP | TE | SD | ST}
  shutdown
  no shutdown

# Bulk operations
show interface fc<slot/port> - fc<slot/port> brief

# Physical topology
show topology
show fcdomain
show fcdomain domain-list
```

---

## FLOGI & Name Server

```bash
# Login database
show flogi database
show flogi database vsan <id>

# Name server
show fcns database
show fcns database vsan <id>
show fcns database detail
show fcns statistics

# Zone member lookup
show fcns database | grep <wwn>
```

---

## Zoning

```bash
# View zoning
show zone
show zone vsan <id>
show zone active vsan <id>
show zoneset
show zoneset active vsan <id>
show zoneset active vsan <id> | grep <wwn>
show zone member vsan <id>

# Create zone / alias
zone name <zone_name> vsan <id>
  member pwwn <wwn>
  member device-alias <alias>

# Device aliases
show device-alias database
device-alias database
  device-alias name <alias> pwwn <wwn>
device-alias commit

# Zoneset
zoneset name <zoneset_name> vsan <id>
  member <zone_name>

# Activate
zoneset activate name <zoneset_name> vsan <id>

# Save
copy running-config startup-config
```

---

## VSANs

```bash
# VSAN status
show vsan
show vsan <id>
show vsan membership
show vsan membership interface fc<slot/port>

# Create VSAN
vsan database
  vsan <id> name "<name>"

# Assign port to VSAN
vsan database
  vsan <id> interface fc<slot/port>
```

---

## ISLs & Trunking

```bash
# ISL status
show topology
show trunk
show interface trunk

# TE port (trunking)
interface fc<slot/port>
  switchport trunk allowed vsan <id>
  switchport mode TE
  no shutdown
```

---

## Diagnostics & Counters

```bash
# Port errors
show interface fc<slot/port> counters
show interface fc<slot/port> counters errors
clear counters interface fc<slot/port>

# CRC / link reset errors
show interface fc<slot/port> | include CRC
show hardware internal errors

# Diagnostics
show diagnostics result module <slot>

# Port analysis
analyze port-channel

# Event log
show logging onboard
show logging last <n>

# Core health
show system internal sysmgr status
```

---

## SPAN & Monitoring

```bash
show monitor session all
monitor session <n> source interface fc<slot/port>
monitor session <n> destination interface fc<slot/port>
no monitor session <n>
```

---

## Firmware & Configuration

```bash
# Firmware
show version
show install all status
install all kickstart <url> system <url>

# Config backup
copy running-config startup-config
copy running-config tftp://<server>/<filename>
copy tftp://<server>/<filename> running-config

# Show full config
show running-config
show startup-config
```

---

## Security & Users

```bash
# Local users
show users
show role
username <user> password <pass> role <role>

# RADIUS / TACACS+
show tacacs-server
show radius-server
show aaa

# SSH keys
show ssh server
show crypto key mypubkey rsa
```
