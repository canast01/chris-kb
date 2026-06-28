---
tags:
  - learning-path
  - nsx
  - nsx-4
  - vmware
---
# NSX — Learning Path

<div class="kb-summary">
Recommended reading order for NSX (NSX-T / NSX 4.x). Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: NSX-T 3.x · NSX 4.x*
</div>

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef done fill:#15803d,stroke:#166534,color:#fff
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```

## Stage 1 — Architecture

**Goal**: Understand the management/control/data plane split, how Geneve tunnels carry overlay traffic between hosts, and where T0/T1 routers fit.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — NSX Manager cluster (management plane), Central Control Plane (CCP), Local Control Plane (LCP) on each host, N-VDS/VDS7, TEP addressing, and Geneve encapsulation
- [Design Standards](../architecture/design-standards/) — T0 per-rack vs shared T0, T1 service router vs distributed router placement, Edge cluster sizing, and BGP peer design with physical fabric
- [Integrations](../architecture/integrations/) — NSX integration with vCenter for transport node preparation, integration with vSAN for storage policy tagging, and Aria Operations for Networks flow visibility

**Why first**: NSX's three-plane architecture means that a management plane outage (NSX Manager down) does not affect existing data plane traffic — but does prevent any policy changes. Understanding this separation prevents panic responses that make outages worse, and explains why Edge node sizing and BGP design matter so much at deployment time.

---

## Stage 2 — Deployment

**Goal**: Know the transport node preparation sequence, Edge cluster sizing, and BGP neighbour configuration before any traffic flows over the overlay.

**Read**:

- [Deploy](../deploy/) — NSX Manager OVA deployment (3-node cluster), transport zone creation, host transport node preparation via vCenter, Edge node deployment, and T0/T1 router creation sequence
- [Install & Upgrade](../operations/install-upgrade/) — NSX upgrade coordinator workflow, MPA/CCP upgrade order, Edge node rolling upgrade, and compatibility with vSphere and VCF versions

**Why second**: Transport node preparation modifies the ESXi host networking by installing the NSX kernel modules and configuring TEP vmk ports. Doing this in the wrong order, or without validating MTU end-to-end, causes Geneve tunnel failures that take the overlay down for all VMs on the affected host.

---

## Stage 3 — Operations

**Goal**: Monitor tunnel health, DFW rule hit counts, and Edge BGP state as part of daily operations, and know how to modify policies safely.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — start here every shift; run the routine covering NSX Manager cluster health, transport node tunnel state, Edge BGP neighbour status, and DFW rule publish errors
- [CLI Reference](../operations/cli-reference/) — NSX Manager CLI (`get logical-routers`, `get bgp neighbor`), Edge node debug commands, and `net-vdl2` on ESXi hosts for tunnel inspection
- [Procedures](../operations/procedures/) — adding a new transport node, expanding an Edge cluster, modifying T0 BGP peers, and emergency DFW rule bypass for a locked-out application
- [Backup & Restore](../operations/backup-restore/) — NSX Manager file-based backup configuration, SFTP schedule, restore procedure for a failed Manager cluster, and what is not included in the backup
- [Scripts](../operations/scripts/) — API scripts for bulk DFW rule export, transport node health polling, and BGP prefix count monitoring

**Why third**: NSX DFW rules are applied in priority order and a misconfigured rule can black-hole application traffic silently. Understanding rule processing and the default-deny posture before modifying any security policy prevents production outages caused by policy changes.

---

## Stage 4 — Security

**Goal**: Design and enforce microsegmentation with DFW, manage role-based access to NSX Manager, and harden the management cluster.

**Read**:

- [Access Control](../security/access-control/) — NSX RBAC roles (Enterprise Admin, Network Engineer, Security Engineer), vIDM integration for SSO, and the audit role for read-only compliance access
- [Authentication](../security/authentication/) — vIDM/Workspace ONE integration for NSX Manager authentication, local admin account management, and certificate replacement for NSX Manager nodes
- [Encryption](../security/encryption/) — TLS enforcement between NSX components, IPsec for T0 VPN services, and encrypting management traffic between NSX Manager and Edge nodes
- [Hardening](../security/hardening/) — disabling default admin via vIDM, API rate limiting, audit log export to syslog, and minimising NSX Manager external attack surface

**Why fourth**: DFW microsegmentation policy is the most consequential security control in the environment. Designing it correctly requires knowing the application traffic flows first (from operations) before attempting to restrict them. Applying DFW rules without this knowledge is the most common cause of application-level outages in NSX environments.

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose broken overlay connectivity, DFW rules blocking legitimate traffic, Edge node BGP flaps, and transport node preparation failures.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — Geneve tunnel down between hosts, DFW rule unintentionally blocking application traffic, T0 BGP peer flapping, and transport node preparation stuck or failed
- [Diagnostics](../troubleshooting/diagnostics/) — Traceflow for overlay path testing, `get logical-router` on Edge CLI, `net-vdl2 -l` on ESXi hosts, and NSX Manager central CLI for cross-node queries
- [Escalation](../troubleshooting/escalation/) — NSX support bundle collection (Manager + Edge + host), required BGP and DFW rule exports before opening a GSS case, and physical network team coordination checklist

**Why last**: Troubleshooting makes most sense once you know the normal operating state.

---

## See also

- [NSX — Deploy](../deploy/)
- [NSX — Procedures](../operations/procedures/)
- [NSX — Common Issues](../troubleshooting/common-issues/)
