---
tags:
  - aria-operations
  - operations
  - vmware
---
# Aria Operations Procedures

<div class="kb-summary">
Day-2 operational procedures for Aria Operations — adding adapters, configuring alert policies, managing custom groups, remote collectors, dashboards, workload optimisation, and API data export.

*Applies to: Aria Ops 8.x*
</div>

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

---

## Add an Adapter Instance

Adapter instances connect Aria Operations to data sources — vCenter, NSX, physical hardware, cloud accounts.

1. Aria Ops → **Data Sources** → Cloud Accounts (for vSphere/NSX) or **Integrations** (for third-party adapters)
2. Click **Add Account** → select the adapter kind (vSphere, NSX-T, AWS, etc.)
3. Enter the adapter target details: FQDN/IP, credentials
4. Click **Validate Connection** — confirm the green tick before saving
5. Click **Add** — the adapter begins collecting data immediately
6. Verify collection: after 5–15 minutes, navigate to the target object in **Environment → Object Browser** and confirm metrics are populating

Add the adapter to a collector group if the target is in an isolated network:
- Edit the adapter instance → change **Collector/Group** to the appropriate remote collector

---

## Update Adapter Credentials

When a service account password changes, update the stored credentials before the adapter goes red.

1. Aria Ops → **Data Sources** → locate the affected adapter instance
2. Click **Edit** on the adapter → update the **Credentials** field with the new password
3. Click **Test Connection** — must pass before saving
4. Click **Save** → confirm the adapter returns to green status within one collection cycle

---

## Add a Remote Collector

Remote collectors reach isolated networks (DMZ, remote sites) without exposing the primary cluster.

1. Deploy the remote collector OVA to the target network segment
2. During OVA deployment, set the primary cluster FQDN and admin credentials
3. Aria Ops → **Administration** → **Remote Collectors** — the new collector appears with **Online** status
4. Assign adapter instances to the collector: edit each adapter → change **Collector/Group** to the remote collector
5. Confirm data is flowing: Administration → Remote Collectors → select collector → verify all assigned adapters show green

---

## Configure an Alert Policy

Policies define symptom thresholds and alert priorities for a set of objects.

1. Aria Ops → **Configure** → **Policies** → **Add Policy**
2. Enter a policy name and description; optionally clone from the **Default Policy** as a baseline
3. Under **Alert/Symptom Definitions**, modify thresholds for the relevant object types:
   - Example: CPU Workload > 85% for 15 minutes → **Symptom: Critical**
   - Example: Datastore Capacity > 80% → **Symptom: Warning**
4. Set **Alert Actions** — which notification plugin fires when an alert triggers
5. Click **Save** — the policy is inactive until assigned to an object group
6. Assign the policy: **Policies** tab → select the policy → **Apply to Groups** → select target groups

---

## Create a Custom Group

Custom groups scope policy assignments and dashboard filters to specific objects.

1. Aria Ops → **Environment** → **Custom Groups** → **Add Group**
2. Set the group type: **Custom** (manual membership) or **Dynamic** (auto-membership based on criteria)
3. For dynamic groups, set membership criteria:
   - Object type: VirtualMachine
   - Property filter: e.g., `summary|tag|Environment = "Production"`
4. Click **Preview Members** to verify the membership before saving
5. Click **Save** — the group is now available for policy assignment and dashboard filters

Assign a policy to the group: **Configure → Policies → select policy → Apply to Groups**.

---

## Configure SMTP Notifications

SMTP must be configured before email notification rules will deliver.

1. Aria Ops → **Administration** → **Outbound Settings** → **Add Outbound Plugin**
2. Select **Standard Email** plugin
3. Configure:
   - **SMTP host**: relay FQDN or IP
   - **SMTP port**: 25 (plain), 587 (STARTTLS), or 465 (SSL)
   - **Sender address**: `aria-ops@example.local`
   - **Authentication**: enable if relay requires credentials
4. Click **Test** — confirm a test email arrives at the specified address
5. Click **Save**

Reference the outbound plugin in notification rules: **Configure → Notifications → Add Rule → Action → Standard Email**.

---

## Configure a Notification Rule

1. Aria Ops → **Configure** → **Notifications** → **Add**
2. Select the trigger: **Alert severity** (Critical, Immediate, Warning) or specific **Alert Definition**
3. Set the filter scope: all objects, a custom group, or specific object types
4. Under **Action**, select the outbound plugin (SMTP email or webhook)
5. Configure the email/webhook details for this rule
6. Click **Test** — confirms the notification delivers before saving
7. Click **Save** — rule is immediately active

