---
tags:
  - operations
  - servicenow
---
# ServiceNow — Install & Upgrade


<div class="kb-summary">
ServiceNow cloud instances are upgraded by ServiceNow as part of the managed service. This page covers the upgrade lifecycle from planning through post-upgrade validation, including plugin management, skipped version handling, and rollback considerations.

*Applies to: ServiceNow (Washington / Xanadu)*
</div>

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Release Cadence

ServiceNow releases two major platform versions per year, each named after a city in alphabetical order:

| Year | Releases (approximate) |
|---|---|
| 2024 | Washington DC (Q1), Xanadu (Q3) |
| 2025 | Yokohama (Q1), Zurich (Q3) |
| 2026 | Accelerate (Q1), Balboa (Q3) |

Each major release includes feature updates, security patches, and bug fixes. **Patch releases** (e.g., Xanadu Patch 3) are applied automatically by ServiceNow on a rolling basis and require no customer action.

---

## Upgrade Lifecycle

```mermaid
flowchart TD
    A["Release Announcement\n(~3 months before GA)"]
    B["Review Release Notes\n& Upgrade Planner Tool"]
    C["Identify Breaking Changes\n& Deprecated Features"]
    D["Update Dev Instance\n(ServiceNow schedules)"]
    E["Developer Testing\nFix compatibility issues"]
    F["ATF Regression Suite\nExecute in Dev"]
    G{ATF Pass?}
    H["Fix Failures\nRe-run ATF"]
    I["Upgrade UAT Instance\n(ServiceNow schedules)"]
    J["UAT / Business Acceptance\nTesting"]
    K{UAT Sign-off?}
    L["Raise Issues\nFix & Re-test"]
    M["Schedule Production Upgrade\nwith ServiceNow (HI portal)"]
    N["Production Upgrade\n(maintenance window)"]
    O["Post-Upgrade Validation\n(automated + manual)"]
    P["Close Upgrade Change Request\nDocument lessons learned"]

    A --> B --> C --> D --> E --> F --> G
    G -- Fail --> H --> F
    G -- Pass --> I --> J --> K
    K -- Fail --> L --> J
    K -- Pass --> M --> N --> O --> P
```
```text
┌────────────────────────────────── ServiceNow — Install and Upgrade ───────────────────────────────────┐
│                                                                                                       │
│  ServiceNow upgrade process: SN delivers patches; tenant validates and activates via HI.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Planning               │  │             Plugin Installation             │   │
│   │        Review release notes (SN docs)        │  │        Request via HI portal or in-UI       │   │
│   │       Identify custom scope conflicts        │  │         Test in sub-prod before prod        │   │
│   │       Schedule upgrade window with SN        │  │       Verify license entitlement first      │   │
│   │      Pre-upgrade: snapshot update sets       │  │      Dependencies resolved by platform      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Plan in sub-prod first → promote to production only after full regression validation               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Upgrade Execution               │  │           Post-Upgrade Validation           │   │
│   │       Upgrade Monitor: track progress        │  │       Skipped: review skipped records       │   │
│   │       SN handles DB migration + patch        │  │     Regression: test critical workflows     │   │
│   │      Customisations flagged if conflict      │  │         Integration smoke tests run         │   │
│   │      Rollback: previous version restore      │  │      User acceptance sign-off required      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow data centres · HI portal · sub-prod + production instances                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HI portal       = ServiceNow internal portal; used to request upgrades, clones, plugins              │
│  Release notes   = SN docs page listing changes, deprecations, new features per version               │
│  Custom scope    = scoped application or customisation that may conflict with base upgrade            │
│  Update Set snap = XML export of current customisations before upgrade begins                         │
│  Upgrade Monitor = sys_upgrade_history; tracks status of all upgrade steps                            │
│  Skipped records = customisations that conflicted; admin must resolve manually                        │
│  DB migration    = schema changes applied automatically during upgrade                                │
│  Rollback        = SN-managed; tenant must request via P1 case within window                          │
│  Regression test = scripted or manual test of core workflows post-upgrade                             │
│  Smoke test      = quick integration check: REST/LDAP/MID connections verified                        │
│  Entitlement     = licensed plugins only; check contract before activation                            │
│  Dependency      = plugin A requires plugin B; platform resolves automatically                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Upgrading Plugins

Some plugins have their own release cycle independent of the platform. After a major platform upgrade:

1. Navigate to **System Definitions > Plugins**
2. Filter: **Upgrade Available = true**
3. Review each plugin's changelog
4. Upgrade in Dev first, validate, then promote to UAT and Production via the same change process

### Plugin Upgrade via CLI

```bash
snc plugin upgrade --id com.snc.itsm.workspace --profile dev
snc plugin upgrade --id com.snc.discovery --profile dev
```

---

## Post-Upgrade Testing Checklist

### Automated

- [ ] ATF Core Regression Suite passes (0 failures)
- [ ] API availability check returns HTTP 200
- [ ] MID Servers reconnect and show **Up** within 15 minutes

### ITSM Process Validation

- [ ] Create test incident — confirm priority calculation, assignment, SLA start
- [ ] Escalate test incident — confirm SLA breach notification fires
- [ ] Resolve test incident — confirm resolution workflow completes
- [ ] Create test change request — confirm approval workflow routes correctly
- [ ] Submit test service catalog request — confirm fulfillment flow

### Integrations

- [ ] LDAP import runs successfully
- [ ] Outbound REST messages reach test endpoints (use test webhooks)
- [ ] PagerDuty test event creates and resolves incident
- [ ] Discovery scan completes and populates CMDB
- [ ] Email: send test notification; confirm receipt at test mailbox

### Performance

- [ ] `stats.do` — no new heap or thread alerts post-upgrade
- [ ] Homepage load time < 3 seconds (compare to pre-upgrade baseline)
- [ ] Run at least 2 business days before declaring the upgrade stable

---

## Rollback Options

ServiceNow cloud upgrades are **not directly reversible** by the customer. Rollback options are:

| Scenario | Option | Timeframe |
|---|---|---|
| Critical defect within 4 hours | Request ServiceNow emergency rollback (HI P1) | 4–8 hours |
| Defect discovered after 4 hours | ServiceNow may restore from pre-upgrade snapshot (HI P1) | 8–24 hours |
| Non-critical issue | Fix forward via hotfix Update Set | Days |
| Plugin-specific issue | Deactivate plugin (if possible) | Minutes |

**Pre-upgrade snapshot:** ServiceNow automatically takes a snapshot before each upgrade. Request restoration via a P1 HI case within 72 hours. After 72 hours, the snapshot may be overwritten.

**Recommendation:** Plan to fix forward for non-P1 issues. The rollback window is narrow and the process disruptive. Thorough pre-upgrade testing is the primary risk mitigation.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Servicenow — Deploy](../../deploy/)
