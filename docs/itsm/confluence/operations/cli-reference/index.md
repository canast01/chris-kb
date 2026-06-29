---
tags:
  - confluence
  - operations
---
# Confluence — CLI Reference

```bash
# Set common variables to avoid repetition
export CF_URL="https://confluence.example.com"
export CF_TOKEN="<your-PAT-here>"
export CF_AUTH="Authorization: Bearer ${CF_TOKEN}"
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`bash: CF_TOKEN: Unbound variable`** — Replace `<your-PAT-here>` with an actual Personal Access Token generated in Confluence settings.
    **`curl: (6) Could not resolve host: confluence.example.com`** — Update `CF_URL` to match your actual Confluence instance hostname (e.g., `https://confluence.company.internal`).
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

```text title="Expected output"
{
  "username": "admin",
  "displayName": "Administrator",
  "email": "admin@company.local"
}
{
  "username": "chris.a",
  "displayName": "Chris Anderson",
  "email": "chris.anderson@company.local",
  "accountId": "557058:12a3b4c5-d6e7-8f9g-0h1i-2j3k4l5m6n7o"
}
confluence-administrators
confluence-users
confluence-developers
confluence-readonly
...
(no output — user added to group successfully)
confluence-administrators
confluence-users
confluence-developers
confluence-readonly
confluence-guests
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443: Connection refused`** — Verify `${CF_URL}` is correct and Confluence server is running and accessible.
    **`jq: parse error: Cannot index string with string "results"`** — Ensure the API endpoint returns JSON; check that `${CF_AUTH}` header is valid and the user has API access permissions.
    **`{"statusCode":401,"message":"Unauthorized"}`** — Verify the `${CF_AUTH}` header contains a valid Bearer token or Basic auth credentials.
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

```text title="Expected output"
"production"
"critical"
"infrastructure"
{"statusCode":200,"successful":true}
{
  "results": [
    {
      "type": "user",
      "user": {
        "type": "known",
        "username": "jsmith",
        "userKey": "557058:8f3a9c2e-1b4d-4f8a-9e2c-5d7a1b3c4e5f",
        "displayName": "John Smith"
      }
    },
    {
      "type": "user",
      "user": {
        "type": "known",
        "username": "mchen",
        "userKey": "557058:a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
        "displayName": "Michelle Chen"
      }
    }
  ],
  "start": 0,
  "limit": 25,
  "size": 2
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443: Connection refused`** — Verify `$CF_URL` is correct and the Confluence instance is running and accessible from your network.
    **`{"statusCode":401,"message":"Unauthorized"}`** — Ensure `$CF_AUTH` is set correctly (e.g., `"Authorization: Bearer $TOKEN"` or `"Authorization: Basic $(echo -n user:pass | base64)"`) and the token/credentials have not expired.
    **`jq: parse error: Cannot index number with string "results"`** — Check that the API response is valid JSON; the endpoint may have returned an error code instead of the expected data structure.
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

```text title="Expected output"
space_key,page_id,page_title
  Exported space: INFRA
  Exported space: OPS
  Exported space: SEC
  Exported space: DEVOPS
  Exported space: PLATFORM
Done. Output: all_pages_20240115.csv
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to confluence.example.com port 443: Connection refused`** — Verify the Confluence URL is correct and the instance is accessible from your network (test with `curl -I https://confluence.example.com`).
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure your PAT token is valid and has API access permissions; an invalid token returns HTML error pages instead of JSON.
    **`Permission denied`** — Run the script from a directory where you have write permissions, or specify an absolute path for the OUTPUT variable.
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

```text title="Expected output"
Trashing page ID: 65847
Trashing page ID: 72193
Trashing page ID: 68521
Trashing page ID: 71004
Trashing page ID: 69156
Trashing page ID: 70832
```

!!! warning "Common errors"
    **`jq: parse error: Invalid JSON text at line 1`** — Verify the Confluence URL is correct and the API token has read permissions on the space.
    **`curl: (401) Unauthorized`** — Ensure the PAT token is valid and has not expired; regenerate it in Confluence if necessary.
    **`curl: (403) Forbidden`** — Confirm the API token has delete permissions; check Confluence user permissions for the OPS space.
```bash
# Download from https://bobswift.atlassian.net/wiki/spaces/ACLI/
# Requires Java 11+

wget https://bobswift.atlassian.net/wiki/download/.../acli-9.x.x-distribution.zip
unzip acli-9.x.x-distribution.zip -d /opt/acli
chmod +x /opt/acli/acli.sh
ln -s /opt/acli/acli.sh /usr/local/bin/acli
```

```text title="Expected output"
--2024-01-15 14:23:45--  https://bobswift.atlassian.net/wiki/download/.../acli-9.x.x-distribution.zip
Resolving bobswift.atlassian.net (bobswift.atlassian.net)... 203.0.113.42
Connecting to bobswift.atlassian.net (bobswift.atlassian.net)|203.0.113.42|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 47382916 (45M) [application/zip]
Saving to: 'acli-9.x.x-distribution.zip'

acli-9.x.x-distribution.zip    100%[=====================================>]  45.18M  3.24MB/s    in 14s
2024-01-15 14:24:00 (3.23 MB/s) - 'acli-9.x.x-distribution.zip' saved [47382916/47382916]

Archive:  acli-9.x.x-distribution.zip
  inflating: /opt/acli/acli.sh
  inflating: /opt/acli/lib/acli-core-9.2.1.jar
  inflating: /opt/acli/lib/commons-cli-1.5.0.jar
  ...
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`wget: command not found`** — Install wget with `apt-get install wget` (Debian/Ubuntu) or `yum install wget` (RHEL/CentOS).
    **`unzip: command not found`** — Install unzip with `apt-get install unzip` or `yum install unzip`.
    **`ln: failed to create symbolic link '/usr/local/bin/acli': File exists`** — Remove the existing symlink with `rm /usr/local/bin/acli` before creating a new one.
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

```text title="Expected output"
Space: OPS
  Key: OPS
  Name: Operations
  Type: GLOBAL
  Status: CURRENT
  Pages: 247
  Last Modified: 2024-01-15 14:32:18

