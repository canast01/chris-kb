---
tags:
  - servicenow
---
# Asset Cleanup and Decommission

<div class="kb-summary">
Asset Cleanup and Decommission reference covering Overview, Decommission Workflow, Data Wiping Standards, Dependency Verification Checklist, Physical Asset Disposal and 1 more sections.

*Applies to: ServiceNow*
</div>

## Overview

Asset cleanup covers the full workflow from decommission decision through physical disposal and CMDB record retirement. Skipping steps creates compliance gaps, security risks from data not wiped, and CMDB inaccuracies that affect downstream processes like change and incident management.

---

## Decommission Workflow

Follow this sequence for every asset decommission — server, VM, network device, or end-user hardware.

| Step | Action                                 | Owner            |
|------|----------------------------------------|------------------|
| 1    | Raise decommission request ticket      | Requestor        |
| 2    | Confirm no active dependencies         | App / infra owner|
| 3    | Obtain approval from asset owner       | Asset Manager    |
| 4    | Notify affected teams (14-day notice)  | Change Manager   |
| 5    | Shut down and isolate asset            | Infra Engineer   |
| 6    | Perform data wipe or disk destruction  | Infra Engineer   |
| 7    | Update CMDB status to Retired          | Asset Manager    |
| 8    | Arrange physical disposal              | Facilities       |

---

## Data Wiping Standards

Data must be handled appropriately based on asset classification.

- **Standard HDD/SSD** — NIST 800-88 compliant wipe (e.g., `shred`, `blkdiscard` for SSDs, or Blancco)
- **Cloud volumes** — delete volume and snapshot; confirm no residual in object storage
- **Encrypted disks** — key destruction sufficient if full-disk encryption was active
- **Physical destruction** — required for damaged media or devices holding sensitive data; use certified vendor

Document the wipe method, tool version, and operator in the decommission ticket.

---

## Dependency Verification Checklist

Before any shutdown, confirm no live dependencies remain.

- [ ] Check monitoring: no active alerts referencing this asset
- [ ] Check load balancer / DNS: asset removed from rotation
- [ ] Check backup jobs: exclude asset from backup schedules
- [ ] Check application config: no references in connection strings or env vars
- [ ] Check CMDB relationships: all upstream/downstream CIs reviewed
- [ ] Confirm with app owners in writing (email or ticket comment)

---

## Physical Asset Disposal

For physical hardware leaving the organisation:

- Use only approved WEEE-compliant disposal vendors
- Obtain a certificate of destruction for each device containing persistent storage
- Record vendor name, collection date, and certificate reference in the decommission ticket
- For leased equipment, coordinate return with the vendor before disposal

| Disposal Route     | When to Use                          | Documentation Required        |
|--------------------|--------------------------------------|-------------------------------|
| Certified vendor   | End-of-life owned hardware           | Certificate of destruction    |
| Lease return       | Leased servers/laptops               | Vendor receipt                |
| Internal reuse     | Hardware reassigned to another team  | Asset transfer form           |
| Donation           | Non-sensitive, wiped end-user devices| Wipe certificate + donor form |

---

## CMDB Record Updates

After decommission is complete, update the following:

- [ ] Set CI status to `Retired` with retirement date
- [ ] Remove all active CI relationships
- [ ] Record disposal method and certificate reference in the CI notes field
- [ ] Close all open tickets linked to the CI
- [ ] Notify cost allocation team if the asset carried a cost code
