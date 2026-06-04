# FabricOS — Procedures


<div class="kb-summary">
> Part of the [Operations](../index.md) reference.
</div>

---

## Zoning Workflow

```mermaid
flowchart TD
    start([New host to zone]) --> getWWPN["Collect host HBA WWPNs\nnsshow after FLOGI\nor esxcli storage san fc list"]
    getWWPN --> createAlias["alicreate host alias\nalicreate array alias"]
    createAlias --> createZone["zonecreate\n(one zone per HBA port)"]
    createZone --> addCfg["cfgadd to active zone set"]
    addCfg --> preview["zoneshow — review before activate"]
    preview --> cfgEnable["cfgenable zoneset-name\n(live immediately in fabric)"]
    cfgEnable --> cfgSave["cfgsave\n(persist to flash)"]
    cfgSave --> verify["Verify host sees storage\nnszonemember · host-side rescan"]
    verify --> done([Zoning complete])

    style done fill:#15803d,color:#fff
    style start fill:#2563eb,color:#fff
```

```text
┌────────────────────────────── Brocade Fabric OS — Operations Procedures ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Standard FOS operational procedures for day-to-day SAN administration             │   │
│   │            Zone change: create alias -> create zone -> add to zone set -> cfgenable           │   │
│   │      Port management: portdisable/portenable; portcfgpersistentdisable for permanent off      │   │
│   │          Firmware upgrade: firmwaredownload -s; verify with firmwareshow after reboot         │   │
│   │              Config backup: configupload to save switch config to SCP/FTP server              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Pre-checks -> change procedure -> post-checks -> documentation and rollback plan                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Zone Mgmt          │  │          Port Mgmt          │  │          Lifecycle          │   │
│   │          alicreate          │  │         portdisable         │  │       firmwaredownload      │   │
│   │          zonecreate         │  │          portenable         │  │         configupload        │   │
│   │            cfgadd           │  │         portcfgspeed        │  │        configdownload       │   │
│   │          cfgenable          │  │         portcfgmode         │  │         supportshow         │   │
│   │           cfgsave           │  │           portshow          │  │         firmwareshow        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Always cfgsave after cfgenable; changes without cfgsave lost on switch reboot                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Procedure     │   CLI command    │       Impact      │     Rollback     │      Notes       │   │
│   │     Zone add     │    cfgenable     │    Fabric-wide    │  cfgenable old   │   CAB required   │   │
│   │   Port disable   │   portdisable    │     Port only     │    portenable    │    Log first     │   │
│   │    FW upgrade    │ firmwaredownload │   Switch reboot   │  Prior version   │    NDU for HA    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SSH to switch mgmt IP · SCP server for config/firmware files                             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    alicreate      = FOS CLI command to create a WWN alias for a host or storage port                  │
│    zonecreate     = Creates a new zone with specified member aliases or WWNs                          │
│    cfgadd         = Adds a zone to an existing zone configuration                                     │
│    cfgenable      = Activates the named zone configuration across the entire fabric                   │
│    cfgsave        = Saves the zone database to non-volatile memory on all switches                    │
│    portdisable    = Administratively disables an FC port (state: No_Light or D_Port)                  │
│    portcfgspeed   = Sets port speed (auto, 8G, 16G, 32G, 64G)                                         │
│    firmwaredownload = Downloads FOS image from SCP/FTP and reboots switch to activate                 │
│    configupload   = Uploads running switch config to SCP/FTP for backup                               │
│    configdownload = Restores switch config from previously uploaded backup file                       │
│    supportshow    = Collects full diagnostic data bundle for TAC support                              │
│    NDU            = Non-Disruptive Upgrade; HA chassis upgrades one blade at a time                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Create Aliases

```bash
# Host HBA
alicreate "esxi01_hba0", "10:00:00:00:c9:ab:cd:ef"

# Array port
alicreate "fa01_ct0_p0", "52:4a:93:7c:00:00:00:01"
alicreate "fa01_ct0_p1", "52:4a:93:7c:00:00:00:02"
```

### Create and Manage Zones

```bash
# Create zone
zonecreate "esxi01_hba0__fa01_ct0_p0", "esxi01_hba0; fa01_ct0_p0; fa01_ct0_p1"

# Add member to existing zone
zoneadd "esxi01_hba0__fa01_ct0_p0", "fa01_ct0_p2"

# Remove member from zone
zoneremove "esxi01_hba0__fa01_ct0_p0", "fa01_ct0_p2"

# Delete a zone (remove from zone set first)
zonedelete "esxi01_hba0__fa01_ct0_p0"
```

### Zone Set Management

```bash
# Create zone set and add initial members
cfgcreate "dc1-fabA-prod", "esxi01_hba0__fa01_ct0_p0; esxi01_hba1__fa01_ct1_p0"

# Add zone to existing zone set
cfgadd "dc1-fabA-prod", "esxi02_hba0__fa01_ct0_p0"

# Remove zone from zone set
cfgremove "dc1-fabA-prod", "esxi02_hba0__fa01_ct0_p0"

