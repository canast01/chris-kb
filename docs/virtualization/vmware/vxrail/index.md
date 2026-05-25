---
title: VxRail
---

# VxRail

<div class="kb-summary">
Technical and operational reference for Dell VxRail. Covers VxRail Manager, HCI node management, lifecycle upgrades, vSAN integration, hardware health, and troubleshooting for VxRail clusters managed within VMware vSphere environments.
</div>

```text
┌─────────────────────────── VxRail Stack ────────────────────────────────────────┐
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                        vCenter Server                                   │    │
│  │          (VxRail Plugin ► Cluster │ Hosts │ LCM │ Support)              │    │
│  └───────────────────────────┬─────────────────────────────────────────────┘    │
│                               │ manages                                          │
│  ┌───────────────────────────▼─────────────────────────────────────────────┐    │
│  │                     VxRail Manager VM                                   │    │
│  │          (Lifecycle │ Node Config │ REST API │ SupportAssist)           │    │
│  └──┬────────────────────────────────────────────────────────────┬─────────┘    │
│     │ configures / upgrades                                       │ monitors     │
│  ┌──▼─────────────────────────────────────────────────────────┐  │              │
│  │                  VxRail HCI Nodes                          │  │              │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │  │               │
│  │  │  Node-01     │  │  Node-02     │  │  Node-03 ...  │     │  │              │
│  │  │ ESXi │ iDRAC │  │ ESXi │ iDRAC │  │ ESXi │ iDRAC │     │  │               │
│  │  │  NVMe/SSD    │  │  NVMe/SSD    │  │  NVMe/SSD    │     │  │               │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │  │               │
│  └──────────────────────────┬─────────────────────────────────┘  │              │
│                              │ contributes disks                  │ iDRAC HW     │
│  ┌──────────────────────────▼─────────────────────────────────────▼─────────┐   │
│  │      vSAN Datastore (software-defined storage across all nodes)          │   │
│  │           FTT policy │ RAID-5/6 │ Disk Groups │ Resync                  │    │
│  └──────────────────────────────────────────────────────────────────────────┘   │
│                                        │ NSX transport nodes (optional)          │
└─────────────────────────────────────────────────────────────────────────────────┘
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
