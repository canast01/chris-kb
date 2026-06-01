# Pure Storage Evergreen Vendor Support


<div class="kb-summary">
Pure Storage Evergreen Vendor Support reference covering Support Portal, Opening a Case, Information to Collect, SLA Tiers, Escalation Path.
</div>

```text
Evergreen Support Touchpoints
  Pure1 phone-home ──► proactive monitoring + auto case creation
          │
          ▼
  support.purestorage.com ──► manual case creation
  ├── P1 (array down / data loss risk) ── 24/7, 30 min response
  ├── P2 (degraded, no data loss risk)── 24/7, 2 hr response
  ├── P3 (non-critical impact) ───────── business hours
  └── P4 (info / feature request) ────── best effort
          │
          ▼
  Pure Account Team (separate from support):
  ├── Subscription renewals
  ├── Ever Modern scheduling
  └── True Forward capacity amendments
```
## Support Portal

Pure Storage support is accessed through the support portal at **https://support.purestorage.com**.

All arrays under an Evergreen subscription have phonehome telemetry active via Pure1 (https://pure1.purestorage.com). Pure1 provides a unified view of array health, open support cases, subscription status, and lifecycle milestones. For hardware faults detected by phonehome, Pure1 can automatically open a support case and initiate part dispatch — for many hardware failures, a replacement arrives before the customer is aware of the fault.

Ensure phonehome is active at all times. To verify:

```bash
purearray phonehome --status
```

## Opening a Case

When opening a case manually through the support portal or by phone, provide:

| Field | How to Obtain |
|---|---|
| Array serial number | `purearray list` or Purity GUI > System > Array |
| Purity//FA version | `purearray list` — look for the `version` field |
| Subscription entitlement ID | Pure1 > Subscription dashboard — the contract or subscription reference number |
| Symptom description | Clear description of what is failing, when it started, and what changed |
| Impact severity | Production down, degraded, or non-critical — set accurately to receive correct SLA response |

For controller refresh or Ever Modern scheduling issues, also have the subscription renewal date and the current controller generation ready.

## Information to Collect

Run the following before or immediately after opening a case:

```bash
# Array identity and Purity version
purearray list

# Full diagnostic bundle (Pure Support can pull via phonehome)
purediag

# All active alerts
purealert list

# Drive health and status
puredrive list

# Capacity usage summary
purearray list --space

# Controller and hardware component status
purearray list --hardware

# Host path and connection status
purehostconnection list

# Replication pod and ActiveCluster status
purepod list
```

Attach `purediag` output to the case if phonehome is offline. If phonehome is active, inform the support engineer that the diagnostic bundle is available for remote pull.

## SLA Tiers

| Priority | Response Time | Description |
|---|---|---|
| P1 | 1 hour, 24x7 | Production system down or critically impaired; no workaround available |
| P2 | 4 hours, 24x7 | Production system degraded with a workaround in place; operation is impacted |
| P3 | Next business day | Non-critical issue; system operational with minor or no user impact |
| P4 | Best effort | General enquiry, feature request, or documentation question |

Follow P1 and P2 case submissions with a direct phone call to the Pure Support line to ensure immediate engineer engagement.

## Escalation Path

**Standard escalation — within a case:**

1. Request escalation to a duty manager through the support portal or by asking the support engineer — this triggers senior support resource assignment
2. For sustained or complex incidents, ask the support engineer to engage a Pure Solutions Architect or senior engineer for additional expertise

**Customer Success Manager (CSM):**

Evergreen subscriptions include a dedicated CSM. The CSM is the primary point of contact for:

- Subscription lifecycle issues (renewal, True Forward, controller refresh scheduling)
- Escalating unresolved support cases to Pure management
- Quarterly business reviews and capacity planning discussions
- Advocacy for feature requests or prioritisation within Pure's product roadmap

Contact your CSM directly for any subscription-related concern rather than routing through the support portal. For major incidents impacting production, the CSM can mobilise account team and engineering resources in parallel with the support case.

**Pure TAM (Technical Account Manager):**

Customers with a TAM engagement can escalate major incidents to the TAM for cross-functional coordination across support, engineering, and account management.