# Activate zone set (live immediately in fabric)
cfgenable "dc1-fabA-prod"

# Save to flash (persists across reboot)
cfgsave
```

### Example: Zone a New Host to FlashArray

```bash
# 1. Create host HBA aliases
alicreate "web01_hba0", "10:00:00:90:fa:12:34:56"
alicreate "web01_hba1", "10:00:00:90:fa:12:34:57"

# 2. Create zones (Fabric A — HBA0 to CT0 ports)
zonecreate "web01_hba0__fa01_ct0_p0", "web01_hba0; fa01_ct0_p0; fa01_ct0_p1"

# 3. Create zones (Fabric B switch — HBA1 to CT1 ports)
zonecreate "web01_hba1__fa01_ct1_p0", "web01_hba1; fa01_ct1_p0; fa01_ct1_p1"

# 4. Add to zone set
cfgadd "dc1-fabA-prod", "web01_hba0__fa01_ct0_p0"

# 5. Activate and save
cfgenable "dc1-fabA-prod"
cfgsave
```

### Zone Audit

```bash
# Show all zones and member count — find zones with > 1 initiator
zoneshow

# Cross-check alias WWNs against physical HBA WWNs
alishow
# Compare with: host: cat /sys/class/fc_host/host*/port_name

# Show what a WWN can talk to
nszonemember "<alias_or_wwn>"
```

### Zoning Troubleshooting

| Symptom | Command | Action |
|---|---|---|
| Host HBA not visible in name server | `nsshow` | Check cable, HBA driver, FLOGI; confirm VSAN membership |
| Host can't see LUNs | `zoneshow "<alias>"` | Confirm zone is in active zone set; check alias WWN |
| Zone set not active | `cfgshow` — no asterisk | Run `cfgenable "<zset>"` then `cfgsave` |
| Two hosts in same zone | `zoneshow` | Split into single-initiator zones immediately |
| Alias WWN is wrong | `alishow` | Delete and recreate alias with correct WWN |
| Change not persisted after reboot | | Run `cfgsave` after every change |

## Add a New Switch to an Existing Fabric

Connect ISL cables → `switchDisable` on new switch → configure domain ID (must be unique in fabric) → set fabric parameters to match existing → `switchEnable` → verify `fabricshow` shows new switch.

```bash
# Disable new switch before connecting to fabric
switchDisable

# Set domain ID (must be unique across the fabric)
configure
# Answer domain ID prompt with a unique value

# Re-enable switch
switchEnable

# Verify new switch appears in fabric
fabricshow
```

## Create a Zone and Zone Configuration

`zonecreate "zone_host01_array01", "10:00:00:00:00:00:00:01; 50:00:00:00:00:00:00:02"` → `cfgadd "cfg_prod", "zone_host01_array01"` → `cfgsave` → `cfgenable "cfg_prod"`.

```bash
zonecreate "zone_host01_array01", "10:00:00:00:00:00:00:01; 50:00:00:00:00:00:00:02"
cfgadd "cfg_prod", "zone_host01_array01"
cfgsave
cfgenable "cfg_prod"
```

## Add a Member to an Existing Zone

`zoneadd "zone_host01_array01", "10:00:00:00:00:00:00:03"` → `cfgsave` → `cfgenable "cfg_prod"`.

```bash
zoneadd "zone_host01_array01", "10:00:00:00:00:00:00:03"
cfgsave
cfgenable "cfg_prod"
```

## Remove a Zone Member

`zoneremove "zone_host01_array01", "10:00:00:00:00:00:00:03"` → `cfgsave` → `cfgenable`.

```bash
zoneremove "zone_host01_array01", "10:00:00:00:00:00:00:03"
cfgsave
cfgenable "cfg_prod"
```

## Replace a Failed SFP

Identify failed port with `portshow <port>` → hot-replace SFP (no switch reboot needed) → verify with `sfpshow <port>`.

```bash
# Identify the failed port
portshow <port>

# Hot-replace SFP (no reboot needed)
# -- Physical replacement --

# Verify new SFP
sfpshow <port>
```

## Replace a Failed Switch (Fabric Resilience)

ISL failover to redundant paths → install replacement switch → restore domain ID and port config from backup → reconnect ISLs → verify fabric.

```bash
# Verify redundant paths are carrying traffic before replacing
fabricshow
portshow

# After replacement: restore config from backup
configdownload -all -P ftp -h <server> -u <user> -f <filename>

# Verify fabric topology is restored
fabricshow
```

## Collect Support Bundle

`supportsave` → saves fabric and switch state to USB or remote FTP — use for TAC cases.

```bash
supportsave
```

## Monitor Port Errors

`porterrshow` — shows CRC errors, LR in/out, link failures per port; investigate any port with non-zero CRC.

```bash
porterrshow
```

## Back Up Switch Configuration

`configupload -all -P ftp -h <server> -u <user> -f <filename>` — saves running configuration for DR.

```bash
configupload -all -P ftp -h <server> -u <user> -f <filename>
```
