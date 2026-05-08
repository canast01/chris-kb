# Jira — Scripts

All scripts use environment variables for credentials. Set these before running:

```bash
export JIRA_URL="https://jira.example.com"
export JIRA_USER="admin@example.com"
export JIRA_TOKEN="your-api-token"
export JIRA_DB_HOST="db.example.com"
export JIRA_DB_NAME="jiradb"
export JIRA_DB_USER="jira"
export PGPASSWORD="${JIRA_DB_PASSWORD}"
```

---

## 1. Issue Export to CSV

Exports any JQL query result to a CSV file with configurable fields.

```bash
#!/bin/bash
# jira-export-csv.sh — Export JQL results to CSV
# Usage: ./jira-export-csv.sh "project = PROJ AND status != Done" /tmp/issues.csv

JQL="${1:-project = PROJ AND status != Done}"
OUTPUT="${2:-/tmp/jira-export-$(date +%Y%m%d-%H%M%S).csv}"
FIELDS="key,summary,issuetype,status,priority,assignee,reporter,created,updated,duedate,labels,components"
MAX_RESULTS=1000
START_AT=0

echo "Exporting: ${JQL}"
echo "Output: ${OUTPUT}"

# Write CSV header
echo "Key,Summary,Issue Type,Status,Priority,Assignee,Reporter,Created,Updated,Due Date,Labels,Components" > "${OUTPUT}"

while true; do
  RESPONSE=$(curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
    -G "${JIRA_URL}/rest/api/2/search" \
    --data-urlencode "jql=${JQL}" \
    --data-urlencode "fields=${FIELDS}" \
    --data-urlencode "maxResults=${MAX_RESULTS}" \
    --data-urlencode "startAt=${START_AT}")

  TOTAL=$(echo "${RESPONSE}" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['total'])")
  COUNT=$(echo "${RESPONSE}" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['issues']))")

  if [ "${COUNT}" -eq 0 ]; then
    break
  fi

  echo "${RESPONSE}" | python3 - << 'PYEOF'
import sys, json, csv

data = json.load(sys.stdin)
writer = csv.writer(sys.stdout)

for issue in data['issues']:
    f = issue['fields']
    def safe(v, attr=None):
        if v is None:
            return ''
        if attr:
            return v.get(attr, '') if isinstance(v, dict) else ''
        return str(v)
    def list_field(v, attr='name'):
        if not v:
            return ''
        return '; '.join(i.get(attr, '') for i in v if i)

    writer.writerow([
        issue['key'],
        safe(f.get('summary')),
        safe(f.get('issuetype'), 'name'),
        safe(f.get('status'), 'name'),
        safe(f.get('priority'), 'name'),
        safe(f.get('assignee'), 'displayName'),
        safe(f.get('reporter'), 'displayName'),
        safe(f.get('created', ''))[:10],
        safe(f.get('updated', ''))[:10],
        safe(f.get('duedate', '')),
        list_field(f.get('labels', []), '__str__').replace("'", ""),
        list_field(f.get('components', [])),
    ])
PYEOF
  >> "${OUTPUT}"

  START_AT=$((START_AT + COUNT))
  echo "  Fetched ${START_AT} / ${TOTAL}"
  if [ "${START_AT}" -ge "${TOTAL}" ]; then
    break
  fi
done

LINE_COUNT=$(wc -l < "${OUTPUT}")
echo "Export complete: ${OUTPUT} (${LINE_COUNT} rows)"
```

---

## 2. User Audit Script

Lists all Jira users, their active status, group memberships, and last login.

