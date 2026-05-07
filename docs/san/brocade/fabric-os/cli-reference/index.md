# Brocade Fabric OS CLI Reference

Commonly used Brocade FOS commands for managing Fibre Channel SAN switches. Log in via SSH to the switch management IP. Most commands run without needing to enter a specific mode.

---


<div class="kb-grid kb-grid-1">

<a class="kb-card" href="switch-status/">
  <strong>Switch Status</strong>
  <span>Switch Status notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="vf/">
  <strong>Vf</strong>
  <span>Vf notes, checks, commands, and references.</span>
</a>

</div>
## Switch Status & Identity

The first commands to run when connecting to a switch. `switchshow` gives you a full port-by-port overview — which ports are up, what devices are connected, and their WWNs. `switchstatusshow` gives the overall health verdict.

```bash
switchshow         # ports, state, speed, and connected WWNs — most useful daily command
switchstatusshow   # overall switch health status (expected: HEALTHY)
version            # Fabric OS version
ipAddrShow         # management IP addresses
licenseShow        # installed licenses
chassisShow        # chassis hardware inventory
slotShow           # blade/slot population
```

### Health Status

```bash
switchstatusshow
```

Expected output: `HEALTHY`. Any other status requires investigation.

### Firmware Version

```bash
version
firmwareShow
```

### Fan, Power, Temperature

```bash
psShow      # power supplies
fanShow     # fan status
tempShow    # temperature sensors
sensorShow  # all environmental sensors
```

All sensors should show `OK`. Any sensor in `FAILED` state requires immediate action.

### Uptime & SNMP

```bash
uptime
snmpConfig --show
syslogDIPShow    # syslog destinations
```

### Pre-Change Baseline (Run Before Any Change)

```bash
switchshow
switchstatusshow
fabricshow
nsShow
aliShow
zoneShow --all
```

### Common Issues

| Issue | Check | Action |
|---|---|---|
| Switch status not HEALTHY | Environmental or hardware | Check `psShow`, `fanShow`, `tempShow` |
| Firmware version mismatch | `version` | Schedule Fabric OS upgrade |
| License missing | `licenseShow` | Add license key via `licenseAdd` |

---

## Ports

Individual port management — enable/disable ports, check errors, and configure speed. Ports are identified as `slot/port` (e.g., `0/1` on a fixed-form switch is just port `1`).

### Port Status

```bash
portShow <slot/port>           # detailed port info (state, speed, WWN, connected device)
portStatsShow <slot/port>      # TX/RX frames, errors
portErrShow                    # error summary across all ports
portLogShow <slot/port>        # port event log
portCfgShow <slot/port>        # port configuration
```

### Port States

| State | Meaning |
|---|---|
| Online | Healthy, device logged in |
| No_Light | No SFP or no signal |
| No_Module | No SFP installed |
| Offline (Admin) | Administratively disabled |
| In_Sync | Link up but no device logged in |
| Faulty | Hardware fault |

### Enable / Disable a Port

```bash
portDisable <slot/port>
portEnable <slot/port>

# Persistent disable/enable — survives switch reboot
portPersistentDisable <slot/port>
portPersistentEnable <slot/port>
```

### Port Speed Configuration

```bash
portCfgSpeed <slot/port> <speed>
# speed: 0=auto, 4, 8, 16, 32 (Gbps)
```

### Long Distance Mode

```bash
portCfgLongDistance <slot/port> <mode>
# modes: L0 (normal), L1, L2, LE, LD, LS
```

### Port Error Counters

```bash
portStatsShow <slot/port>
portErrShow
portStatsReset <slot/port>    # reset counters after investigation
```

Key error fields:
| Field | Cause | Action |
|---|---|---|
| LossSignal | SFP or cable issue | Replace SFP; check cable |
| LossSync | Signal quality | Check SFP power level |
| EncInFrm | Encoding errors | Replace SFP |

### Common Port Issues

