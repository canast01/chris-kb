---
tags:
  - operations
  - servicenow
---
# ServiceNow — CLI Reference

```bash
export INSTANCE="https://mycompany.service-now.com"
export USER="api_user"
export PASS="your-password"
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bash: export: `your-password': not a valid identifier` | Wrap the password in quotes if it contains special characters: `export PASS="your-password"` or use single quotes for literal strings. |
    | `bash: mycompany.service-now.com: command not found` | Remove the protocol from the INSTANCE variable or wrap the full URL in quotes: `export INSTANCE="https://mycompany.service-now.com"`. |
```bash
# Create an incident
curl -s -u "$USER:$PASS" \
  -X POST \
  "$INSTANCE/api/now/table/incident" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "short_description": "Database connectivity failure",
    "impact": "1",
    "urgency": "1",
    "category": "database",
    "assignment_group": "Database Operations",
    "caller_id": "john.doe@example.com"
  }' | jq '.result | {sys_id, number}'
```

```text title="Expected output"
{
  "sys_id": "d4c1a2f3b5e8c9d2a1f4e7b3c6d9a2f5",
  "number": "INC0010847"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to servicenow-instance.service-now.com port 443: Connection refused` | Verify the `$INSTANCE` variable is set correctly and the ServiceNow instance is accessible (e.g., `echo $INSTANCE`). |
    | `{"error":{"message":"Invalid field value","detail":"Invalid value for field 'impact': must be between 1 and 5"},"status":"failure"}` | Ensure all field values conform to ServiceNow's constraints; check the incident table schema for valid impact/urgency ranges. |
    | `jq: parse error: Cannot index number with string "sys_id"` | Verify the API response contains a `result` object by testing without the jq filter first (`curl ... | jq '.'`) to inspect the full response structure. |
```bash
# Assign an incident to a user and update state to In Progress
curl -s -u "$USER:$PASS" \
  -X PATCH \
  "$INSTANCE/api/now/table/incident/abc123def456abc123def456abc12345" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "state": "2",
    "assigned_to": "jane.smith",
    "work_notes": "Investigating database logs"
  }' | jq '.result.number'
```

```text title="Expected output"
INC0012847
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to instance.service-now.com port 443: Connection timed out` | Verify the $INSTANCE variable is set correctly and the ServiceNow instance is accessible from your network. |
    | `{"error":{"message":"Invalid table API id","status":"failure"}}` | Confirm the incident sys_id (abc123def456abc123def456abc12345) exists and is valid by querying the incident table first. |
    | `jq: parse error: Cannot index string with string "result"` | Remove the `| jq '.result.number'` pipe if the API response is not JSON-formatted, or check that the PATCH request succeeded with a 200 status code. |
```bash
# Delete a record (use with caution; prefer closing/cancelling)
curl -s -u "$USER:$PASS" \
  -X DELETE \
  "$INSTANCE/api/now/table/incident/abc123def456abc123def456abc12345" \
  -o /dev/null -w "%{http_code}"
# Expected: 204
```

```text title="Expected output"
204
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to instance.service-now.com port 443: Connection timed out` | Verify the `$INSTANCE` variable is set correctly and the ServiceNow instance is accessible from your network. |
    | `{"error":{"message":"Invalid table API DELETE not allowed","status":"failure"}}` | Check that the table allows DELETE operations in its ACL configuration; some tables restrict deletion for compliance reasons. |
    | `401 Unauthorized` | Ensure `$USER` and `$PASS` credentials are valid and the user has the `rest_api_explorer` or appropriate delete role assigned in ServiceNow. |
```bash
# Count open incidents by priority
curl -s -u "$USER:$PASS" \
  "$INSTANCE/api/now/stats/incident?sysparm_query=active=true&sysparm_count=true&sysparm_group_by=priority" \
  -H "Accept: application/json" | jq '.result.stats'
```

```text title="Expected output"
[
  {
    "priority": "1",
    "count": "23"
  },
  {
    "priority": "2",
    "count": "87"
  },
  {
    "priority": "3",
    "count": "156"
  },
  {
    "priority": "4",
    "count": "312"
  },
  {
    "priority": "5",
    "count": "428"
  }
]
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to instance.service-now.com port 443: Connection timed out` | Verify the `$INSTANCE` variable is set correctly and the ServiceNow instance is accessible from your network. |
    | `jq: parse error: Invalid JSON text at line 1` | Remove the `-H "Accept: application/json"` header or ensure the API endpoint returns valid JSON; some ServiceNow versions require `Content-Type` instead. |
    | `401 Unauthorized` | Verify that `$USER` and `$PASS` credentials are correct and the user account has API access permissions in ServiceNow. |