```bash
#!/bin/bash
# jira-user-audit.sh — Export user list with status and groups
OUTPUT="/tmp/jira-user-audit-$(date +%Y%m%d).csv"
echo "Username,Display Name,Email,Active,Groups" > "${OUTPUT}"

START_AT=0
MAX_RESULTS=200

while true; do
  RESPONSE=$(curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
    "${JIRA_URL}/rest/api/2/user/search?username=.&maxResults=${MAX_RESULTS}&startAt=${START_AT}")

  COUNT=$(echo "${RESPONSE}" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")

  if [ "${COUNT}" -eq 0 ]; then
    break
  fi

  # For each user, get group membership
  USERNAMES=$(echo "${RESPONSE}" | python3 -c "
import sys, json
for u in json.load(sys.stdin):
    print(u['name'])
")

  while read -r USERNAME; do
    USER_DATA=$(curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
      "${JIRA_URL}/rest/api/2/user?username=${USERNAME}&expand=groups")

    echo "${USER_DATA}" | python3 -c "
import sys, json
u = json.load(sys.stdin)
groups = '; '.join(g['name'] for g in u.get('groups', {}).get('items', []))
print(','.join([
    u.get('name',''),
    u.get('displayName','').replace(',',''),
    u.get('emailAddress',''),
    str(u.get('active', False)),
    groups
]))
" >> "${OUTPUT}"
  done <<< "${USERNAMES}"

  START_AT=$((START_AT + COUNT))
  echo "Processed ${START_AT} users..."
done

echo "User audit saved: ${OUTPUT}"
```

### Inactive User Report (SQL)

```sql
-- Users who have not logged in for 90+ days
SELECT u.user_name, u.lower_display_name, u.email_address,
       TO_TIMESTAMP(a.attribute_value::bigint / 1000) AS last_login
FROM cwd_user u
LEFT JOIN cwd_user_attribute a
  ON u.id = a.user_id AND a.attribute_name = 'login.lastLoginMillis'
WHERE a.attribute_value IS NULL
   OR TO_TIMESTAMP(a.attribute_value::bigint / 1000) < now() - interval '90 days'
ORDER BY last_login ASC NULLS FIRST;
```

---

## 3. Bulk Issue Transition

Transitions all issues matching a JQL filter to a target workflow status.

```bash
#!/bin/bash
# jira-bulk-transition.sh — Transition all matching issues
# Usage: ./jira-bulk-transition.sh "project=PROJ AND status='To Do'" "In Progress"

JQL="$1"
TARGET_STATUS="$2"
DRY_RUN="${3:-false}"

if [ -z "${JQL}" ] || [ -z "${TARGET_STATUS}" ]; then
  echo "Usage: $0 <jql> <target-status> [dry-run=true]"
  exit 1
fi

echo "JQL:    ${JQL}"
echo "Target: ${TARGET_STATUS}"
echo "Dry run: ${DRY_RUN}"

# Fetch issue keys
KEYS=$(curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  -G "${JIRA_URL}/rest/api/2/search" \
  --data-urlencode "jql=${JQL}" \
  --data-urlencode "fields=key,status" \
  --data-urlencode "maxResults=500" \
  | python3 -c "
import sys, json
for i in json.load(sys.stdin)['issues']:
    print(i['key'])
")

TOTAL=$(echo "${KEYS}" | wc -l)
echo "Issues to transition: ${TOTAL}"

for KEY in ${KEYS}; do
  # Get available transitions for this issue
  TRANSITION_ID=$(curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
    "${JIRA_URL}/rest/api/2/issue/${KEY}/transitions" \
    | python3 -c "
import sys, json
transitions = json.load(sys.stdin)['transitions']
for t in transitions:
    if t['to']['name'].lower() == '${TARGET_STATUS}'.lower():
        print(t['id'])
        break
")

  if [ -z "${TRANSITION_ID}" ]; then
    echo "  SKIP ${KEY} — transition to '${TARGET_STATUS}' not available"
    continue
  fi

  if [ "${DRY_RUN}" = "true" ]; then
    echo "  DRY-RUN: Would transition ${KEY} using transition ID ${TRANSITION_ID}"
  else
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
      -u "${JIRA_USER}:${JIRA_TOKEN}" \
      -X POST \
      -H "Content-Type: application/json" \
      "${JIRA_URL}/rest/api/2/issue/${KEY}/transitions" \
      -d "{\"transition\": {\"id\": \"${TRANSITION_ID}\"}}")

    if [ "${HTTP_CODE}" = "204" ]; then
      echo "  OK ${KEY} → ${TARGET_STATUS}"
    else
      echo "  FAIL ${KEY} — HTTP ${HTTP_CODE}"
    fi
  fi
done
echo "Done."
```

