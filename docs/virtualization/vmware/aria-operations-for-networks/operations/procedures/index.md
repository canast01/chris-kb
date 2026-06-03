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
```

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
```bash
# AON UI search
flows where source = physical and time_range = "last 15 minutes"
```
```bash
sudo tcpdump -i eth0 -n udp port 2055 -c 20
```
```text
flows where destination application = "CRM-App" and destination port = 3306
flows where source application = "CRM-App" and destination = internet
```
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

```

```bash
curl -sk -X POST "${PLATFORM}/api/ni/compliance/check" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "compliance_template": "PCI_DSS",
    "scope": {"application_id": "application-12345"}
  }' | python3 -m json.tool
```
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
```bash
DS_ID="datasource-vcenter-001"

curl -sk -X POST "${PLATFORM}/api/ni/datasources/${DS_ID}/sync" \
  -H "Authorization: NetworkInsight ${TOKEN}" \
  | python3 -m json.tool
```
