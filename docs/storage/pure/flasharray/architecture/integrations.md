---
tags:
  - architecture
  - pure
---
# FlashArray — Integrations

<div class="kb-summary">
Integrations reference covering VMware Integration, Backup Integration, Pure1 Monitoring, Authentication, REST API.

*Applies to: FlashArray Purity 6.x*
</div>
![FlashArray — Integrations](../../../../assets/storage-pure-flasharray-architecture-integrations.svg)

**Generate an API token for a service account:**

```bash
# On the array CLI
pureadmin create --role array_admin svc-monitoring
pureadmin apitoken create svc-monitoring
# Copy the token and store in a secrets manager
```

**Common API calls:**

```bash
# Get array status
GET /api/2.x/arrays

# List volumes
GET /api/2.x/volumes

# List active alerts
GET /api/2.x/alerts?filter=state%3D%27open%27

# Get array capacity
GET /api/2.x/arrays?space=true
```

Full API reference: [Pure Storage API documentation](https://support.purestorage.com/bundle/m_fa_rest_api)

---

## See also

- [FlashArray — How It Works](../how-it-works/)
- [FlashArray — Design Standards](../design-standards/)
