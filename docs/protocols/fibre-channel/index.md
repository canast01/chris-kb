# Fibre Channel


<div class="kb-summary">
High-speed serial protocol for Storage Area Network (SAN) connectivity between hosts and storage arrays.
</div>

        FC END-TO-END PATH
```
┌────────┐    ┌─────┐    ┌──────────────┐    ┌─────┐    ┌─────────┐    ┌─────┐
│  Host  │    │ HBA │    │  FC Switch A │    │ ISL │    │FC Switch│    │Array│
│        ├───►│(SFP)├───►│  port  ──────┼───►│─────┼───►│port     ├───►│ LUN │
│        │    │WWPN │    │   (F_port)   │    │     │    │(F_port) │    │     │
└────────┘    └─────┘    └──────────────┘    └─────┘    └─────────┘    └─────┘
```
   FLOGI ──────────────────────►  FC_ID assigned
   PLOGI ──────────────────────────────────────────────────────────►
   PRLI  ──────────────────────────────────────────────────────────►  SCSI session
```xml


<div class="kb-grid kb-grid-1">

<a class="kb-card" href="fabric-login/">
  <strong>Fabric Login</strong>
  <span>Fabric Login notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="paths/">
  <strong>Paths</strong>
  <span>Paths notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostic steps, and resolution guides.</span>
</a>

<a class="kb-card" href="wwns/">
  <strong>Wwns</strong>
  <span>Wwns notes, checks, commands, and references.</span>
</a>

</div>
## Key Concepts

| Concept | Description |
|---|---|
| WWN (World Wide Name) | 64-bit unique identifier for HBAs and storage ports |
| WWPN (Port Name) | WWN of a specific FC port |
| WWNN (Node Name) | WWN of the HBA adapter |
| FLOGI | Fabric Login — HBA registers with the switch |
| FCNS (Name Server) | Switch database mapping WWPN to FC address |
| Zone | Defines which initiators can see which targets |
| VSAN | Virtual SAN — logical fabric isolation on Cisco MDS |
| ISL | Inter-Switch Link — trunk between fabric switches |

## FC Port Speeds

| Speed | Standard |
|---|---|
| 8G | FC8 |
| 16G | FC16 |
| 32G | FC32 |
| 64G | FC64 |

## Health Checks — Cisco MDS

```bash
# Port status
show interface fc brief

# FLOGI database — confirmed logged-in devices
show flogi database

# FC Name Server — host-to-storage mapping
show fcns database

# Active zones
show zoneset active

# Interface error counters
show interface fc1/1 counters errors

# Port utilisation
show interface fc1/1 counters brief
```

## Health Checks — Brocade

```bash
# Switch and port status
switchshow

# Port error counters
porterrshow

# FLOGI entries
nsshow

# Active zoning
cfgshow | head -30
cfgactvshow

# Per-port stats
portshow <port-number>
```

## Zoning Operations

**Cisco MDS — add initiator to zone:**
```bash
conf t
zone name <zone-name> vsan <vsan-id>
  member pwwn <host-wwpn>
  member pwwn <storage-wwpn>
zoneset activate name <zoneset-name> vsan <vsan-id>
```

**Brocade — add member to zone:**
```bash
zoneadd "<zone-name>", "<wwpn>"
cfgsave
cfgenable "<zoneset-name>"
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Host can't see storage | FLOGI, FCNS, zone | Verify FLOGI registered; confirm both WWPNs in same zone |
| High port error counters | `porterrshow` / `counters errors` | Check SFP, cable, speed negotiation; replace SFP if CRC errors persist |
| ISL down | `show interface` / `switchshow` | Check physical cable and SFP on both ends |
| Slow I/O / high latency | Buffer credit | Check `show interface fc <x> counters` for BB_credit_0 (credit starvation) |
| VSAN mismatch | `show vsan` (MDS) | Confirm both switch ports are in the same VSAN |
