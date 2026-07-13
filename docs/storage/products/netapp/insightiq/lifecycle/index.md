---
tags:
  - netapp
description: "InsightIQ Lifecycle reference covering Compatibility Validation, Pre-Upgrade Checklist, Backup, Cluster Registration, Cluster Removal and 1 more sections."
---
# InsightIQ Lifecycle

<div class="kb-summary">
InsightIQ Lifecycle reference covering Compatibility Validation, Pre-Upgrade Checklist, Backup, Cluster Registration, Cluster Removal and 1 more sections.

*Applies to: InsightIQ*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
compatibility_validation: "Compatibility Validation" {shape: rectangle}
preupgrade_checklist: "Pre-Upgrade Checklist" {shape: rectangle}
cluster_registration: "Cluster Registration" {shape: rectangle}
cluster_removal: "Cluster Removal" {shape: rectangle}
eol_tracking: "EOL Tracking" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> compatibility_validation
compatibility_validation -> preupgrade_checklist
preupgrade_checklist -> cluster_registration
cluster_registration -> cluster_removal
cluster_removal -> eol_tracking
eol_tracking -> validate
```

## Compatibility Validation

Before any InsightIQ upgrade, or before upgrading a monitored OneFS cluster, validate compatibility using the [NetApp Interoperability Matrix Tool (IMT)](https://mysupport.netapp.com/matrix).

Search for: **InsightIQ** → confirm supported OneFS versions for the target InsightIQ release.

Key compatibility rules:
- InsightIQ 4.x: supports OneFS 7.2, 8.x, and 9.0–9.2
- InsightIQ 4.1+: required for OneFS 9.3+
- Always check IMT before a cluster OS upgrade — a OneFS upgrade may require an InsightIQ upgrade first

## Pre-Upgrade Checklist

Backup files should be replicated to an external backup target (NAS, S3-compatible, or enterprise backup solution).

## Cluster Registration

Adding a new PowerScale cluster to InsightIQ:

```text
1. InsightIQ web UI > Administration > Clusters > Add Cluster
2. Enter:
   - Cluster management IP (SmartConnect zone or management IP)
   - Username: svc-insightiq (read-only OneFS account)
   - Password: from secrets manager
   - Display name: <site>-pscale-<number>
3. Save — InsightIQ will begin collecting within one poll interval (~5 minutes)
4. Verify the cluster appears on the dashboard with throughput data after 15 minutes
```

## Cluster Removal

```text
1. InsightIQ web UI > Administration > Clusters > [Cluster] > Remove
2. Choose whether to retain historical data (recommended: retain for 30 days post-removal for audit)
3. Update any scheduled reports that referenced the removed cluster
```

## EOL Tracking

InsightIQ EOL dates are published on the [NetApp Support Lifecycle page](https://mysupport.netapp.com/).

- Review EOL status annually
- Plan upgrades to avoid running EOL software in production
- Note: for OneFS 9.5+, evaluate whether native OneFS performance reporting reduces dependency on InsightIQ
