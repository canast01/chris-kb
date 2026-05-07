# Asset Lifecycle Management

## Overview

Every asset moves through a predictable set of stages from procurement to disposal. Tracking these stages in the CMDB enables proactive refresh planning, accurate budgeting, and timely EOL management — avoiding the risk of running unsupported hardware or software in production.

---

## Lifecycle Stages

| Stage          | Description                                              | CMDB Status       |
|----------------|----------------------------------------------------------|-------------------|
| Requested       | Purchase request raised, not yet approved               | Ordered           |
| Procurement     | PO raised, asset on order                               | Ordered           |
| Receiving       | Asset received, tagged, and inventoried                 | In Stock          |
| Deployment      | Asset configured and placed in service                  | Active            |
| Operational     | Asset in production use                                 | Active            |
| Under Review    | Flagged for refresh, evaluation in progress             | Under Review      |
| Decommission    | Retirement approved, shutdown and wipe in progress      | Decommissioning   |
| Retired         | Disposed or returned; record closed                     | Retired           |

Stage transitions must be reflected in the CMDB within 48 hours of the physical change.

---

## Refresh Cycles

Default refresh cycles by asset class. Adjust based on vendor support timelines and actual failure rates.

| Asset Class         | Target Refresh Cycle | EOL Warning Lead Time |
|---------------------|----------------------|-----------------------|
| Physical servers    | 5 years              | 12 months             |
| Laptops / desktops  | 4 years              | 6 months              |
| Network switches    | 7 years              | 12 months             |
| Firewalls           | 5 years              | 12 months             |
| SAN / NAS storage   | 5 years              | 12 months             |
| UPS units           | 7–10 years           | 18 months             |

Trigger a refresh review when: vendor EOL is announced, hardware failure rate exceeds 10% in a cohort, or the asset no longer meets performance requirements.

---

## EOL Tracking

Maintain an EOL register separate from the main CMDB for forward planning. At minimum track:

- Asset tag and CI reference
- Vendor EOL date (hardware and OS/firmware)
- Current contract / support end date
- Assigned refresh budget year
- Owner and escalation contact

- [ ] Review EOL register monthly for items within 12-month window
- [ ] Raise refresh project request at least 6 months before EOL
- [ ] Confirm vendor support extension availability if refresh is delayed
- [ ] Update CMDB with EOL dates from vendor bulletins as they are published

---

## Budget Planning

Asset refresh planning feeds directly into the annual capital budget cycle.

Steps to prepare the refresh budget:

1. Export all CIs with `Active` status and deployment date
2. Apply refresh cycle per asset class to calculate projected refresh year
3. Cross-reference with EOL register
4. Estimate replacement cost per unit (use current vendor pricing + 10% contingency)
5. Group by budget year and present to finance by agreed submission deadline

| Budget Year | Assets Due for Refresh | Estimated Cost |
|-------------|------------------------|----------------|
| 2026        | (from CMDB export)     | TBD            |
| 2027        | (from CMDB export)     | TBD            |
| 2028        | (from CMDB export)     | TBD            |

---

## Roles and Responsibilities

| Role               | Responsibility                                        |
|--------------------|-------------------------------------------------------|
| Asset Manager      | Maintain lifecycle register; own CMDB accuracy        |
| Infra Lead         | Trigger refresh projects; validate technical readiness|
| Finance            | Approve capital spend; track depreciation             |
| Procurement        | Manage vendor relationships and purchase orders       |
| Change Manager     | Coordinate decommission within change process         |
