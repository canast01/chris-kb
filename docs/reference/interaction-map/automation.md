---
tags:
  - aria-automation
  - aria-operations
  - tanzu
  - horizon
  - automation
  - architecture
description: "How Aria Automation, Aria Operations, Aria Logs, Aria Networks, Tanzu, and Horizon connect to the vSphere and NSX layers — APIs, data flows, and..."
---
# Automation Domain — Interaction Map

*Applies to: All products*

<div class="kb-summary">
How Aria Automation, Aria Operations, Aria Logs, Aria Networks, Tanzu, and Horizon connect to the vSphere and NSX layers — APIs, data flows, and authentication.
</div>

![Automation Domain Interaction Map](../../assets/interaction-map-automation.svg)

## Integration summary

| From | To | Protocol / API | Notes |
|---|---|---|---|
| Aria Automation | vCenter | vSphere API (cloud account) | vRA deploys VMs by calling vCenter |
| Aria Automation | NSX | NSX Policy REST API | vRA creates segments and security groups |
| Aria Operations | vCenter | vCenter adapter (suite-api) | Polls vSphere metrics every 5 min (default) |
| Aria Operations | NSX | NSX adapter | Collects NSX Manager health and inventory |
| Aria Logs | All VMs | syslog UDP/514 or liagent :9543 | Every VM ships logs; liagent provides structured fields |
| Aria Networks | NSX | IPFIX + NSX REST API | Flow data via IPFIX; topology via NSX Policy API |
| Aria Networks | vCenter | vCenter REST API | VM inventory and network adapter mapping |
| Tanzu | vCenter | WCP / vSphere API | Supervisor cluster runs on vCenter; `kubectl vsphere` |
| Horizon | vCenter | vSphere API | Horizon clones/provisions VMs via vCenter |

## Aria product API authentication

All Aria products use a **CSP (Cloud Services Platform) token** or a product-local session:

```bash
# Get CSP token (used by all Aria APIs)
TOKEN=$(curl -sk -X POST https://vra/csp/gateway/am/api/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"VMware1!"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# Use token for any Aria API
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://vra/deployment/api/deployments
```


```text title="Expected output"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTcwOTMxNjgwMCwiZXhwIjoxNzA5MzIwNDAwfQ.x5K9mZ2pL8qN3vR6tY1wA4bC7dE9fG2hJ5kM8nO1pQ
{
  "content": [
    {
      "id": "deployment-001",
      "name": "prod-k8s-cluster",
      "status": "ACTIVE",
      "createdAt": "2024-03-01T10:15:32Z"
    },
    {
      "id": "deployment-002",
      "name": "dev-app-stack",
      "status": "ACTIVE",
      "createdAt": "2024-02-28T14:22:18Z"
    }
  ],
  "totalElements": 2
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command to skip SSL verification (already present in example; if error persists, verify vra hostname resolves correctly). |
    | `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` | Verify credentials are correct and CSP gateway is accessible; check response with `curl -sk -X POST https://vra/csp/gateway/am/api/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"VMware1!"}'` to see actual error message. |
    | `curl: (7) Failed to connect to vra port 443: Name or service not known` | Ensure the vra hostname is resolvable and reachable from your network; add it to /etc/hosts or use the full FQDN if necessary. |
## Tanzu architecture layers

![Automation Domain — Interaction Map — Diagram](../../assets/reference-interaction-map-automation-diagram.svg)

For **TKGs** (vSphere with Tanzu): the Supervisor runs directly on vSphere; no separate management cluster needed.

## Horizon provisioning flow

![Automation Domain — Interaction Map — Diagram](../../assets/reference-interaction-map-automation-d2.svg)

## See also

- [Aria Automation Cheat Sheet](../../cheat-sheets/aria-automation/)
- [Aria Operations Cheat Sheet](../../cheat-sheets/aria-operations/)
- [Tanzu Cheat Sheet](../../cheat-sheets/tanzu/)
- [Horizon Cheat Sheet](../../cheat-sheets/horizon/)
- [Back to Interaction Map](index.md)
