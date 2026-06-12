# Aria Ops for Logs — Procedures

<div class="kb-summary">
Step-by-step procedures for Aria Operations for Logs — adding log sources, installing content packs, managing disk and retention, configuring alerts and notifications, certificate rotation, and cluster scaling.
</div>

```text
┌──────────────────────────────── Aria Operations for Logs — Procedures ────────────────────────────────┐
│                                                                                                       │
│  Common operational procedures: add sources, rotate certs, manage disk, adjust alerts.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Add Log Source                │  │             Certificate Rotation            │   │
│   │     1. Install content pack if available     │  │    1. Generate new cert with correct SAN    │   │
│   │      2. Configure device syslog to vRLI      │  │        2. Import cert via VAMI → SSL        │   │
│   │     3. Verify events arriving in Explore     │  │        3. Restart loginsight service        │   │
│   │      4. Tag source: env/product fields       │  │     4. Verify sources still sending logs    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Disk and retention management prevent appliance from filling up during high-volume events.           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Disk Management                │  │               Alert Management              │   │
│   │       Monitor: Admin → System Monitor        │  │         Add: Queries → create alert         │   │
│   │        Archive: trigger manual export        │  │      Test: fire test from alert editor      │   │
│   │        Purge: reduce retention period        │  │       Route: map to webhook/email/SNow      │   │
│   │      Expand: add worker for more space       │  │     Suppress: noise via suppression rule    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI appliance · /storage disk · NFS archive target · vCenter · syslog sources                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Content pack      = Install before onboarding; provides parsers and dashboards for source            │
│  Explore           = vRLI real-time log viewer; used to confirm new sources are sending               │
│  Source tag        = Custom field on ingested events identifying environment or product               │
│  SAN cert          = Subject Alternative Name; FQDN of vRLI must be in cert SAN list                  │
│  loginsight service= Linux service restarted after cert change to apply new TLS cert                  │
│  System Monitor    = vRLI Admin section showing disk, CPU, RAM, and ingestion metrics                 │
│  Manual archive    = Trigger export of log data to NFS/S3 before disk fills                           │
│  Retention period  = Days of hot log data kept on disk; reduce to free space                          │
│  Worker node       = Add for more disk and processing; joins cluster automatically                    │
│  Alert suppression = Rule preventing noisy known-good events from firing notifications                │
│  Webhook route     = Notification channel sending HTTP POST to external system on alert               │
│  Alert test        = Manual trigger in alert editor; confirms notification delivery                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Add a Syslog Log Source

1. Configure the source device to forward syslog to the vRLI appliance IP on UDP/514 or TCP/514
2. Install a content pack for the device type (if available): **Administration → Content Packs → Marketplace** → search and install
3. In vRLI **Explore**, filter by `hostname = <device-fqdn>` and confirm events are arriving
4. Tag the source for easier filtering:
   - Navigate to the event in Explore → click a field → **Extract Field** → define a custom field (e.g., `env = production`)
5. Optional: add a source alias — **Administration → Agents → Sources** → locate the source IP → assign a friendly name

```bash
# Verify syslog is reaching vRLI from the source device
# On the source device (Linux example):
logger -n <vrli-ip> -P 514 -d "Test message from $(hostname)"

