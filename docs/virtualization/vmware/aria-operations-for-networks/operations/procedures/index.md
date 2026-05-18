# Aria Operations for Networks — Procedures

```
┌──────────── Aria Networks Operational Procedure Flow ──────────────────────────┐
│                                                                                 │
│  Add data source (vCenter / NSX-T / physical switch)                            │
│  Settings ► Accounts and Data Sources ► Add Source ► Validate ► Submit          │
│  Verify: Last Sync timestamp < 20 min │ search for hosts/segments               │
│       │                                                                         │
│       ▼                                                                         │
│  Configure NetFlow/IPFIX (physical switches)                                    │
│  Switch: define exporter ► flow record ► monitor ► apply to interfaces          │
│  Collector: tcpdump -i eth0 udp port 2055 ── confirm packets arriving           │
│       │                                                                         │
│       ▼                                                                         │
│  Microsegmentation analysis                                                     │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  Define application (VM names / NSX tags / subnets)                     │   │
│  │  Observe 7–30 days ► View Flows tab ► intra/inter-tier/external         │   │
│  │  Plan & Assess ► Recommendations ► review ► Export CSV or Push to NSX  │    │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│       │                                                                         │
│       ▼                                                                         │
│  Alerts / compliance reports                                                    │
│  Saved search ► Alert (threshold + notification) │ Compliance framework PDF    │
└────────────────────────────────────────────────────────────────────────────────┘
```

## Add a New vCenter Data Source

1. Settings → Accounts and Data Sources → Add Source → vCenter Server
2. Fill in:
   - **Nickname**: descriptive label (e.g., `vCenter-ProdDC`)
   - **vCenter IP/FQDN**: `vcenter.corp.local`
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
PLATFORM="https://aon.corp.local"

curl -sk -X POST "${PLATFORM}/api/ni/datasources/vcenter" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "nickname": "vCenter-ProdDC",
    "credentials": {
      "ip": "vcenter.corp.local",
      "username": "svc-aon@vsphere.local",
      "password": "PASSWORD"
    },
    "collector_id": "collector-001",
    "enabled": true
  }' | python3 -m json.tool
```

## Add NSX-T Manager Data Source

1. Settings → Accounts and Data Sources → Add Source → NSX-T Manager
2. Fill in:
   - **Nickname**: `NSX-T-ProdDC`
   - **NSX-T Manager IP/FQDN**: `nsxmgr.corp.local`
   - **Username**: `svc-aon` (Auditor role)
   - **Password**: —
   - **Collector**: same Collector as the associated vCenter
3. Click **Validate** → **Submit**

Post-add verification:
- Settings → Accounts and Data Sources → NSX-T-ProdDC → Last Sync should show < 15 minutes ago
- Search bar: `NSX-T Logical Switches` or `segments` — should return segment list

```bash
curl -sk -X POST "${PLATFORM}/api/ni/datasources/nsxt" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "nickname": "NSX-T-ProdDC",
    "credentials": {
      "ip": "nsxmgr.corp.local",
      "username": "svc-aon",
      "password": "PASSWORD"
    },
    "collector_id": "collector-001",
    "enabled": true
  }' | python3 -m json.tool
```

## Configure NetFlow Export from a Cisco Switch

This procedure targets Cisco IOS-XE. See the Integrations page for NX-OS and Arista.

```ios
! On the Cisco switch — replace 10.10.10.51 with your Collector VM IP

flow exporter AON-EXPORTER
 destination 10.10.10.51
 source GigabitEthernet0/0/0
 transport udp 2055
 export-protocol netflow-v9
 template data timeout 60

flow record AON-RECORD
 match ipv4 source address
 match ipv4 destination address
 match transport source-port
 match transport destination-port
 match ip protocol
 collect counter bytes long
 collect counter packets long
 collect timestamp sys-uptime first
 collect timestamp sys-uptime last

flow monitor AON-MONITOR
 exporter AON-EXPORTER
 cache timeout active 60
 cache timeout inactive 15
 record AON-RECORD

interface GigabitEthernet1/0/1
 ip flow monitor AON-MONITOR input
 ip flow monitor AON-MONITOR output
```

Verify in AON within 5–10 minutes:

```
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
```
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
PLATFORM="https://aon.corp.local"

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
   ```
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
