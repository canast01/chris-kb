---
tags:
  - operations
  - san
---
# FabricOS — Procedures


<div class="kb-summary">
FabricOS procedures: `switchshow`, `fabricshow`, zone configuration with `cfgadd`/`cfgsave`/`cfgenable`, ISL management, and port enable/disable.

*Applies to: Brocade FOS 9.x*
</div>

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

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


### Create Aliases

![Create Aliases](../../../../assets/fabric-os-proc-create-aliases.svg)

```bash
# Host HBA
alicreate "esxi01_hba0", "10:00:00:00:c9:ab:cd:ef"

# Array port
alicreate "fa01_ct0_p0", "52:4a:93:7c:00:00:00:01"
alicreate "fa01_ct0_p1", "52:4a:93:7c:00:00:00:02"
```

### Create and Manage Zones

![Create and Manage Zones](../../../../assets/fabric-os-proc-create-and-manage-zones.svg)

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

![Zone Set Management](../../../../assets/fabric-os-proc-zone-set-management.svg)

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

![Example: Zone a New Host to FlashArray](../../../../assets/fabric-os-proc-example-zone-a-new-host-to-flasharray.svg)

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

![Zone Audit](../../../../assets/fabric-os-proc-zone-audit.svg)

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

![Zoning Troubleshooting](../../../../assets/fabric-os-proc-zoning-troubleshooting.svg)

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

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Fabric Os — Health Checks](health-checks/)
- [Fabric Os — CLI Reference](cli-reference/)
- [Fabric Os — Common Issues](../troubleshooting/common-issues/)
