# Aria Operations for Logs — CLI Reference

```bash
# SSH to the Log Insight appliance
ssh admin@<li-appliance-fqdn>

# Check appliance status
li-admin status

# Show cluster node status
li-admin cluster-info

# Restart Log Insight services
li-admin restart

# Check log collection status
li-admin log-collection-status

# Show current storage usage
li-admin storage
```text
┌────────────────────────────── Aria Operations for Logs — CLI Reference ───────────────────────────────┐
│                                                                                                       │
│  vRLI management uses the REST API, VAMI, and limited SSH commands on the appliance.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              REST API Commands               │  │           VAMI Operations (:9543)           │   │
│   │       GET /api/v1/cluster/nodes health       │  │         Network: IP/hostname/DNS/NTP        │   │
│   │       GET /api/v1/config/export config       │  │       SSL: cert import and management       │   │
│   │      POST /api/v1/config/import restore      │  │       Admin password: change via VAMI       │   │
│   │       POST /api/v1/events/ingest push        │  │        Support bundle: generate here        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SSH commands for service checks and log review on the vRLI Linux appliance.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            SSH Appliance Commands            │  │                Log Locations                │   │
│   │          service loginsight status           │  │             /var/log/loginsight/            │   │
│   │          service loginsight restart          │  │       /var/log/loginsight/runtime.log       │   │
│   │           df -h: check disk usage            │  │       /var/log/loginsight/queries.log       │   │
│   │          netstat -tulpn: port check          │  │        /var/log/loginsight/alerts.log       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI Linux appliance · VAMI at :9543 · REST API at :443/9000 · NFS storage                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VAMI              = Virtual Appliance Management Interface at port 9543 for vRLI                     │
│  /api/v1           = vRLI REST API base path; all management operations available here                │
│  loginsight service= Linux service managing vRLI processes; restart to clear soft faults              │
│  Ingest API        = POST /api/v1/events/ingest; JSON body with log events + fields                   │
│  Config export API = GET /api/v1/config/export; returns full config JSON for backup                   │
│  Config import API = POST /api/v1/config/import; restores config from JSON backup                     │
│  Cluster nodes API = GET /api/v1/cluster/nodes; shows master+worker health status                     │
│  runtime.log       = Main vRLI application log; check for startup errors and exceptions               │
│  queries.log       = Slow or failed query log; diagnose performance issues                            │
│  alerts.log        = Alert firing history; confirm alerting is working                                │
│  df -h             = Check disk usage on vRLI appliance; /storage partition critical                  │
│  API bearer token  = Auth via POST /api/v1/sessions; returns sessionId for API calls                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Run a log query
curl -k -X POST https://<li-fqdn>/api/v1/events/query \
  -H "Authorization: Bearer <sessionId>" \
  -H "Content-Type: application/json" \
  -d '{"query":"text CONTAINS error","startTimeMillis":<epoch_ms>,"endTimeMillis":<epoch_ms>}'

# List all alerts
curl -k -X GET https://<li-fqdn>/api/v1/alerts \
  -H "Authorization: Bearer <sessionId>"

# List alert recommendations
curl -k -X GET https://<li-fqdn>/api/v1/notification/channels \
  -H "Authorization: Bearer <sessionId>"
```
```bash
# Send logs via CFAPI (Log Insight Ingestion API)
curl -k -X POST https://<li-fqdn>:9543/api/v1/events/ingest/<agentId> \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"text":"test log message","timestamp":<epoch_ms>,"fields":[{"name":"hostname","content":"myhost"}]}]}'
```
```bash
# List data sources (agents)
curl -k -X GET https://<li-fqdn>/api/v1/agents \
  -H "Authorization: Bearer <sessionId>"

# List content packs
curl -k -X GET https://<li-fqdn>/api/v1/content/contentpackmetadata \
  -H "Authorization: Bearer <sessionId>"

# Get system info
curl -k -X GET https://<li-fqdn>/api/v1/system/info \
  -H "Authorization: Bearer <sessionId>"

# Get storage info
curl -k -X GET https://<li-fqdn>/api/v1/system/storage \
  -H "Authorization: Bearer <sessionId>"
```
```bash
# Daily health check
li-admin status
li-admin cluster-info
li-admin storage

# Check for active alerts via API
curl -k -X GET https://<li-fqdn>/api/v1/alerts?active=true \
  -H "Authorization: Bearer <sessionId>"

# Verify agent connectivity
curl -k -X GET https://<li-fqdn>/api/v1/agents \
  -H "Authorization: Bearer <sessionId>"
```