Page created successfully.
  Page ID: 98765
  Title: New Page from CLI
  Space: OPS
  Parent: Parent Page Title
  URL: https://confluence.example.com/display/OPS/New+Page+from+CLI

Space exported successfully.
  File: /tmp/OPS_export.zip
  Size: 12.4 MB
  Compressed pages: 247
  Export completed in 18 seconds

Page copied successfully.
  Source Page ID: 45231
  Destination Page ID: 45232
  Source Space: OPS
  Destination Space: ARCHIVE
  New Title: Archived: Source Page Title

CQL query executed successfully.
  Results: 34 pages
  Output file: runbooks.csv
  Format: CSV
  Rows exported: 34
```

!!! warning "Common errors"
    **`Error: Unable to authenticate user 'admin'. Check credentials and server URL.`** — Verify `$ADMIN_PASS` is set correctly and the server URL is accessible with `curl -I https://confluence.example.com`.
    **`Error: Space 'OPS' does not exist or user lacks permission to access it.`** — Confirm the space key is correct and the admin user has space-level permissions in Confluence.
    **`Error: File 'page_content.html' not found.`** — Ensure the file path is absolute or relative to the current working directory, and verify it exists with `ls -la page_content.html`.
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

```text title="Expected output"
Starting Confluence...
If you experience issues starting Confluence, please see the Troubleshooting guide at http://confluence.atlassian.com/display/DOC/Troubleshooting

waiting for Confluence to start ..... started in 47 seconds.
PID file: /opt/atlassian/confluence/work/catalina.pid

Shutting down Confluence
Using CATALINA_BASE:   /opt/atlassian/confluence
Using CATALINA_HOME:   /opt/atlassian/confluence
Using CATALINA_TMPDIR: /opt/atlassian/confluence/temp
Using JRE_HOME:        /usr/lib/jvm/java-11-openjdk-amd64
Using CLASSPATH:       /opt/atlassian/confluence/bin/bootstrap.jar:/opt/atlassian/confluence/bin/tomcat-juli.jar
Confluence stopped.

3847 /opt/atlassian/confluence/bin/java -Xms1024m -Xmx2048m -XX:+UseG1GC org.apache.catalina.startup.Bootstrap start

LISTEN     0      128                 *:8090              *:*      users:(("java",pid=3847,fd=45))
```

!!! warning "Common errors"
    **`/opt/atlassian/confluence/bin/start-confluence.sh: Permission denied`** — Run `chmod +x /opt/atlassian/confluence/bin/start-confluence.sh` to make the script executable.
    **`Address already in use`** — Either stop the existing Confluence process with `stop-confluence.sh` or change the port in `/opt/atlassian/confluence/conf/server.xml`.
    **`Not running`** — The process is not active; check `/opt/atlassian/confluence/logs/catalina.out` for startup errors and retry with `start-confluence.sh`.
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

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`mkdir: cannot create directory '/var/atlassian/application-data/confluence/dumps/': Permission denied`** — Run the command with sudo or ensure the confluence user owns the parent directory with `chown -R confluence:confluence /var/atlassian/application-data/confluence/`.
    **`Error occurred during initialization of VM: Could not allocate metaspace: 1073741824 bytes`** — Reduce `-XX:MaxMetaspaceSize` value (e.g., to 512m) or increase system available memory.
    **`-Xmx8g is invalid or too large for this system`** — Verify available RAM with `free -h` and set `-Xmx` to no more than 75% of total system memory.
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

```text title="Expected output"
12847
3 thread dumps captured:
/tmp/threaddump_1_143022.txt
/tmp/threaddump_2_143032.txt
/tmp/threaddump_3_143042.txt

Stack trace written to /tmp/threaddump_1_143022.txt
Stack trace written to /tmp/threaddump_2_143032.txt
Stack trace written to /tmp/threaddump_3_143042.txt
```

!!! warning "Common errors"
    **`jstack: command not found`** — Install the JDK (not just JRE) or use `kill -3` to write dumps to catalina.out instead.
    **`jstack: Unable to open socket file: target process not responding or HotSpot VM not loaded`** — Ensure the Confluence process is running and you are executing jstack as the same user (or root) that owns the Java process.
    **`Permission denied`** — Run the command with `sudo` or as the confluence service user to access the running JVM process.
```bash
# On-demand heap dump (non-destructive, app stays up)
CONF_PID=$(pgrep -f "confluence" | head -1)
jmap -dump:format=b,file=/tmp/confluence-heap-$(date +%Y%m%d%H%M).hprof "$CONF_PID"

# Analyze with Eclipse MAT or VisualVM
```
```text
Admin > General Configuration > Logging and Profiling
```
```bash
# Enable debug for LDAP
curl -s -X PUT -H "$CF_AUTH" -H "Content-Type: application/json" \
  "${CF_URL}/rest/api/admin/logging" \
  -d '{"level": "DEBUG", "package": "com.atlassian.confluence.user.crowd"}'
```
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
- [Confluence — Scripts](../scripts/)
- [Confluence — Health Checks](../health-checks/)
