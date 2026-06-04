# Aria Operations Procedures

```text
┌───────────────────────────────────── Aria Operations Procedures ──────────────────────────────────────┐
│                                                                                                       │
│  Add adapter, certificate rotation, and policy management procedures for vROps.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Add Adapter Instance             │  │             Certificate Rotation            │   │
│   │            1. Data Sources > Add             │  │           1. Generate CSR in VAMI           │   │
│   │            2. Choose adapter kind            │  │            2. Get CA-signed cert            │   │
│   │         3. Enter host + credentials          │  │          3. Upload cert in VAMI SSL         │   │
│   │         4. Test + Save; check green          │  │           4. Verify browser trust           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Adapter add and cert rotation are routine; policy management is ongoing governance.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Policy Management               │  │             Credential Rotation             │   │
│   │            1. Policies > Add/Edit            │  │         1. Update source account pw         │   │
│   │          2. Set symptom thresholds           │  │           2. Edit adapter instance          │   │
│   │          3. Assign to object groups          │  │           3. Enter new credential           │   │
│   │           4. Validate alert firing           │  │                4. Test + Save               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster; vCenter/NSX as adapter targets; CA for cert signing; AD for accounts                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Adapter Instance    = Configured connection from vROps to a specific data source                     │
│  Adapter Kind        = Type of adapter: vSphere, NSX, AWS, etc.                                       │
│  Test Connection     = vROps built-in check validating credentials and reachability                   │
│  CSR                 = Certificate Signing Request; sent to CA for signing                            │
│  VAMI SSL            = Certificate upload page in VAMI for vROps web cert                             │
│  Policy              = Named ruleset defining alert thresholds for an object group                    │
│  Symptom             = Single condition (e.g. CPU > 90%) contributing to an alert                     │
│  Object Group        = Collection of objects sharing a policy assignment                              │
│  Credential Rotation = Updating stored adapter credentials after password change                      │
│  Adapter Green       = Status showing adapter collecting without errors                               │
│  Alert Validation    = Test that a known condition triggers the expected alert                        │
│  Policy Inheritance  = Child groups inherit parent policy; overridden at child level                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── Aria Operations Procedures ──────────────────────────────────────┐
│                                                                                                       │
│  Add adapter, certificate rotation, and policy management procedures for vROps.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Add Adapter Instance             │  │             Certificate Rotation            │   │
│   │            1. Data Sources > Add             │  │           1. Generate CSR in VAMI           │   │
│   │            2. Choose adapter kind            │  │            2. Get CA-signed cert            │   │
│   │         3. Enter host + credentials          │  │          3. Upload cert in VAMI SSL         │   │
│   │         4. Test + Save; check green          │  │           4. Verify browser trust           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Adapter add and cert rotation are routine; policy management is ongoing governance.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Policy Management               │  │             Credential Rotation             │   │
│   │            1. Policies > Add/Edit            │  │         1. Update source account pw         │   │
│   │          2. Set symptom thresholds           │  │           2. Edit adapter instance          │   │
│   │          3. Assign to object groups          │  │           3. Enter new credential           │   │
│   │           4. Validate alert firing           │  │                4. Test + Save               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster; vCenter/NSX as adapter targets; CA for cert signing; AD for accounts                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Adapter Instance    = Configured connection from vROps to a specific data source                     │
│  Adapter Kind        = Type of adapter: vSphere, NSX, AWS, etc.                                       │
│  Test Connection     = vROps built-in check validating credentials and reachability                   │
│  CSR                 = Certificate Signing Request; sent to CA for signing                            │
│  VAMI SSL            = Certificate upload page in VAMI for vROps web cert                             │
│  Policy              = Named ruleset defining alert thresholds for an object group                    │
│  Symptom             = Single condition (e.g. CPU > 90%) contributing to an alert                     │
│  Object Group        = Collection of objects sharing a policy assignment                              │
│  Credential Rotation = Updating stored adapter credentials after password change                      │
│  Adapter Green       = Status showing adapter collecting without errors                               │
│  Alert Validation    = Test that a known condition triggers the expected alert                        │
│  Policy Inheritance  = Child groups inherit parent policy; overridden at child level                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────────────────────┐
│  Ops Team Triage                                                                                      │
│  Alerts → All Alerts → filter Critical/Immediate                                                      │
│  → open alert → Symptoms tab → affected object                                                        │
│  → review metric history                                                                              │
└──────────────────────┬──────────────────────────────┘
```
```text
┌───────────────────┐  ┌─────────────────────────────┐
│ Acknowledge alert │  │ Escalate · add notes                                                           │
│ Resolve issue     │  │ Open ITSM ticket                                                               │
│ Cancel alert only │  └─────────────────────────────┘
│ after full fix                                                                                        │
└───────────────────┘
```
```text
┌─────────────────────────────────────────────────────┐
│  Planned Maintenance? → Create Maintenance Schedule                                                   │
│  Admin → Maintenance Schedules → Add Schedule                                                         │
│  select objects + time window → alerts suppressed                                                     │
└─────────────────────────────────────────────────────┘
```

