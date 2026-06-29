---
tags:
  - confluence
  - operations
---
# Confluence — Operations Scripts

```bash
# Common variables — set these in your shell or CI/CD environment
export CF_URL="https://confluence.example.com"
export CF_TOKEN="<personal-access-token>"
export DB_HOST="db.internal.example.com"
export DB_PORT="5432"
export DB_NAME="confluencedb"
export DB_USER="confluence"
export PGPASSWORD="<db-password>"
export SHARED_HOME="/mnt/confluence-shared"
export BACKUP_DIR="/backup/confluence"
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`bash: CF_TOKEN: command not found`** — Ensure you're using `export` syntax correctly and that the token value is quoted if it contains special characters.
    **`bash: PGPASSWORD: Syntax error near unexpected token '<'`** — Replace `<db-password>` and `<personal-access-token>` with actual values; literal angle brackets are not valid in variable assignments.
```bash
#!/bin/bash
# stale-page-cleanup.sh
# Usage: ./stale-page-cleanup.sh [--execute]
# Without --execute: dry run (report only)

DAYS=730        # Pages older than 2 years
SPACE="ARCHIVE" # Limit to one space (or remove for all spaces)
EXECUTE=false
[ "${1:-}" == "--execute" ] && EXECUTE=true

CQL="space=${SPACE}+AND+type=page+AND+lastModified+<%3D+-${DAYS}d"
REPORT="stale_pages_$(date +%Y%m%d).csv"

echo "page_id,title,space,last_modified,url" > "$REPORT"

start=0; limit=50
while true; do
  resp=$(curl -sf \
    -H "Authorization: Bearer $CF_TOKEN" \
    "${CF_URL}/rest/api/content/search?cql=${CQL}&limit=${limit}&start=${start}&expand=version,space")
  
  count=$(echo "$resp" | jq '.results | length')
  [ "$count" -eq 0 ] && break

  echo "$resp" | jq -r '.results[] | [.id, .title, .space.key, .version.when, ._links.webui] | @csv' \
    >> "$REPORT"

  if [ "$EXECUTE" == "true" ]; then
    page_ids=$(echo "$resp" | jq -r '.results[].id')
    for pid in $page_ids; do
      echo "Trashing page: $pid"
      curl -sf -X DELETE \
        -H "Authorization: Bearer $CF_TOKEN" \
        "${CF_URL}/rest/api/content/${pid}"
    done
  fi

  start=$((start + limit))
done

echo "Report: $REPORT"
[ "$EXECUTE" == "false" ] && echo "DRY RUN — use --execute to trash pages"
```

```text title="Expected output"
page_id,title,space,last_modified,url
123456,"Legacy Q1 2022 Meeting Notes",ARCHIVE,"2022-03-15T09:42:31.000Z","/wiki/spaces/ARCHIVE/pages/123456"
123457,"Deprecated Build Process v3",ARCHIVE,"2022-01-22T14:18:05.000Z","/wiki/spaces/ARCHIVE/pages/123457"
123458,"Old Vendor Integration Docs",ARCHIVE,"2021-11-08T11:33:22.000Z","/wiki/spaces/ARCHIVE/pages/123458"
123459,"2021 Infrastructure Runbooks",ARCHIVE,"2021-09-30T16:45:10.000Z","/wiki/spaces/ARCHIVE/pages/123459"
123460,"Retired API v2 Reference",ARCHIVE,"2021-07-14T08:12:44.000Z","/wiki/spaces/ARCHIVE/pages/123460"
Report: stale_pages_20250117.csv
DRY RUN — use --execute to trash pages
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to host`** — Verify `$CF_URL` is set correctly and Confluence server is reachable (e.g., `echo $CF_URL`).
    **`jq: parse error: Invalid JSON text at line 1`** — Confirm `$CF_TOKEN` is valid and has API access; an auth failure returns HTML instead of JSON.
    **`curl: (22) HTTP 403`** — Ensure the bearer token has `delete:content` permission in Confluence; request elevated access if needed.
```bash
#!/bin/bash
# audit-log-export.sh
# Exports audit events for the past N days to CSV

DAYS=30
OUTPUT="confluence_audit_$(date +%Y%m%d).csv"
START_EPOCH=$(( $(date +%s) - DAYS * 86400 ))
START_MS=$((START_EPOCH * 1000))

echo "timestamp,author,remote_addr,category,summary,description" > "$OUTPUT"

