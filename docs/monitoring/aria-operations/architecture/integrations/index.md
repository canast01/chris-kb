# Aria Operations — Integrations

<div class="kb-summary">
Adapter-based integration model: each source system connects via a Management Pack adapter running on the analytics cluster or a Remote Collector. Native adapters cover vSphere, NSX, vSAN, and storage; third-party MPs extend to public cloud, network, and ITSM.
</div>

## Native Adapters

| Adapter | Source | Data Collected |
|---|---|---|
| vCenter Server | vCenter | VMs, hosts, clusters, datastores, resource pools |
| NSX-T | NSX Manager | Logical switches, segments, gateways, DFW rule hit counts |
| vSAN | vCenter (vSAN API) | Disk group health, IOPS, latency, capacity |
| VMware Cloud on AWS | SDDC Manager | Cloud VM performance and capacity |
| Aria Operations for Logs | Log Insight / Aria Logs | Log-correlated alert context |

## Storage Management Packs

| Management Pack | Vendor | Key Metrics |
|---|---|---|
| NetApp ONTAP MP | NetApp | SVM, volume, aggregate, SnapMirror lag |
| Pure Storage MP | Pure Storage | FlashArray volume, array health, capacity |
| Dell PowerMax MP | Dell | SRDF state, host I/O, storage group utilisation |
| Dell PowerStore MP | Dell | Array health, volume latency, capacity |

## ITSM and Notification Integrations

| Integration | Direction | Use Case |
|---|---|---|
| ServiceNow | Outbound (REST) | Auto-create incidents from Critical alerts |
| PagerDuty | Outbound (webhook) | On-call alerting for Critical severity |
| Slack / Teams | Outbound (webhook) | Warning-level alert notification channel |
| SMTP | Outbound | Email delivery for alert notifications |
| Aria Automation | Bidirectional | Remediation action triggers from alert policies |

## REST API

Aria Operations exposes a REST API for external integration:

```bash
# Authenticate
curl -k -X POST https://ariaops.corp.example.com/suite-api/api/auth/token/acquire \
  -H "Content-Type: application/json" \
  -d '{"username":"svc-ariaops","password":"<pass>","authSource":"LOCAL"}'

# List all critical alerts
curl -k -X GET https://ariaops.corp.example.com/suite-api/api/alerts \
  -H "Authorization: vRealizeOpsToken <token>" \
  -G --data-urlencode "alertCriticality=CRITICAL"
```
```
