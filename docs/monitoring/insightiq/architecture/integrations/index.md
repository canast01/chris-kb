# InsightIQ — Integrations

<div class="kb-summary">
InsightIQ integrates exclusively with PowerScale (Isilon) clusters via the OneFS REST API. External integrations are limited to email alerting, syslog forwarding, and the InsightIQ REST API for report automation.
</div>

## PowerScale OneFS Integration

InsightIQ collects data from PowerScale using a dedicated read-only API account:

```bash
# Create read-only service account on PowerScale
isi auth users create insightiq-svc --enabled yes \
  --set-password

# Assign audit and read-only platform API role
isi auth roles modify AuditAdmin --add-user insightiq-svc
```

| OneFS Version | API Port | Notes |
|---|---|---|
| 8.x | 8080 | Legacy PAPI |
| 9.0+ | 443 | Unified REST API; 8080 still works |

## Alert and Notification Integrations

| Integration | Configuration | Use Case |
|---|---|---|
| Email (SMTP) | Settings → Notifications → Email | Capacity threshold alerts |
| Syslog | Settings → Notifications → Syslog | Forward events to SIEM |

Syslog format is RFC 5424; configure your SIEM to parse InsightIQ facility `local0`.

## InsightIQ REST API

InsightIQ exposes a REST API for automating report generation and exporting metrics:

```bash
# Authenticate
curl -k -X POST https://insightiq.corp.example.com/api/v1/auth \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<pass>"}'

# List monitored clusters
curl -k -H "Cookie: session=<token>" \
  https://insightiq.corp.example.com/api/v1/clusters

# Get cluster capacity summary
curl -k -H "Cookie: session=<token>" \
  "https://insightiq.corp.example.com/api/v1/clusters/{cluster_id}/capacity"
```

## Scope Limitation

- InsightIQ monitors **PowerScale only** — it does not support PowerStore, Unity, or PowerMax
- For multi-vendor monitoring, use CloudIQ (Dell) or Aria Operations with storage Management Packs
- No native CMDB connector — update CMDB entries manually or via API scripting
