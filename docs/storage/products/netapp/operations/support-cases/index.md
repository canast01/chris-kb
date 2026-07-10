---
tags:
  - netapp
  - operations
---
# NetApp Operations — Support Cases

<div class="kb-summary">
Support Cases reference covering Opening a Support Case, Case Severity Levels, Generating a Support Bundle, Information to Include in a Case, Keystone-Specific Cases and 2 more sections.

*Applies to: ONTAP 9.x*
</div>

```d2
direction: down

opening_a_support_case: "Opening a Support Case" {shape: rectangle}
case_severity_levels: "Case Severity Levels" {shape: rectangle}
generating_a_support_bundle: "Generating a Support Bundle" {shape: rectangle}
information_to_include_in_a_case: "Information to Include in a Case" {shape: rectangle}
keystonespecific_cases: "Keystone-Specific Cases" {shape: rectangle}
escalating_a_case: "Escalating a Case" {shape: rectangle}

opening_a_support_case -> case_severity_levels: uses
case_severity_levels -> generating_a_support_bundle: uses
generating_a_support_bundle -> information_to_include_in_a_case: uses
information_to_include_in_a_case -> keystonespecific_cases: uses
keystonespecific_cases -> escalating_a_case: uses
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Opening a Support Case

**Via NetApp Support Portal (mysupport.netapp.com):**
1. Log in and navigate to **My AutoSupport → Cases → Create Case**
2. Select the affected system (by serial number or site)
3. Provide a detailed description, symptom timeline, and impact
4. Attach relevant logs or AutoSupport bundles
5. Select severity and submit

**Via Phone:**
NetApp provides 24/7 phone support for P1 and P2 cases.

## Case Severity Levels

| Severity | Definition | Target Response |
|---|---|---|
| P1 — Critical | Production system down, data loss risk | 15–30 minutes (24/7) |
| P2 — High | Degraded operation, redundancy lost | 1–2 hours (24/7) |
| P3 — Medium | Non-critical issue, workaround available | 4 business hours |
| P4 — Low | Question, guidance, feature request | Next business day |

## Generating a Support Bundle

Before opening a case, collect an AutoSupport:

```bash
# Generate a manual AutoSupport (sends to NetApp automatically)
system node autosupport invoke -node * -type all -message "Opening case for <issue>"

# Confirm AutoSupport delivery
system node autosupport history show | head -20
```


```text title="Expected output"
node-01: Autosupport message posted successfully.
node-02: Autosupport message posted successfully.

Node     Seq Num   Date                     Subject
-------- --------- ------------------------ -----------------------------------------------
node-01  847       11/15/2024 14:32:15 UTC  AutoSupport INVOKE: Opening case for disk failure
node-01  846       11/15/2024 13:18:42 UTC  WEEKLY AUTOSUPPORT
node-01  845       11/14/2024 22:05:33 UTC  DAILY AUTOSUPPORT
node-02  923       11/15/2024 14:32:18 UTC  AutoSupport INVOKE: Opening case for disk failure
node-02  922       11/15/2024 13:19:01 UTC  WEEKLY AUTOSUPPORT
node-02  921       11/14/2024 22:06:12 UTC  DAILY AUTOSUPPORT
node-02  920       11/13/2024 10:44:27 UTC  DAILY AUTOSUPPORT
node-01  844       11/13/2024 10:43:55 UTC  DAILY AUTOSUPPORT
...
```

!!! warning "Common errors"
    **`Error: command not found: system`** — Ensure you are logged into the NetApp cluster management interface (SSH to the cluster IP), not a Linux host.
    **`Error: AutoSupport is not enabled`** — Enable AutoSupport with `system node autosupport modify -node * -state enable` before invoking.
    **`Error: Invalid node name "*"`** — Replace `*` with specific node names (e.g., `node-01 node-02`) if wildcard expansion fails in your shell context.
## Information to Include in a Case

- Array serial number and system name
- ONTAP version (`system node image show`)
- Symptom description with timestamps
- Affected volumes, SVMs, or nodes
- Recent changes (upgrades, configuration, cabling)
- Output of:
  - `cluster show`
  - `system health status show`
  - `event log show -severity error -time ">24h"`
  - `storage failover show`

## Keystone-Specific Cases

For Keystone subscription issues, engage via:
- NetApp Support Portal — select subscription
- Keystone Success Manager — for billing and capacity disputes
- BlueXP → Support → Create Case — for BlueXP-managed services

## Escalating a Case

If a case is not progressing:
1. Request escalation directly within the case
2. Contact your NetApp TAM (Technical Account Manager)
3. For P1: call NetApp support directly — do not rely on email

## Tracking Open Cases

All open and closed cases are visible at **mysupport.netapp.com → Cases**.

AutoSupport also generates case numbers automatically when critical EMS events are triggered — check **My AutoSupport → Cases** for system-initiated cases.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [NetApp — Health Checks](../health-checks/)
