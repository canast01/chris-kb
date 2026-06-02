# Data Domain — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering DDOS Version Matrix, Backup Software Compatibility, Hardware Model Lifecycle, Upgrade Procedure — Single Node (In-Service), Upgrade Procedure — HA Active-Standby Pair (Rolling) and 2 more sections.
</div>

```
┌─────────────────────────────── Dell Data Domain — Install and Upgrade ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Data Domain install: rack and power, initial config via CLI or GUI, license activation    │   │
│   │      Initial setup: set hostname, IPs, NTP, DNS, admin password via serial console or GUI     │   │
│   │       DDOS upgrade: upload upgrade bundle to DD, pre-check, upgrade, verify via sysstat       │   │
│   │  Post-install: register with DDMC, configure DD Boost, enable replication, enroll in CloudIQ  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Rack → power → serial console config → license → network → DD Boost → backup app config            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Initial Install       │  │        Configuration        │  │         DDOS Upgrade        │   │
│   │        Rack and cable       │  │        Hostname / DNS       │  │        Upload bundle        │   │
│   │        Serial console       │  │          NTP config         │  │        Run pre-check        │   │
│   │      License activation     │  │       DD Boost enable       │  │       Execute upgrade       │   │
│   │         Network IPs         │  │      Replication setup      │  │        Verify sysstat       │   │
│   │        Register DDMC        │  │        CloudIQ enroll       │  │       Test backup job       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    DDOS upgrade is non-disruptive for most versions; schedule during maintenance window anyway        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Phase       │       Task       │        Tool       │      Owner       │     Duration     │   │
│   │     Hardware     │  Rack and cable  │      Physical     │     DC team      │    2-4 hours     │   │
│   │  Initial config  │  Console setup   │    Serial / GUI   │   Storage eng.   │    1-2 hours     │   │
│   │   Integration    │Backup app config │    DD GUI + app   │   Storage eng.   │    2-4 hours     │   │
│   │   DDOS upgrade   │  Upload + apply  │    DD GUI / CLI   │   Storage eng.   │    30-60 min     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: dedicated backup LAN for DD Boost; management LAN for GUI/SSH; replication WAN link      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Serial console = First access method; configure via DB-9 RS-232 or USB serial at 9600 baud         │
│    License activation = Apply DD capacity and feature license keys via GUI; tied to chassis SN        │
│    DD Boost enable = Activate DD Boost protocol in GUI; configure backup app with DD Boost user       │
│    Replication setup = Configure source→target replication context; IP, path, schedule, throttle      │
│    DDMC registration = Add new DD to Data Domain Management Center for centralized management         │
│    CloudIQ enroll = Install SCG and register DD to CloudIQ via SCG for health monitoring              │
│    DDOS upgrade   = Data Domain OS upgrade; uploaded as .rpm bundle; upgrade wizard in GUI            │
│    Pre-check      = DDOS upgrade pre-check verifies readiness; abort if any critical warning          │
│    sysstat        = DD CLI command showing system health post-upgrade; verify all services green      │
│    NTP config     = Required for replication timestamp accuracy; use same NTP source as backup app    │
│    Backup LAN     = Dedicated VLAN or network for DD Boost traffic; isolate from production LAN       │
│    Test backup job = Run full backup cycle after install; verify dedup ratio and job completion       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## DDOS Version Matrix

| DDOS Version | Status | Notes |
|---|---|---|
| 7.13.x | Current / Recommended | Latest GA release; required for CloudIQ Gen 2 features |
| 7.12.x | Active support | Widely deployed; compatible with Veeam v12, NetBackup 10.x |
| 7.10.x | Active support | Minimum for DD Boost protocol version 4 |
| 7.7.x | Limited support | Approaching end of support; plan upgrade |
| 6.x and earlier | End of support | No security patches; upgrade required |

Check the current Data Domain Compatibility Guide on [Dell Support](https://www.dell.com/support) for exact compatibility with your backup software versions.

## Backup Software Compatibility

| Backup Software | Supported DD Boost Version | Notes |
|---|---|---|
| Veeam Backup & Replication 12.x | DD Boost 4.x (DDOS 7.10+) | DDVDP protocol; requires DD Boost for Veeam plug-in |
| Veeam 11.x | DD Boost 3.x (DDOS 7.7+) | Legacy plug-in version |
| NetBackup 10.x | DD Boost 4.x | OST plug-in; check NetBackup HCL |
| NetBackup 9.x | DD Boost 3.x | |
| CommVault Simpana / CS 11.28+ | SISL + DD Boost 4.x | DD MediaAgent integration |
| Avamar 19.x | DD Boost 4.x | RAIN dedup integration |
| IBM Spectrum Protect (TSM) | VTL or NFS | No native DD Boost support |

## Hardware Model Lifecycle

| Platform | Status | Notes |
|---|---|---|
| DD9900 | Current | High-end; HA pair option; up to 68 TB/hr ingest |
| DD9400 | Current | Mid-high; up to 34 TB/hr ingest |
| DD6900 | Current | Mid-range; standard for regional DCs |
| DD3300 | Current | Entry/ROBO; integrated 2U appliance |
| DD990 / DD2500 | End of support | Hardware and software support ended |
| DD880 and earlier | End of support | Decommission — no firmware or security updates |

## Upgrade Procedure — Single Node (In-Service)

DDOS minor version upgrades are non-disruptive (no reboot required). Major version upgrades require a controlled reboot.

1. Confirm current DDOS version: `system show`
2. Review the DDOS Release Notes for the target version — check for known issues and prerequisites
3. Download the upgrade package from Dell Support and verify the MD5/SHA256 checksum
4. Confirm all replication contexts are in `Normal` state: `replication show`
5. Confirm filesystem clean is not running: `filesys clean status`
6. Upload the upgrade package via System Manager GUI or: `system upgrade stage file <upgrade-package.rpm>`
7. Initiate the upgrade: `system upgrade apply`
8. Monitor upgrade progress in the System Manager GUI or via the CLI
9. After upgrade, verify: `filesys status`, `replication show`, `alerts show current`
10. Run a test backup and restore from each connected backup application

## Upgrade Procedure — HA Active-Standby Pair (Rolling)

1. Confirm both nodes are healthy and the standby is in `Standby` state
2. Upgrade the **standby** node first using the standard procedure above
3. After standby upgrade completes, initiate a controlled failover to make the upgraded node active
4. Verify all services are healthy on the now-active (upgraded) node
5. Upgrade the original active node (now standby) using the standard procedure
6. Fail back to the original primary if required
7. Confirm both nodes are running the same DDOS version: `system show` on both nodes

## EOL Tracking

| Action | Trigger | Responsible |
|---|---|---|
| Flag for upgrade planning | DDOS version moves to "Limited support" | Storage engineer |
| Initiate hardware refresh project | Hardware model reaches End of Support | Storage architect |
| Decommission array | Replacement array validated and all backup jobs migrated | Storage engineer + Backup team lead |

Track DDOS EOL dates in the team's capacity/lifecycle spreadsheet. Dell publishes EOL notices at least 6 months in advance.

## Refresh Planning

- **Software refresh cadence**: Keep DDOS within two minor versions of the current release. Do not defer DDOS upgrades beyond 18 months.
- **Hardware refresh trigger**: Plan hardware refresh when the platform reaches End of Support or when ingest throughput requirements exceed the current model's rated capacity.
- **Data migration on refresh**: Use MTree replication to seed the replacement array before cutover. Configure backup software to point to the new DD once replication is in sync.
- **Decommission checklist**:
  - [ ] All replication contexts removed from old array
  - [ ] All backup software storage units deregistered from old DD
  - [ ] DD Boost users deleted
  - [ ] SCG registration removed from old DD
  - [ ] Array powered down and deregistered from Dell Support portal
  - [ ] Physical decommission or return to Dell (if leased)