---

## Install a Management Pack (Solution)

Management packs extend Aria Ops with adapters and dashboards for third-party products.

1. Obtain the PAK file for the management pack from the vendor or VMware Marketplace
2. Aria Ops → **Administration** → **Repository** → **Upload** → select the PAK file
3. Review the certificate warning — click **Install** to proceed
4. Once installed, navigate to **Data Sources** → the new adapter kind is now available
5. Add adapter instances for the new management pack as needed

---

## Create a Custom Dashboard

1. Aria Ops → **Visualize** → **Dashboards** → **New**
2. Enter a dashboard name and description; set visibility: **Private** or **Shared with group**
3. Drag widgets from the widget panel:
   - **Metric Chart** — time-series metrics for selected objects
   - **Topology Graph** — object relationship visualisation
   - **Alert List** — active alerts filtered by scope or severity
   - **Heatmap** — colour-coded object health across a group
4. Configure each widget: select object type, specific objects, and metric or alert filter
5. Arrange and resize widgets → click **Save**
6. Share: **Actions → Share** → select the user group

---

## Generate a Report

Reports export object metrics, alert summaries, and capacity data to PDF or CSV.

1. Aria Ops → **Visualize** → **Reports** → **Add Report Template**
2. Select a built-in template (e.g., "VM CPU Report", "Capacity Summary") or start from blank
3. Add report sections: select object type, time range, and metrics to include
4. Click **Generate** to produce an immediate report or **Schedule** to deliver on a recurring basis
5. Scheduled reports are emailed to the configured recipient list via the SMTP outbound plugin

---

## Create a Super Metric

Super metrics aggregate metrics from multiple objects or calculate derived values.

1. Aria Ops → **Configure** → **Super Metrics** → **Add Super Metric**
2. Build the formula using the formula editor:
   - Example: average CPU across all VMs in a cluster: `avg(${this, metric=cpu|usage_average, depth=2, where=objecttype=VirtualMachine})`
3. Set the object type this super metric applies to (e.g., Cluster Compute Resource)
4. Click **Save** → assign the super metric to a policy to enable collection
5. Verify collection: navigate to a cluster object → **Metrics** tab → locate the super metric

---

## Reclaim Idle VM Resources

1. Aria Ops → **Optimize** → **Reclamation** → **Idle VMs**
2. Review the list of VMs with sustained low CPU, memory, and network utilisation
3. Each VM shows projected savings (vCPU, memory, storage)
4. For each VM: **Approve** (Aria Ops schedules the right-sizing action) or **Defer** (snooze)
5. Approved actions are executed via vCenter — VMs are right-sized or powered off
6. Track savings: **Optimize → Reclamation → Savings** tab

---

## Query Idle VMs via API

```bash
# Acquire token
TOKEN=$(curl -sk -X POST "https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","authSource":"local","password":"<pw>"}' \
  | jq -r '.token')

# Query idle VMs (CPU < 5%, connected)
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

## Export Metrics Data via API

```bash
# Acquire token
TOKEN=$(curl -sk -X POST "https://<aria-ops>/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","authSource":"local","password":"<pw>"}' \
  | jq -r '.token')

# Get resource ID for a VM by name
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://<aria-ops>/suite-api/api/resources?name=<vm-name>&resourceKind=VirtualMachine" \
  | jq '.resourceList[].identifier'

# Export metric rollup for the resource
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://<aria-ops>/suite-api/api/resources/<resource-id>/stats?statKey=cpu|usage_average&rollUpType=AVG&intervalType=HOURS&intervalQuantifier=24" \
  | jq '.values[].stat-list.stat[]'
```

Token lifetime is 60 minutes; re-acquire for long-running scripts.

---

## Trigger a Test Notification

```bash
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/notifications/test" \
  -H "Content-Type: application/json" \
  -d '{"notificationRuleId":"<rule-id>"}'
```

---

## Generate a Support Bundle

Via UI: **Administration → Support → Generate Support Bundle** — downloads directly from the browser.

Via CLI:
```bash
ssh admin@vrops-prod-01.example.local
vracli support bundle generate

# Confirm bundle location
ls -lh /storage/log/support-bundle/