---

## 4. Project Cleanup Script

Archives stale issues and identifies projects with no recent activity.

```bash
#!/bin/bash
# jira-project-cleanup.sh — Report stale projects and issues

OUTPUT_DIR="/tmp/jira-cleanup-$(date +%Y%m%d)"
mkdir -p "${OUTPUT_DIR}"

echo "=== Projects with no issues updated in 180+ days ==="
curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/project" \
  | python3 -c "
import sys, json
projects = json.load(sys.stdin)
print('project_key,project_name,lead')
for p in projects:
    lead = p.get('lead', {}).get('displayName', '')
    print(f\"{p['key']},{p['name'].replace(',','')},{lead}\")
" > "${OUTPUT_DIR}/all-projects.csv"

# For each project, check last activity date
while IFS=',' read -r KEY NAME LEAD; do
  [ "${KEY}" = "project_key" ] && continue
  LAST_UPDATED=$(curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
    -G "${JIRA_URL}/rest/api/2/search" \
    --data-urlencode "jql=project = ${KEY} ORDER BY updated DESC" \
    --data-urlencode "fields=updated" \
    --data-urlencode "maxResults=1" \
    | python3 -c "
import sys, json
d = json.load(sys.stdin)
issues = d.get('issues', [])
if issues:
    print(issues[0]['fields']['updated'][:10])
else:
    print('NO_ISSUES')
")
  echo "${KEY},${NAME},${LEAD},${LAST_UPDATED}" >> "${OUTPUT_DIR}/project-activity.csv"
done < "${OUTPUT_DIR}/all-projects.csv"

# Filter stale (no activity in 180 days)
python3 << 'PYEOF'
import csv
from datetime import datetime, timedelta

stale_threshold = datetime.now() - timedelta(days=180)
stale = []

with open('/tmp/jira-cleanup-$(date +%Y%m%d)/project-activity.csv') as f:
    for row in csv.reader(f):
        if len(row) < 4:
            continue
        key, name, lead, last = row
        if last == 'NO_ISSUES':
            stale.append(row + ['empty'])
        else:
            try:
                dt = datetime.strptime(last, '%Y-%m-%d')
                if dt < stale_threshold:
                    stale.append(row + ['stale'])
            except ValueError:
                pass

print(f"\nStale projects ({len(stale)}):")
for row in stale:
    print(f"  [{row[0]}] {row[1]} — last activity: {row[3]} ({row[4]})")
PYEOF
```

---

## 5. Plugin / App List Export

```bash
#!/bin/bash
# jira-plugin-list.sh — Export all installed apps with version and status
OUTPUT="/tmp/jira-plugins-$(date +%Y%m%d).csv"

curl -s -u "${JIRA_USER}:${JIRA_TOKEN}" \
  "${JIRA_URL}/rest/api/2/plugins/1.0/plugin" \
  | python3 -c "
import sys, json, csv

plugins = json.load(sys.stdin)
writer = csv.writer(sys.stdout)
writer.writerow(['Key', 'Name', 'Version', 'Enabled', 'Vendor', 'License'])

for p in sorted(plugins, key=lambda x: x.get('key','')):
    vendor = p.get('vendor', {}).get('name', '') if isinstance(p.get('vendor'), dict) else ''
    writer.writerow([
        p.get('key', ''),
        p.get('name', ''),
        p.get('version', ''),
        p.get('enabled', False),
        vendor,
        p.get('licenseState', ''),
    ])
" > "${OUTPUT}"

echo "Plugin list exported: ${OUTPUT}"
echo "Total plugins: $(wc -l < ${OUTPUT})"
echo "Enabled:  $(grep -c ',True,' ${OUTPUT})"
echo "Disabled: $(grep -c ',False,' ${OUTPUT})"
```

---

## 6. Log Rotation Automation

Jira rotates `atlassian-jira.log` automatically, but Tomcat `catalina.out` grows unbounded. Manage with `logrotate`:

