# Aria Operations — CLI Reference

```text
Aria Operations — CLI Command Reference Map
┌─────────────────────────────────────────────────────┐
│  SSH: admin@<aria-ops-primary-fqdn>                 │
│       (sudo -i for advanced maintenance tasks)      │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┼──────────────┐
          ▼            ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────┐
│ Cluster Mgmt │ │ Adapters     │ │ Certificates      │
│              │ │              │ │                   │
│ vracli       │ │ vracli       │ │ vracli            │
│ cluster      │ │ adapter list │ │ certificate show  │
│ health       │ │              │ │                   │
│              │ │ vracli       │ │ vracli            │
│ vracli       │ │ adapter list │ │ certificate       │
│ cluster      │ │ --verbose    │ │ import            │
│ list-nodes   │ │              │ │ --cert --key --ca │
│              │ │ vracli       │ │                   │
│ vracli       │ │ adapter      │ └──────────────────┘
│ version      │ │ restart                            │
│              │ │ --id <id>                          │
│ vracli       │ └──────────────┘
│ cluster                                             │
│ restart                                             │
└──────────────┘
┌─────────────────────────────────────────────────────┐
│  REST API  base: https://<aria-ops>/suite-api/api   │
│  POST /api/auth/token/acquire   authenticate        │
│  GET  /api/resources            list objects        │
│  GET  /api/alerts?activeOnly=true  active alerts    │
│  GET  /api/cluster/nodes        node status         │
└─────────────────────────────────────────────────────┘
```

## Access

```bash
# SSH to primary node
ssh admin@<aria-ops-primary-fqdn>

# For maintenance mode or advanced tasks, escalate to root via sudo
sudo -i
```

---

## vracli Commands

### Cluster Management

```bash
# Show cluster health and node roles
vracli cluster health

# List all nodes and their status
vracli cluster list-nodes

# Restart all services on the node (use with care)
vracli cluster restart

# Show current version
vracli version
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