| Issue | Check | Action |
|---|---|---|
| Port shows No_Light | SFP installed? | Seat SFP; check cable |
| Port flapping | Signal quality | Replace SFP; check cable |
| High error count | Encoding or signal | `portErrShow`; replace SFP |
| Device not logging in | Port state = Offline | `portEnable`; check zoning |

---

## Fabric, Topology & Name Server

The fabric is the collection of all switches connected together. The name server is the fabric's directory — every device that logs into the fabric registers here, so hosts and storage targets can find each other.

### Fabric & Topology

```bash
# Fabric membership — all switches in the fabric
fabricShow

# Physical ISL topology
topologyShow

# Name server — all logged-in devices
nsShow
nsAllShow       # name server across entire fabric

# Domain IDs and routing
routeShow
pathInfo <target_wwn>

# Fabric events
fabricLog --show
```

### ISLs & Trunks

```bash
# ISL (Inter-Switch Link) status — links between switches
islShow

# Trunk status (multiple ISLs bonded together)
trunkShow
portTrunkArea --show

# Trunk debug
trunkDebug <port>
```

### Name Server & FLOGI

FLOGI (Fabric Login) is the process a device uses to join the fabric. If a device's WWN is missing from `nsShow`, it has not successfully logged in.

```bash
# Name server
nsShow
nsAllShow
nsLookup <wwn>

# FLOGI / login database
portLoginShow
```

---

## Zoning

Zoning is the most important security and segmentation feature in a SAN. A zone defines which devices can see each other. Without zoning, all devices in a fabric can talk to all other devices — a major security and stability risk.

```bash
# View current zones, config, and aliases
zoneShow
cfgShow
aliShow

# Create alias (human-readable name for a WWN)
alicreate "<alias_name>","<wwn>"
aliadd "<alias_name>","<wwn>"

# Create a zone (typically one initiator + one or more targets)
zonecreate "<zone_name>","<alias1>;<alias2>"
zoneadd "<zone_name>","<alias>"

# Zone configuration (a named set of zones to activate together)
cfgcreate "<cfg_name>","<zone1>;<zone2>"
cfgadd "<cfg_name>","<zone_name>"
cfgremove "<cfg_name>","<zone_name>"

# Activate a zone config (makes zoning live — disrupts traffic in changed zones)
cfgenable "<cfg_name>"

# Save zone config to persistent storage (required — otherwise lost on reboot)
cfgsave

# Deactivate all zoning (emergency only — all devices see each other)
cfgdisable

# Abort uncommitted zone transaction
cfgtransabort

# Peer zones (allows multiple initiators to share a zone without seeing each other)
zonecreate --peerzone "<zone_name>" -principal "<wwn>" -members "<wwn1>;<wwn2>"
```

> **Always run `cfgsave` after `cfgenable`** — without saving, the active config is lost if the switch reboots.

---

## Diagnostics & Health

These tools help you troubleshoot problems and collect data for support cases. MAPS provides automated alerting when thresholds are breached.

### Switch Health Summary

```bash
switchStatusShow       # overall health: HEALTHY / MARGINAL / DOWN
supportShow            # full diagnostic dump (used when opening support cases)
supportSave            # save diagnostics bundle to FTP/SCP for TAC
```

### Event Log

```bash
errShow                # show all error log entries
errDump                # dump full error log
errClear               # clear error log (use with caution)
```

### Port Diagnostics

```bash
# Run a port loopback test (port must be offline)
portTest <slot/port>

# Spin fabric test (inter-switch frame forwarding)
spinFab <slot/port>

# View port event history
portLogShow <slot/port>
portLogClear <slot/port>
```

### MAPS (Monitoring and Alerting Policy Suite)

MAPS provides threshold-based alerting for fabric health events:

```bash
# Show MAPS policy status
mapsPolicy --show

# Show MAPS alerts
mapsDb --show

# Show current dashboard (health summary)
mapsDashboard --show
```

### Fabric Diagnostics

