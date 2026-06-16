---
tags:
  - troubleshooting
  - aria-operations-for-networks
  - vmware
  - known-issues
---
# VMware Aria Operations for Networks — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Aria Operations for Networks (vRNI) bugs, error codes, and workarounds covering collector connectivity, data source configuration, and flow analysis.

*Applies to: Aria Operations for Networks 6.x*
</div>

```text
┌───────────────────────────────── VMware Aria Operations for Networks ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Network visibility platform — topology, flow analytics, micro-seg audit            │   │
│   │                Protocols: HTTPS (UI/API) · IPFIX / NetFlow · REST API · SNMP v3               │   │
│   │               Management: Aria Networks web UI · REST API · Slack / email alerts              │   │
│   │              Collector polls NSX/vCenter -> flow data -> topology map -> analysis             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Platform          │  │       Aria Networks VM      │  │        OVA appliance        │   │
│   │          Collection         │  │        Data collector       │  │          Per-DC VM          │   │
│   │             Flow            │  │       IPFIX / NetFlow       │  │        VM-to-VM flows       │   │
│   │           Topology          │  │        NSX + vCenter        │  │      Logical + physical     │   │
│   │          Analytics          │  │       Micro-seg audit       │  │      Policy recommends      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  Aria Networks   │ Central platform │     HTTPS 443     │   vIDM / local   │ OVA + collectors │   │
│   │    Collector     │ Data collection  │    IPFIX / API    │  Service creds   │Relays to platform│   │
│   │    NSX source    │ Flow + topology  │      REST API     │    NSX admin     │ Main data source │   │
│   │    Micro-seg     │  Security audit  │      Internal     │      Admin       │ DFW suggestions  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: collector VMs (per-DC) -> NSX/vCenter APIs -> Aria Networks platform                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Aria Networks = VMware network visibility platform (formerly vRealize Network Insight)               │
│  Collector    = Aria Networks VM per DC that polls NSX/vCenter and forwards data                      │
│  IPFIX        = IP Flow Information Export; standard for VM-to-VM flow telemetry                      │
│  Micro-seg audit = analysis of actual traffic vs NSX DFW policy; finds gaps                           │
│  Topology     = visual map of VMs, logical switches, routers, and physical paths                      │
│  NSX DFW      = Distributed Firewall; security policy analyzed by Aria Networks                       │
│  Security group = NSX object grouping VMs by tag or criteria for policy                               │
│  Flow table   = time-series of src/dst/port/bytes per VM pair                                         │
│  Path query   = Aria Networks trace of how traffic flows from A to B                                  │
│  Data source  = registered vCenter, NSX, or physical switch in Aria Networks                          │
│  Recommendation = Aria-suggested DFW rule based on observed flow patterns                             │
│  Pinned entity = saved object in Aria Networks for quick-access analysis                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- vRNI errors appear in `Settings → Infrastructure and Support → Data Sources`.
- Logs: SSH to Platform node; logs under `/home/ubuntu/log/`.

## Data Sources

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| vCenter data source shows `Auth failed` | vRNI 6.x | vCenter credentials changed or service account locked | Update credentials in vRNI data source settings | N/A |
| NSX-T data source `Connection timeout` | vRNI 6.x | Collector cannot reach NSX Manager on 443 | Verify TCP 443 from Collector to NSX Manager IPs | N/A |
| `SNMP collection failed` for physical switch | vRNI 6.x | SNMP v2c community string mismatch or UDP 161 blocked | Update community string; verify UDP 161 from Collector to switch | N/A |

## Flow Analysis

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| IPFIX flows not appearing from NSX | vRNI 6.x | IPFIX not enabled on NSX logical switches | Enable IPFIX on NSX-T via `Fabric → Profiles → IPFIX Collector Profile` | N/A |
| Flow data missing for specific VMs | vRNI 6.x | VM not in inventory scope of connected vCenter | Ensure VM's vCenter is added as data source; resync inventory | N/A |

## Platform

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Platform UI unreachable` after upgrade | vRNI 6.x | Upgrade script left `nginx` service in failed state | SSH to Platform: `service nginx restart` | N/A |
| Collector shows `Offline` after reboot | vRNI 6.x | Collector appliance NTP drift from Platform | Sync Collector NTP source with Platform; restart Collector registration | N/A |

## See also

- [VMware Aria Operations for Networks — Common Issues](common-issues.md)
- [VMware NSX — Known Issues](../../nsx/troubleshooting/known-issues/)
- [VMware Aria Operations — Known Issues](../../aria-operations/troubleshooting/known-issues/)
