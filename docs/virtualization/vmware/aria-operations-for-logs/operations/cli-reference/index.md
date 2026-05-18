# Aria Ops for Logs — CLI Reference

```
┌─────────────────────────────────────────────────────────────┐
│         Aria Ops for Logs CLI Reference                     │
├──────────────────────────────┬──────────────────────────────┤
│  li-admin (appliance CLI)    │  REST API                    │
├──────────────────────────────┼──────────────────────────────┤
│ li-admin status              │ POST /api/v1/sessions        │
│ li-admin cluster-info        │ GET  /api/v1/alerts          │
│ li-admin restart             │ POST /api/v1/events/query    │
│ li-admin log-collection-     │ GET  /api/v1/agents          │
│   status                     │ GET  /api/v1/system/info     │
│ li-admin storage             │ GET  /api/v1/system/storage  │
│                              │ POST /api/v2/support/bundle  │
│  vracli (Aria Suite CLI)     │ GET  /api/v2/cluster/nodes   │
│ vracli status                │ GET  /api/v2/cluster/stats   │
│ vracli certificate list      │                              │
│ vracli certificate import    │  Auth: HTTP Basic per-call   │
│ vracli ntp set <server>      │  Base: https://<vrli-fqdn>   │
└──────────────────────────────┴──────────────────────────────┘
```

Aria Operations for Logs (formerly vRealize Log Insight) exposes a REST API and a `vracli` / `li-admin` CLI available on the virtual appliance via SSH. The Ingestion API receives log data from agents and third-party sources.

---

## Appliance CLI (SSH Access)

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
```

---

## vracli (Aria Suite Appliance CLI)

```bash
# Check cluster health
vracli status

# Show service status
vracli services

# View current configuration
vracli config show

# Update NTP
vracli ntp set <ntp-server>

# Manage certificates
vracli certificate list
vracli certificate import --cert <cert.pem> --key <key.pem>
```

---

## REST API — Authentication

```bash
# Get session token
curl -k -X POST https://<li-fqdn>/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","provider":"Local"}'

# Use token in subsequent requests
# Header: Authorization: Bearer <sessionId>
```

---

## REST API — Queries & Alerts

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

---

## REST API — Ingestion

```bash
# Send logs via CFAPI (Log Insight Ingestion API)
curl -k -X POST https://<li-fqdn>:9543/api/v1/events/ingest/<agentId> \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"text":"test log message","timestamp":<epoch_ms>,"fields":[{"name":"hostname","content":"myhost"}]}]}'
```

---

## REST API — Administration

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

---

## Common Patterns

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