```bash
# Average resolution time for P1 incidents closed this month
curl -s -u "$USER:$PASS" \
  "$INSTANCE/api/now/stats/incident?sysparm_query=priority=1^resolved_atONThis month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()&sysparm_avg_fields=resolve_time" \
  -H "Accept: application/json" | jq .
```

```text title="Expected output"
{
  "result": {
    "stats": [
      {
        "count": "12",
        "sum": "432000",
        "average": "36000",
        "minimum": "1800",
        "maximum": "86400",
        "table": "incident"
      }
    ],
    "query": "priority=1^resolved_atONThis month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()",
    "offset": "0"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to instance.service-now.com port 443: Connection refused` | Verify the `$INSTANCE` variable is set correctly (e.g., `export INSTANCE="https://dev12345.service-now.com"`) and the instance is accessible. |
    | `{"error":{"message":"Invalid table API. (Hint: allowed tables are ...)","status":"failure"}}` | Confirm the `/api/now/stats/` endpoint is available in your ServiceNow version; use `/api/now/table/incident` with aggregation parameters as an alternative. |
    | `jq: parse error: Invalid numeric literal at line 1 column 10` | Remove the `-s` flag or check that the API response is valid JSON; add `-v` to curl to debug the raw response. |
```bash
# Push a CI record to the import set staging table
curl -s -u "$USER:$PASS" \
  -X POST \
  "$INSTANCE/api/now/import/u_import_cmdb_server" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "u_name": "LON-SRV-WEB-01",
    "u_ip_address": "10.10.1.50",
    "u_os": "RHEL 9",
    "u_environment": "production",
    "u_support_group": "Linux Operations"
  }' | jq '.result | {status, sys_id}'
```
```python
import requests
from requests.auth import HTTPBasicAuth
import os

INSTANCE = os.environ["SN_INSTANCE"]  # https://mycompany.service-now.com
AUTH = HTTPBasicAuth(os.environ["SN_USER"], os.environ["SN_PASS"])
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

session = requests.Session()
session.auth = AUTH
session.headers.update(HEADERS)
```
```python
def get_open_p1_incidents():
    url = f"{INSTANCE}/api/now/table/incident"
    params = {
        "sysparm_query": "priority=1^active=true",
        "sysparm_fields": "number,short_description,assigned_to,sys_created_on",
        "sysparm_display_value": "true",
        "sysparm_limit": 50,
    }
    response = session.get(url, params=params)
    response.raise_for_status()
    return response.json()["result"]

for inc in get_open_p1_incidents():
    print(f"{inc['number']}: {inc['short_description']} — {inc['assigned_to']['display_value']}")
```
```python
def create_change_request(short_desc: str, description: str, assignment_group: str) -> dict:
    url = f"{INSTANCE}/api/now/table/change_request"
    payload = {
        "short_description": short_desc,
        "description": description,
        "type": "normal",
        "category": "Infrastructure",
        "assignment_group": assignment_group,
        "risk": "2",       # Medium
        "impact": "2",     # Department
    }
    response = session.post(url, json=payload)
    response.raise_for_status()
    result = response.json()["result"]
    print(f"Created: {result['number']} ({result['sys_id']})")
    return result
```
```python
def get_all_records(table: str, query: str, fields: str) -> list:
    url = f"{INSTANCE}/api/now/table/{table}"
    limit = 100
    offset = 0
    all_records = []

    while True:
        params = {
            "sysparm_query": query,
            "sysparm_fields": fields,
            "sysparm_limit": limit,
            "sysparm_offset": offset,
            "sysparm_exclude_reference_link": "true",
        }
        response = session.get(url, params=params)
        response.raise_for_status()
        records = response.json()["result"]
        if not records:
            break
        all_records.extend(records)
        offset += limit

    return all_records
```
```javascript
// Example: custom endpoint that returns MID Server health
// GET /api/mycompany/operations/mid_health

(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    var gr = new GlideRecord('ecc_agent');
    gr.addQuery('status', 'Up');
    gr.query();

    var midServers = [];
    while (gr.next()) {
        midServers.push({
            name: gr.getDisplayValue('name'),
            status: gr.getDisplayValue('status'),
            version: gr.getDisplayValue('mid_version'),
            last_refreshed: gr.getDisplayValue('last_refreshed')
        });
    }

    response.setStatus(200);
    response.setBody({ mid_servers: midServers, count: midServers.length });
})(request, response);
```
```bash
curl -s -u "$USER:$PASS" \
  "$INSTANCE/api/mycompany/operations/mid_health" \
  -H "Accept: application/json" | jq .
```

