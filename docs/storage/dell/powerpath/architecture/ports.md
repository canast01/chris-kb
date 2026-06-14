---
tags:
  - powerpath
  - dell
  - multipath
  - networking
  - firewall
  - ports
---
# Dell PowerPath — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell PowerPath (multipath I/O software). PowerPath runs on hosts as a kernel driver and transparent to the network layer — no inbound ports are required. The only port concern is the PowerPath Management Appliance (PPMA) if deployed for centralised license management.

*Applies to: PowerPath for Linux / Windows / VMware 6.x*
</div>

## PowerPath (Host Agent — No Inbound Ports)

PowerPath is a multipath driver installed on hosts. It intercepts I/O to SAN targets (FC, iSCSI). It has no network listener — all paths are via existing SAN connectivity:

- **FC paths**: via Fibre Channel fabric (no IP ports)
- **iSCSI paths**: via iSCSI protocol on port 3260 TCP (same as regular iSCSI — no new rules needed beyond existing iSCSI access)

## PowerPath Management Appliance (PPMA) — Optional Centralised Management

If PPMA is deployed for license management and reporting:

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 8443 | TCP | Admin browsers | PPMA web UI |
| 9988 | TCP | PowerPath hosts | PowerPath hosts → PPMA license check and telemetry |

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 9988 | TCP | PowerPath-managed hosts | PPMA appliance | Host-to-PPMA registration and license communication |
| 443 | TCP | PPMA | *.dell.com | PPMA license validation and support |

## Firewall Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Admin browsers | PPMA | 8443 | Only if PPMA is deployed |
| PowerPath hosts | PPMA | 9988 | Only if PPMA is deployed |
| PPMA | *.dell.com | 443 | License validation |

No additional firewall rules are required for PowerPath itself — only for PPMA if deployed.

## See also

- [Dell PowerPath — Architecture](how-it-works/)
- [Dell PowerStore — Ports](../../powerstore/architecture/ports/)
- [NetApp ONTAP — Ports](../../../netapp/ontap/architecture/ports/)
