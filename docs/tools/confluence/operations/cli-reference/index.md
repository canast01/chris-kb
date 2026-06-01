# Confluence — CLI Reference


<div class="kb-summary">
Confluence administration via command line spans three toolsets: the **Atlassian CLI** (third-party Java tool for scripted space/page operations), **REST API via curl** (direct API access), and **JVM / application administration** commands.
</div>

 This page provides ready-to-use examples for all three.

---

## REST API via curl

All examples below use a **Personal Access Token (PAT)**. Generate one at:
**Profile > Settings > Personal Access Tokens > Create Token**

```bash
# Set common variables to avoid repetition
export CF_URL="https://confluence.example.com"
export CF_TOKEN="<your-PAT-here>"
export CF_AUTH="Authorization: Bearer ${CF_TOKEN}"
```
```
┌───────────────────────────────────── Confluence — CLI Reference ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                   Confluence admin CLI — run on server as confluence OS user                  │   │
│   │             ./start-confluence.sh / ./stop-confluence.sh — start/stop application             │   │
│   │                  ./confluence.sh status — show running/stopped state and PID                  │   │
│   │                   Confluence REST API: GET /rest/api/space — list all spaces                  │   │
│   │             Confluence REST API: GET /rest/api/content?type=page — search content             │   │
│   │               pg_dump -U confluence confluence > backup.sql — PostgreSQL backup               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  SSH to Confluence server · commands run as confluence OS user · DB on separate host                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  start-confluence.sh = Script in CONFLUENCE_INSTALL/bin/ to start the app server                      │
│  stop-confluence.sh = Graceful shutdown; waits for active sessions to complete                        │
│  REST API = Confluence programmatic interface at /rest/api; auth: Basic or OAuth                      │
│  Space REST = GET /rest/api/space returns all spaces with key, name, and type                         │
│  Content REST = GET /rest/api/content; supports CQL query for filtering                               │
│  CQL = Confluence Query Language; structured search (type=page AND space=TEAM)                        │
│  pg_dump = PostgreSQL backup utility; creates SQL dump of Confluence DB                               │
│  CONFLUENCE_INSTALL = Installation directory; contains bin/, conf/, and lib/                          │
│  CONFLUENCE_HOME = Data directory; contains attachments, indexes, and backups                         │
│  Log files = CONFLUENCE_HOME/logs/atlassian-confluence.log for app events                             │
│  catalina.out = Tomcat log; CONFLUENCE_INSTALL/logs/catalina.out                                      │
│  Heap dump = -XX:+HeapDumpOnOutOfMemoryError in JVM_SUPPORT_RECOMMENDED_ARGS                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

### Users and Groups

```bash
# Get current authenticated user
curl -s -H "$CF_AUTH" \
  "${CF_URL}/rest/api/user/current" | jq '{username, displayName, email}'

# Get a user by username
curl -s -H "$CF_AUTH" \
  "${CF_URL}/rest/api/user?username=chris.a" | jq '.'

# List members of a group
curl -s -H "$CF_AUTH" \
  "${CF_URL}/rest/api/group/confluence-administrators/member" \
  | jq '.results[].username'

# Add user to a group
curl -s -X POST -H "$CF_AUTH" -H "Content-Type: application/json" \
  "${CF_URL}/rest/api/group/confluence-users/user?accountId=<accountId>" 

# Get all groups
curl -s -H "$CF_AUTH" \
  "${CF_URL}/rest/api/group?limit=50" | jq '.results[].name'
```

### Labels and Watchers

```bash
# Get labels on a page
curl -s -H "$CF_AUTH" \
  "${CF_URL}/rest/api/content/12345/label" | jq '.results[].name'

# Add a label to a page
curl -s -X POST -H "$CF_AUTH" -H "Content-Type: application/json" \
  "${CF_URL}/rest/api/content/12345/label" \
  -d '[{"prefix": "global", "name": "runbook"}]'

# List watchers of a page
curl -s -H "$CF_AUTH" \
  "${CF_URL}/rest/api/content/12345/notification/child-created" | jq '.'
