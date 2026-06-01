---
title: Azure Backup and DR
---

# Azure Backup and DR


<div class="kb-summary">
Backup and recovery notes for Azure Backup, Site Recovery, vaults, jobs, and restore validation.
</div>

```
┌──────────────────────────────────── Azure Backup and DR Overview ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Azure Backup and DR — Recovery Services Vault, Azure Backup, and Azure Site Recovery     │   │
│   │   Azure Backup: VM, SQL, SAP, files, blobs — all via Recovery Services Vault; policy-driven   │   │
│   │  Azure Site Recovery (ASR): continuous replication; orchestrated failover + failback for VMs  │   │
│   │    Recovery Services Vault: central container for backup items and ASR replication configs    │   │
│   │   Restore testing: mandatory for RTO/RPO validation; test failover in isolated network (ASR)  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Backup policies protect data · ASR replicates VMs for DR                                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Azure Backup        │  │      Recovery Svc Vault     │  │     Azure Site Recovery     │   │
│   │      VM: daily + weekly     │  │      GRS: geo-redundant     │  │    Replication: Azure→Az    │   │
│   │     SQL/SAP: log backup     │  │       Soft delete: 14d      │  │       RPO: ~30 seconds      │   │
│   │     Files/blobs: policy     │  │      Immutability: WORM     │  │    Failover: 1-click plan   │   │
│   │     Backup jobs: monitor    │  │     Access policy: RBAC     │  │   Test failover: isolated   │   │
│   │   Restore: disk or full VM  │  │    Reports: backup health   │  │     Failback: re-protect    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Backup protects point-in-time data · Vault stores recovery points · ASR enables DR orchestration   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Azure Backup   │       RSV        │        ASR        │   Restore Test   │    Compliance    │   │
│   │    VM: enable    │   GRS setting    │   Enable repltn   │  Test failover   │  Backup report   │   │
│   │  Policy: daily   │   Soft delete    │    RPO: monitor   │  Validate: app   │ Policy coverage  │   │
│   │   Job: monitor   │   Immutability   │   Failover plan   │   RTO measured   │   Gaps: alert    │   │
│   │   Restore: VM    │    RBAC: ops     │     Re-protect    │   Cleanup test   │   Audit: vault   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure Storage (GRS vaults) · ASR replication infrastructure · paired regions · VM host fabric        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Recovery Services Vault= Azure container for backup items and ASR replication configs; scoped per    │
│  Azure Backup    = Managed backup for VMs, SQL, SAP, files, blobs; policy-driven; encrypted at rest   │
│  Backup Policy   = Defines schedule (daily/weekly) and retention (daily/weekly/monthly/yearly)        │
│  Soft delete     = 14-day recovery window after accidental backup item deletion; default enabled      │
│  Immutability    = WORM policy on vault; prevents deletion of recovery points; compliance requirement │
│  GRS             = Geo-Redundant Storage; vault data replicated to paired region; 6 copies total      │
│  Azure Site Recovery= Continuous replication of VMs to another region; orchestrated failover/failback │
│  RPO             = Recovery Point Objective; ASR achieves ~30s RPO for Azure-to-Azure VM replication  │
│  Test failover   = ASR feature; spins up replica VM in isolated VNet; validates app without affecting │
│  Failback        = Re-protecting and reversing replication direction after a failover test or real    │
│  Recovery plan   = ASR orchestration of failover order, scripts, and timing for multi-VM workloads    │
│  Replication health= ASR metric; monitors churn rate, RPO breach, and agent connectivity on source VM │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────── Azure Backup and DR Overview ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Azure Backup and DR — Recovery Services Vault, Azure Backup, and Azure Site Recovery     │   │
│   │   Azure Backup: VM, SQL, SAP, files, blobs — all via Recovery Services Vault; policy-driven   │   │
│   │  Azure Site Recovery (ASR): continuous replication; orchestrated failover + failback for VMs  │   │
│   │    Recovery Services Vault: central container for backup items and ASR replication configs    │   │
│   │   Restore testing: mandatory for RTO/RPO validation; test failover in isolated network (ASR)  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Backup policies protect data · ASR replicates VMs for DR                                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Azure Backup        │  │      Recovery Svc Vault     │  │     Azure Site Recovery     │   │
│   │      VM: daily + weekly     │  │      GRS: geo-redundant     │  │    Replication: Azure→Az    │   │
│   │     SQL/SAP: log backup     │  │       Soft delete: 14d      │  │       RPO: ~30 seconds      │   │
│   │     Files/blobs: policy     │  │      Immutability: WORM     │  │    Failover: 1-click plan   │   │
│   │     Backup jobs: monitor    │  │     Access policy: RBAC     │  │   Test failover: isolated   │   │
│   │   Restore: disk or full VM  │  │    Reports: backup health   │  │     Failback: re-protect    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Backup protects point-in-time data · Vault stores recovery points · ASR enables DR orchestration   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Azure Backup   │       RSV        │        ASR        │   Restore Test   │    Compliance    │   │
│   │    VM: enable    │   GRS setting    │   Enable repltn   │  Test failover   │  Backup report   │   │
│   │  Policy: daily   │   Soft delete    │    RPO: monitor   │  Validate: app   │ Policy coverage  │   │
│   │   Job: monitor   │   Immutability   │   Failover plan   │   RTO measured   │   Gaps: alert    │   │
│   │   Restore: VM    │    RBAC: ops     │     Re-protect    │   Cleanup test   │   Audit: vault   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure Storage (GRS vaults) · ASR replication infrastructure · paired regions · VM host fabric        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Recovery Services Vault= Azure container for backup items and ASR replication configs; scoped per    │
│  Azure Backup    = Managed backup for VMs, SQL, SAP, files, blobs; policy-driven; encrypted at rest   │
│  Backup Policy   = Defines schedule (daily/weekly) and retention (daily/weekly/monthly/yearly)        │
│  Soft delete     = 14-day recovery window after accidental backup item deletion; default enabled      │
│  Immutability    = WORM policy on vault; prevents deletion of recovery points; compliance requirement │
│  GRS             = Geo-Redundant Storage; vault data replicated to paired region; 6 copies total      │
│  Azure Site Recovery= Continuous replication of VMs to another region; orchestrated failover/failback │
│  RPO             = Recovery Point Objective; ASR achieves ~30s RPO for Azure-to-Azure VM replication  │
│  Test failover   = ASR feature; spins up replica VM in isolated VNet; validates app without affecting │
│  Failback        = Re-protecting and reversing replication direction after a failover test or real    │
│  Recovery plan   = ASR orchestration of failover order, scripts, and timing for multi-VM workloads    │
│  Replication health= ASR metric; monitors churn rate, RPO breach, and agent connectivity on source VM │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="azure-backup/">
  <strong>Azure Backup</strong>
  <span>Azure Backup notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="recovery-services-vault/">
  <strong>Recovery Services Vault</strong>
  <span>Recovery Services Vault notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="backup-jobs/">
  <strong>Backup Jobs</strong>
  <span>Backup Jobs notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="backup-policies/">
  <strong>Backup Policies</strong>
  <span>Backup Policies notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="restore-testing/">
  <strong>Restore Testing</strong>
  <span>Restore Testing notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="azure-site-recovery/">
  <strong>Azure Site Recovery</strong>
  <span>Azure Site Recovery notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="replication-health/">
  <strong>Replication Health</strong>
  <span>Replication Health notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="failover/">
  <strong>Failover</strong>
  <span>Failover notes, checks, commands, troubleshooting, and validation.</span>
</a>

<a class="kb-card" href="failback/">
  <strong>Failback</strong>
  <span>Failback notes, checks, commands, troubleshooting, and validation.</span>
</a>

</div>
