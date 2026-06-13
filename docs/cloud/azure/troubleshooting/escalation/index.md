---
tags:
  - azure
  - troubleshooting
search:
  boost: 1.5
---
# Azure — Escalation


<div class="kb-summary">
What to collect before opening a support case and how to engage Microsoft support.
</div>
```text
┌────────────────────────────── Cloud Azure Troubleshooting — Escalation ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Azure escalation: severity triage, vendor support contact, and required artifacts       │   │
│   │         L1: basic checks, restart services; L2: log analysis, config review, vendor SR        │   │
│   │        Severity: P1 production down → immediate SR + on-call page; P2/P3 business hours       │   │
│   │         Before escalating: collect support bundle, event timeline, and change history         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Detect issue → triage severity → collect artifacts → open SR → update                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Severity     │     Criteria     │   Response time   │      Owner       │    Vendor SLA    │   │
│   │        P1        │ Production down  │     Immediate     │   On-call + L2   │    1 hr 24x7     │   │
│   │        P2        │  Major degraded  │       1 hour      │   L2 engineer    │   4 hr biz hrs   │   │
│   │        P3        │  Minor degraded  │      4 hours      │   L2 engineer    │   8 hr biz hrs   │   │
│   │        P4        │    No impact     │    Next biz day   │    L1 support    │    2 biz days    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Troubleshooting infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Troubleshooting platform overview and core concepts               │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Azure Vendor Support

Azure Support plans range from Developer (business-hours email, general guidance) through Standard (24/7 phone, <2 hr critical response) and Professional Direct (24/7 phone, <1 hr critical response, ProDirect engineer) to Premier/Unified (dedicated support, <15 min critical response, proactive services). Support tickets are opened via the Azure Portal under Help + Support or programmatically via the Azure Support API. Before opening a ticket, collect the subscription ID, affected resource IDs, region, timestamp of the issue, and relevant diagnostic logs from Azure Monitor or the Activity Log.

| Plan | Best for | Critical response SLA |
|---|---|---|
| Developer | Dev/test, non-production | < 8 hours (business hours) |
| Standard | Production workloads | < 2 hours |
| Professional Direct | Business-critical production | < 1 hour |
| Premier / Unified | Enterprise / mission-critical | < 15 minutes + TAM |

**Key resources:**

- Azure Portal Support: `portal.azure.com` → Help + Support → Create a support request
- Azure Service Health: `portal.azure.com/#blade/Microsoft_Azure_Health` — service issues, planned maintenance, health advisories
- Microsoft FastTrack for Azure: deployment guidance for eligible workloads (>= $5k/month spend)
- Support API: `az support tickets create` (requires appropriate support plan)

---

## Before Opening a Support Ticket

Collect the following before contacting Microsoft Support:

- Subscription ID: `az account show --query id -o tsv`
- Affected resource IDs: `az resource show --name <name> -g <rg> --query id -o tsv`
- Region and time of issue (UTC)
- Activity Log events around the incident time
- Azure Monitor alert details and metric screenshots
- Diagnostic logs from the affected resource

```bash
# Collect subscription and resource info
az account show --query '{SubscriptionId:id, Name:name, TenantId:tenantId}' -o json

# Export Activity Log for the incident window
az monitor activity-log list \
  --start-time <start-utc> \
  --end-time <end-utc> \
  --resource-group <rg> \
  --output json > activity-log-export.json

# Create support ticket via CLI (requires active support plan)
az support tickets create \
  --ticket-name "incident-$(date +%Y%m%d)" \
  --title "Description of issue" \
  --description "Detailed description" \
  --problem-classification "/providers/Microsoft.Support/services/<service>/problemClassifications/<id>" \
  --severity "critical" \
  --contact-first-name "<name>" \
  --contact-last-name "<name>" \
  --contact-method "email" \
  --contact-email "<email>"
```

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
