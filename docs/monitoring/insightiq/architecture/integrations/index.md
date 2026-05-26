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

## Scope Limitation

- InsightIQ monitors **PowerScale only** — it does not support PowerStore, Unity, or PowerMax
- For multi-vendor monitoring, use CloudIQ (Dell) or Aria Operations with storage Management Packs
- No native CMDB connector — update CMDB entries manually or via API scripting
