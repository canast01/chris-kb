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
```
