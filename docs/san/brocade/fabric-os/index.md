# Brocade Fabric OS

<div class="kb-summary">
Brocade Fabric OS knowledge base covering switch architecture, zoning, ISLs, ports, firmware, CLI references, health checks, scripts, and troubleshooting guides for Fibre Channel SAN environments.
</div>

```text
┌──────────────────────────────────── Brocade Fabric OS — Overview ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Fabric OS (FOS): Brocade switch OS for FC SAN — zoning, routing, management          │   │
│   │           Runs on all Brocade FC switches (G630, G720, G730, X7 director platforms)           │   │
│   │             Core services: FCNS (name server), FCSM, zone management, ISL trunking            │   │
│   │         Management interfaces: CLI (SSH), REST API (FOS 8.2+), SANnav GUI integration         │   │
│   │     Fabric-wide config distribution: zone DB, fabric parameters, principal switch election    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Core OS services -> fabric-level functions -> management and integration layer                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         FC Services         │  │         Fabric Layer        │  │          Management         │   │
│   │       FCNS name server      │  │         Zone DB sync        │  │         CLI via SSH         │   │
│   │      Port login (FLOGI)     │  │         ISL trunking        │  │           REST API          │   │
│   │      FC routing (FSPF)      │  │       Principal switch      │  │          SANnav GUI         │   │
│   │        FCSM security        │  │        Fabric params        │  │         SNMP/syslog         │   │
│   │       RAS/diagnostics       │  │        Domain ID mgmt       │  │          LDAP auth          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Zone changes replicated across fabric; principal switch coordinates domain IDs                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │       Role       │      Protocol     │     Version      │      Notes       │   │
│   │       FCNS       │   Name server    │       FC-GS       │      FOS 6+      │  Per-fabric DB   │   │
│   │       FSPF       │    FC routing    │       FC-SW       │      FOS 6+      │ Least-cost path  │   │
│   │     REST API     │  Mgmt interface  │       HTTPS       │     FOS 8.2+     │     JSON/XML     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Brocade G630/G720/G730 switches · X7-8/X7-4 directors · FC SFP optics · ISL cables       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Fabric OS      = Brocade proprietary OS running on all Brocade FC switch hardware                  │
│    FCNS           = Fibre Channel Name Server; maps WWN to N_Port ID within the fabric                │
│    FSPF           = Fabric Shortest Path First; FC link-state routing protocol                        │
│    FLOGI          = Fabric Login; HBA registers with fabric and obtains FC address (FCID)             │
│    FCSM           = FC Security Manager; enforces DH-CHAP switch authentication                       │
│    Zone DB        = Fabric-wide zone configuration replicated to all switches in fabric               │
│    ISL trunk      = Multiple ISLs bundled for bandwidth aggregation between switches                  │
│    Principal switch = Elected switch managing domain ID assignments for the fabric                    │
│    Domain ID      = Unique numeric identifier for each switch in the fabric (1-239)                   │
│    REST API       = FOS 8.2+ HTTP management interface; JSON/XML payloads over HTTPS                  │
│    MAPS           = Monitoring and Alerting Policy Suite; FOS threshold alert engine                  │
│    portcfg        = FOS CLI command to configure port speed, mode, and behaviour                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>

## Overview

Brocade Fabric OS (FOS) is the operating system for Brocade/Broadcom Fibre Channel SAN switches and directors. Current generation platforms (G620, G720, G730, X7-4, X7-8) run FOS 9.x and support 32G and 64G FC port speeds. FOS manages the entire fabric — port negotiation, principal switch election, name server, zoning enforcement, ISL trunking, and Virtual Fabrics.

Fabrics are deployed in a **dual-fabric** design. Each server HBA port connects to a separate, independent fabric. Storage arrays present target ports into both fabrics. No traffic is shared between Fabric A and Fabric B — redundancy is achieved by running production I/O across both fabrics simultaneously.

---

## Daily Checks

Run these commands on each switch at the start of every operational shift, or automate them via SANnav scheduled tasks.

| Check | Command | Expected Result |
|---|---|---|
| Review switch health | `switchstatusshow` | `HEALTHY` — any other status requires investigation |
| Check all port states | `switchshow` | All used ports `Online`; no unexpected `Faulty` or `No_Light` |
| Check port error counters | `porterrshow` | Zero or flat counters — any increment on `enc_in`, `loss_sync`, or `link_fail` requires investigation |
| Validate ISLs are up | `islshow` | All ISLs `Online` at expected speed (32G or 64G) |
| Confirm fabric membership | `fabricshow` | All expected switches present; correct principal switch |
| Validate active zone config | `cfgshow \| head -20` | Active zone set name matches expected; no unexpected changes |
| Check error log | `errshow` | No new CRITICAL or ERROR entries since last check |
| Check environmental sensors | `sensorshow` | All sensors `OK` — no temperature, fan, or PSU warnings |

```bash
# Run all daily checks in sequence
switchstatusshow
switchshow
porterrshow
islshow
fabricshow
cfgshow | head -20
errshow
sensorshow
```

---

## Key Commands Reference

| Category | Command | Purpose |
|---|---|---|
| Switch status | `switchshow` | All ports, states, speeds, connected WWNs |
| Switch health | `switchstatusshow` | Overall switch health (HEALTHY/MARGINAL/DOWN) |
| Fabric | `fabricshow` | All switches in fabric, domain IDs, principal |
| ISL | `islshow` | ISL port states and throughput |
| ISL trunks | `trunkshow` | Trunk group membership and status |
| Name server | `nsshow` | All logged-in hosts and storage targets |
| Zoning | `cfgshow` | Full zone database — active config, zones, aliases |
| Errors | `errshow` | Switch error log |
| Port detail | `portshow <port>` | Single-port detail — state, speed, connected WWN |
| Port errors | `porterrshow` | Error counter summary across all ports |
| Diagnostics | `supportshow` | Full diagnostic bundle for TAC cases |
| Firmware | `firmwareshow` | Current and backup firmware versions |
| Config backup | `configupload` | Upload switch config to FTP/SCP server |
| SFP health | `sfpshow` | SFP optical power levels and alarm thresholds |
| Performance | `portperfshow` | Real-time per-port throughput |

---

## Upgrade Workflow

Firmware upgrades are applied one fabric at a time. Fabric B is upgraded first, then Fabric A after validation.

1. Confirm both fabrics are healthy: `switchstatusshow` and `fabricshow` on all switches
2. Back up all switch configurations: `configupload -all scp://<user>@<server>/<path>/<switch>.cfg`
3. Verify HCL compatibility for the target FOS version against all connected HBAs and arrays
4. Stage firmware on the upgrade server — confirm MD5 checksum matches Broadcom release notes
5. Upgrade Fabric B switches (one switch at a time for fixed-form; non-disruptive on directors):
   ```bash
   firmwaredownload -s -b <server_ip> <path/to/fos.bin> <username> <password>
   firmwaredownloadstatus    # monitor until complete
   version                   # confirm new version active
   ```