```

---

## Bulk Operations

### Bulk Export All Space Page Titles

```bash
#!/bin/bash
# export-all-pages.sh — outputs CSV: space_key,page_id,page_title

CF_URL="https://confluence.example.com"
CF_TOKEN="<PAT>"
OUTPUT="all_pages_$(date +%Y%m%d).csv"

echo "space_key,page_id,page_title" > "$OUTPUT"

# Get all space keys
spaces=$(curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "${CF_URL}/rest/api/space?limit=500" | jq -r '.results[].key')

for space in $spaces; do
  start=0
  limit=50
  while true; do
    resp=$(curl -s -H "Authorization: Bearer $CF_TOKEN" \
      "${CF_URL}/rest/api/content?spaceKey=${space}&type=page&limit=${limit}&start=${start}")
    count=$(echo "$resp" | jq '.results | length')
    [ "$count" -eq 0 ] && break
    echo "$resp" | jq -r --arg s "$space" \
      '.results[] | [$s, .id, .title] | @csv' >> "$OUTPUT"
    start=$((start + limit))
  done
  echo "  Exported space: $space"
done

echo "Done. Output: $OUTPUT"
```

### Bulk Delete Pages by Label

```bash
#!/bin/bash
# delete-pages-by-label.sh — trash all pages with a given label in a space

SPACE="OPS"
LABEL="deprecated"
CF_URL="https://confluence.example.com"
CF_TOKEN="<PAT>"

page_ids=$(curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "${CF_URL}/rest/api/content/search?cql=space=${SPACE}+AND+label=${LABEL}+AND+type=page&limit=200" \
  | jq -r '.results[].id')

for pid in $page_ids; do
  echo "Trashing page ID: $pid"
  curl -s -X DELETE -H "Authorization: Bearer $CF_TOKEN" \
    "${CF_URL}/rest/api/content/${pid}"
done
```

---

## Atlassian CLI (acli)

The **Atlassian CLI** (originally Bob Swift's CLI, now maintained as `acli`) is a Java-based command-line tool for scripting Confluence operations beyond what raw curl handles ergonomically.

### Installation

```bash
# Download from https://bobswift.atlassian.net/wiki/spaces/ACLI/
# Requires Java 11+

wget https://bobswift.atlassian.net/wiki/download/.../acli-9.x.x-distribution.zip
unzip acli-9.x.x-distribution.zip -d /opt/acli
chmod +x /opt/acli/acli.sh
ln -s /opt/acli/acli.sh /usr/local/bin/acli
```

### Common acli Operations

```bash
# Base connection options (use in all commands)
ACLI_OPTS="--server https://confluence.example.com \
  --user admin \
  --password ${ADMIN_PASS} \
  --product confluence"

# Get space info
acli $ACLI_OPTS --action getSpace --space OPS

# Create a page from a file
acli $ACLI_OPTS \
  --action addPage \
  --space OPS \
  --title "New Page from CLI" \
  --file page_content.html \
  --parent "Parent Page Title"

# Export a space to XML
acli $ACLI_OPTS \
  --action exportSpace \
  --space OPS \
  --exportType xml \
  --file /tmp/OPS_export.zip

# Copy a page to another space
acli $ACLI_OPTS \
  --action copyPage \
  --space OPS \
  --title "Source Page Title" \
  --toSpace ARCHIVE \
  --toTitle "Archived: Source Page Title"

# Run a CQL query and export results to CSV
acli $ACLI_OPTS \
  --action runFromCql \
  --cql "space = OPS AND label = runbook" \
  --outputFormat csv \
  --file runbooks.csv
```

---

## JVM and Application Administration

### start / stop / status

```bash
# Start Confluence
/opt/atlassian/confluence/bin/start-confluence.sh

# Stop Confluence (graceful)
/opt/atlassian/confluence/bin/stop-confluence.sh

# Check if Confluence process is running
pgrep -fl "confluence" || echo "Not running"

