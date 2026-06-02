# FabricOS — Escalation


<div class="kb-summary">
> Part of the [Troubleshooting](../index.md) reference.
</div>

---

## Opening a Support Case

Support portal: [support.broadcom.com](https://support.broadcom.com)

1. Log in with the team account
2. Create Service Request → select Brocade SAN Switching as the product area
3. Enter the switch serial number to link the SR to the support contract
4. Upload the `supportsave` bundle (see below) immediately — dramatically speeds up triage

---

## Collecting supportsave (Diagnostic Bundle)

Run `supportsave` on the affected switch before opening the case:

```bash
# Configure FTP/SCP target first (if not already set)
ssave --ftp <ftp-server-ip> <username> <password> <path>
# Or SCP:
ssave --scp <username>@<scp-server-ip>:<path>

# Run supportsave (takes 2–5 minutes)
supportsave

# The output archive includes:
# - Running configuration
# - All logs (raslog, auditlog, switch event log)
# - Fabric database (zone, device, routing)
# - Port statistics
# - SNMP trap history
```
```
┌─────────────────────────── Brocade Fabric OS — Troubleshooting Escalation ────────────────────────────┐
│                                                                                                       │
│  Escalation path: internal SAN team → Broadcom TAC with supportshow bundle and timeline.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Internal Escalation              │  │           Broadcom TAC Escalation           │   │
│   │        SAN L1 → SAN L2: logs+timeline        │  │         Open case: support.broadcom         │   │
│   │       SAN L2 → L3: supportsave bundle        │  │         Serial/contract number req.         │   │
│   │           L3 → TAC: full diag data           │  │          Sev-1: fabric down in prod         │   │
│   │          Incident manager for Sev-1          │  │          Remote: TAC SSH to switch          │   │
│   │        Change freeze during incident         │  │          Escalation to engineering          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Collect supportsave from all affected switches before engaging Broadcom TAC.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Escalation Data Package            │  │             Escalation Criteria             │   │
│   │         supportsave from each switch         │  │          Sev-1: fabric/storage down         │   │
│   │         Fabric topology: fabricshow          │  │          Sev-2: degraded production         │   │
│   │         Zone config: cfgshow output          │  │          Sev-3: non-critical issue          │   │
│   │         Error timeline from errshow          │  │           Sev-4: general question           │   │
│   │        Recent changes before failure         │  │          Post-incident: RCA request         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Brocade FC switch · management Ethernet · serial console · Broadcom TAC upload portal                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  supportsave     = saves full diagnostic bundle to SCP/FTP/USB; required for TAC                      │
│  errshow         = error log snapshot; provides timeline of events before failure                     │
│  fabricshow      = fabric topology; shows all domain IDs and switch names                             │
│  cfgshow         = zone config snapshot; shows active and saved zone databases                        │
│  Sev-1           = production down; fabric or storage completely inaccessible                         │
│  RCA             = Root Cause Analysis; post-incident document requested from TAC                     │
│  Broadcom TAC    = Technical Assistance Center; opened at support.broadcom.com                        │
│  Incident manager= internal role; coordinates bridge call and vendor TAC engagement                   │
│  Serial number   = switch chassis serial; required to open Broadcom support case                      │
│  Change freeze   = no config changes during active Sev-1 incident investigation                       │
│  Remote access   = TAC engineer SSH into switch via customer-granted access                           │
│  Post-incident   = RCA + preventive actions + monitoring improvements after resolution                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