```bash
fabricShow             # all switches in fabric, domain IDs, state
nsShow                 # name server — all logged-in devices
nsAllShow              # name server across entire fabric
topologyShow           # ISL topology and domain connections
```

### Buffer Credit Diagnostics

```bash
portBufShow <slot/port>     # buffer-to-buffer credits
```

Low BB credits cause I/O delays. Check during performance issues.

### Common Issues

| Issue | Check | Action |
|---|---|---|
| Switch status MARGINAL | `errShow` | Investigate hardware errors |
| Port diagnostics fail | Port offline | Disable port before running `portTest` |
| MAPS alert firing | `mapsDb --show` | Investigate threshold breach |

---

## Firmware, Upgrades & Config Backup

Keep Fabric OS up to date for security patches and new features. Configuration backup is essential — run it before any significant change or maintenance window.

### Firmware & Upgrades

```bash
# Current firmware
version
firmwareShow

# Firmware upgrade (download from server)
firmwareDownload -s <server_ip> -p <path/firmware.bin>

# Monitor upgrade progress
firmwareDownloadStatus

# HA (High Availability) status before upgrade
haShow

# Force CP failover (test HA or force standby CP to become active)
haFailover
```

### Configuration Backup

```bash
# Upload (backup) config to a server
configUpload -all -host <server_ip> -u <user> -f <backup_file>

# Download (restore) config from a server
configDownload -all -host <server_ip> -u <user> -f <backup_file>

# Show running config
configShow
```

---

## Security & Users

User accounts and authentication settings. Brocade supports local accounts, RADIUS, and TACACS+ for centralized authentication. Use RADIUS/TACACS+ in enterprise environments to enforce consistent access controls.

### User Accounts

```bash
# List all user accounts
userConfig --show

# Change a user's password
passwd <username>

# Create a user
userConfig --add <username> -r <role> -l <chassis|switch>

# Delete a user
userConfig --delete <username>

# List available roles
roleConfig --show
```

### Built-in Roles

| Role | Permissions |
|---|---|
| admin | Full access |
| switchadmin | Switch-level operations |
| zoneadmin | Zone management only |
| fabricadmin | Fabric-wide read/write |
| operator | Read-only + basic operations |
| user | Read-only |

### Authentication (RADIUS / TACACS+)

```bash
# Show AAA configuration
aaaConfig --show
authUtil --show

# Configure RADIUS
aaaConfig --add <server_ip> -p <port> -s <secret> -t radius

# Configure TACACS+
aaaConfig --add <server_ip> -p <port> -s <secret> -t tacacs+
```

### Secure Fabric OS Policies

```bash
secPolicyShow
secPolicyShow "SCC_POLICY"    # Switch Connection Control — which switches can join fabric
secPolicyShow "DCC_POLICY"    # Device Connection Control — which WWNs can log in
```

### SSH Configuration

```bash
sshUtil --show
sshUtil --genkey -t rsa
```

---

## Virtual Fabrics (VF)

Virtual Fabrics partition a physical Brocade chassis into multiple logical switches (Logical Switches), each with its own Fabric ID (FID). This lets one physical chassis appear as multiple independent SAN switches.

```bash
# List all logical switches and their FIDs
lscfg --show

# Switch CLI context to a specific logical switch
setContext <fid>

# Create a logical switch
lscfg --create <fid> [-base]    # -base creates a base fabric

# Delete a logical switch
lscfg --delete <fid>

# Assign a port to a logical switch
lscfg --config <fid> -port <slot/port>

# Check port assignments per slot
lscfg --show -slot <slot>
```

### Context Switching

```bash
setContext <fid>       # enter the context of logical switch <fid>
# All subsequent commands run in context of that FID
setContext 128         # 128 = default/base fabric
```

### Common VF Issues

| Issue | Check | Action |
|---|---|---|
| Device not visible | Wrong FID context | `setContext <fid>` then `switchshow` |
| Port in wrong FID | `lscfg --show` | Reassign port to correct FID |
| VF not enabled | License | Verify VF license with `licenseShow` |
```
