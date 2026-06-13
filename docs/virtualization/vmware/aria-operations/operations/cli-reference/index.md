---
tags:
  - aria-operations
  - operations
  - vmware
---
# Aria Operations — CLI Reference


<div class="kb-summary">
CLI Reference reference covering vracli Commands, chkconfig (Legacy / Service Enable/Disable), Useful Paths, REST API Quick Reference, Related Sections.
</div>

Aria Operations — CLI Command Reference Map
```text
┌──────────────────────────────────── Aria Operations CLI Reference ────────────────────────────────────┐
│                                                                                                       │
│  REST API, VAMI, and SSH service commands for Aria Operations (vROps).                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Key REST API Endpoints            │  │               VAMI Operations               │   │
│   │        POST /suite-api/api/auth/token        │  │             https://<vrops>:5480            │   │
│   │          GET /suite-api/api/alerts           │  │           Cluster management page           │   │
│   │         GET /suite-api/api/resources         │  │             Backup / restore UI             │   │
│   │        GET /suite-api/api/statistics         │  │            Certificate management           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  REST API for automation; VAMI for appliance config; SSH for service-level control.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             SSH Service Commands             │  │            Useful Admin Commands            │   │
│   │         service vmware-vcops status          │  │           df -h: disk usage check           │   │
│   │         service vmware-vcops restart         │  │            top: CPU/RAM real-time           │   │
│   │         tail -f /var/log/vcops/*.log         │  │           vcops-support bundle gen          │   │
│   │           cluster-mgmt-cli status            │  │           ntpq -p: NTP sync check           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps master/data nodes on vSphere; SSH via jump host; VAMI browser on port 5480                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  suite-api           = vROps REST API path prefix; all endpoints under /suite-api                     │
│  Auth Token          = Bearer token from POST /auth/token; required for API calls                     │
│  GET /alerts         = Returns all active alerts with severity and resource context                   │
│  GET /resources      = Lists monitored objects with adapter kind and resource kind                    │
│  GET /statistics     = Retrieves metric values for a resource over a time range                       │
│  VAMI                = Virtual Appliance Mgmt Interface; port 5480 browser access                     │
│  vmware-vcops        = Main vROps service name on the appliance OS                                    │
│  cluster-mgmt-cli    = CLI tool for checking cluster node health and status                           │
│  vcops-support       = CLI command to generate vROps support bundle                                   │
│  vcops/*.log         = Log directory for analytics, collector, and UI logs                            │
│  ntpq -p             = Verifies NTP peer sync; important for metric timestamps                        │
│  df -h               = Disk usage; vROps is disk-heavy; monitor /storage/db                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  REST API  base: https://<aria-ops>/suite-api/api                                                     │
│  POST /api/auth/token/acquire   authenticate                                                          │
│  GET  /api/resources            list objects                                                          │
│  GET  /api/alerts?activeOnly=true  active alerts                                                      │
│  GET  /api/cluster/nodes        node status                                                           │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
### Adapter Management

```bash
# List all adapters and collection status
vracli adapter list

# List adapters with verbose output
vracli adapter list --verbose

# Restart a specific adapter (get ID from list output)
vracli adapter restart --id <adapter-id>
```

### Status and Services

```bash
# Overall service health summary
vracli status

# Check individual service
systemctl status vmware-vcops-<service-name>

# List all VMware services
systemctl list-units 'vmware-*'
```

### Certificate Management

```bash
# View current certificate info
vracli certificate show

# Replace certificate (PEM format)
vracli certificate import --cert /tmp/aria-ops.crt --key /tmp/aria-ops.key --ca /tmp/ca-chain.crt
```

### Support

```bash
# Generate support bundle
vracli support bundle generate

# List existing support bundles
ls -lh /storage/log/support-bundle/

# View recent logs
vracli log tail --lines 100
```

### Authentication and Users

```bash
# List configured auth sources
vracli auth list

# Test LDAP connectivity
vracli auth test --source <ldap-source-name>
```

---

## chkconfig (Legacy / Service Enable/Disable)

```bash
# List services and their runlevel status
chkconfig --list | grep vmware

# Enable a service at boot
chkconfig vmware-vcops on
```

---

## Useful Paths

| Path | Contents |
|------|----------|
| `/storage/log/` | All Aria Operations logs |
| `/storage/log/support-bundle/` | Generated support bundles |
| `/storage/core/` | Core data directory |
| `/usr/lib/vmware-vcopssuite/utilities/` | vracli utilities location |

---

## REST API Quick Reference

Base URL: `https://<aria-ops-fqdn>/suite-api/api`

```bash
# Authenticate and get token
curl -sk -X POST "https://<aria-ops>/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","authSource":"LOCAL","password":"<password>"}' | jq .

# List resources
curl -sk -H "Authorization: vRealizeOpsToken <token>" \
  "https://<aria-ops>/suite-api/api/resources" | jq .

# Get all active alerts
curl -sk -H "Authorization: vRealizeOpsToken <token>" \
  "https://<aria-ops>/suite-api/api/alerts?activeOnly=true" | jq .
```

---

## Related Sections

- [Operations](../index.md) — operational runbooks
- [Scripts](../scripts/index.md) — automation using the API
- [Troubleshooting](../../troubleshooting/index.md) — diagnostic commands
