# Aria Operations for Networks — Procedures


<div class="kb-summary">
Procedures reference covering Add a New vCenter Data Source, Configure NetFlow Export from a Cisco Switch, Run Microsegmentation Analysis for an Application, Export Security Group Recommendations to NSX, Create a Saved Search / Alert and 3 more sections.
</div>

## Add a New vCenter Data Source

1. Settings → Accounts and Data Sources → Add Source → vCenter Server
2. Fill in:
   - **Nickname**: descriptive label (e.g., `vCenter-ProdDC`)
   - **vCenter IP/FQDN**: `vcenter.example.local`
   - **Username**: `svc-aon@vsphere.local`
   - **Password**: service account password
   - **Collector**: select the Collector VM associated with this site
3. Click **Validate** — AON tests connectivity and credential validity
4. Click **Submit**

Verify sync within 10–15 minutes:
- Settings → Accounts and Data Sources → select the new vCenter → check **Last Sync** timestamp
- Search bar: `hosts where datasource = "vCenter-ProdDC"` — should return ESXi hosts

**Via REST API:**

```bash
TOKEN="<your-token>"
PLATFORM="https://aon.example.local"

curl -sk -X POST "${PLATFORM}/api/ni/datasources/vcenter" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "nickname": "vCenter-ProdDC",
    "credentials": {
      "ip": "vcenter.example.local",
      "username": "svc-aon@vsphere.local",
      "password": "PASSWORD"
    },
    "collector_id": "collector-001",
    "enabled": true
  }' | python3 -m json.tool
```text
┌───────────────────────────────────── vRNI Operational Procedures ─────────────────────────────────────┐
│                                                                                                       │
│  Add data source, certificate rotation, and credential rotation procedures for vRNI.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Add Data Source                │  │             Certificate Rotation            │   │
│   │          1. Settings > Data Sources          │  │           1. Generate new cert/CSR          │   │
│   │            2. Select source type             │  │           2. Upload cert via VAMI           │   │
│   │          3. Enter IP + credentials           │  │            3. Restart UI service            │   │
│   │         4. Test + Save; verify green         │  │          4. Validate browser trust          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Data source addition and cert rotation are common day-2 operational tasks.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Credential Rotation              │  │            Application Definition           │   │
│   │         1. Update source account pw          │  │          1. Applications > Add New          │   │
│   │         2. Edit data source in vRNI          │  │          2. Define VM/IP membership         │   │
│   │           3. Enter new credential            │  │           3. Name tiers and groups          │   │
│   │         4. Test + Save; verify green         │  │           4. View app in Flow Map           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform VM; vCenter and NSX as credential targets; CA for cert signing                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Data Source         = vRNI connection object; requires valid credentials to collect                  │
│  Credential Rotation = Updating stored API/service account password in vRNI source config             │
│  Certificate         = TLS cert for vRNI web UI; uploaded via VAMI SSL settings                       │
│  CSR                 = Certificate Signing Request; generated for CA-signed cert flow                 │
│  VAMI                = Virtual Appliance Management Interface; used for cert upload                   │
│  Application         = Logical grouping of VMs/IPs in vRNI for Flow Map filtering                     │
│  Tier                = Sub-group within an Application; e.g. Web, App, DB layers                      │
│  Flow Map            = Visual traffic graph; Applications appear as named nodes                       │
│  Green Status        = Data source successfully syncing; last seen < 15 minutes ago                   │
│  Service Account     = Dedicated read-only account used by vRNI for API polling                       │
│  LDAP Credential     = Directory service account for vRNI group-based auth mapping                    │
│  Test Connection     = vRNI built-in check that validates API reachability + auth                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Verify in AON within 5–10 minutes:

```bash
# AON UI search
flows where source = physical and time_range = "last 15 minutes"
```

On the Collector VM:

```bash
sudo tcpdump -i eth0 -n udp port 2055 -c 20
```

## Run Microsegmentation Analysis for an Application

### Step 1: Define the Application

Plan & Assess → Applications → Add Application

- **Name**: `CRM-App`
- **Membership**: add tiers by:
  - VM name contains: `crm-`
  - or NSX tag = `App:CRM`
  - or IP subnet = `10.10.30.0/24`

### Step 2: Wait for Baseline Traffic

AON recommends a minimum 30-day observation period. For a preliminary view, 7 days is acceptable with reduced recommendation quality.

Check the observation window in the application detail view: Plan & Assess → Applications → CRM-App → Flows tab.

### Step 3: View Observed Flows

In the application view, review:
- **Intra-tier flows**: within the same tier (expected — do not need to be allowed explicitly in a zero-trust model unless required)
- **Inter-tier flows**: between tiers (e.g., web → app, app → db)
- **External flows**: to/from IPs outside the application definition

