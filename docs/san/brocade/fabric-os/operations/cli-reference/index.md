```bash
switchshow         # ports, state, speed, and connected WWNs — most useful daily command
switchstatusshow   # overall switch health status (expected: HEALTHY)
version            # Fabric OS version
ipAddrShow         # management IP addresses
licenseShow        # installed licenses
chassisShow        # chassis hardware inventory
slotShow           # blade/slot population
```

```text
┌────────────────────────────────── Brocade Fabric OS — CLI Reference ──────────────────────────────────┐
│                                                                                                       │
│  Fabric OS CLI commands: fabric management, port control, zoning, diagnostics, firmware.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Fabric & Switch Commands           │  │             Port & ISL Commands             │   │
│   │       switchshow: port + fabric state        │  │             portshow <slot/port>            │   │
│   │         fabricshow: fabric topology          │  │            portenable/portdisable           │   │
│   │          nsshow: name server logins          │  │           islshow: ISL utilisation          │   │
│   │       switchstatusshow: overall health       │  │         portcfgspeed: set port speed        │   │
│   │         chassisshow: blade inventory         │  │          portloginshow: login list          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  switchshow is the first command for any Fabric OS health check; nsshow shows device logins.          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Zoning & Security Commands          │  │            Firmware & Diagnostics           │   │
│   │         cfgshow: display zone config         │  │         firmwareshow: version check         │   │
│   │            zonecreate/zonedelete             │  │        firmwaredownload: upgrade FOS        │   │
│   │          cfgsave + cfgenable <cfg>           │  │         porttest: run loopback test         │   │
│   │          secpolicyadd/secpolicydel           │  │         diagstatus: diagnostic state        │   │
│   │           authutil: FCAP / DH-CHAP           │  │        supportshow: full tech bundle        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Brocade FC switch chassis · blades · SFP transceivers · FC host bus adapters                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  switchshow      = primary CLI for port status, fabric domain ID, and zoning state                    │
│  nsshow          = Name Server show; lists all devices logged into fabric on local switch             │
│  fabricshow      = displays fabric principal switch, all domain IDs, and topology                     │
│  cfgshow         = zone config show; lists all zones, aliases, and active config                      │
│  cfgsave         = saves zone database changes to flash; required before cfgenable                    │
│  cfgenable       = activates named zone configuration across the fabric                               │
│  islshow         = Inter-Switch Link show; displays ISL bandwidth utilisation per port                │
│  firmwaredownload= downloads and installs new Fabric OS version via non-disruptive HA                 │
│  supportshow     = generates full diagnostic bundle; upload to Broadcom TAC                           │
│  porttest        = runs loopback diagnostic on a port; requires port offline                          │
│  DH-CHAP         = Diffie-Hellman Challenge Handshake Auth Protocol; FC switch auth                   │
│  FCAP            = Fibre Channel Authentication Protocol; cert-based switch auth                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
psShow      # power supplies
fanShow     # fan status
tempShow    # temperature sensors
sensorShow  # all environmental sensors
```
```bash
uptime
snmpConfig --show
syslogDIPShow    # syslog destinations
```
```bash
switchshow
switchstatusshow
fabricshow
nsShow
aliShow
zoneShow --all
```
```bash
portShow <slot/port>           # detailed port info (state, speed, WWN, connected device)
portStatsShow <slot/port>      # TX/RX frames, errors
portErrShow                    # error summary across all ports
portLogShow <slot/port>        # port event log
portLogDump                    # dump full port log to console
portCfgShow <slot/port>        # port configuration
```
```bash
portDisable <slot/port>
portEnable <slot/port>

# Persistent disable/enable — survives switch reboot
portPersistentDisable <slot/port>
portPersistentEnable <slot/port>
```
```bash
portCfgSpeed <slot/port> <speed>
# speed: 0=auto, 4, 8, 16, 32 (Gbps)
```
```bash
portCfgLongDistance <slot/port> <mode>
# modes: L0 (normal), L1, L2, LE, LD, LS
```
```bash
portStatsShow <slot/port>
portErrShow
portStatsReset <slot/port>    # reset counters after investigation
```
```bash
# Fabric membership — all switches in the fabric
fabricShow

# Physical ISL topology
topologyShow

# Name server — all logged-in devices
nsShow
nsAllShow       # name server across entire fabric

# Domain IDs and routing
lsanZoneShow
routeShow
pathInfo <target_wwn>

# Fabric events
fabricLog --show
```
```bash
# ISL (Inter-Switch Link) status — links between switches
islShow

# Trunk status (multiple ISLs bonded together)
trunkShow
portTrunkArea --show

# Trunk debug
trunkDebug <port>
```
```bash
# Name server
nsShow
nsAllShow
nsLookup <wwn>

# FLOGI / login database
portLoginShow
```
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
```bash
switchStatusShow       # overall health: HEALTHY / MARGINAL / DOWN
supportShow            # full diagnostic dump (used when opening support cases)
supportSave            # save diagnostics bundle to FTP/SCP for TAC
```
```bash
errShow                # show all error log entries
errDump                # dump full error log
errClear               # clear error log (use with caution)
```
```bash
# Run a port loopback test (port must be offline)
portTest <slot/port>

# Spin fabric test (inter-switch frame forwarding)
spinFab <slot/port>

# View port event history
portLogShow <slot/port>
portLogClear <slot/port>
```
```bash
# Show MAPS policy status
mapsPolicy --show

# Show MAPS alerts
mapsDb --show

# Show current dashboard (health summary)
mapsDashboard --show
```
```bash
fabricShow             # all switches in fabric, domain IDs, state
nsShow                 # name server — all logged-in devices
nsAllShow              # name server across entire fabric
topologyShow           # ISL topology and domain connections
```
```bash
sensorShow             # all environmental sensors
tempShow
fanShow
psShow
```
```bash
portBufShow <slot/port>     # buffer-to-buffer credits
```
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
```bash
# Upload (backup) config to a server
configUpload -all -host <server_ip> -u <user> -f <backup_file>

# Download (restore) config from a server
configDownload -all -host <server_ip> -u <user> -f <backup_file>

# Show running config
configShow
```
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
```bash
# Show AAA configuration
aaaConfig --show
authUtil --show

# Configure RADIUS
aaaConfig --add <server_ip> -p <port> -s <secret> -t radius

# Configure TACACS+
aaaConfig --add <server_ip> -p <port> -s <secret> -t tacacs+
```
```bash
secPolicyShow
secPolicyShow "SCC_POLICY"    # Switch Connection Control — which switches can join fabric
secPolicyShow "DCC_POLICY"    # Device Connection Control — which WWNs can log in
```
```bash
sshUtil --show
sshUtil --genkey -t rsa
```
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
```bash
setContext <fid>       # enter the context of logical switch <fid>
# All subsequent commands run in context of that FID
setContext 128         # 128 = default/base fabric
```
```bash
lscfg --port <slot/port> -lport <fid>    # assign port as XISL
```
