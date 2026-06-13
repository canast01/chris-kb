---
tags:
  - windows
---
# SQL Server

<div class="kb-summary">
Microsoft SQL Server for Windows Server — Always On AG, failover clustering, backup/restore.

*Applies to: SQL Server 2019 / 2022*
</div>

```text
┌───────────────────────────────────────────── SQL Server ──────────────────────────────────────────────┐
│                                                                                                       │
│   Microsoft SQL Server — relational database engine for Windows Server environments                   │
│   Always On AG provides log-based HA with automatic failover and readable secondary replicas          │
│   SQL Agent, SSIS, SSRS are included components for scheduling, ETL, and reporting                    │
│                                                                                                       │
│   Sections in this guide                                                                              │
│   Architecture: engine components, HA topologies (AG/FCI), design standards, integrations             │
│   Deploy: installation, post-install configuration, tempdb setup, firewall, validation                │
│   Operations: health checks, backup/restore, CLI reference, index maintenance, scripts                │
│   Security: Windows auth vs. mixed mode, logins/roles, TDE, auditing, hardening                       │
│   Troubleshooting: blocking chains, AG issues, log full, diagnostics, escalation                      │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Always On AG   = Availability Group; log shipping-based HA; requires WSFC                           │
│   Buffer Pool    = SQL Server memory cache for data and index pages                                   │
│   SQL Agent      = built-in scheduler; runs backup jobs, index maintenance, and alerts                │
│   TDE            = Transparent Data Encryption; encrypts data files and backups at rest               │
│   DMV            = Dynamic Management View; sys.dm_* views for runtime diagnostics                    │
│   tempdb         = shared system database for temp tables, sort spills, row version store             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">
  <a class="kb-card" href="architecture/">Architecture</a>
  <a class="kb-card" href="deploy/">Deploy</a>
  <a class="kb-card" href="operations/">Operations</a>
  <a class="kb-card" href="security/">Security</a>
  <a class="kb-card" href="troubleshooting/">Troubleshooting</a>
</div>
