# Azure — Escalation

> What to collect before opening a support case and how to engage Microsoft support.

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
