---
tags:
  - dell
  - operations
---
# FOD — Procedures


<div class="kb-summary">
Procedures reference covering Incident Triage, Maintenance Window, Operational Tasks.
</div>

```text
┌────────────────────────────────── Dell FoD — Operational Procedures ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      FoD procedures: feature request, key purchase, key application, and quarterly audit      │   │
│   │         Request: document feature need in ITSM; validate prereqs; get budget approval         │   │
│   │         Apply: import .lic file via array GUI or CLI within approved CR change window         │   │
│   │        Audit: quarterly reconcile of array license list against CMDB and key inventory        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Request → prereq → CR → purchase → download → vault → apply → verify → CMDB → close CR             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Request Phase        │  │         Apply Phase         │  │         Audit Phase         │   │
│   │         ITSM ticket         │  │        Log into array       │  │       Array lic. list       │   │
│   │           FW check          │  │         Import .lic         │  │         CMDB compare        │   │
│   │           Raise CR          │  │        Confirm active       │  │       Inventory update      │   │
│   │           Buy key           │  │         Update CMDB         │  │       Unused key check      │   │
│   │        Store in vault       │  │           Close CR          │  │        Portal verify        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    FoD key application takes under 1 minute; no array downtime; all hosts unaffected                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Phase       │       Step       │        Tool       │      Owner       │     Duration     │   │
│   │     Request      │  ITSM + prereqs  │   ITSM + portal   │   Storage lead   │     1-2 days     │   │
│   │     Purchase     │  Buy + download  │  Licensing portal │   Storage lead   │     1-3 days     │   │
│   │      Apply       │   Import .lic    │   Array GUI/CLI   │   Storage eng.   │     < 5 min      │   │
│   │      Audit       │ Quarterly audit  │   CMDB + portal   │   Storage lead   │    1-2 hours     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: apply FoD during business hours; no maintenance window required; zero-downtime           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ITSM ticket    = Feature request logged in ServiceNow / Jira with business justification           │
│    FW check       = Verify array firmware meets minimum requirement listed in FoD release notes       │
│    Import .lic    = Array GUI: Settings > Licenses > Import License; browse to .lic file              │
│    Confirm active = After import, license status shows feature as Active in array license list        │
│    Close CR       = Mark CR resolved after CMDB updated and feature confirmed active                  │
│    Array lic list = Full list of active licenses on array; export from GUI for audit comparison       │
│    CMDB compare   = Match array license list to CMDB entries; flag any discrepancies                  │
│    Inventory update = Add new FoD key to inventory doc: feature, SN, applied date, applied by         │
│    Unused key check = Keys purchased but not applied; confirm stored in vault; plan application       │
│    Portal verify  = Confirm licensing portal order history matches keys in local inventory            │
│    Store in vault = Save .lic file to HashiCorp Vault immediately after download from portal          │
│    Zero-downtime  = FoD application does not interrupt I/O; hosts and workloads unaffected            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [Flex on Demand](../index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Incident Triage

**On alert or issue:**
1. Log in to the Dell APEX console (console.dell.com/apex) or Unisphere to check current burst consumption
2. Identify when burst was triggered and which workloads drove the increase
3. If the burst ceiling has been reached, new capacity allocations will fail — immediately assess which workloads can be reduced or tiered
4. Contact the Dell account team to request an emergency burst ceiling increase or expedited base capacity expansion
5. Review the previous month's consumption report to determine if a sustained base capacity increase is warranted

| Symptom | Likely Cause | Action |
|---|---|---|
| Burst ceiling reached, no new capacity available | Workload growth exceeded contracted burst allowance | Reduce provisioning, contact Dell account team for emergency ceiling raise |
| Unexpected billing charges | Sustained burst usage above contracted base | Pull consumption report, identify workloads driving burst, plan base capacity increase |
| Capacity allocation error in Unisphere | Array reporting over-subscription beyond burst | Check SRP utilization via REST API, confirm burst state, open Dell support case |
| FOD consumption not resetting at month boundary | Reporting/billing cycle misalignment | Confirm billing cycle dates with Dell account team, pull consumption report |

## Maintenance Window

FOD itself has no software maintenance requirement. However, any planned workload or storage change that will affect consumption must be documented:

1. Before the window: record current base capacity consumption and burst consumption (in TB and %)
2. Perform the planned workload or storage configuration change
3. Monitor capacity consumption in Unisphere during the window — watch for unexpected burst activation
4. After the window: compare post-change consumption figures against pre-change baseline
5. If the change caused a sustained increase in capacity, update the capacity planning record and notify the Dell account team within 5 business days

## Operational Tasks

| Task | Notes |
|---|---|
| Enrol an array in FOD | Work with the Dell account team to set the committed baseline at contract time |
| Review monthly metered usage report | From CloudIQ or APEX Console; compare to contracted baseline |
| Adjust committed baseline | At contract renewal, based on observed consumption trend |
| Request physical capacity addition | When burst headroom is running low — Dell adds capacity under the FOD agreement |
| Export CloudIQ usage data via API | For internal chargeback or capacity planning reporting |

---

## Activate a Features on Demand Licence

1. Obtain the activation key from Dell (delivered via the Dell licensing portal or by email)
2. Apply the key using SYMCLI:
   ```bash
   symcfg -sid <sid> -auth <activation-key> activate
   ```
3. Verify the feature is now active:
   ```bash
   symcfg -sid <sid> list -fod
   ```
   The target feature should show status `Active`.
4. Update the CMDB and the licence inventory record with the feature name, activation date, and expiry date
5. Store the activation key in the organisation's secret/licence vault

## Renew an Expiring FOD Licence

1. Monitor expiry dates from the quarterly audit or via `symcfg -sid <sid> list -fod -v`
2. Contact Dell or log in to MyService360 to purchase a renewal for the expiring feature
3. Receive the new activation key from Dell (typically via email or the licensing portal)
4. Apply the renewal key within an approved change window:
   ```bash
   symcfg -sid <sid> -auth <new-activation-key> activate
   ```
5. Verify the new expiry date:
   ```bash
   symcfg -sid <sid> list -fod -v
   ```
6. Update the CMDB and licence inventory with the new expiry date

## List All Active FOD Features

```bash
# List all FOD features with name, status, and expiry date
symcfg -sid <sid> list -fod -v
```

The output includes feature name, licence state (Active / Inactive / Expired), and expiry date. Use this output as the basis for quarterly licence audits and renewals.

## Deactivate an Unused FOD Feature

1. Confirm with the application or storage team that the feature is genuinely unused and safe to deactivate
2. Raise a change request — deactivation may affect functionality if any workload still depends on the feature
3. Deactivate the feature:
   ```bash
   symcfg -sid <sid> -auth <key> deactivate -feature <feature-name>
   ```
4. Verify the feature is no longer active:
   ```bash
   symcfg -sid <sid> list -fod
   ```
5. Update the CMDB and licence inventory; return the licence to Dell or reallocate to another array as applicable

## Audit FOD Usage vs Entitlement

1. Export the full FOD feature list for each array:
   ```bash
   symcfg -sid <sid> list -fod -v > fod_audit_<sid>.txt
   ```
2. Compare the exported list against the organisation's licence entitlement register (CMDB or licence spreadsheet)
3. Identify any features that are active but not in the entitlement register (potential unlicensed use)
4. Identify any features in the entitlement register that are not active on the array (potential unused licences)
5. For over-licensed features: plan deactivation or reallocation
6. For unused entitlements: confirm whether the feature was never applied or was deactivated; update the inventory accordingly
7. Document audit findings and remediation actions; repeat quarterly

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