# Download to local machine
scp admin@vrops-prod-01.example.local:/storage/log/support-bundle/*.zip .
```

---

## Upgrade Aria Operations (via Aria Suite Lifecycle)

1. **Pre-upgrade snapshot** — take VM snapshots of all Aria Operations nodes (master, data, remote collectors) before starting
2. Verify LCM has the upgrade bundle: LCM UI → **Lifecycle Operations** → **Settings** → **Binary Mapping** → confirm the target Aria Operations version is listed with status **Available**
3. LCM UI → **Environments** → select the environment containing Aria Operations → **Products** → click **Aria Operations**
4. Click **Upgrade** → select the target version from the dropdown
5. Click **Run Precheck** — all checks must pass before proceeding; resolve any failures (NTP drift, disk space, credential expiry)
6. Click **Upgrade** → confirm the upgrade plan → click **Proceed**
7. Monitor progress: LCM shows per-product upgrade stages; expect 45–90 minutes depending on cluster size
8. **Post-upgrade validation:**
   - Verify all adapters collecting: **Administration → Solutions** — all adapter instances must show green
   - Verify alert policies: **Configure → Policies** — confirm custom policies are intact and applied to correct object groups
   - Check Cassandra health: SSH to master node → `su -s /bin/bash vcops-svc -c "cd /usr/lib/vmware-vcops/cassandra/bin && ./nodetool status"` — all nodes show `UN`
9. Delete VM snapshots after 48 hours of confirmed stable operation

---

## Add a Remote Collector Group

Remote Collector Groups (RCGs) pin adapter collection to a specific set of remote collectors — essential for isolated network segments (DMZ, remote sites, cloud VPCs).

1. Aria Ops → **Administration** → **Remote Collectors** → **Remote Collector Groups** → **Add Group**
2. Enter a group name (e.g., `rcg-dmz-segment`, `rcg-site-london`)
3. From the **Available Collectors** list, select the remote collectors to add → move to **Selected Collectors**
4. Click **Save** — the group is immediately available for adapter assignment
5. Assign adapters to the group: **Data Sources** (or **Integrations**) → edit each adapter instance → set **Collector/Group** to the new RCG
6. Verify: **Administration → Remote Collector Groups** → select the group → confirm all assigned adapters show green collection status

When an adapter is pinned to an RCG, Aria Operations load-balances collection across all collectors in that group; removing a collector from the group immediately shifts load to remaining collectors.

---

## Configure Alert Criticality and Business Hours

1. Aria Ops → **Alerts** → **Alert Policies** → select the target policy → **Edit**
2. Under the **Alerts** tab, locate the alert definition → set **Criticality** from the dropdown: `Critical`, `Immediate`, `Warning`, or `Information`
3. To configure Business Hours: **Edit Policy** → **Business Hours** tab → enable Business Hours → define the schedule (days, start time, end time, timezone)
4. Set **Non-Business Hours Behavior**: choose `Defer notifications` (Aria Ops holds alerts until the next business window opens) or `Suppress alerts entirely`
5. Click **Save**
6. Verify: trigger a test condition outside business hours → confirm the notification is deferred and fires at the next business window open time

Business hours apply per-policy; assign different policies to production vs. non-production object groups to reduce off-hours alert noise without silencing critical production alerts.

---

## Create a Custom Alert Definition

1. Aria Ops → **Configure** → **Alerts** → **Alert Definitions** → **Add**
2. Enter **Name** and **Description**; set **Impact**: select the object type this alert targets (e.g., `VirtualMachine`, `Datastore`)
3. **Symptoms tab** → **Add Symptom** → **Metric / Property Symptom**:
   - Select metric (e.g., `cpu|usage_average`)
   - Operator: `>` value: `90`, duration: `15` minutes → set symptom criticality: `Critical`
   - Add additional symptoms as needed; set **Condition** to `ANY` (alert fires on first match) or `ALL`
4. **Recommendations tab** → **Add Recommendation** → enter remediation instructions (supports links to KB articles)
5. Click **Save**
6. Activate: assign the alert definition to a policy — **Configure → Policies → edit policy → Alert/Symptom Definitions → enable the new definition**
7. **Test**: reproduce the threshold condition on a test object; confirm the alert fires in **Alerts → All Alerts** with the correct severity within two collection cycles

---

## Configure LDAP / Identity Source Integration

1. Aria Ops → **Administration** → **Access Control** → **Identity Sources** → **Add**
2. Select type: **LDAP** or **Active Directory** (Integrated Windows Auth)
3. Enter LDAP connection details:
   - **LDAP URL**: `ldap://ad.example.local:389` (or `ldaps://` for TLS, port 636)
   - **Base DN**: `DC=example,DC=local`
   - **Bind DN**: `CN=svc-vrops,OU=Service Accounts,DC=example,DC=local`
   - **Bind Password**: service account password
   - **User Search Base** and **Group Search Base** if non-standard
4. Click **Test** — confirm the bind succeeds and user/group search returns results
5. Click **Save** → **Import Groups**: search for and import the AD groups that need Aria Ops access
6. Assign roles to groups: **Access Control → Groups** → select imported group → **Edit** → assign role (`Administrator`, `Content Admin`, `Read Only`, or a custom role)
7. **Verify**: log out → log in using an AD user in the imported group → confirm the correct role is applied and object visibility matches the role scope

---

## Configure Data Retention (Rollup Periods)

Default retention: raw metrics 6 months, hourly rollup 1 year, daily rollup 5 years. Reduce raw retention to save disk; extend daily rollup for long-term capacity trending.

1. Aria Ops → **Administration** → **Global Settings** → **Data Retention**
2. Edit the retention periods:
   - **Raw data**: 1–6 months (reduce to 3 months on disk-constrained clusters)
   - **Hourly rollup**: 6–18 months
   - **Daily rollup**: 1–5 years
3. Click **Save**
4. If prompted, restart the analytics service: SSH to master → `systemctl restart vmware-vcops-analytics`; the service restarts in ~3–5 minutes
5. Verify the new settings applied: **Administration → Global Settings → Data Retention** → confirm saved values

Reducing raw retention triggers a background purge of older data; disk reclamation appears within 24–48 hours as Cassandra compaction completes.

---

## Configure a Cost Metric (Aria Cost Integration)

1. Aria Ops → **Administration** → **Configuration** → **Cost Drivers** (or **Cost Settings** depending on version)
2. Define rates per unit:
   - **CPU rate**: cost per GHz per month (e.g., `$0.012`)
   - **Memory rate**: cost per GB per month (e.g., `$0.008`)
   - **Disk rate**: cost per GB per month (e.g., `$0.0003`)
3. Assign rates to scopes: select cloud accounts or vSphere clusters → apply the rate card
4. Click **Save**
5. Wait for the next collection cycle (typically 5 minutes) → verify cost data appears in:
   - **Optimize → Cost** → select a VM or cluster → confirm **Cost** tab shows calculated values
   - Built-in **VM Cost** and **Cluster Cost** dashboards populate

For Cloudhealth integration: **Administration → Integrations → Cloudhealth** → enter API key → map cloud accounts; cost data flows into Aria Ops dashboards after the first Cloudhealth sync (up to 24 hours).

---

## Restart a Failed Adapter Service

When an adapter shows "Not Collecting" in the Solutions page:

1. **UI restart**: **Administration → Solutions** → select the adapter instance → **Actions → Restart Adapter Instance** → wait one collection cycle → verify status returns to green
2. **Service-level restart** (if UI restart fails):
   ```bash
   ssh admin@vrops-prod-01.example.local
   # Restart watchdog — it detects and restarts all failed services
   sudo systemctl restart vmware-vcops-watchdog
   # Monitor service recovery (~2 minutes)
   sudo systemctl list-units 'vmware-*' --state=active
   ```
3. **Check adapter logs** for root cause:
   ```bash
   # Adapter logs are in per-adapter subdirectories
   ls /usr/lib/vmware-vcops/user/log/adapters/
   # Tail the log for the failing adapter (example: vSphere adapter)
   tail -200 /usr/lib/vmware-vcops/user/log/adapters/VMwareVim25Adapter/adapter.log | grep -i "ERROR\|exception\|authentication"
   ```
4. **Common causes and fixes:**
   - `Authentication failed` → update credentials: **Data Sources → edit adapter → update password → Test Connection**
   - `Connection refused` / `timeout` → verify network path from collector to target; check firewall rules
   - `Certificate validation failed` → add target cert to Aria Ops trust store or disable SSL verification for internal hosts
5. After fixing root cause, re-run UI restart and confirm green status within one collection cycle