# Check listen port
ss -tlnp | grep 8090
```

### JVM Options (`setenv.sh`)

Located at: `/opt/atlassian/confluence/bin/setenv.sh`

```bash
# Production-recommended JVM flags
JAVA_OPTS="-Xms4g -Xmx8g \
  -XX:+UseG1GC \
  -XX:G1HeapRegionSize=16m \
  -XX:MaxGCPauseMillis=500 \
  -XX:MaxMetaspaceSize=1g \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/var/atlassian/application-data/confluence/dumps/ \
  -Djava.awt.headless=true \
  -Dfile.encoding=UTF-8 \
  -Dconfluence.document.conversion.threads=4"
```

### Thread Dump Collection

```bash
# Find the Confluence PID
CONF_PID=$(pgrep -f "confluence" | head -1)

# Capture three thread dumps 10 seconds apart (for analysis)
for i in 1 2 3; do
  kill -3 "$CONF_PID"      # Dumps to catalina.out / GC log
  # OR use jstack:
  jstack "$CONF_PID" > "/tmp/threaddump_${i}_$(date +%H%M%S).txt"
  sleep 10
done
```

### Heap Dump

```bash
# On-demand heap dump (non-destructive, app stays up)
CONF_PID=$(pgrep -f "confluence" | head -1)
jmap -dump:format=b,file=/tmp/confluence-heap-$(date +%Y%m%d%H%M).hprof "$CONF_PID"

# Analyze with Eclipse MAT or VisualVM
```

### Log Level Changes (Runtime)

Log levels can be changed at runtime without restart:

```text
Admin > General Configuration > Logging and Profiling
```

Or via the REST API:

```bash
# Enable debug for LDAP
curl -s -X PUT -H "$CF_AUTH" -H "Content-Type: application/json" \
  "${CF_URL}/rest/api/admin/logging" \
  -d '{"level": "DEBUG", "package": "com.atlassian.confluence.user.crowd"}'
```

### Groovy Script Runner (Admin Console)

If the **Script Runner** app (by Adaptavist) is installed:

**Admin > Script Runner > Script Console**

```groovy
// List all spaces with page counts
import com.atlassian.confluence.spaces.SpaceManager
import com.atlassian.confluence.pages.PageManager
import com.atlassian.spring.container.ContainerManager

def spaceManager = ContainerManager.getComponent('spaceManager') as SpaceManager
def pageManager  = ContainerManager.getComponent('pageManager') as PageManager

spaceManager.getAllSpaces().each { space ->
    def count = pageManager.getPages(space, true).size()
    println "${space.key}: ${count} pages"
}
```

```groovy
// Find pages not updated in 2+ years
import com.atlassian.confluence.pages.PageManager
import com.atlassian.confluence.spaces.SpaceManager
import com.atlassian.spring.container.ContainerManager
import java.time.Instant
import java.time.temporal.ChronoUnit

def cutoff = Instant.now().minus(730, ChronoUnit.DAYS)
def pageManager = ContainerManager.getComponent('pageManager') as PageManager
def spaceManager = ContainerManager.getComponent('spaceManager') as SpaceManager

spaceManager.getAllSpaces().each { space ->
    pageManager.getPages(space, true).each { page ->
        if (page.getLastModificationDate().toInstant().isBefore(cutoff)) {
            println "${space.key} | ${page.id} | ${page.title} | ${page.getLastModificationDate()}"
        }
    }
}
```

---

## Key Confluence System Properties

Set via `JAVA_OPTS` in `setenv.sh` or as `-D` flags:

| Property | Default | Description |
|---|---|---|
| `confluence.document.conversion.threads` | 4 | Office/PDF conversion thread pool |
| `confluence.search.lucene.index.dir` | `<shared-home>/index` | Override index location |
| `atlassian.mail.senddisabled` | false | Set `true` to suppress all outbound mail |
| `upm.plugin.install.timeout` | 120000 | Plugin install timeout (ms) |
| `confluence.upgrade.recovery.file.enabled` | true | Write upgrade recovery file |
| `com.sun.jndi.ldap.connect.timeout` | 10000 | LDAP connect timeout (ms) |
