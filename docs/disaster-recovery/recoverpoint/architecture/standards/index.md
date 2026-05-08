# RecoverPoint — Standards

> Part of the [RecoverPoint](../../) > [Architecture](../) reference.

---

## Naming Conventions

### Consistency Groups

```
CG-<app>-<env>
```

Examples:
- `CG-ORACLE-PROD`
- `CG-SAP-PROD`
- `CG-SQLCLUSTER-DEV`

### Copy Names

| Copy role | Format | Example |
|---|---|---|
| Production copy | `PROD-<site>` | `PROD-SITEA` |
| DR copy | `DR-<site>` | `DR-SITEB` |
| Local CDP copy | `LOCAL-<site>` | `LOCAL-SITEA` |

### Journal Volume Names

```
JRN-<CG-name>-<PROD|DR>
```

Example: `JRN-CG-ORACLE-PROD-DR`

### RPA Cluster Names

```
RPAC-<site>-<number>
```

Example: `RPAC-SITEA-01`, `RPAC-SITEB-01`

---

## Splitter Selection

| Environment | Recommended Splitter |
|---|---|
| PowerMax / VMAX All Flash | Hardware splitter (array-embedded) |
| VMware environment (non-PowerMax) | Software splitter (RP4VM) |
| iSCSI-attached storage | iSCSI splitter |

---

## Configuration Baseline

- Each CG must have at minimum one production copy and one DR copy.
- Journal volumes should be dedicated LUNs; do not share with application data.
- Journal size: minimum 10x the hourly write rate; size for the required recovery window.
- Enable compression on the replication link for WAN-connected sites unless link is already dedicated DWDM.
- CGs protecting the same application tier (e.g., Oracle DB + redo logs) must be in the same consistency group to ensure write-order consistency.
- RPO target must be documented per CG and reviewed quarterly.

---

## Consistency Group Configuration Checklist

- [ ] CG name follows `CG-<app>-<env>` convention
- [ ] Production and DR copy names set correctly
- [ ] Journal volumes provisioned and sized per standard
- [ ] RPO target configured and alarms set
- [ ] Splitter type confirmed for array type
- [ ] Replication link bandwidth allocated
- [ ] Test failover scheduled and documented in change record
- [ ] CG owner and application contact recorded in CMDB

---

## RPO Tiers

| Tier | Target RPO | Review Frequency |
|---|---|---|
| Tier 1 (Critical) | < 15 seconds | Monthly DR test |
| Tier 2 (Business) | < 5 minutes | Quarterly DR test |
| Tier 3 (Standard) | < 30 minutes | Semi-annual DR test |