start=0; limit=200
while true; do
  resp=$(curl -sf \
    -H "Authorization: Bearer $CF_TOKEN" \
    "${CF_URL}/rest/api/audit?startDate=${START_MS}&limit=${limit}&start=${start}")

  count=$(echo "$resp" | jq '.results | length')
  [ "$count" -eq 0 ] && break

  echo "$resp" | jq -r '.results[] | [
    .creationDate,
    (.author.name // "system"),
    (.remoteAddress // ""),
    (.category // ""),
    (.summary // ""),
    (.description // "")
  ] | @csv' >> "$OUTPUT"

  start=$((start + limit))
done

echo "Audit log exported: $OUTPUT ($(wc -l < "$OUTPUT") records)"
```

```text title="Expected output"
Audit log exported: confluence_audit_20240115.csv (1247 records)
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443: Connection refused`** — Verify the CF_URL environment variable is set correctly and the Confluence instance is running and accessible.
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure CF_TOKEN is valid and has audit API permissions; an authentication error returns HTML instead of JSON.
    **`wc: confluence_audit_20240115.csv: No such file or directory`** — Check that the script has write permissions in the current directory and sufficient disk space.
```bash
#!/bin/bash
# disk-usage-report.sh

SHARED_HOME="/mnt/confluence-shared"
WARN_GB=100   # Warn if any single category exceeds this
OUTPUT="disk_report_$(date +%Y%m%d).txt"

{
  echo "Confluence Disk Usage Report — $(date)"
  echo "======================================="
  echo ""
  echo "Total shared home:"
  du -sh "$SHARED_HOME" 2>/dev/null
  echo ""
  echo "By category:"
  du -sh "${SHARED_HOME}/"* 2>/dev/null | sort -rh
  echo ""
  echo "Attachment breakdown (top 20 spaces):"
  du -sh "${SHARED_HOME}/attachments/"* 2>/dev/null | sort -rh | head -20
  echo ""
  echo "Database size:"
  psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t \
    -c "SELECT pg_size_pretty(pg_database_size('${DB_NAME}'));"
  echo ""
  echo "Largest tables in database:"
  psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t \
    -c "SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename::regclass))
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY pg_total_relation_size(tablename::regclass) DESC
        LIMIT 15;"
} | tee "$OUTPUT"

echo "Report saved: $OUTPUT"
```
```python
#!/usr/bin/env python3
# token-rotation.py
# Creates a new PAT, validates it, updates the secret store, revokes the old token

import requests
import json
import subprocess
import sys
from datetime import datetime, timedelta

CF_URL       = "https://confluence.example.com"
ADMIN_USER   = "svc-confluence-admin"
ADMIN_TOKEN  = "<current-admin-PAT>"   # Bootstrap token
TARGET_USER  = "svc-automation"
SECRET_NAME  = "confluence/svc-automation/pat"   # AWS Secrets Manager path
TOKEN_TTL    = 90  # Days

HEADERS = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type":  "application/json",
}

def create_token(name: str, expiry_days: int) -> dict:
    expiry = (datetime.utcnow() + timedelta(days=expiry_days)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    resp = requests.post(
        f"{CF_URL}/rest/pat/latest/tokens",
        headers=HEADERS,
        json={"name": name, "expiringAt": expiry},
    )
    resp.raise_for_status()
    return resp.json()

def list_tokens() -> list:
    resp = requests.get(f"{CF_URL}/rest/pat/latest/tokens", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def revoke_token(token_id: str):
    resp = requests.delete(f"{CF_URL}/rest/pat/latest/tokens/{token_id}", headers=HEADERS)
    resp.raise_for_status()

def validate_token(new_token: str) -> bool:
    resp = requests.get(
        f"{CF_URL}/rest/api/user/current",
        headers={"Authorization": f"Bearer {new_token}"},
    )
    return resp.status_code == 200

def update_secret(token_value: str):
    subprocess.run(
        ["aws", "secretsmanager", "put-secret-value",
         "--secret-id", SECRET_NAME,
         "--secret-string", json.dumps({"pat": token_value})],
        check=True, capture_output=True,
    )

# 1. Create new token
token_name = f"svc-automation-{datetime.utcnow().strftime('%Y%m%d')}"
new_token_data = create_token(token_name, TOKEN_TTL)
new_token_value = new_token_data["token"]
new_token_id    = new_token_data["id"]
print(f"Created token: {token_name} (ID: {new_token_id})")

# 2. Validate
if not validate_token(new_token_value):
    print("ERROR: New token validation failed — aborting rotation")
    revoke_token(new_token_id)
    sys.exit(1)
print("Token validated successfully")

# 3. Update secret store
update_secret(new_token_value)
print(f"Secret updated: {SECRET_NAME}")

# 4. Revoke old tokens with the same prefix
tokens = list_tokens()
for t in tokens:
    if t["name"].startswith("svc-automation-") and t["id"] != new_token_id:
        print(f"Revoking old token: {t['name']} (ID: {t['id']})")
        revoke_token(t["id"])

print("Token rotation complete")
```
```bash
#!/bin/bash
# space-permission-audit.sh

OUTPUT="space_permissions_$(date +%Y%m%d).csv"
echo "space_key,space_name,principal_type,principal,permission" > "$OUTPUT"

spaces=$(curl -sf \
  -H "Authorization: Bearer $CF_TOKEN" \
  "${CF_URL}/rest/api/space?limit=500" \
  | jq -r '.results[] | "\(.key)\t\(.name)"')

while IFS=$'\t' read -r key name; do
  perms=$(curl -sf \
    -H "Authorization: Bearer $CF_TOKEN" \
    "${CF_URL}/rest/api/space/${key}/permission")

  echo "$perms" | jq -r --arg k "$key" --arg n "$name" \
    '.permissions[] | [$k, $n, .subjects.user.results[]?.displayName, .operation.key] | @csv' \
    >> "$OUTPUT" 2>/dev/null

  echo "$perms" | jq -r --arg k "$key" --arg n "$name" \
    '.permissions[] | [$k, $n, "group", .subjects.group.results[]?.name, .operation.key] | @csv' \
    >> "$OUTPUT" 2>/dev/null
done <<< "$spaces"

echo "Permission audit: $OUTPUT ($(wc -l < "$OUTPUT") rows)"
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

- [Confluence — Procedures](../procedures/)
- [Confluence — CLI Reference](../cli-reference/)
- [Confluence — Health Checks](../health-checks/)
