# FabricOS — Operations


<div class="kb-summary">
FabricOS — Operations reference.
</div>

```
┌──────────────────────────────────────── FabricOS — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Day-to-day FabricOS operational tasks via CLI and SANnav — health, zones, maintenance     │   │
│   │       Health: switchshow, fabricshow, portshow, errshow, sfpshow — run daily or on alert      │   │
│   │          Zone management: zonecreate, aliadd, zoneadd, cfgenable — change-controlled          │   │
│   │         Maintenance: firmwaredownload, configupload, configbackup, supportshow for TAC        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily health checks → change-controlled zone ops → scheduled maintenance tasks                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Health Commands       │  │        Zone Commands        │  │         Maintenance         │   │
│   │          switchshow         │  │          zonecreate         │  │       firmwaredownload      │   │
│   │          fabricshow         │  │            aliadd           │  │         configupload        │   │
│   │           portshow          │  │           zoneadd           │  │         configbackup        │   │
│   │           errshow           │  │           cfgsave           │  │         supportshow         │   │
│   │           sfpshow           │  │          cfgenable          │  │         portdisable         │   │
│   │         portperfshow        │  │           zoneshow          │  │         portlogdump         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All zone changes require change ticket; cfgenable pushes config to all fabric switches             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Command      │     Purpose      │  Output key field │    Frequency     │      Notes       │   │
│   │    switchshow    │  Switch health   │   State: Online   │      Daily       │ All ports green  │   │
│   │     errshow      │  Error counters  │  CRC, LOS, LOSync │      Daily       │   Zero = clean   │   │
│   │    cfgenable     │ Zone activation  │    Config name    │    Per change    │  Change ticket   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Brocade G630/G720/G730 switches · FC SFP optics · ISL cables                             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    switchshow     = Summary of all FC ports; state, speed, WWN, connected device                      │
│    fabricshow     = List of all switches in the fabric; WWN, domain ID, IP address                    │
│    portshow       = Detailed status of a single port including error counters                         │
│    errshow        = Error counter summary for all ports; CRC/LOS/LOSync per port                      │
│    sfpshow        = SFP transceiver diagnostics; Tx/Rx dBm, temperature, voltage                      │
│    portperfshow   = Real-time port throughput in MB/s; run during I/O for baseline                    │
│    zonecreate     = Create a new zone by name: zonecreate "zone_name", "alias1;alias2"                │
│    aliadd         = Add WWN members to an alias: aliadd "alias_name", "50:01:..."                     │
│    cfgenable      = Activates the named zone configuration across all fabric switches                 │
│    firmwaredownload = Downloads and installs FabricOS from a TFTP/FTP/SCP server                      │
│    configupload   = Upload running config to a remote server for backup                               │
│    supportshow    = Full diagnostic dump for TAC; combines 50+ show commands                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────────── FabricOS — Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Day-to-day FabricOS operational tasks via CLI and SANnav — health, zones, maintenance     │   │
│   │       Health: switchshow, fabricshow, portshow, errshow, sfpshow — run daily or on alert      │   │
│   │          Zone management: zonecreate, aliadd, zoneadd, cfgenable — change-controlled          │   │
│   │         Maintenance: firmwaredownload, configupload, configbackup, supportshow for TAC        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily health checks → change-controlled zone ops → scheduled maintenance tasks                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Health Commands       │  │        Zone Commands        │  │         Maintenance         │   │
│   │          switchshow         │  │          zonecreate         │  │       firmwaredownload      │   │
│   │          fabricshow         │  │            aliadd           │  │         configupload        │   │
│   │           portshow          │  │           zoneadd           │  │         configbackup        │   │
│   │           errshow           │  │           cfgsave           │  │         supportshow         │   │
│   │           sfpshow           │  │          cfgenable          │  │         portdisable         │   │
│   │         portperfshow        │  │           zoneshow          │  │         portlogdump         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All zone changes require change ticket; cfgenable pushes config to all fabric switches             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Command      │     Purpose      │  Output key field │    Frequency     │      Notes       │   │
│   │    switchshow    │  Switch health   │   State: Online   │      Daily       │ All ports green  │   │
│   │     errshow      │  Error counters  │  CRC, LOS, LOSync │      Daily       │   Zero = clean   │   │
│   │    cfgenable     │ Zone activation  │    Config name    │    Per change    │  Change ticket   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Brocade G630/G720/G730 switches · FC SFP optics · ISL cables                             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    switchshow     = Summary of all FC ports; state, speed, WWN, connected device                      │
│    fabricshow     = List of all switches in the fabric; WWN, domain ID, IP address                    │
│    portshow       = Detailed status of a single port including error counters                         │
│    errshow        = Error counter summary for all ports; CRC/LOS/LOSync per port                      │
│    sfpshow        = SFP transceiver diagnostics; Tx/Rx dBm, temperature, voltage                      │
│    portperfshow   = Real-time port throughput in MB/s; run during I/O for baseline                    │
│    zonecreate     = Create a new zone by name: zonecreate "zone_name", "alias1;alias2"                │
│    aliadd         = Add WWN members to an alias: aliadd "alias_name", "50:01:..."                     │
│    cfgenable      = Activates the named zone configuration across all fabric switches                 │
│    firmwaredownload = Downloads and installs FabricOS from a TFTP/FTP/SCP server                      │
│    configupload   = Upload running config to a remote server for backup                               │
│    supportshow    = Full diagnostic dump for TAC; combines 50+ show commands                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Brocade Fabric OS](../index.md) reference.
