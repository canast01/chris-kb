# Aria Automation — Operational Procedures

```bash
# List expired deployments via API
TOKEN=<your-token>
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/deployment/api/deployments?status=CREATE_FAILED&size=50" | \
  jq '.content[] | {id: .id, name: .name, owner: .ownedBy, status: .status}'

# Delete a specific deployment (Day-2 action — fires the destroy workflow)
DEPLOYMENT_ID="<id>"
curl -sk -X DELETE -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/deployment/api/deployments/$DEPLOYMENT_ID"
```

```text
┌────────────────────────────── Aria Automation — Operational Procedures ───────────────────────────────┐
│                                                                                                       │
│  Common vRA operational tasks: cert rotation, password rotation, account changes, cleanup.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Certificate Rotation             │  │              Password Rotation              │   │
│   │      Generate new cert (SAN: vRA FQDN)       │  │      vRA admin password: VAMI → change      │   │
│   │        Import via LCM cert management        │  │     Postgres password: vracli + restart     │   │
│   │       LCM redeploys certs to products        │  │      Cloud account creds: update in UI      │   │
│   │        Validate SSO and catalog after        │  │      Service account: rotate + test ABX     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Account and resource management procedures keep vRA clean and correctly scoped.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Cloud Account Management           │  │               Resource Cleanup              │   │
│   │       Add: wizard + test connectivity        │  │      Orphaned deployments: force delete     │   │
│   │        Update creds: edit + reconnect        │  │    Stale catalog items: unpublish+delete    │   │
│   │      Remove: detach from projects first      │  │      Expired leases: auto or manual del     │   │
│   │      Data collection: trigger manually       │  │     ABX logs: retained 30d, purge older     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliances · LCM appliance · Postgres · vIDM · vCenter · CA for cert issuance                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cert rotation     = Replacing expiring TLS cert on vRA via LCM certificate management UI             │
│  LCM cert push     = LCM distributes updated cert to all products in the Environment                  │
│  VAMI password     = Root/admin password for vRA appliance changed via VAMI web UI at :5480           │
│  Postgres creds    = DB credentials stored in vracli config; update and restart service               │
│  Cloud account creds= AWS access key / vCenter password stored in vRA; edit without removing          │
│  Force delete      = vRA admin can hard-delete stuck deployments via API or UI override               │
│  Orphaned resource = Deployment record in vRA with no matching resource in cloud account              │
│  Data collection   = vRA polls cloud accounts for resource inventory; trigger via UI or API           │
│  Lease expiry      = Automated deletion triggered by lease policy when deployment exceeds TTL         │
│  ABX log retention = Action run logs stored 30 days; older logs purged automatically                  │
│  Unpublish item    = Remove catalog item from consumer view without deleting the template             │
│  Service account   = vRA uses a service account to authenticate to AD, vCenter, and NSX               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
ssh root@vra-prod-01.example.local
curl -sk -o /dev/null -w "%{http_code}" https://vcenter-prod.example.local/rest/com/vmware/cis/session
# Expected: 401 (Unauthorised — server is reachable)
# Any other output (000, curl error) indicates network or DNS issue
```
```bash
kubectl logs -n prelude -l app=vra-nginx --tail=100 | grep -i "error\|5[0-9][0-9]"
kubectl logs -n prelude -l app=iaas-gateway --tail=100 | grep -i "error\|vcenter\|cloud"
```
```text
Infrastructure → Configure → Image Mappings → add entry for new zone
Infrastructure → Configure → Flavor Mappings → add entry for new zone
```
```bash
Service Broker → Content & Policies → Policies → New Policy → Approval Policy
```
```bash
Service Broker → Content → Catalog Items → select item → Policy → assign the approval policy
```
```text
Extensibility → Actions → New Action
```
```python
import requests

def handler(context, inputs):
    webhook_url = inputs.get("slackWebhook")
    deployment_name = inputs["deploymentName"]
    owner = inputs["owner"]
    
    message = {
        "text": f":white_check_mark: Deployment *{deployment_name}* succeeded for {owner}"
    }
    resp = requests.post(webhook_url, json=message)
    return {"status": resp.status_code}
```
```text
Extensibility → Subscriptions → New Subscription
```
