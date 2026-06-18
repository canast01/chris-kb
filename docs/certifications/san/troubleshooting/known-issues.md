---
tags:
  - troubleshooting
  - san
  - certifications
  - known-issues
---
# SAN Certifications — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known issues related to SAN certification exam preparation — covering common exam topic misunderstandings, lab environment issues, and practice test discrepancies.

*Applies to: Brocade BCFP, Cisco CCNP Data Center (SAN track), CompTIA Storage+*
</div>

```text
┌───────────────────────────────────────── SAN Certifications ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Exam prep reference — Brocade BCFP, Cisco CCNP DC (SAN), CompTIA Storage+           │   │
│   │                         Protocols (exam topics): FC-SW · FCoE · iSCSI                         │   │
│   │               Resources: Brocade vFOS lab / Cisco dCloud / official study guides              │   │
│   │            Study guide -> Lab practice -> Practice exam -> Official exam -> Renewal           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Topic            │  │           Resource          │  │            Notes            │   │
│   │         Brocade BCFP        │  │     vFOS virtual switch     │  │     Zoning, fabric admin    │   │
│   │        Cisco CCNP DC        │  │       dCloud MDS/DCNM       │  │      VSAN, IVR, zoning      │   │
│   │           Storage+          │  │      CompTIA self-study     │  │    Vendor-neutral basics    │   │
│   │          Lab access         │  │     vFOS / GNS3 / dCloud    │  │       No FC HW needed       │   │
│   │          Validation         │  │        Practice exams       │  │  Cross-check official docs  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   Brocade vFOS   │Practice fabric OS│        N/A        │    Free trial    │   30-day reset   │   │
│   │   Cisco dCloud   │ Hosted MDS/DCNM  │       HTTPS       │  Cisco account   │Scheduled sessions│   │
│   │  Official guide  │  Exam blueprint  │        N/A        │     Purchase     │Trust official src│   │
│   │  Practice exam   │ Self-assessment  │        N/A        │  Purchase/free   │Verify vs official│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: N/A — virtual labs and hosted vendor lab environments only                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  BCFP           = Brocade Certified Fabric Professional; core Brocade SAN cert                        │
│  CCNP DC        = Cisco Certified Network Professional, Data Center track                             │
│  Storage+       = CompTIA vendor-neutral storage fundamentals certification                           │
│  FC-SW          = native Fibre Channel switching protocol (distinct from FCoE)                        │
│  FCoE           = Fibre Channel over Ethernet; encapsulates FC frames in Ethernet                     │
│  vFOS           = virtual Fabric OS; Brocade OVA for lab practice without hardware                    │
│  dCloud         = Cisco free hosted lab environment for DCNM/MDS/ACI practice                         │
│  Zoning         = SAN access control restricting which initiators see which targets                   │
│  IVR            = Inter-VSAN Routing; Cisco feature for controlled cross-VSAN traffic                 │
│  VSAN (Cisco)   = logical fabric partition on one switch (not VMware vSAN)                            │
│  Zoneset        = the active collection of zones enforced on a fabric                                 │
│  cfgsave        = Brocade command persisting config changes across reboots                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- SAN certification labs require access to physical or virtual FC switch environments — GNS3 / EVE-NG do not emulate FC.
- Practice exams vary widely in quality — cross-reference with official study guides for discrepancies.

## Lab Environment Issues

| Issue | Cause | Workaround |
|---|---|---|
| Brocade Virtual Fabric OS trial expired | 30-day trial license | Use Brocade vFOS OVA; register for free trial reset; or use GNS3 community images |
| Cannot access Cisco DCNM in lab | DCNM licensing required for full features | Use Cisco dCloud for free lab access to DCNM |
| Zoning changes not persisting in practice lab | Lab environment resetting between sessions | Save configuration: `cfgsave` (Brocade) or `copy running-config startup-config` (Cisco MDS) |

## Exam Preparation

| Issue | Cause | Workaround |
|---|---|---|
| Practice exam question contradicts official guide | Third-party practice exam outdated or incorrect | Trust official Brocade/Cisco documentation; verify via official study guides |
| FC protocol questions mixing FC-SW and FCoE | FCoE is a separate protocol — exam questions distinguish them | Review FC-SW (native FC) vs FCoE (FC over Ethernet) as separate topics |

## See also

- [SAN — Common Issues](index.md)
- [Brocade Fabric OS — Known Issues](../../../san/brocade/fabric-os/troubleshooting/known-issues.md)
- [Cisco MDS — Known Issues](../../../san/cisco/mds/troubleshooting/known-issues.md)