# In vRLI Explore, search:
# text contains "Test message" AND hostname = <source-hostname>
```

---

## Install a Content Pack

Content packs provide pre-built parsers, extracted fields, and dashboards for specific products.

1. vRLI → **Administration** → **Content Packs** → **Marketplace**
2. Browse or search for the product (e.g., VMware vSphere, NSX, Cisco, Palo Alto)
3. Click **Install** — vRLI downloads and applies the content pack
4. After installation, navigate to **Dashboards** → confirm new product-specific dashboards appear
5. If the content pack adds new extracted fields, existing historical data does not retroactively parse — only new incoming events are parsed

---

## Add a vSphere/vCenter Log Source (via Integration)

For VMware product logs, use the native integration rather than generic syslog:

1. vRLI → **Administration** → **vSphere Integration** → **New Connection**
2. Enter the vCenter FQDN and credentials (read-only service account sufficient)
3. Click **Test Connection** → confirm green
4. Select log collection options: ESXi hostd/vpxa logs, vCenter events, vSAN logs
5. Click **Save** — vRLI configures ESXi hosts to forward logs via the vSphere Integration agent

---

## Configure Disk Retention

Reduce retention to free disk space or increase it if disk has capacity.

1. vRLI → **Administration** → **Configuration** → **General**
2. Under **Retention**, set **Log Retention Period** (default: 30 days)
3. Reducing the retention period causes vRLI to purge older data during the next maintenance window
4. Monitor disk usage: **Administration → System Monitor → Disk** tab

```bash
# Check current disk usage on the vRLI appliance
ssh root@<vrli-fqdn>
df -h /storage
# /storage should be below 80% — vRLI starts dropping logs when full
```

---

## Archive Log Data to NFS

Archive before purging or before reducing retention.

1. vRLI → **Administration** → **Configuration** → **Archive**
2. Configure the archive target: NFS or S3 (enter mount path or bucket details)
3. Click **Test Connection** → confirm write access
4. Set an archive schedule: automatic daily/weekly archiving
5. To trigger immediate archive: **Administration → Archive → Archive Now**

---

## Add a Worker Node (Scale-Out)

Add a worker node to increase disk capacity and ingestion throughput.

1. Deploy the vRLI OVA — same version as the master node
2. During OVA deployment, configure the appliance IP, FQDN, and NTP
3. After deployment, log into the new node's VAMI (`https://<worker-fqdn>:9543`)
4. Select **Join existing deployment** → enter the master node FQDN and admin credentials
5. The master node picks up the new worker automatically — confirm under **Administration → Cluster**
6. Verify: **Administration → System Monitor → Nodes** — new worker shows **Active**

---

## Configure an Alert

Alerts trigger when a log query result meets a count or rate threshold.

1. vRLI → **Interactive Analytics** → build the query that should trigger the alert
2. Click **Create Alert from Query**
3. Configure alert conditions:
   - **Count threshold**: fire when matching events > N in a time window
   - **Static (presence)**: fire when any matching event appears
4. Set the notification action:
   - **Email**: configure SMTP first (Administration → SMTP)
   - **Webhook**: enter the endpoint URL and payload template
   - **Aria Operations alert**: sends alert to vROps if integrated
5. Click **Save** → test the alert with **Send Test Notification**

---

## Configure SMTP for Alert Notifications

1. vRLI → **Administration** → **SMTP**
2. Enter SMTP relay host, port (25 / 587 / 465), and sender address
3. Enable authentication if the relay requires credentials
4. Click **Test** — confirms delivery to the specified test recipient
5. Click **Save** — SMTP is now available as a notification channel in alert rules

---

## Configure a Webhook Notification Channel

```bash
# Create a webhook channel via API
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/notification/channels \
  -H "Content-Type: application/json" \
  -d '{
    "type": "WEBHOOK",
    "name": "teams-alerts",
    "webhookUrl": "https://example.webhook.office.com/webhookb2/...",
    "contentType": "application/json",
    "body": "{\"text\": \"Alert: ${alertName} - ${hitCount} events\"}"
  }'

# Test the webhook channel
curl -sk -X POST -u admin:<password> \
  "https://<vrli-fqdn>/api/v1/notification/channels/<channel-id>/test"
```

Payload variables: `${alertName}`, `${hitCount}`, `${url}`, `${fields}`, `${timestamp}`.

---

## Create an Alert Suppression Rule

Suppress recurring benign alerts to reduce noise.

1. vRLI → **Interactive Analytics** → identify the noisy query
2. Create an alert for it (if not already alerting) → note the alert ID
3. vRLI → **Administration** → **Alert Suppression** → **Add Rule**
4. Set suppression conditions: match on alert name or query terms
5. Set suppression duration: suppress for N hours or until manually lifted
6. Confirm the alert no longer fires during the suppression window

