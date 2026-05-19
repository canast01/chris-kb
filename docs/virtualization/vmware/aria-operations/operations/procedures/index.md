# Aria Operations — Procedures

```
Aria Operations — Alert Lifecycle
┌─────────────────────────────────────────────────────┐
│  Alert Fires                                        │
│  (symptom threshold breached for N wait cycles)     │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  Notification Delivered                             │
│  → email (SMTP) · ServiceNow ticket · webhook       │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  Ops Team Triage                                    │
│  Alerts → All Alerts → filter Critical/Immediate    │
│  → open alert → Symptoms tab → affected object      │
│  → review metric history                            │
└──────────────────────┬──────────────────────────────┘
                       │ root cause found?
                ┌──────┴──────┐
                │ Yes         │ No
                ▼             ▼
┌───────────────────┐  ┌─────────────────────────────┐
│ Acknowledge alert │  │ Escalate · add notes         │
│ Resolve issue     │  │ Open ITSM ticket             │
│ Cancel alert only │  └─────────────────────────────┘
│ after full fix                                      │
└───────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────┐
│  Planned Maintenance? → Create Maintenance Schedule │
│  Admin → Maintenance Schedules → Add Schedule       │
│  select objects + time window → alerts suppressed   │
└─────────────────────────────────────────────────────┘
```

## Alert Management

### Investigating and Acknowledging Alerts

1. Navigate to **Alerts → All Alerts**
2. Filter by **Criticality = Critical or Immediate**
3. Click the alert to open the detail view — review the **Symptoms** tab to understand what triggered it
4. Navigate to the affected object and review recent metric history
5. Acknowledge the alert only after identifying root cause:

```bash
# Acknowledge a specific alert via API
TOKEN=<your-token>
ALERT_ID="<alert-uuid>"
curl -sk -X PATCH -H "Authorization: vRealizeOpsToken $TOKEN" \
  -H "Content-Type: application/json" \
  "https://vrops-prod-01.example.local/suite-api/api/alerts/$ALERT_ID" \
  -d '{"status":"ACKNOWLEDGED","cancelTimeUTC":0}'
```

6. Cancel alerts only after the underlying issue is fully resolved — not as a suppression mechanism

### Maintenance Windows

Create a maintenance schedule to suppress alerts for planned work:

```
Administration → Maintenance Schedules → Add Schedule
```

- Name: `ESXi-03 Maintenance 2026-05-10`
- Objects: select specific hosts, clusters, or datastores
- Duration: start time + estimated duration
- Recurrence: once (or recurring for weekly maintenance)

Alerts triggered during a maintenance window are suppressed and logged separately. Verify the schedule is active before the maintenance window starts.

---

## Capacity Reclamation Workflow

Aria Operations identifies idle and oversized VMs through its capacity analytics engine.

1. Navigate to **Optimize → Reclaim → Idle VMs**
2. Review the list — VMs with CPU and memory utilisation below threshold for >30 days
3. Export the report: **Export → CSV** — send to VM owners for confirmation
4. After owner sign-off, power down or delete the VM from vCenter
5. Navigate to **Optimize → Reclaim → Oversized VMs** — repeat for right-sizing candidates
6. After reclamation, run **Capacity → Recalculate** to update baselines

```bash
# Query idle VMs via API
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/resources/query" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
    "resourceKind": ["VirtualMachine"],
    "propertyConditions": {
      "conditions": [
        {"key": "summary|guest|mks|connectionState", "operator": "EQ", "stringValue": "connected"},
        {"key": "cpu|usage_average", "operator": "LT", "doubleValue": 5.0}
      ]
    }
  }' | jq '.resourceList[] | {name: .resourceKey.name, cpuAvg: .properties["cpu|usage_average"]}'
```

---

## Common Maintenance Tasks

| Task | Steps |
|---|---|
| Restart an adapter | **Administration → Solutions → select adapter → Restart Instance** |
| Restart all cluster services | `vracli cluster restart` (causes brief unavailability — use with care) |
| Clear stale objects | **Environment → Object Browser → Deleted Objects → Purge** |
| Update certificate | **Administration → Certificates → Replace Certificate** |
| Add a data node | **Administration → Cluster Management → Add Node** — provide IP and credentials |
| Remove a data node | **Administration → Cluster Management → select node → Remove** — data rebalances automatically |
| Force adapter collection | **Administration → Solutions → select adapter → Test Connection → Collect Now** |

---

## Creating a Custom Dashboard

1. **Visualize → Dashboards → Create Dashboard**
2. Add widgets from the left panel (Metric Chart, Scoreboard, Alert List, Resource List)
3. For each widget, configure:
   - **Subject**: select an object type (VirtualMachine, ClusterComputeResource)
   - **Metrics**: add specific metrics (e.g., `cpu|usage_average`, `mem|usage_average`)
   - **Time range**: last 7 days / last 30 days
4. Connect widgets so that clicking an object in a Resource List widget populates the Metric Chart below it (**Widget Interactions** → Configure)
5. Save and share: set visibility to **Shared** to make it available to all users with appropriate roles

---

## Creating an Alert Definition

Custom alert definitions trigger when specific metric thresholds are breached.

```
Administration → Alert Settings → Alert Definitions → Add
```

1. Set alert name, description, and base object type (e.g., `VirtualMachine`)
2. Add symptoms:
   - Symptom type: **Metric/Property**
   - Metric: `cpu|usage_average`
   - Operator: `>` 90%
   - Threshold: 90
   - Wait cycle: 3 (alert fires only after 3 consecutive collection cycles above threshold)
3. Add a recommendation (remediation suggestion shown in the alert detail)
4. Set criticality: Warning / Immediate / Critical
5. Assign to an alert policy

Apply the alert policy to an object group:

```
Administration → Alert Settings → Alert Policies → select policy → Apply to Groups
```

---

## Configuring Notification Rules

Alert notifications route to email, ServiceNow, or webhook:

```
Alerts → Notifications → Add Notification Rule
```

1. Filter: apply to alerts with Criticality = Critical targeting the `Production VMs` object group
2. Action: select the outbound plugin (SMTP, ServiceNow, REST webhook)
3. Set notification frequency: alert triggers once (not on every collection cycle)

Test the notification rule by manually triggering a test alert:

```bash
# Trigger a test notification
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/notifications/test" \
  -H "Content-Type: application/json" \
  -d '{"notificationRuleId":"<rule-id>"}'
```

---

## Support Bundle Generation

```bash
# Via UI: Administration → Support → Generate Support Bundle
# Bundle is downloaded directly from the UI

# Via CLI
ssh admin@vrops-prod-01.example.local
vracli support bundle generate

# The bundle is placed at:
ls -lh /storage/log/support-bundle/
# Download to local machine
scp admin@vrops-prod-01.example.local:/storage/log/support-bundle/*.zip .
```

The support bundle includes: cluster configuration, application logs, adapter logs, alert history, and system diagnostics. Required when opening a Broadcom SR.
