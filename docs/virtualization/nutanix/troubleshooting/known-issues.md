---
tags:
  - troubleshooting
  - nutanix
  - known-issues
---
# Nutanix — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Nutanix AOS / AHV bugs, error codes, and workarounds covering CVM, storage, AHV networking, and Prism issues.

*Applies to: Nutanix AOS 6.x / AHV 20220304.x+*
</div>

```text
┌───────────────────────────────────────────── Nutanix HCI ─────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Hyper-converged infrastructure — compute, storage, and networking on AOS           │   │
│   │             Protocols: iSCSI (internal) · NFS · SMB · REST API · iDRAC/IPMI (IPMI)            │   │
│   │            Management: Prism Element (per-cluster) · Prism Central (multi-cluster)            │   │
│   │                VM I/O -> AHV hypervisor -> CVM DSF -> distributed storage ring                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Storage           │  │          CVM + DSF          │  │        1 CVM per node       │   │
│   │           Compute           │  │        AHV hypervisor       │  │     KVM-based (default)     │   │
│   │           Network           │  │           AHV OVS           │  │     Open vSwitch fabric     │   │
│   │          Management         │  │        Prism Central        │  │      Multi-cluster mgmt     │   │
│   │            Health           │  │          NCC checks         │  │     Cluster health tests    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │       CVM        │Storage controller│    iSCSI / NFS    │     Internal     │Must stay running │   │
│   │       AHV        │    Hypervisor    │      Internal     │       N/A        │ ESXi also works  │   │
│   │  Prism Element   │    Cluster UI    │     HTTPS 9440    │    Local / AD    │ Per-cluster view │   │
│   │       NCC        │  Health checks   │      Internal     │      Admin       │Run after changes │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: Nutanix nodes (NX/OEM) -> CVM ring -> Prism -> management network                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CVM          = Controller VM; Nutanix storage services running on each node                          │
│  DSF          = Distributed Storage Fabric; Nutanix virtual SAN across all CVMs                       │
│  AOS          = Acropolis OS; Nutanix core software stack                                             │
│  AHV          = Acropolis Hypervisor; Nutanix default KVM-based hypervisor                            │
│  NCC          = Nutanix Cluster Check; suite of health tests run via CLI or Prism                     │
│  Prism Element = per-cluster web UI on port 9440; direct cluster management                           │
│  Prism Central = multi-cluster management appliance; policies, compliance, VM mgmt                    │
│  Stargate     = CVM I/O service; handles all VM disk read/write operations                            │
│  Cassandra    = CVM metadata service; distributed ring storing extent map                             │
│  Curator      = background maintenance service; reclaim, rebalance, disk repair                       │
│  RF           = Replication Factor; number of data copies (RF2 or RF3)                                │
│  Expand cluster = adding nodes; must pass NCC before and after expansion                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Run `cluster status` from any CVM to check all services.
- Nutanix NCC (Node Configuration Checker): `ncc health_checks run_all` from any CVM.
- CVM logs under `/home/nutanix/data/logs/` — key log is `stargate.out` for storage issues.

## CVM and Services

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| CVM service `Stargate` in crash loop | AOS 6.x | Disk I/O error on SSD tier causing Stargate panic | Check `disk_operator.out` for SMART errors; replace failing disk | N/A |
| `Zookeeper not running` on single CVM | AOS 6.x | CVM network partition or CVM OOM | Restart CVM; check CVM memory allocation (min 20 GB reserved) | N/A |
| `Cassandra` ring not converging after node addition | AOS 6.x | New node NTP skew from cluster | Sync NTP on new node; run `nodetool status` from CVM to verify ring | N/A |

## Storage

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| VM disk I/O latency spikes during dedup/compression | AOS 6.x | Background data transformation running during peak hours | Schedule data transformation during off-peak via Prism → Data Resiliency | N/A |
| Storage container full but cluster has free capacity | AOS 6.x | Container reservation set too high | Remove or reduce reservation on container; capacity redistributes automatically | N/A |
| vDisk stuck in `Under Replicated` state | AOS 6.x | Node in maintenance mode with insufficient data copies | Exit maintenance mode; or increase replication factor temporarily | N/A |

## AHV Networking

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| VM loses connectivity after AHV host upgrade | AOS 6.x | OVS bridge reconfigured during upgrade; bond mode changed | Verify OVS bond mode matches upstream switch LACP settings post-upgrade | N/A |
| VLAN traffic not passing for guest VMs | AOS 6.x | VLAN not configured on Prism network; upstream trunk missing | Add VLAN in Prism → VM Network; verify upstream switch trunk includes VLAN ID | N/A |

## Prism

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Prism Central login fails: `SSO metadata error` | Prism Central 2022.x | IdP metadata URL unreachable | Verify Prism Central can reach IdP metadata URL on 443; or re-upload metadata manually | N/A |
| Prism alert `Disk I/O timeout` not clearing | AOS 6.x | Historical alert not auto-resolving | Manually resolve alert in Prism → Alerts after confirming disk is healthy | N/A |

## See also

- [Nutanix — Common Issues](common-issues/)
- [Nutanix — Diagnostics](diagnostics.md)