---

## Rotate the vRLI Certificate

The vRLI FQDN must be in the certificate SAN; a mismatch breaks browser trust.

1. Generate a new certificate with the correct SAN (vRLI FQDN + any cluster node FQDNs)
2. vRLI VAMI (`https://<vrli-fqdn>:9543`) → **SSL** → **Replace Certificate**
3. Upload the signed certificate (PEM) and private key
4. VAMI applies the certificate and restarts the `loginsight` service — service outage ~60 seconds
5. After restart, verify browser trust: open `https://<vrli-fqdn>` — no certificate warnings
6. Confirm log sources are still sending: **Explore** → check for recent events from all sources

---

## Integrate with Aria Operations

When integrated, vRLI alerts appear as Aria Operations alerts for correlated root cause analysis.

```bash
# Configure vROps integration from vRLI
curl -sk -X POST -u admin:<password> \
  https://<vrli-fqdn>/api/v1/operations-server-config \
  -H "Content-Type: application/json" \
  -d '{
    "serverHost": "<vrops-fqdn>",
    "serverPort": 443,
    "username": "admin",
    "password": "<password>",
    "enabled": true
  }'
```

After configuration, alerts in vRLI that match the integration criteria create corresponding events in Aria Operations, visible in the **Workbench** and alert timeline.

---

## Add an NSX Syslog Source

Configure each NSX Manager and Edge node to forward syslog to the vRLI VIP or master IP.

1. NSX Manager UI → **System** → **Fabric** → **Nodes** → **NSX Managers** tab
2. Select an NSX Manager node → **Actions** → **Set Syslog Servers**
3. Click **Add** → enter:
   - **Server**: vRLI VIP (cluster mode) or master node IP
   - **Port**: `514`
   - **Protocol**: `UDP`
   - **Log Level**: `INFO`
4. Click **Save** → repeat for every NSX Manager node and every Edge node (Edge nodes: **System → Fabric → Nodes → Edge Transport Nodes → select node → Actions → Set Syslog Servers**)
5. Verify: vRLI → **Dashboards** → **Content Packs** → **VMware NSX-T** → check "Last Received" timestamp on key widgets (Firewall Events, DFW Drops); events should appear within 60 seconds of syslog config save

```bash
# Confirm NSX is reaching vRLI — run on vRLI master
grep -i "nsx\|tnc\|edge" /var/log/loginsight/ingestion.log | tail -20

# Quick EPS check from NSX source in vRLI Explore:
# hostname contains "nsx" AND _source = syslog
```

---

## Configure Event Forwarding to SIEM

Forward filtered vRLI events to an external SIEM (Splunk, QRadar, ArcSight) via syslog.

1. vRLI UI → **Administration** → **General** → **Forwarding** → **Add Destination**
2. Set **Destination Type**: `Syslog`
3. Enter SIEM **Host** and **Port** (default Splunk syslog: TCP 1514; QRadar: UDP 514)
4. Set **Protocol**: `TCP` (preferred — prevents UDP loss on high-volume bursts)
5. Optional — restrict forwarding to matching events only:
   - Toggle **Filter by Query** → enter or select a saved query (e.g., `loglevel = ERROR AND appname = vpxd`)
6. Toggle **Enable** → click **Save**
7. Verify: generate a matching event on the source system; confirm receipt in the SIEM raw event viewer within 30 seconds

```bash
# Test TCP reachability to SIEM from vRLI appliance
nc -zv <siem-host> <siem-port>

# Monitor forwarding errors
grep -i "forward\|destination\|connect" /var/log/loginsight/runtime.log | tail -30
```

---

## Create a Custom Extracted Field

Extract structured field values from unstructured log text using regex, enabling filter-by-field queries.