6. Validate Fabric B is healthy: `switchshow`, `fabricshow`, `islshow`, `porterrshow`
7. Confirm host multipath is balanced across both fabrics before touching Fabric A
8. Repeat steps 5–6 for Fabric A switches
9. Confirm all switches in both fabrics are on the same FOS version: `version`

---

## Zoning — Quick Reference

Zoning is the primary access control mechanism in a Brocade fabric. The preferred model is **single-initiator, WWN-based** zoning using aliases.

```bash
# View current state
cfgshow          # Full database: zone sets, zones, aliases
zoneshow         # Active zone configuration only
alishow          # All defined aliases
nsshow           # All logged-in devices

# Create aliases (human-readable names for WWPNs)
alicreate "esxi01_hba0", "10:00:00:00:c9:12:34:56"
alicreate "pure_ct0_p0", "52:4a:93:7c:00:00:00:01"

# Create zone (one initiator + one or more targets)
zonecreate "esxi01_hba0__pure_ct0_p0", "esxi01_hba0; pure_ct0_p0"

# Add zone to active zone set and activate
cfgadd "dc1-fabA-prod", "esxi01_hba0__pure_ct0_p0"
cfgenable "dc1-fabA-prod"

# Always save after activating — otherwise change is lost on reboot
cfgsave
```

---

## Platform Summary

| Platform | Type | Max FC Ports | FC Speed | Notes |
|---|---|---|---|---|
| G610 | Fixed | 24x | 32G | Entry-level fixed switch |
| G620 | Fixed | 64x | 32G | Mid-range workhorse |
| G720 | Fixed | 64x | 64G | High-performance fixed |
| G730 | Fixed | 64x | 64G | High-performance, latest gen |
| X7-4 | Director | Up to 192 | 32G/64G | 4-slot director — dual CP |
| X7-8 | Director | Up to 384 | 32G/64G | 8-slot director — dual CP |
| SAN256B-7 | Director | Up to 256 | 64G | High-density director |

Directors (X7-4, X7-8, SAN256B-7) support non-disruptive firmware upgrades via dual Control Processors (CPs). Fixed-form switches (G-series) require a reboot to apply firmware — always upgrade one fabric while the other carries traffic.
