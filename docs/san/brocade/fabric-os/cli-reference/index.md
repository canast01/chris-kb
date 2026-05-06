# Brocade Fabric OS CLI Reference

Commonly used Brocade FOS commands for managing Fibre Channel SAN switches.

---

## Switch Status & Identity

```bash
# Switch overview
switchshow
switchstatusshow
version
ipAddrShow
licenseShow
chassisShow
slotShow

# Fan, power, temperature
psShow
fanShow
tempShow
sensorShow
```

---

## Ports

```bash
# Port status
portShow <slot/port>
portStatsShow <slot/port>
portErrShow
portLogShow <slot/port>
portLogDump
portCfgShow <slot/port>

# Port admin
portDisable <slot/port>
portEnable <slot/port>
portCfgSpeed <slot/port> <speed>    # 0=auto, 4, 8, 16, 32
portCfgLongDistance <slot/port> <mode>

# Port stats reset
portStatsReset <slot/port>
```

---

## Fabric & Topology

```bash
# Fabric membership
fabricShow
topologyShow
nsShow
nsAllShow

# Domain IDs and routing
lsanZoneShow
routeShow
pathInfo <target_wwn>

# Fabric events
fabricLog --show
```

---

## Zoning

```bash
# View zones
zoneShow
cfgShow
aliShow

# Create alias
alicreate "<alias_name>","<wwn>"
aliadd "<alias_name>","<wwn>"

# Create zone
zonecreate "<zone_name>","<alias1>;<alias2>"
zoneadd "<zone_name>","<alias>"

# Zone config
cfgcreate "<cfg_name>","<zone1>;<zone2>"
cfgadd "<cfg_name>","<zone_name>"
cfgremove "<cfg_name>","<zone_name>"

# Activate / save
cfgenable "<cfg_name>"
cfgsave
cfgdisable

# Transactional save (abort if issues)
cfgtransabort

# Peer zones
zonecreate --peerzone "<zone_name>" -principal "<wwn>" -members "<wwn1>;<wwn2>"
```

---

## ISLs & Trunks

```bash
# ISL and trunk status
islShow
trunkShow
portTrunkArea --show

# Trunk debug
trunkDebug <port>
```

---

## Name Server & FLOGI

```bash
# Name server
nsShow
nsAllShow
nsLookup <wwn>

# FLOGI / login database
portLoginShow
```

---

## Diagnostics & Health

```bash
# Switch health check
switchStatusShow
supportShow        # Full diagnostic dump
supportSave        # Save diagnostics to file

# Port diagnostics
portTest <slot/port>
spinFab --help

# Error isolation
errShow
errClear
errDump

# Link reset
portLogClear <slot/port>
```

---

## Firmware & Upgrades

```bash
# Current firmware
version
firmwareShow

# Firmware upgrade
firmwareDownload -s <server_ip> -p <path/firmware.bin>
firmwareDownloadStatus

# Boot check
haShow          # Check HA / CP status
haFailover      # Force CP failover
```

---

## Security & Users

```bash
# User accounts
userConfig --show
passwd <username>

# Roles
roleConfig --show

# Auth / RADIUS
aaaConfig --show
authUtil --show
```

---

## Configuration Backup

```bash
# Save / backup
configUpload -all -host <server_ip> -u <user> -f <backup_file>
configDownload -all -host <server_ip> -u <user> -f <backup_file>

# Show saved config
configShow

# Factory reset (destructive)
# configDefault
```

---

## VF / Logical Switches

```bash
# Virtual Fabrics
lscfg --show
lscfg --create <fid>
lscfg --delete <fid>
setContext <fid>

# XISL (inter-switch links between VFs)
lscfg --port <slot/port> -lport <fid>
```