Filter flows:
```text
flows where destination application = "CRM-App" and destination port = 3306
flows where source application = "CRM-App" and destination = internet
```

### Step 4: Generate Recommendations

Plan & Assess → Micro-Segmentation → select CRM-App → View Recommendations

AON presents:
- Recommended security groups (membership lists)
- Recommended DFW rules (source group, destination group, ports, action)
- Flows that would be **allowed** vs **blocked** by the recommendation

Review carefully — recommendations are based on observed traffic, which may include diagnostic or management flows that should be excluded.

### Step 5: Export or Push to NSX

**Export to CSV/JSON:**
Recommendations tab → Export → CSV or JSON

**Push directly to NSX-T:**
Recommendations tab → Export to NSX → Select target NSX-T Manager → Confirm

AON will create:
1. NSX security groups with the recommended VM membership
2. DFW rules in a new policy section named `AON-<AppName>`

## Export Security Group Recommendations to NSX

```bash
TOKEN="<your-token>"
PLATFORM="https://aon.example.local"

# Get application ID
APP_ID=$(curl -sk "${PLATFORM}/api/ni/groups/applications" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -c "
import sys,json
for a in json.load(sys.stdin).get('results',[]):
    if a.get('name') == 'CRM-App':
        print(a['entity_id'])
")

echo "App ID: $APP_ID"

# Get NSX-T data source ID
NSX_ID=$(curl -sk "${PLATFORM}/api/ni/datasources" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -c "
import sys,json
for d in json.load(sys.stdin).get('results',[]):
    if 'NSX' in d.get('datasource_type','') and d.get('enabled'):
        print(d['entity_id'])
        break
")

echo "NSX DS ID: $NSX_ID"

# Push recommendations to NSX
curl -sk -X POST "${PLATFORM}/api/ni/applications/${APP_ID}/security-groups/export" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"nsx_manager_id\": \"${NSX_ID}\"}" \
  | python3 -m json.tool
```

## Create a Saved Search / Alert

### Saved Search

1. Enter a search query in the search bar:
```sql
   flows where destination port = 22 and flow type = North-South
   ```
2. Click **Save** → enter a name: `External-SSH-Flows`
3. Saved searches appear under Home → Saved Searches

### Alert / Pinned Notification

Settings → Alerts → Add Alert

| Field | Value |
|---|---|
| Name | `Critical-Flows-SSH-External` |
| Condition | Search query: `flows where destination port = 22 and source = internet` |
| Threshold | Count > 0 |
| Severity | Critical |
| Notification | Email / Webhook / Syslog |

Alerts fire when the condition remains true for the configured duration.

## Generate Compliance Report

Plan & Assess → Compliance → select a compliance framework:

- **PCI DSS**: checks for cardholder data environment segmentation
- **HIPAA**: checks for PHI data flow segmentation
- **NIST**: checks for segmentation consistent with NIST SP 800-53

Select the framework → Select scope (application or tag group) → Generate Report

The report outputs:
- Compliant controls (green)
- Non-compliant controls (red) with finding details
- Recommended remediation actions

Export the report: Reports → Download PDF or CSV.

**Via API (compliance checks):**

```bash
curl -sk -X POST "${PLATFORM}/api/ni/compliance/check" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "compliance_template": "PCI_DSS",
    "scope": {"application_id": "application-12345"}
  }' | python3 -m json.tool
```

## Decommission a Collector

When removing a site or replacing a Collector VM:

1. **Re-associate data sources** to a different Collector (if applicable):

   Settings → Accounts and Data Sources → select vCenter/NSX source → Edit → change Collector

2. **Remove the Collector from the Platform:**

   Settings → Accounts and Data Sources → Collectors → select Collector → Delete

   All data sources assigned to this Collector will stop syncing until re-assigned.

3. **Power off and delete the Collector VM** from vCenter.

```bash
# Verify no data sources remain assigned to the Collector being decommissioned
COLLECTOR_ID="collector-001"

curl -sk "${PLATFORM}/api/ni/datasources" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -c "
import sys,json
for d in json.load(sys.stdin).get('results',[]):
    if d.get('collector_id') == '${COLLECTOR_ID}':
        print(f\"WARNING: {d.get('nickname')} still assigned to this collector\")
"
```

## Force Data Source Re-Sync

If a data source is stale and waiting for the next polling interval:

Settings → Accounts and Data Sources → select source → Actions → Sync Now

Via API:

```bash
DS_ID="datasource-vcenter-001"

curl -sk -X POST "${PLATFORM}/api/ni/datasources/${DS_ID}/sync" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -m json.tool
```