1. vRLI → **Explore Logs** → run a query returning the log events that contain the value to extract
2. Click any log entry to expand it → locate the value to capture
3. Click **Extract Field** next to the value → the field extraction dialog opens
4. Enter a **Field Name** (lowercase, no spaces; e.g., `vm_name`)
5. Write a regex with a named capture group matching the value:
```text
   vm\s+'(?P<vm_name>[^']+)'
   ```
6. Click **Test** — verify the capture group matches across the sample events shown
7. Click **Save** → the field is registered globally and applies to all new incoming events

Use the extracted field in queries:
```text
vm_name = prod-web-01
vm_name contains "db-"
```
The field appears in the filter suggestion dropdown after the first event containing it is indexed.

---

## Configure Role-Based Access (User Management)

vRLI supports four roles: **Viewer** (read-only dashboards), **User** (explore + alerts), **Admin** (full config), **Super Admin** (multi-tenant admin). LDAP/AD group sync avoids per-user provisioning.

**Add a local user:**
1. vRLI → **Administration** → **Access Control** → **Users** → **Add User**
2. Enter username, email address, and assign role (Viewer / User / Admin / Super Admin)
3. Click **Save** → user receives a password-set email if SMTP is configured

**Configure LDAP/AD integration:**
1. vRLI → **Administration** → **Access Control** → **Authentication** → **LDAP**
2. Enter:
   - **Domain**: `corp.local`
   - **Connection**: `ldap://<dc-fqdn>:389` or `ldaps://<dc-fqdn>:636`
   - **Bind DN**: `CN=svc-vrli,OU=Service Accounts,DC=corp,DC=local`
   - **Bind Password**: service account password
   - **User Base DN**: `OU=Users,DC=corp,DC=local`
   - **Group Base DN**: `OU=Groups,DC=corp,DC=local`
3. Click **Test Connection** → confirm green
4. Click **Import Groups** → search for the AD group → select → assign role
5. Verify: log in as a member of the imported group; confirm the assigned role is enforced (e.g., Viewer cannot access Administration menu)

---

## Configure High Availability (Cluster Mode)

vRLI HA requires a minimum of 3 nodes (1 master + 2 workers). Workers must already be joined to the cluster (see **Add a Worker Node** above). HA adds a Virtual IP that survives master node failure.

1. vRLI → **Administration** → **Cluster** → **Enable High Availability**
2. Enter the **Virtual IP** (VIP) — a free IP on the same management network segment as the vRLI nodes; must be reserved in IPAM/DNS
3. Click **Save** — vRLI configures keepalived across all cluster nodes
4. After HA is enabled, update all log sources and SIEM forwarders to point to the VIP:
   - Syslog: UDP/TCP port 514 → VIP
   - Encrypted syslog: TCP port 1514 → VIP
   - vRLI API: HTTPS port 9000 → VIP
   - UI: HTTPS port 443 → VIP
5. Verify VIP is active:

```bash
# From a management host — confirm VIP is responding on syslog and API ports
nc -zv <vrli-vip> 514
curl -sk https://<vrli-vip>:9000/api/v1/version | jq .version

# On vRLI master — confirm keepalived is holding the VIP
ip addr show | grep <vrli-vip>
```

6. Test HA failover: power off the master VM → confirm VIP moves to a worker (now promoted master) within ~30 seconds

---

## Upgrade vRLI via Aria Suite Lifecycle

Preferred upgrade path for LCM-managed deployments. LCM orchestrates node-by-node upgrade with rollback support.

**Pre-upgrade checks:**
1. Snapshot all vRLI nodes (master + all workers) — label with date and current vRLI version
2. Verify LCM has downloaded the upgrade bundle: LCM → **Lifecycle Operations** → **Settings** → **Binary Mapping** → confirm target vRLI version listed
3. Confirm all cluster nodes are **ACTIVE** (see Health Checks) before proceeding