```text title="Expected output"
{
  "mid_servers": [
    {
      "name": "mid-prod-01",
      "status": "operational",
      "cpu_usage": 42.3,
      "memory_usage": 68.5,
      "last_heartbeat": "2024-01-15T14:32:18Z",
      "version": "v2.1.4"
    },
    {
      "name": "mid-prod-02",
      "status": "operational",
      "cpu_usage": 38.1,
      "memory_usage": 71.2,
      "last_heartbeat": "2024-01-15T14:32:22Z",
      "version": "v2.1.4"
    },
    {
      "name": "mid-dr-01",
      "status": "degraded",
      "cpu_usage": 89.7,
      "memory_usage": 92.1,
      "last_heartbeat": "2024-01-15T14:28:45Z",
      "version": "v2.1.3"
    }
  ],
  "summary": {
    "total_servers": 3,
    "operational": 2,
    "degraded": 1,
    "offline": 0
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (7) Failed to connect to instance.service-now.com port 443: Connection refused` | Verify the $INSTANCE variable is set correctly and the ServiceNow instance is accessible from your network. |
    | `jq: parse error: Invalid JSON text at line 1` | Remove the `-s` flag temporarily to see the actual response; the API may be returning an error page or HTML instead of JSON. |
    | `curl: (401) Unauthorized` | Ensure $USER and $PASS credentials are correct and the API user has the `mycompany_operations_read` role in ServiceNow. |
```bash
# macOS via Homebrew
brew install servicenow-cli

# Or download from developer.servicenow.com/dev.do#!/downloads
```

```text title="Expected output"
==> Downloading https://github.com/ServiceNow/servicenow-cli/releases/download/v2.4.1/servicenow-cli-2.4.1.tar.gz
==> Downloading from https://ghcr.io/v2/servicenow/servicenow-cli
######################################################################## 100.0%
==> Installing servicenow-cli
==> Pouring servicenow-cli--2.4.1.arm64_monterey.bottle.tar.gz
🍺  /usr/local/Cellar/servicenow-cli/2.4.1 is now installed
servicenow-cli 2.4.1 installed successfully
Run 'snow --version' to verify installation
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: servicenow-cli: no bottle available for this macOS version` | Update Homebrew with `brew update` and try again, or install from developer.servicenow.com directly. |
    | `Error: Permission denied @ rb_sysopen - /usr/local/Cellar/servicenow-cli` | Run the command with `sudo brew install servicenow-cli` or fix Homebrew permissions with `sudo chown -R $(whoami) /usr/local/Cellar`. |
```bash
snc configure profile set \
  --profile production \
  --url https://mycompany.service-now.com \
  --username api_user \
  --password "$SN_PASS"

snc configure profile activate --profile production
```

```text title="Expected output"
Profile 'production' configured successfully
  URL: https://mycompany.service-now.com
  Username: api_user
  Instance: mycompany

Profile 'production' activated
Active profile: production
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Invalid URL format. Expected https://[instance].service-now.com` | Verify the URL matches the correct ServiceNow instance domain format without trailing slashes. |
    | `Error: Authentication failed - Invalid credentials` | Confirm the API user account exists, is active, and the password stored in $SN_PASS is correct and not expired. |
    | `Error: Profile 'production' not found` | Ensure the profile was successfully created in the first command before attempting to activate it; check with `snc configure profile list`. |
```bash
# Verify connectivity
snc instance info

# List available plugin versions
snc plugin list --available

# Install a plugin
snc plugin install com.snc.change_management

# Retrieve an Update Set
snc update-set retrieve --name "Sprint-2026-Q2"

# Export Update Set to XML
snc update-set export --name "Sprint-2026-Q2" --output ./exports/

# Import an Update Set XML to a target instance
snc update-set import --file ./exports/sprint-2026-q2.xml --profile dev

# Execute a background script
snc script run --file ./scripts/bulk_close_incidents.js

# ATF test suite execution
snc atf run --suite "ITSM Regression Suite"
```
```yaml
- name: Deploy Update Set to UAT
  run: |
    snc configure profile set \
      --profile uat \
      --url ${{ secrets.SN_UAT_URL }} \
      --username ${{ secrets.SN_USER }} \
      --password ${{ secrets.SN_PASS }}
    snc update-set import \
      --file ./exports/latest.xml \
      --profile uat \
      --preview-only false
```
```bash
# Obtain token
TOKEN=$(curl -s -X POST \
  "$INSTANCE/oauth_token.do" \
  -d "grant_type=password" \
  -d "client_id=$SN_CLIENT_ID" \
  -d "client_secret=$SN_CLIENT_SECRET" \
  -d "username=$USER" \
  -d "password=$PASS" | jq -r '.access_token')

# Use token
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  "$INSTANCE/api/now/table/incident?sysparm_limit=5" | jq '.result[].number'
```

```d2
direction: down

verify: "Verify" {shape: rectangle}

```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Servicenow — Procedures](../procedures/)
- [Servicenow — Scripts](../scripts/)
- [Servicenow — Health Checks](../health-checks/)
