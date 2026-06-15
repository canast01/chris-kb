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

```text
┌─────────────────────────────────────────── Dell PowerPath ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                 PowerPath: multipath I/O host software for Dell storage arrays                │   │
│   │                                Protocols: FC · iSCSI · NVMe-oF                                │   │
│   │                    Management: powermt CLI / PowerPath Management Appliance                   │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Driver           │  │        powermt daemon       │  │           OS-level          │   │
│   │            Paths            │  │        Active-active        │  │         ≥4 paths/LUN        │   │
│   │            Policy           │  │        Adaptive/ALUA        │  │        Array-specific       │   │
│   │           Failover          │  │         Auto reroute        │  │          <5 sec RTO         │   │
│   │          Management         │  │           pp_mgmt           │  │         Centralised         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Command      │      Notes       │    Frequency     │   │
│   │ powermt display  │ Show path state  │  powermt display  │   Active/dead    │   Daily check    │   │
│   │  powermt check   │  Refresh paths   │   powermt check   │  After changes   │   Post-zoning    │   │
│   │  powermt config  │  Apply license   │  powermt config l │     Per host     │   Install time   │   │
│   │     pp_mgmt      │ Central monitor  │       Web UI      │     Optional     │    Multi-host    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Host OS (Windows/Linux) · HBA or iSCSI NIC ports · FC/IP switches · Dell arrays          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerPath          = Dell multipath driver; manages multiple I/O paths to storage for HA/performa  │
│    powermt            = CLI utility; powermt display, powermt check, powermt save are core commands   │
│    Pseudo device      = virtual block device created by PowerPath aggregating physical I/O paths      │
│    Path health        = alive or dead status per path; dead paths trigger automatic I/O failover      │
│    Adaptive policy    = load-balancing that distributes I/O across all active paths evenly            │
│    CLARiiON policy    = active/passive policy for older VNX/CLARiiON arrays (one active path)         │
│    ALUA               = Asymmetric Logical Unit Access; array signals preferred vs. non-preferred pa  │
│    Trespass           = LUN ownership movement between SP-A and SP-B on Unity or VNX arrays           │
│    Ghost path         = stale path entry in PowerPath no longer backed by a physical device           │
│    powermt check      = validates all paths and refreshes device table; run after fabric changes      │
│    pp_mgmt            = PowerPath Management Appliance; central monitoring for all PowerPath hosts    │
│    License key        = host-based license required per server; applied via powermt config license    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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