**Upgrade steps:**
1. LCM → **Environments** → select the environment containing vRLI
2. **Products** → **Aria Operations for Logs** → **Upgrade**
3. Select the **Target Version** from the dropdown
4. Click **Run Precheck** — LCM validates disk space, node connectivity, and product version compatibility
5. Resolve any precheck findings; re-run precheck until all pass
6. Click **Proceed** → monitor progress in LCM → **Requests**
7. LCM upgrades master first, then workers sequentially; total time: 30–60 minutes for a 3-node cluster

**Post-upgrade verification:**
```bash
# Confirm version on master
curl -sk -u 'admin:<password>' \
  https://<vrli-fqdn>/api/v1/version | jq .version

# Check all cluster nodes rejoined
curl -sk -u 'admin:<password>' \
  https://<vrli-fqdn>/api/v2/cluster/nodes | \
  jq '.nodes[] | {host: .hostname, state: .state, version: .version}'
```
- vRLI UI → **Administration** → **Content Packs** → confirm all installed packs still active
- vRLI UI → **Administration** → **Cluster** → confirm all nodes **ACTIVE**
- Delete node snapshots after a 48-hour burn-in period

---

## Configure a Custom Dashboard

Build a dashboard combining event trend widgets, field distribution charts, and saved query results.

1. vRLI → **Dashboards** → **+ New Dashboard** → enter a name and optional description
2. Click **Add Widget** → select widget type:
   - **Event Trends**: line chart of event count over time matching a query
   - **Field Trends**: bar chart of top values for a specific extracted field
   - **Events**: live table of matching log events
   - **Text**: static markdown notes or section headers
   - **URL**: embed an external iframe (e.g., Grafana panel)
3. For each widget: enter the filter query, set the time range, and configure the field or chart parameters
4. Drag to resize and arrange widgets on the canvas
5. Click **Save to Dashboard**

**Export/Import a dashboard:**
1. **Dashboards** → select the dashboard → **Actions** → **Export** → save the JSON file
2. On the target vRLI instance: **Dashboards** → **Actions** → **Import** → upload the JSON
3. After import, verify widget queries execute without field-not-found errors (custom extracted fields must also exist on the target instance)

---

## Back Up and Restore vRLI Configuration

Configuration backup covers: alert definitions, content packs, user accounts, saved queries, forwarding rules, and SMTP/webhook settings. **Log data is not included.**

**Backup:**
1. vRLI → **Administration** → **General** → **Configuration Backup**
2. Click **Download Backup** → a JSON file is saved to the browser download directory
3. Store the JSON in a versioned location (Git, object storage) — recommended frequency: weekly or before any major change

**Restore:**
1. Deploy a fresh vRLI appliance (same or newer version than the backup source)
2. Complete initial setup (network, admin password) but do not configure anything further
3. vRLI → **Administration** → **General** → **Configuration Backup** → **Restore**
4. Upload the JSON backup file → click **Restore** → vRLI applies all configuration objects
5. Verify: check alert definitions, forwarding rules, and user accounts are present
6. Reconnect log sources (sources must be reconfigured to point to the new appliance FQDN/IP; log data is not restored)

```bash
# Automate backup via API (run weekly from a management host)
curl -sk -u 'admin:<password>' \
  "https://<vrli-fqdn>/api/v1/configuration/backup" \
  -o "vrli-backup-$(date +%Y%m%d).json"
```

---

## Common Search Queries

```bash
# Host disconnect events
text contains "hostd" AND text contains "disconnected"

# vMotion failures
text contains "vmotion" AND text contains "failed" AND appname = "vpxd"

# HA events
text contains "HA failover" OR text contains "HA heartbeat"

# vSAN component errors
text contains "LSOM" AND loglevel = ERROR

# NSX DFW drops
text contains "DENY" AND appname = "nsx" AND text contains "DROP"

# Failed logins (SSH brute force detection)
text contains "Failed password" AND hostname contains "prod-"
```

Time-range tips: always set a time range — start with last 1 hour for active incidents; expand to 7 days for intermittent issues. Use the timeline histogram to identify event spikes before filtering further.