```ini
# /etc/logrotate.d/jira
/opt/atlassian/jira/logs/catalina.out {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    sharedscripts
    postrotate
        # Signal Tomcat to reopen log file (not required for most Linux configs)
        /bin/kill -HUP $(cat /opt/atlassian/jira/work/catalina.pid 2>/dev/null) 2>/dev/null || true
    endscript
}

/opt/atlassian/jira/logs/atlassian-jira*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
}

/opt/atlassian/jira/logs/localhost_access_log.*.txt {
    weekly
    rotate 8
    compress
    delaycompress
    missingok
    notifempty
}
```

Test log rotation config:

```bash
logrotate --debug /etc/logrotate.d/jira
```

Archive old logs to object storage:

```bash
#!/bin/bash
# archive-logs.sh — Move logs older than 30 days to S3
LOG_DIR="/opt/atlassian/jira/logs"
S3_BUCKET="s3://your-log-archive/jira"

find "${LOG_DIR}" -name "*.gz" -mtime +30 -exec \
  aws s3 mv {} "${S3_BUCKET}/$(hostname)/" \;

echo "Log archive complete: $(date)"
```

---

## 7. JVM Heap Dump Capture

Use for diagnosing OutOfMemoryError or suspected memory leaks.

```bash
#!/bin/bash
# jira-heap-dump.sh — Capture JVM heap dump from Jira process

OUTPUT_DIR="/var/atlassian/jira-dumps"
mkdir -p "${OUTPUT_DIR}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
HEAP_FILE="${OUTPUT_DIR}/jira-heap-${TIMESTAMP}.hprof"

# Get Jira PID
JIRA_PID=$(pgrep -f 'atlassian-jira' | head -1)

if [ -z "${JIRA_PID}" ]; then
  echo "ERROR: Jira process not found"
  exit 1
fi

echo "Jira PID: ${JIRA_PID}"
echo "Capturing heap dump to: ${HEAP_FILE}"
echo "NOTE: JVM will pause briefly during dump. Expect 30-120 seconds."

# Capture heap dump (live objects only — most useful for leak analysis)
sudo -u jira jmap -dump:format=b,live,file="${HEAP_FILE}" "${JIRA_PID}"

if [ $? -eq 0 ]; then
  SIZE=$(du -sh "${HEAP_FILE}" | cut -f1)
  echo "Heap dump captured: ${HEAP_FILE} (${SIZE})"
  echo "Analyse with: jhat, Eclipse MAT, or VisualVM"
else
  echo "ERROR: Heap dump failed"
  exit 1
fi
```

### Thread Dump (No JVM Pause)

```bash
#!/bin/bash
# jira-thread-dump.sh — Capture 3 consecutive thread dumps (for deadlock/hang analysis)

JIRA_PID=$(pgrep -f 'atlassian-jira' | head -1)
OUTPUT_DIR="/var/atlassian/jira-dumps"
mkdir -p "${OUTPUT_DIR}"

for i in 1 2 3; do
  DUMP_FILE="${OUTPUT_DIR}/jira-threads-$(date +%Y%m%d-%H%M%S)-${i}.txt"
  sudo -u jira kill -3 "${JIRA_PID}"
  # Thread dump goes to catalina.out
  sleep 10
  echo "Thread dump ${i}/3 sent to catalina.out"
done

# Extract from catalina.out
grep -A 2000 "Full thread dump" /opt/atlassian/jira/logs/catalina.out \
  | tail -2000 > "${OUTPUT_DIR}/jira-thread-dump-$(date +%Y%m%d).txt"

echo "Thread dumps extracted to: ${OUTPUT_DIR}"
```

### JVM Statistics (Real-Time)

```bash
# Monitor GC in real time
JIRA_PID=$(pgrep -f 'atlassian-jira' | head -1)

# GC stats every 5 seconds
jstat -gc "${JIRA_PID}" 5000

# JVM flags in use
jcmd "${JIRA_PID}" VM.flags

# JVM heap summary
jcmd "${JIRA_PID}" GC.heap_info

# JVM system properties
jcmd "${JIRA_PID}" VM.system_properties | grep -E "jira|atlassian|java.heap|Xmx"
```
