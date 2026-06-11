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
