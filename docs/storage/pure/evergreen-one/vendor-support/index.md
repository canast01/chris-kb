# Pure Storage Evergreen//One Vendor Support

```text
  Pure Support Case Flow

  ┌─────────────────────┐     ┌─────────────────────────┐
  │  Collect info       │     │  My Pure Storage Portal  │
  │  ├─ purearray list  │     │  support.purestorage.com │
  │  ├─ purealert list  │────►│  Create Case             │
  │  ├─ purediag bundle │     │  ├─ P1: prod down  ─ 1h  │
  │  └─ phonehome status│     │  ├─ P2: degraded   ─ 4h  │
  └─────────────────────┘     │  ├─ P3: non-crit  ─ NBD  │
                               │  └─ P4: query    ─ best │
                               └────────────┬────────────┘
                                            │ P1/P2
                                            ▼
                               ┌────────────────────────┐
                               │  Phone Pure Support    │
                               │  (do not wait on email)│
                               └────────────┬───────────┘
                                            │ not progressing
                                            ▼
                               ┌────────────────────────┐
                               │  CSM escalation        │
                               │  Billing / SLA credits │
                               │  Capacity increase     │
                               │  Contract renewal      │
                               └────────────────────────┘
  Phonehome active ──► Pure auto-detects hw faults proactively
```

## Support Portal

Pure Storage support is accessed through the support portal at **https://support.purestorage.com**.

For Evergreen//One, Pure1 (https://pure1.purestorage.com) is also the primary interface for SLA compliance reporting and service-level issues. Many hardware faults are resolved before the customer is aware: Pure1 phonehome telemetry allows Pure to detect impending failures and dispatch replacement parts proactively, often completing the replacement without customer action.

Ensure phonehome is active at all times. To verify array phonehome status:

```bash
purearray phonehome --status
```

Any disruption to phonehome connectivity should be treated as urgent — Pure's SLA monitoring, proactive maintenance, and automatic case creation all depend on continuous telemetry.

## Opening a Case

When opening a case manually through the support portal or by phone:

| Field | How to Obtain |
|---|---|
| Array serial number | `purearray list` or Purity GUI > System > Array |
| Purity//FA or Purity//FB version | `purearray list` |
| Subscription entitlement ID | Pure1 > Subscription dashboard — the Evergreen//One contract reference |
| Symptom description | What is failing, when it started, and any relevant recent changes |
| Impact severity | Production down, degraded, or non-critical — set accurately for correct SLA response |

For billing, capacity, or SLA credit disputes, contact your CSM (Customer Success Manager) directly rather than the technical support portal — subscription and billing issues are handled by the account team, not support engineering.

## Information to Collect

```bash
# Array identity and Purity version
purearray list

# Full diagnostic bundle
purediag

# All active alerts
purealert list

# Drive health and status
puredrive list

# Capacity summary
purearray list --space

# Hardware component status
purearray list --hardware

# Host path status
purehostconnection list

# Replication pod and ActiveCluster status
purepod list
```

For service-level issues, also download from Pure1:
- Monthly consumption report (Pure1 > Evergreen//One > Consumption > Export)
- SLA compliance report (Pure1 > Evergreen//One > SLA > Export)

Attach the relevant reports to any billing or SLA credit case.

## SLA Tiers

| Priority | Response Time | Description |
|---|---|---|
| P1 | 1 hour, 24x7 | Production system down or critically impaired; no workaround available |
| P2 | 4 hours, 24x7 | Production system degraded; workaround in place but operation is impacted |
| P3 | Next business day | Non-critical issue; system operational with minor impact |
| P4 | Best effort | General enquiry, feature request, or documentation question |

For P1 and P2 cases, follow up the portal submission with a direct phone call to the Pure Support line. The Evergreen//One availability SLA (99.9999%) means Pure has strong contractual motivation to resolve P1 incidents within the response window — escalate immediately if response is not received within the SLA.

## Escalation Path

**Dedicated CSM (Customer Success Manager)**

Every Evergreen//One customer has a dedicated CSM. The CSM is the first point of escalation for all subscription issues:

- Monthly and annual billing disputes
- Committed reserve adjustments and capacity increase coordination
- SLA credit claims — the CSM confirms credits are applied to the correct invoice period
- Escalating unresolved support cases to Pure engineering or management
- Annual service reviews and contract renewal negotiation

Contact the CSM directly for any issue that is not purely a technical hardware or software incident. Do not route subscription, billing, or SLA credit issues through the technical support portal.

**Technical Support Escalation**

For technical incidents not progressing at the expected pace:

1. Request escalation to a duty manager via the support portal or through the support engineer
2. Ask the support engineer to engage a Pure Solutions Architect for complex technical issues
3. Contact your CSM to apply account-level pressure for major incidents affecting the SLA

**Executive Escalation**

For sustained outages or repeated SLA breaches, the CSM can initiate executive escalation within Pure, engaging senior management and engineering to prioritise resolution. Document all breach events and credits in the service record for use in escalation and renewal negotiations.
