# Confluence — Scripts

Production-ready scripts for Confluence administration. All scripts assume a Data Center deployment with PostgreSQL. Set environment variables before running.

---

## Environment Setup

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

---

## 1. Space Export Automation

Exports all spaces to XML format and uploads to S3. Safe to run while Confluence is live.

```bash
#!/bin/bash
# space-export-all.sh
# Exports every space to XML and stores in $BACKUP_DIR/spaces/

set -euo pipefail

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
EXPORT_DIR="${BACKUP_DIR}/spaces/${TIMESTAMP}"
mkdir -p "$EXPORT_DIR"
LOG="${EXPORT_DIR}/export.log"

echo "[$(date)] Starting space export" | tee -a "$LOG"

# Fetch all space keys
spaces=$(curl -sf \
  -H "Authorization: Bearer $CF_TOKEN" \
  "${CF_URL}/rest/api/space?limit=500" \
  | jq -r '.results[].key')

TOTAL=$(echo "$spaces" | wc -l)
COUNT=0

for space in $spaces; do
  COUNT=$((COUNT + 1))
  echo "[$(date)] [$COUNT/$TOTAL] Exporting space: $space" | tee -a "$LOG"

  # Trigger export
  resp=$(curl -sf -X POST \
    -H "Authorization: Bearer $CF_TOKEN" \
    -H "Content-Type: application/json" \
    "${CF_URL}/rest/api/space/${space}/export" \
    -d '{"type": "xml"}')

  download_url=$(echo "$resp" | jq -r '.url // empty')
  if [ -z "$download_url" ]; then
    echo "[$(date)] WARN: No download URL for $space — skipping" | tee -a "$LOG"
    continue
  fi

  # Download the ZIP
  curl -sf -H "Authorization: Bearer $CF_TOKEN" \
    "${CF_URL}${download_url}" \
    --output "${EXPORT_DIR}/${space}.zip"

  echo "[$(date)] Saved: ${EXPORT_DIR}/${space}.zip" | tee -a "$LOG"
done

# Upload to S3
if command -v aws &>/dev/null; then
  aws s3 sync "$EXPORT_DIR" "s3://company-confluence-backups/spaces/${TIMESTAMP}/" \
    --sse aws:kms \
    --kms-key-id alias/confluence-backup-key
  echo "[$(date)] Uploaded to S3" | tee -a "$LOG"
fi

echo "[$(date)] Space export complete. $COUNT spaces processed." | tee -a "$LOG"
```

---

## 2. User Sync Report

Compares users in Confluence against Active Directory to find orphaned accounts.

```python
#!/usr/bin/env python3
# user-sync-report.py
# Outputs CSV of Confluence users not present in LDAP

import csv
import json
import sys
import ldap3
import requests
from datetime import datetime

CF_URL   = "https://confluence.example.com"
CF_TOKEN = "<PAT>"
LDAP_URL = "ldaps://dc01.example.com:636"
LDAP_BASE = "DC=example,DC=com"
LDAP_USER = "CN=svc-confluence,OU=Services,DC=example,DC=com"
LDAP_PASS = "<service-account-password>"
OUTPUT    = f"user_sync_report_{datetime.now().strftime('%Y%m%d')}.csv"

def get_confluence_users():
    users = []
    start = 0
    limit = 200
    while True:
        resp = requests.get(
            f"{CF_URL}/rest/api/user/list",
            headers={"Authorization": f"Bearer {CF_TOKEN}"},
            params={"start": start, "limit": limit},
        )
        resp.raise_for_status()
        data = resp.json()
        batch = data.get("results", [])
        users.extend(batch)
        if len(batch) < limit:
            break
        start += limit
    return users

def get_ldap_sAMAccountNames():
    server = ldap3.Server(LDAP_URL, use_ssl=True)
    conn   = ldap3.Connection(server, user=LDAP_USER, password=LDAP_PASS, auto_bind=True)
    conn.search(
        search_base=LDAP_BASE,
        search_filter="(&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))",
        attributes=["sAMAccountName"],
    )
    return {str(e.sAMAccountName).lower() for e in conn.entries}

cf_users   = get_confluence_users()
ldap_users = get_ldap_sAMAccountNames()

with open(OUTPUT, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["username", "display_name", "email", "status", "in_ldap"])
    for u in cf_users:
        username = u.get("username", "").lower()
        in_ldap  = username in ldap_users
        writer.writerow([
            username,
            u.get("displayName"),
            u.get("email"),
            u.get("type"),
            in_ldap,
        ])

print(f"Report written: {OUTPUT}")
print(f"Total Confluence users: {len(cf_users)}")
print(f"Not in LDAP: {sum(1 for u in cf_users if u.get('username','').lower() not in ldap_users)}")
```

---

## 3. Stale Page Cleanup

Identifies and optionally trashes pages not modified in N days. Outputs a report; requires `--execute` flag to actually trash.

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

---

## 4. Audit Log Export

Exports the Confluence audit log to CSV for compliance or SIEM ingestion.

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

---

## 5. Disk Usage Report

Breaks down shared home disk usage by category and alerts if any exceeds threshold.

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

---

## 6. REST API Token Rotation

Rotates Confluence Personal Access Tokens for service accounts. Requires the v2 API (Confluence 8.x+).

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

---

## 7. Space Permission Audit

Reports all space-level permissions across all spaces — useful for quarterly access reviews.

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