```text
┌───────────────────────────────────── Aria Operations Procedures ──────────────────────────────────────┐
│                                                                                                       │
│  Add adapter, certificate rotation, and policy management procedures for vROps.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Add Adapter Instance             │  │             Certificate Rotation            │   │
│   │            1. Data Sources > Add             │  │           1. Generate CSR in VAMI           │   │
│   │            2. Choose adapter kind            │  │            2. Get CA-signed cert            │   │
│   │         3. Enter host + credentials          │  │          3. Upload cert in VAMI SSL         │   │
│   │         4. Test + Save; check green          │  │           4. Verify browser trust           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Adapter add and cert rotation are routine; policy management is ongoing governance.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Policy Management               │  │             Credential Rotation             │   │
│   │            1. Policies > Add/Edit            │  │         1. Update source account pw         │   │
│   │          2. Set symptom thresholds           │  │           2. Edit adapter instance          │   │
│   │          3. Assign to object groups          │  │           3. Enter new credential           │   │
│   │           4. Validate alert firing           │  │                4. Test + Save               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster; vCenter/NSX as adapter targets; CA for cert signing; AD for accounts                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Adapter Instance    = Configured connection from vROps to a specific data source                     │
│  Adapter Kind        = Type of adapter: vSphere, NSX, AWS, etc.                                       │
│  Test Connection     = vROps built-in check validating credentials and reachability                   │
│  CSR                 = Certificate Signing Request; sent to CA for signing                            │
│  VAMI SSL            = Certificate upload page in VAMI for vROps web cert                             │
│  Policy              = Named ruleset defining alert thresholds for an object group                    │
│  Symptom             = Single condition (e.g. CPU > 90%) contributing to an alert                     │
│  Object Group        = Collection of objects sharing a policy assignment                              │
│  Credential Rotation = Updating stored adapter credentials after password change                      │
│  Adapter Green       = Status showing adapter collecting without errors                               │
│  Alert Validation    = Test that a known condition triggers the expected alert                        │
│  Policy Inheritance  = Child groups inherit parent policy; overridden at child level                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
## Query idle VMs via API
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
```text
Administration → Alert Settings → Alert Definitions → Add
```
```text
Administration → Alert Settings → Alert Policies → select policy → Apply to Groups
```
```text
Alerts → Notifications → Add Notification Rule
```
```bash
## Trigger a test notification
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/notifications/test" \
  -H "Content-Type: application/json" \
  -d '{"notificationRuleId":"<rule-id>"}'
```
```bash
## Via UI: Administration → Support → Generate Support Bundle
## Bundle is downloaded directly from the UI

## Via CLI
ssh admin@vrops-prod-01.example.local
vracli support bundle generate

## The bundle is placed at:
ls -lh /storage/log/support-bundle/
## Download to local machine
scp admin@vrops-prod-01.example.local:/storage/log/support-bundle/*.zip .

---

## Add a Remote Collector

Remote collectors allow Aria Operations to reach isolated networks (DMZ, remote sites) without requiring direct access from the primary cluster nodes.

1. Aria Ops → Administration → Remote Collectors → **Add**
2. Specify the collector IP or FQDN and an identifying name
3. Deploy the remote collector OVA to the target network segment — or configure an existing collector appliance to point at the Aria Ops cluster
4. Once registered, the collector appears in the list with **Online** status
5. Assign adapter instances to the collector: edit each adapter instance → change **Collector/Group** to the new remote collector
6. Verify data is flowing: Administration → Remote Collectors → select collector → confirm all assigned adapters show green

---

## Create a Custom Dashboard

1. Aria Ops → Visualize → Dashboards → **New**
2. Enter a dashboard name and description; set visibility (private or shared to group)
3. Drag widgets from the widget panel onto the canvas:
   - **Metric Chart** — plot time-series metrics for selected objects
   - **Topology Graph** — visualise object relationships
   - **Alert List** — show active alerts filtered by scope or severity
4. Configure each widget's data source: select object type, specific objects, and the metric or alert filter
5. Arrange and resize widgets to create the layout
6. Click **Save** → share the dashboard to a user group via **Actions → Share**

---

## Configure a Notification (Email/Webhook)

1. Aria Ops → Configure → Notifications → **Add**
2. Select the trigger type:
   - **Alert severity** — fire when an alert reaches Critical/Immediate
   - **Symptom** — fire when a specific symptom is true
3. Configure the notification action:
   - **SMTP email** — specify recipients, subject template, and SMTP relay details (Administration → SMTP Settings must be configured first)
   - **REST webhook** — specify the endpoint URL, HTTP method, and payload template
4. Click **Test** to send a test notification and confirm delivery
5. Save the notification rule — it is now active for all matching future alerts

---

## Reclaim Idle VM Resources (Workload Optimization)

1. Aria Ops → Optimize → Reclamation → **Idle VMs**
2. Aria Operations identifies VMs with sustained low CPU, memory, and network utilisation based on the configured reclamation policy
3. Review the reclamation recommendations — each VM shows projected savings (vCPU, memory, storage)
4. For each VM select **Approve** (Aria Ops schedules the right-sizing action) or **Defer** (snooze for a set period)
5. Approved actions are executed via vCenter — VMs are right-sized or powered off depending on the recommendation type
6. Track cumulative savings over time: Optimize → Reclamation → **Savings** tab

---

## Export Metrics Data via API

Acquire an authentication token:

```bash
TOKEN=$(curl -sk -X POST "https://<aria-ops>/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","authSource":"local","password":"<pw>"}' \
  | jq -r '.token')
```

Use the token to query metric data for a resource:

```bash
## Get resource ID for a VM by name
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://<aria-ops>/suite-api/api/resources?name=<vm-name>&resourceKind=VirtualMachine" \
  | jq '.resourceList[].identifier'

## Export metric rollup for the resource
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://<aria-ops>/suite-api/api/resources/<resource-id>/stats?statKey=cpu|usage_average&rollUpType=AVG&intervalType=HOURS&intervalQuantifier=24" \
  | jq '.values[].stat-list.stat[]'
```

Token lifetime is 60 minutes by default; re-acquire as needed for long-running export scripts.
```
